import logging
import unittest

from pyrolite_meltsutil.tables import import_tables
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.vis.templates import (  # plot_xy_phase_groupby,
    plot_phasemasses,
    plot_phasevolumes,
)

logger = logging.Logger(__name__)


class TestPlotTemplates(unittest.TestCase):
    def setUp(self):
        self.fromdir = get_data_example("batch/363f3d0a0b/")
        self.system, self.phases = import_tables(self.fromdir)

    def test_default_phasevolumes(self):
        ax = plot_phasevolumes(self.phases)

    def test_default_phasemasses(self):
        ax = plot_phasemasses(self.phases)


if __name__ == "__main__":
    unittest.main()
