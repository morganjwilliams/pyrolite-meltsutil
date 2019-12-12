import unittest
from pyrolite.util.general import temp_path, remove_tempdir
from pyrolite_meltsutil.tables.load import (
    import_tables,
    read_phasemain,
    read_melts_table,
    read_alphamelts_table_phases,
    aggregate_tables,
)
from pyrolite_meltsutil.util.general import get_data_example
import logging

logger = logging.Logger(__name__)


class TestReadalphaMELTSTable(unittest.TestCase):
    def setUp(self):
        self.file = get_data_example("batch/363f3d0a0b/alphaMELTS_tbl.txt")

    def test_default(self):
        src = self.file
        out = read_alphamelts_table_phases(src)


class TestReadPhasemain(unittest.TestCase):
    def setUp(self):
        self.file = get_data_example("batch/363f3d0a0b/Phase_main_tbl.txt")

    def test_default(self):
        src = self.file
        out = read_phasemain(src)


class TestImportTables(unittest.TestCase):
    def setUp(self):
        self.fromdir = get_data_example("batch/363f3d0a0b/")

    def test_default(self):
        src = self.fromdir
        out = import_tables(src)


class TestAggregateTables(unittest.TestCase):
    def setUp(self):
        self.fromdir = get_data_example("batch/")

    def test_default(self):
        src = self.fromdir
        out = aggregate_tables(src)


if __name__ == "__main__":
    unittest.main()
