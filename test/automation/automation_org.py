import io
import unittest
import pandas as pd
from pyrolite.util.general import check_perl, temp_path, remove_tempdir
from pyrolite_meltsutil.env import MELTS_Env
from pyrolite_meltsutil.automation.org import make_meltsfolder
from pyrolite_meltsutil.util.general import get_local_example
import logging

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


class TestMakeMeltsFolder(unittest.TestCase):
    def setUp(self):
        self.indir = temp_path() / ("testmelts" + self.__class__.__name__)
        self.indir.mkdir(parents=True)
        self.meltsfile = MELTSFILE
        self.env = ENV  # use default

    def test_default(self):
        folder = make_meltsfolder(
            "MORB", "MORB", self.meltsfile, env=self.env, indir=self.indir
        )

    def tearDown(self):
        if self.indir.exists():
            remove_tempdir(self.indir)


if __name__ == "__main__":
    unittest.main()
