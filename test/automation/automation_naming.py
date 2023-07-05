import logging
import unittest

from pyrolite_meltsutil.automation.naming import exp_hash, exp_name
from pyrolite_meltsutil.tables.load import import_batch_config
from pyrolite_meltsutil.util.general import get_data_example

logger = logging.Logger(__name__)

# note that these tests are principally for regression testing & interoperability


class TestExpHash(unittest.TestCase):
    def setUp(self):
        self.exps = {
            k: c
            for (k, (n, c, e)) in import_batch_config(
                get_data_example("montecarlo")
            ).items()
        }

    def test_default(self):
        for k, c in self.exps.items():
            self.assertTrue(k == exp_hash(c))


class TestExpName(unittest.TestCase):
    def setUp(self):
        self.exps = {
            n: c
            for (k, (n, c, e)) in import_batch_config(
                get_data_example("montecarlo")
            ).items()
        }

    def test_default(self):
        for n, c in self.exps.items():
            self.assertTrue(n == exp_name(c))


if __name__ == "__main__":
    unittest.main()
