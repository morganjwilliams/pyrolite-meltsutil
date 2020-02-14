import unittest
import numpy as np
import periodictable as pt
from pyrolite.util.general import temp_path, remove_tempdir
from pyrolite_meltsutil.parse import *
from pyrolite_meltsutil.util.general import get_local_example, check_perl

MELTSFILE = get_local_example("Morb.melts")
ENV = get_local_example("alphamelts_default_env.txt")

class TestReadMeltsfile(unittest.TestCase):
    def setUp(self):
        pass

    def test_default(self):
        file, path = read_meltsfile(MELTSFILE)


class TestReadEnvfile(unittest.TestCase):
    def setUp(self):
        pass

    def test_default(self):
        file, path = read_meltsfile(ENV)


class TestParseMELTSComposition(unittest.TestCase):
    def setUp(self):
        self.cstring = """Fe''0.18Mg0.83Fe'''0.04Al1.43Cr0.52Ti0.01O4"""

    def test_parse_dict(self):
        ret = from_melts_cstr(self.cstring, formula=False)
        self.assertTrue(isinstance(ret, dict))
        self.assertTrue("Fe{2+}" in ret.keys())
        self.assertTrue(np.isclose(ret["Fe{2+}"], 0.18))

    def test_parse_formula(self):
        ret = from_melts_cstr(self.cstring, formula=True)
        self.assertTrue(isinstance(ret, pt.formulas.Formula))


if __name__ == "__main__":
    unittest.main()
