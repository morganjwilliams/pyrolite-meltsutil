import unittest
import logging
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.tables import import_tables
from pyrolite_meltsutil.vis.scss import plot_sulfur_saturation_point

logger = logging.Logger(__name__)


class TestPlotSCSS(unittest.TestCase):
    def setUp(self):
        self.fromdir = get_data_example("batch/363f3d0a0b/")
        self.system, self.phases = import_tables(self.fromdir)
        self.liquid = self.phases.loc[self.phases.phase == "liquid", :]

    def test_default_plot_sulfur_saturation_point(self):
        ax = plot_sulfur_saturation_point(self.liquid)


if __name__ == "__main__":
    unittest.main()
