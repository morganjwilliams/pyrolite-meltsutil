import unittest
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.tables.load import import_tables
from pyrolite_meltsutil.util.tables import phasename, tuple_reindex, integrate_solids
import logging

logger = logging.Logger(__name__)


class TestPhasename(unittest.TestCase):
    def setUp(self):
        pass


class TestTupleReindex(unittest.TestCase):
    def setUp(self):
        pass


class TestIntegrateSolids(unittest.TestCase):
    def setUp(self):
        self.fracdir = get_data_example("batch/363f3d0a0b/")
        self.nofracdir = get_data_example("montecarlo/97ed8127d9")
        self.fracsystem, self.fracphases = import_tables(self.fracdir)
        self.nofracsystem, self.nofracphases = import_tables(self.nofracdir)

    def test_frac(self):
        cumulate = integrate_solids(self.fracphases)

    def test_non_frac(self):
        cumulate = integrate_solids(self.nofracphases)


if __name__ == "__main__":
    unittest.main()
