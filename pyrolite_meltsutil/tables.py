"""
Utilities for reading alphaMELTS table outputs.
"""
import os, sys
import re
import io
import logging
import pandas as pd
from pathlib import Path
import pyrolite.geochem
from .parse import from_melts_cstr
from .meltsfile import to_meltsfiles
from pyrolite.util.pd import zero_to_nan, to_frame, to_ser

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def read_table(filepath, kelvin=False, **kwargs):
    """
    Read a melts table (a space-separated value file).

    Parameters
    -----------
    filepath : :class:`str` | :class:`pathlib.Path`
        Filepath to the melts table.
    kelvin : :class:`bool`
        Whether the imported table has temperature listed in kelvin.

    Returns
    -------
    :class:`pandas.DataFrame`
        DataFrame with table information.
    """
    path = Path(filepath)

    title = get_table_title(filepath)
    df = pd.read_csv(filepath, sep=" ", **kwargs)
    df = df.dropna(how="all", axis=1)

    if ("Temperature" in df.columns) and not kelvin:
        df.Temperature -= 273.15
    if ("MgO" in df.columns) and ("FeO" in df.columns):
        # should update this to be if there's both iron and magnesium species
        df.pyrochem.add_MgNo()
    return df


def format_meltstable(df, tablename=None):
    """
    Format an imported melts table based on its name and content.

    Parameters
    -----------
    df : :class:`pandas.DataFrame`
        Dataframe comtaining melts table.
    tablename : :class:`str`
        Name of the imported table.

    Returns
    -------
    :class:`pandas.DataFrame`
        DataFrame with table information.
    """
    if df is not None:
        # what to do with traces?
        df.pyrochem.compositional = df.pyrochem.compositional.apply(
            pd.to_numeric, errors="coerce"
        )
        if "mass" in df.columns:
            if tablename == "phasemass":
                mins = [
                    i
                    for i in df.columns
                    if i not in ["Pressure", "Temperature", "mass"]
                ]
                df[mins] = df[mins].apply(pd.to_numeric, errors="coerce")
                df[mins] = df[mins].div(
                    df["mass"].values / 100.0, axis="index"
                )  # weight %

            df["mass%"] = df["mass"] / df["mass"].values[0]

        if "V" in df.columns:
            if tablename == "phasevol":
                # divide chem/mineral masses by the total volume.
                mins = [
                    i
                    for i in df.columns
                    if i not in ["Pressure", "Temperature", "mass", "V"]
                ]
                df[mins] = df.loc[:, mins].apply(pd.to_numeric, errors="coerce")
                df[mins] = df[mins].div(df["V"] / 100.0, axis="index")  # volume %

            df["V%"] = df["V"] / df["V"].values[0]
    return df


def get_table_title(filepath):
    """
    Open a table and extract the filename.

    Parameters
    -----------
    filepath : :class:`str` | :class:`pathlib.Path`
        Path to the table file.

    Returns
    --------
    :class:`str`
    """
    with open(filepath) as f:
        title = f.readline().replace("Title: ", "").strip()
    return title


def get_experiments_summary(dir, **kwargs):
    """
    Aggregate alphaMELTS experiment results across folders within a directory,
    or for a list of directories.

    Parameters
    -----------
    dir : :class:`str` | :class:`pathlib.Path` | :class:`list`
        Directory to aggregate folders from, or list of folders.

    Returns
    --------
    :class:`dict`
        Dictonary of experiment outputs indexed by titles.
    """
    if isinstance(dir, list):
        target_folders = dir
    else:
        dir = Path(dir)
        target_folders = [p for p in dir.iterdir() if p.is_dir()]
    summary = {}
    for ix, t in enumerate(target_folders):
        output = MeltsOutput(t, **kwargs)
        summary[output.title] = {}
        summary[output.title]["phases"] = {
            i[: i.find("_")] if i.find("_") > 0 else i for i in output.phasenames
        }
        summary[output.title]["output"] = output
    return summary


def write_summary_phaselist(dir=None, summary=None, filename="phaselist.txt"):
    """
    Write the list of phases from an alphamelts experiment to file.

    Parameters
    -----------
    dir : :class:`str` | :class:`pathlib.Path`
        Path to the experiment directory.
    summary : :class:`dict`
        Summary of a series of melts experiements, optional.
    """
    if summary is None:
        summary = get_experiments_summary(dir, kelvin=False)
    try:
        mnl = max([len(name) for name in summary])
        phases = [
            name + " " * (mnl - len(name) + 2) + ", ".join(D["phases"])
            for name, D in summary.items()
        ]
        with open(dir / filename, "w") as f:
            f.write("\n".join([phases]))
    except (TypeError):
        open(dir / filename, "a").close()  # touch file - nothing to add here


class MeltsOutput(object):
    """
    alphaMELTS output tables acessible from a single object.

    Todo
    -----
    * Master experimenttable so everything is accessible without having to browse tables
    """

    def __init__(self, directory, kelvin=True):
        self.title = None
        self.kelvin = kelvin
        self.phasenames = set([])
        self.majors = set([])
        self.traces = set([])
        self.phases = {}
        dir = Path(directory)
        for tablename, table, tableload in [
            # these tables have absolute masses and volumes
            ("phasemass", "Phase_mass_tbl.txt", self._read_phasemass),
            ("phasevol", "Phase_vol_tbl.txt", self._read_phasevol),
            ("system", "System_main_tbl.txt", self._read_systemmain),
            # comp tables and phasemain have wt% masses
            ("liquidcomp", "Liquid_comp_tbl.txt", self._read_liquidcomp),
            ("solidcomp", "Solid_comp_tbl.txt", self._read_solidcomp),
            ("bulkcomp", "Bulk_comp_tbl.txt", self._read_bulkcomp),
            ("tracecomp", "Trace_main_tbl.txt", self._read_trace),
            ("phasemain", "Phase_main_tbl.txt", self._read_phasemain),
        ]:
            tpath = dir / table
            try:
                assert (
                    tpath.exists and tpath.is_file
                ), "Expected file {} does not exist.".format(tpath)
                title = get_table_title(tpath)
                self._set_title(title)

                tbl = tableload(tpath)
                tbl = format_meltstable(tbl, tablename=tablename)
            except:
                logger.debug("Error on table import: {} {}".format(self.title, tpath))
                tbl = pd.DataFrame()  # empty dataframe
            setattr(self, tablename, tbl)

    @property
    def tables(self):
        """
        Get the set of tables accesible from the output object.

        Returns
        -------
        :class:`set`
            Tables accesible from the :class:`MeltsOutput` object.
        """
        return {
            "bulkcomp",
            "solidcomp",
            "liquidcomp",
            "phasemass",
            "phasevol",
            "tracecomp",
            "system",
        }

    def _set_title(self, title):
        if self.title is None:
            self.title = title
        else:
            if title == self.title:
                pass
            else:
                logger.debug(
                    "File with conflicting title found: {}; expected {}".format(
                        title, self.title
                    )
                )

    def _read_solidcomp(self, filepath, skiprows=3):
        table = read_table(filepath, skiprows=skiprows, kelvin=self.kelvin)
        table = zero_to_nan(table)
        return table

    def _read_liquidcomp(self, filepath, skiprows=3):
        table = read_table(filepath, skiprows=skiprows, kelvin=self.kelvin)
        table = zero_to_nan(table)
        return table

    def _read_bulkcomp(self, filepath, skiprows=3):
        table = read_table(filepath, skiprows=skiprows, kelvin=self.kelvin)
        table = zero_to_nan(table)
        return table

    def _read_phasemass(self, filepath, skiprows=3):
        table = read_table(filepath, skiprows=skiprows, kelvin=self.kelvin)
        table = zero_to_nan(table)
        self.phasenames = self.phasenames | set(
            [
                i
                for i in table.columns
                if i not in ["Pressure", "Temperature", "mass", "V"]
            ]
        )
        return table

    def _read_phasevol(self, filepath, skiprows=3):
        table = read_table(filepath, skiprows=skiprows, kelvin=self.kelvin)
        table = zero_to_nan(table)
        self.phasenames = self.phasenames | set(
            [
                i
                for i in table.columns
                if i not in ["Pressure", "Temperature", "mass", "V"]
            ]
        )
        return table

    def _read_systemmain(self, filepath, skiprows=3):
        table = read_table(filepath, skiprows=skiprows, kelvin=self.kelvin)
        table = zero_to_nan(table)
        return table

    def _read_trace(self, filepath, header=3):
        pass

    def _read_phasemain(self, filepath, header=3):
        # can throw errors if run before alphamelts is exited
        with open(filepath) as f:
            data = f.read().split("\n\n")[1:]
            for tab in data:
                lines = re.split(r"[\n\r]", tab)
                phase = lines[0].split()[0].strip()
                table = pd.read_csv(
                    io.BytesIO("\n".join(lines[1:]).encode("UTF-8")), sep=" "
                )
                table = zero_to_nan(table)
                if "formula" in table.columns:
                    table.loc[:, "formula"] = table.loc[:, "formula"].apply(
                        from_melts_cstr
                    )
                if ("Temperature" in table.columns) and not self.kelvin:
                    table.Temperature -= 273.15
                self.phases[phase] = table

    def _read_logfile(filepath):
        pass
