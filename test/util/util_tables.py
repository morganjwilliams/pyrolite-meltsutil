import logging
import unittest

import numpy as np

from pyrolite_meltsutil.tables.load import import_tables
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.util.tables import (
    integrate_solid_composition,
    integrate_solid_proportions,
    phasename,
    tuple_reindex,
)

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
        self.nofracdir = get_data_example("montecarlo/80de472f12")
        self.fracsystem, self.fracphases = import_tables(self.fracdir)
        self.nofracsystem, self.nofracphases = import_tables(self.nofracdir)

    def test_frac_compositions(self):
        cumulate = integrate_solid_composition(self.fracphases, frac=True)
        # should have an index equivalent to the system index
        self.assertTrue(cumulate.index.size == self.fracsystem.index.size)
        self.assertTrue((cumulate.index == self.fracsystem.index).all())

    def test_non_frac_compositions(self):
        cumulate = integrate_solid_composition(self.nofracphases, frac=False)
        # should have an index equivalent to the system index
        self.assertTrue(cumulate.index.size == self.nofracsystem.index.size)
        self.assertTrue((cumulate.index == self.nofracsystem.index).all())

    def test_frac_proportions(self):
        cumulate = integrate_solid_proportions(self.fracphases, frac=True)
        # should have an index equivalent to the system index
        self.assertTrue(cumulate.index.size == self.fracsystem.index.size)
        self.assertTrue((cumulate.index == self.fracsystem.index).all())
        mincols = [
            i for i in cumulate.columns if i not in ["pressure", "temperature", "step"]
        ]
        self.assertTrue(  # sums are 100% or nan/0
            all(
                np.isclose(cumulate[mincols].sum(axis=1).values, 100, atol=10e-3)
                + np.isclose(cumulate[mincols].sum(axis=1).values, 0, atol=10e-3)
            )
        )

    def test_non_frac_proportions(self):
        cumulate = integrate_solid_proportions(self.nofracphases, frac=False)
        # should have an index equivalent to the system index
        self.assertTrue(cumulate.index.size == self.nofracsystem.index.size)
        self.assertTrue((cumulate.index == self.nofracsystem.index).all())
        mincols = [
            i for i in cumulate.columns if i not in ["pressure", "temperature", "step"]
        ]
        self.assertTrue(  # sums are 100% or nan/0
            all(
                np.isclose(cumulate[mincols].sum(axis=1).values, 100, atol=10e-2)
                + np.isclose(cumulate[mincols].sum(axis=1).values, 0, atol=10e-2)
            )
        )


if __name__ == "__main__":
    unittest.main()
