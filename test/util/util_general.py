import logging
import unittest

from pyrolite_meltsutil.util.general import check_perl


class TestCheckPerl(unittest.TestCase):
    """Tests the check for a working perl installation."""

    def test_check_perl(self):
        val = check_perl()
        self.assertTrue(isinstance(val, bool))


if __name__ == "__main__":
    unittest.main()
