import logging
import unittest

from pyrolite.util.general import remove_tempdir, temp_path

from pyrolite_meltsutil.tables.load import (
    aggregate_tables,
    import_batch_config,
    import_tables,
    phasetable_from_alphameltstxt,
    phasetable_from_phasemain,
    read_melts_tablefile,
    read_phase_table,
)
from pyrolite_meltsutil.util.general import get_data_example

logger = logging.Logger(__name__)


class TestPhasetableFromalphaMELTS(unittest.TestCase):
    def setUp(self):
        self.file = get_data_example("batch/363f3d0a0b/alphaMELTS_tbl.txt")

    def test_default(self):
        src = self.file
        out = phasetable_from_alphameltstxt(src)


class TestPhasetableFromPhasemain(unittest.TestCase):
    def setUp(self):
        self.file = get_data_example("batch/363f3d0a0b/Phase_main_tbl.txt")

    def test_default(self):
        src = self.file
        out = phasetable_from_phasemain(src)


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


class TestImportBatchConfig(unittest.TestCase):
    def setUp(self):
        self.fromdir = get_data_example("batch/")

    def test_default(self):
        src = self.fromdir
        out = import_batch_config(src)
        self.assertIsInstance(out, dict)
        self.assertIn("363f3d0a0b", out.keys())


if __name__ == "__main__":
    unittest.main()
