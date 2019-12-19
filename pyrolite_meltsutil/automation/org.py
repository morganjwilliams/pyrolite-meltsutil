from pathlib import Path
from ..parse import read_envfile, read_meltsfile
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def make_meltsfolder(
    name, title=None, meltsfile=None, indir=None, env="./alphamelts_default_env.txt"
):
    """
    Create a folder for a given meltsfile, including the default environment file.
    From this folder, pass these to alphamelts with
    :code:`run_alphamelts.command -m <meltsfile> -f <envfile>`.

    Parameters
    -----------
    name : :class:`str`
        Name of the folder.
    title : :class:`str`
        Title of the experiment. This will be the meltsfile name.
    meltsfile : :class:`str`
        String containing meltsfile info.
    indir : :class:`str` | :class:`pathlib.Path`
        Path to the base directory to create melts folders in.
    env : :class:`str` | :class:`pathlib.Path`
        Path to a specific environment file to use as the default environment for the
        experiment.

    Returns
    --------
    :class:`pathlib.Path`
        Path to melts folder.

    Todo
    ------
        * Options for naming environment files
    """
    if indir is None:
        indir = Path("./")
    else:
        indir = Path(indir)
    assert meltsfile is not None
    name = str(name)  # need to pathify this!
    title = title or name
    title = str(title)  # need to pathify this!
    experiment_folder = indir / name
    if not experiment_folder.exists():
        experiment_folder.mkdir(parents=True)

    meltsfile, mpath = read_meltsfile(meltsfile)
    assert experiment_folder.exists() and experiment_folder.is_dir()
    (experiment_folder / title).with_suffix(".melts").touch()
    with open(str((experiment_folder / title).with_suffix(".melts")), "w") as f:
        f.write(meltsfile)

    (experiment_folder / "environment").with_suffix(".txt").touch()
    env, epath = read_envfile(env, unset_variables=False)
    with open(str(experiment_folder / "environment.txt"), "w") as f:
        f.write(env)

    return experiment_folder  # return the folder name
