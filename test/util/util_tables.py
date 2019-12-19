import unittest
import numpy as np
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.tables.load import import_tables
from pyrolite_meltsutil.util.tables import (
    phasename,
    tuple_reindex,
    integrate_solid_proportions,
    integrate_solid_composition,
)
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

    def test_frac_compositions(self):
        cumulate = integrate_solid_composition(self.fracphases)
        # should have an index equivalent to the system index
        self.assertTrue(cumulate.index.size == self.fracsystem.index.size)
        self.assertTrue((cumulate.index == self.fracsystem.index).all())

    def test_non_frac_compositions(self):
        cumulate = integrate_solid_composition(self.nofracphases)
        # should have an index equivalent to the system index
        self.assertTrue(cumulate.index.size == self.nofracsystem.index.size)
        self.assertTrue((cumulate.index == self.nofracsystem.index).all())

    def test_frac_proportions(self):
        cumulate = integrate_solid_proportions(self.fracphases)
        # should have an index equivalent to the system index
        self.assertTrue(cumulate.index.size == self.fracsystem.index.size)
        self.assertTrue((cumulate.index == self.fracsystem.index).all())
        self.assertTrue(  # sums are 100% or nan/0
            all(
                np.isclose(cumulate.sum(axis=1).values, 100)
                + np.isclose(cumulate.sum(axis=1).values, 0)
            )
        )

    def test_non_frac_proportions(self):
        cumulate = integrate_solid_proportions(self.nofracphases)
        # should have an index equivalent to the system index
        self.assertTrue(cumulate.index.size == self.nofracsystem.index.size)
        self.assertTrue((cumulate.index == self.nofracsystem.index).all())
        self.assertTrue(  # sums are 100% or nan/0
            all(
                np.isclose(cumulate.sum(axis=1).values, 100)
                + np.isclose(cumulate.sum(axis=1).values, 0)
            )
        )


if __name__ == "__main__":
    unittest.main()
