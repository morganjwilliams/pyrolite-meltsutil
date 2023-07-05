import io
import logging
import unittest

import pandas as pd
from pyrolite.geochem.norm import get_reference_composition
from pyrolite.util.general import remove_tempdir, temp_path
from pyrolite.util.pd import to_numeric

from pyrolite_meltsutil.automation import MeltsBatch, MeltsExperiment, MeltsProcess
from pyrolite_meltsutil.automation.org import make_meltsfolder
from pyrolite_meltsutil.env import MELTS_Env
from pyrolite_meltsutil.util.general import check_perl, get_local_example

logger = logging.Logger(__name__)

ENV = MELTS_Env()
ENV.VERSION = "MELTS"
ENV.MODE = "isobaric"
ENV.MINP = 2000
ENV.MAXP = 10000
ENV.MINT = 500
ENV.MAXT = 1500
ENV.DELTAT = -10
ENV.DELTAP = 0

with open(str(get_local_example("Morb.melts"))) as f:
    MELTSFILE = f.read()


@unittest.skipIf(not check_perl(), "Perl is not installed.")
class TestMeltsProcess(unittest.TestCase):
    def setUp(self):
        self.fromdir = temp_path() / ("testmelts" + self.__class__.__name__)
        self.fromdir.mkdir(parents=True)
        self.meltsfile = MELTSFILE
        self.env = ENV  # use default

    def test_default(self):
        title = "TestMeltsProcess"
        folder = make_meltsfolder(
            name=title,
            meltsfile=self.meltsfile,
            title=title,
            env=self.env,
            indir=self.fromdir,
        )
        process = MeltsProcess(
            meltsfile="{}.melts".format(title),
            env="environment.txt",
            fromdir=str(folder),
        )
        txtfiles = list(self.fromdir.glob("**/*.txt"))
        meltsfiles = list(self.fromdir.glob("**/*.melts"))
        process.write([3, 1, 4], wait=True, log=False)
        process.terminate()

    def tearDown(self):
        if self.fromdir.exists():
            try:
                remove_tempdir(self.fromdir)
            except FileNotFoundError:
                pass


@unittest.skipIf(not check_perl(), "Perl is not installed.")
class TestMeltsExperiment(unittest.TestCase):
    def setUp(self):
        self.fromdir = temp_path() / ("testmelts" + self.__class__.__name__)
        self.fromdir.mkdir(parents=True)
        self.meltsfile = MELTSFILE
        self.env = ENV  # use default

    def test_default(self):
        exp = MeltsExperiment(
            meltsfile=self.meltsfile,
            title="TestMeltsExperiment",
            env=self.env,
            fromdir=self.fromdir,
        )
        # check the folder has been created correctly
        txtfiles = list(self.fromdir.glob("**/*.txt"))
        meltsfiles = list(self.fromdir.glob("**/*.melts"))
        exp.run()
        exp.cleanup()

    def tearDown(self):
        if self.fromdir.exists():
            try:
                remove_tempdir(self.fromdir)
            except FileNotFoundError:
                pass


@unittest.skipIf(not check_perl(), "Perl is not installed.")
class TestMeltsBatch(unittest.TestCase):
    def setUp(self):
        self.fromdir = temp_path() / ("testmelts" + self.__class__.__name__)
        self.fromdir.mkdir(parents=True)
        Gale_MORB = get_reference_composition("MORB_Gale2013")
        majors = [
            "SiO2",
            "Al2O3",
            "FeO",
            "MnO",
            "MgO",
            "CaO",
            "Na2O",
            "TiO2",
            "K2O",
            "P2O5",
        ]
        MORB = Gale_MORB.comp.loc[:, majors].apply(pd.to_numeric)
        MORB = pd.concat([MORB, MORB]).reset_index(drop=True)
        MORB["Title"] = [
            "{}_{}".format(Gale_MORB.name, ix).replace("_", "")
            for ix in MORB.index.values.astype(str)
        ]
        MORB["Initial Temperature"] = 1300
        MORB["Final Temperature"] = 800
        MORB["Initial Pressure"] = 5000
        MORB["Final Pressure"] = 5000
        MORB["Log fO2 Path"] = "FMQ"
        MORB["Increment Temperature"] = -5
        MORB["Increment Pressure"] = 0
        self.df = MORB
        self.env = ENV

    def test_default(self):
        batch = MeltsBatch(
            self.df,
            default_config={
                "Initial Pressure": 7000,
                "Initial Temperature": 1400,
                "Final Temperature": 800,
                "modes": ["isobaric"],
            },
            config_grid={"Initial Pressure": [5000]},
            env=self.env,
            fromdir=self.fromdir,
            logger=logger,
        )
        batch.run()

    def tearDown(self):
        if self.fromdir.exists():
            try:
                remove_tempdir(self.fromdir)
            except FileNotFoundError:
                pass


if __name__ == "__main__":
    unittest.main()
