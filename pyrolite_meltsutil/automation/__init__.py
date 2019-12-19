"""
This submodule contains functions for automated execution of alphamelts 1.9.

Issues
------

    * names are truncated for modifychem melts files?
    * need a timeout so processes can keep going, add unfinished experiments to failed list
"""
import itertools
from pathlib import Path
import time, datetime
import numpy as np
import json
from tqdm import tqdm

from pyrolite.geochem.ind import common_elements, common_oxides
from pyrolite.comp.codata import renormalise
from pyrolite.util.meta import ToLogger
from pyrolite.util.multip import combine_choices

from ..parse import read_envfile, read_meltsfile
from ..env import MELTS_Env
from ..meltsfile import dict_to_meltsfile

from .naming import exp_name, exp_hash
from .org import make_meltsfolder
from .process import MeltsProcess
from .timing import estimate_experiment_duration

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


__chem__ = common_elements(as_set=True) | common_oxides(as_set=True)


class MeltsExperiment(object):
    """
    Melts Experiment Object. For a single call to melts, with one set of outputs.
    Autmatically creates the experiment folder, meltsfile and environment file, runs
    alphaMELTS and collects the results.

    Todo
    ----
        * Automated creation of folders for experiment results (see :func:`make_meltsfolder`)
        * Being able to run melts in an automated way (see :class:`MeltsProcess`)
        * Compressed export/save function
        * Post-processing functions for i) validation and ii) plotting
    """

    def __init__(
        self,
        name="MeltsExperiment",
        title="MeltsExperiment",
        fromdir="./",
        meltsfile=None,
        env=None,
        timeout=None,
    ):
        self.name = name  # folder name
        self.title = title  # meltsfile title
        self.fromdir = fromdir  # create an experiment directory here
        self.log = []
        self.timeout = timeout

        if meltsfile is not None:
            self.set_meltsfile(meltsfile)
        if env is not None:
            self.set_envfile(env)
        else:
            self.set_envfile(MELTS_Env())

        self._make_folder()

    def set_meltsfile(self, meltsfile, **kwargs):
        """
        Set the meltsfile for the experiment.

        Parameters
        ------------
        meltsfile : :class:`pandas.Series` | :class:`str` | :class:`pathlib.Path`
            Either a path to a valid melts file, a :class:`pandas.Series`, or a
            multiline string representation of a melts file object.
        """
        self.meltsfile, self.meltsfilepath = read_meltsfile(meltsfile)

    def set_envfile(self, env):
        """
        Set the environment for the experiment.

        Parameters
        ------------
        env : :class:`str` | :class:`pathlib.Path`
            Either a path to a valid environment file, a :class:`pandas.Series`, or a
            multiline string representation of a environment file object.
        """
        self.envfile, self.envfilepath = read_envfile(env)

    def _make_folder(self):
        """
        Create the experiment folder.
        """
        self.folder = make_meltsfolder(
            name=self.name,
            title=self.title,
            meltsfile=self.meltsfile,
            indir=self.fromdir,
            env=self.envfile,
        )
        self.meltsfilepath = self.folder / (self.title + ".melts")
        self.envfilepath = self.folder / "environment.txt"

    def run(self, log=False, superliquidus_start=True):
        """
        Call 'run_alphamelts.command'.
        """
        self.mp = MeltsProcess(
            meltsfile=str(self.title) + ".melts",
            env="environment.txt",
            fromdir=str(self.folder),
            timeout=self.timeout,
        )
        self.mp.write([3, [0, 1][superliquidus_start], 4], wait=True, log=log)
        self.mp.terminate()

    def cleanup(self):
        pass


def process_modifications(cfg):
    """
    Process modifications to an configuration composition.

    Parameters
    -----------
    cfg : :class:`dict`
        Configuratiion dictionary.

    Returns
    --------
    cfg : :class:`dict`
        Configuratiion dictionary.
    """
    if "modifychem" in cfg:
        modifications = cfg.pop("modifychem", {})  # remove modify chem
        ek, mk = set(cfg.keys()), set(modifications.keys())
        for k, v in modifications.items():
            if not np.isnan(v):
                cfg[k] = v
        allchem = (ek | mk) & __chem__
        unmodified = (ek - mk) & __chem__

        offset = np.nansum(np.array(list(modifications.values())))
        for uk in unmodified:
            cfg[uk] = np.round(cfg[uk] * (100.0 - offset) / 100, 4)
    return cfg


class MeltsBatch(object):
    """
    Batch of :class:`MeltsExperiment`, which may represent evaluation over a grid of
    parameters or configurations.

    Parameters
    -----------
    comp_df : :class:`pandas.DataFrame`
        Dataframe of compositions.
    default_config : :class:`dict`
        Dictionary of default parameters.
    config_grid : class:`dict`
        Dictionary of parameters to systematically vary.

    Attributes
    -----------

    compositions : :class:`list` of :class:`dict`
        Compositions to use for

    configs : :class:`list` of :class:`dict`

    experiments : :class:`list` of :class:`dict`

    Todo
    ------
        * Can start with a single composition or multiple compositions in a dataframe
        * Enable grid search for individual parameters
        * Improved output logging/reporting
        * Calculate relative number of calculations to be performed for the est duration

            This is currently about correct for an isobaric calcuation at 10 degree
            temperature steps over few hundred degrees - but won't work for different
            T steps.

        * Does number precision make a difference?
    """

    def __init__(
        self,
        comp_df,
        fromdir=Path("./"),
        default_config={},
        config_grid={},
        env=None,
        logger=logger,
        timeout=None,
    ):
        self.timeout = timeout
        self.logger = logger
        self.fromdir = Path(fromdir)
        # make a file logger
        fh = logging.FileHandler(self.fromdir / "autolog.log")
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        self.default = default_config
        self.env = env or MELTS_Env()
        # let's establish the grid of configurations
        self.configs = []
        grid = combine_choices(config_grid)
        for i in grid:  # unique configurations
            _cfg = {**self.default, **i}
            if _cfg not in self.configs:
                self.configs.append(_cfg)
        self.compositions = comp_df.fillna(0).to_dict("records")
        # combine these to create full experiment configs
        exprs = [
            {**cfg, **cmp}
            for (cfg, cmp) in itertools.product(self.configs, self.compositions)
        ]
        exprs = [process_modifications(cfg) for cfg in exprs]
        exphashes = np.array([exp_hash(i) for i in exprs])
        _, cnts = np.unique(exphashes, return_counts=True)
        if (cnts > 1).any():
            self.logger.debug("Duplicate experiments detected.")
        self.experiments = {
            hsh: (exp_name(expr), expr, self.env) for hsh, expr in zip(exphashes, exprs)
        }  # this ensures that no duplicates are preserved

        self.est_duration = str(
            datetime.timedelta(seconds=len(self.experiments) * 15)
        )  # 6s/run
        self.logger.info("Estimated Calculation Time: {}".format(self.est_duration))

    def dump(self, experiments=None, to_dir=None):
        """
        Serialize the configuration to a json file.

        Parameters
        -----------
        experiments : :class:`dict`
            Dictionary of experiments to be serialized.
        to_dir : :class:`str` | :class:`pathlib.Path`
            Directory to export file to.
        """
        to_dir = to_dir or self.fromdir
        experiments = experiments or self.experiments
        data = json.dumps(
            {
                h: (t, exp, env.dump(unset_variables=False))
                for (h, (t, exp, env)) in experiments.items()
            },
            sort_keys=False,
            ensure_ascii=False,
        ).encode("utf8")

        target = Path(to_dir) / "meltsBatchConfig.json"
        target.parent.mkdir(parents=True, exist_ok=True)  # may not exist yet?
        # consider reading old data and leaving updated version here
        target.touch(exist_ok=True)
        with open(target, "wb") as f:
            f.write(data)

    def run(self, overwrite=False, exclude=[], superliquidus_start=True, timeout=None):
        self.dump()  # Serialize the config first
        timeout = self.timeout or timeout
        self.started = time.time()
        experiments = self.experiments
        if not overwrite:
            experiments = {
                h: (t, exp, env)
                for h, (t, exp, env) in experiments.items()
                if not (self.fromdir / h).exists()
            }

        self.logger.info("Starting {} Calculations.".format(len(experiments)))
        paths = []
        failed = []
        for hsh, (title, exp, env) in tqdm(
            experiments.items(), file=ToLogger(self.logger), mininterval=2
        ):
            exp_exclude = exclude
            if "exclude" in exp:
                exp_exclude += exp.pop("exclude")  # remove exclude

            self.logger.debug("Start {}.".format(title))
            meltsfile = dict_to_meltsfile(exp, modes=exp["modes"], exclude=exp_exclude)
            M = MeltsExperiment(
                name=hsh,
                title=title,
                meltsfile=meltsfile,
                env=env,
                fromdir=self.fromdir,
                timeout=timeout,
            )
            try:
                M.run(superliquidus_start=superliquidus_start)
                self.logger.debug("Finished {}.".format(title))
            except OSError:
                try:
                    self.logger.warning("Errored @ {}.".format(M.mp.callstring))
                except:
                    pass
                failed.append(title)
        # should check if it actually ran here (e.g. timeouts)
        self.duration = datetime.timedelta(seconds=time.time() - self.started)
        self.logger.info("Calculations Complete after {}".format(self.duration))
        if failed:
            self.logger.warning("Some calculations errored:")
            for f in failed:
                self.logger.warning(f)

    def cleanup(self):
        pass
