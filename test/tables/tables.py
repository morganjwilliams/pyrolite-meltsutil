import unittest
from pyrolite.util.general import temp_path, remove_tempdir
from pyrolite_meltsutil.tables.load import import_tables


class TestImportTables(unittest.TestCase):
    def setUp(self):
        self.dir = temp_path() / "test_melts_temp"
        self.dir.mkdir()

    def test_default(self):
        pass
        # summary = import_tables(self.dir)

    def tearDown(self):
        if self.dir.exists():
            remove_tempdir(self.dir)


if __name__ == "__main__":

    unittest.main()
