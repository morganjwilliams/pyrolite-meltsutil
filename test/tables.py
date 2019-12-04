import unittest
from pyrolite_meltsutil.download import install_melts
from pyrolite.util.meta import stream_log
from pyrolite.util.general import check_perl, temp_path, remove_tempdir
from pyrolite_meltsutil.tables import get_experiments_summary, MeltsOutput
from pyrolite_meltsutil.util import pyrolite_meltsutil_datafolder

_env = (
    pyrolite_meltsutil_datafolder(subfolder="localinstall")
    / "examples"
    / "alphamelts_default_env.txt"
)

_melts = (
    pyrolite_meltsutil_datafolder(subfolder="localinstall") / "examples" / "Morb.melts"
)

if not pyrolite_meltsutil_datafolder(subfolder="localinstall").exists():
    stream_log("pyrolite.ext.alphamelts")
    install_melts(local=True)  # install melts for example files etc


class TestGetExperimentsSummary(unittest.TestCase):
    def setUp(self):
        self.dir = temp_path() / "test_melts_temp"
        self.dir.mkdir()

    def test_default(self):
        pass
        # summary = get_experiments_summary(self.dir)

    def tearDown(self):
        if self.dir.exists():
            remove_tempdir(self.dir)


if __name__ == "__main__":

    unittest.main()
