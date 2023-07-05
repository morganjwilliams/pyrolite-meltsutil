import unittest
from collections import OrderedDict

from pyrolite_meltsutil.util.synthetic import default_data_dictionary


class TestDefaultMELTSDict(unittest.TestCase):
    def test_default(self):
        D = default_data_dictionary()
        self.assertIsInstance(D, (OrderedDict, dict))
        self.assertIn("title", D)
        self.assertIn("initialize", D)
        self.assertIn("calculationMode", D)
        self.assertIn("constraints", D)


if __name__ == "__main__":
    unittest.main()
