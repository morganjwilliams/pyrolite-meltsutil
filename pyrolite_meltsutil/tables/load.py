"""
Functions for loading alphaMELTS tables to :class:`pandas.DataFrame`.

Notes
-------

    * Some variable abbreviations are converted to their names (e.g.
        enthalpy, entropy and volume).
"""
import re
import io
import json
import pandas as pd
import numpy as np
from pathlib import Path
from pyrolite.util.pd import zero_to_nan
from ..parse import from_melts_cstr
from ..util.tables import phasename, tuple_reindex, integrate_solids
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

TABLES = {
    "Phase_mass_tbl.txt",
    "Phase_vol_tbl.txt",
    "System_main_tbl.txt",
    "Liquid_comp_tbl.txt",
    "Solid_comp_tbl.txt",
    "Bulk_comp_tbl.txt",
    "Trace_main_tbl.txt",
    "Phase_main_tbl.txt",
}

THERMO = {"H": "enthalpy", "S": "entropy", "V": "volume"}
THERMO.update({c: c.lower() for c in ["Pressure", "Temperature"]})


def convert_thermo_names(df):
    """
    Convert the abbreviations for thermodynamic variables (e.g. H, S) to
    expanded names. This avoids some issues with pulling out compositions.

    Parameters
    ------------
    :class:`pandas.DataFrame`
        DataFrame to convert column names for.

    Returns
    -------
    :class:`pandas.DataFrame`
        DataFrame with table information.
    """
    df.rename(columns=THERMO, inplace=True)
    return df


def read_melts_table(filepath, kelvin=False, **kwargs):
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

    # title = get_table_title(filepath)
    df = pd.read_csv(filepath, sep=" ", **kwargs)
    df = df.dropna(how="all", axis=1)

    if ("Temperature" in df.columns) and not kelvin:
        df["Temperature"] -= 273.15
    if ("MgO" in df.columns) and ("FeO" in df.columns):
        # should update this to be if there's both iron and magnesium species
        df.pyrochem.add_MgNo()
    df = zero_to_nan(df)
    df = tuple_reindex(df)
    df = convert_thermo_names(df)
    return df


def read_alphamelts_table_phases(filepath, kelvin=False):
    """
    Read the phasemain file into a single table. Note that the alphaMELTS table
    includes all other tables also (except for traces).

    Parameters
    ------------
    filepath : :class:`str` | :class:`pathlib.Path`
        Filepath to the melts table.
    kelvin : :class:`bool`
        Whether the exported table has temperature listed in kelvin.

    Returns
    -------
    :class:`pandas.DataFrame`
        DataFrame with table information.
    """
    df = pd.DataFrame()
    with open(str(filepath)) as f:
        data = f.read()
        title_line = re.split(r"[\n\r]+", data)[0]
        _, *tables = re.split(title_line.strip(), data)
        system, liquidcomp, phases, phasemass, phasevol, solidcomp, bulkcomp = tables
        for tab in re.split(r"[\n\r][\n\r]+", phases.strip()):
            lines = [i for i in re.split(r"[\n\r]", tab) if i]
            phaseID = lines[0].split()[0].strip()
            buff = io.BytesIO("\n".join(lines[1:]).encode("UTF-8"))
            table = pd.read_csv(buff, sep=" ")
            table["phaseID"] = phaseID
            table["phase"] = phasename(phaseID)

            df = df.append(table, sort=False)

    df = convert_thermo_names(df)
    non_num = ["step", "structure", "phaseID", "phase", "formula"]
    num = [i for i in df.columns if i not in non_num]
    df[num] = df[num].apply(pd.to_numeric, errors="coerce")

    if "formula" in df.columns:
        df.loc[:, "formula"] = df.loc[:, "formula"].apply(from_melts_cstr)

    if ("temperature" in df.columns) and not kelvin:
        df["temperature"] -= 273.15

    if ("MgO" in df.columns) and ("FeO" in df.columns):
        # should update this to be if there's both iron and magnesium species
        df.pyrochem.add_MgNo()

    df = zero_to_nan(df)
    df = tuple_reindex(df)
    return df


def read_phasemain(filepath, kelvin=False):
    """
    Read the phasemain file into a single table.

    Parameters
    ------------
    filepath : :class:`str` | :class:`pathlib.Path`
        Filepath to the melts table.
    kelvin : :class:`bool`
        Whether the exported table has temperature listed in kelvin.

    Returns
    -------
    :class:`pandas.DataFrame`
        DataFrame with table information.
    """
    df = pd.DataFrame()
    with open(str(filepath)) as f:
        data = re.split(r"[\n\r][\n\r]+", f.read())[1:]  # double line sep
        for tab in data:
            lines = [i for i in re.split(r"[\n\r]", tab) if i]
            phaseID = lines[0].split()[0].strip()
            buff = io.BytesIO("\n".join(lines[1:]).encode("UTF-8"))
            try:
                table = pd.read_csv(buff, sep=" ")
            except:
                msg = "Read issue at: {}-{}\n{}\nFrom:\n{}".format(
                    filepath, phaseID, tab, data
                )
                raise Exception(msg)
            table["phaseID"] = phaseID
            table["phase"] = phasename(phaseID)

            df = df.append(table, sort=False)

    df = convert_thermo_names(df)
    non_num = ["step", "structure", "phaseID", "phase", "formula"]
    num = [i for i in df.columns if i not in non_num]
    df[num] = df[num].apply(pd.to_numeric, errors="coerce")

    if "formula" in df.columns:
        df.loc[:, "formula"] = df.loc[:, "formula"].apply(from_melts_cstr)

    if ("temperature" in df.columns) and not kelvin:
        df["temperature"] -= 273.15

    if ("MgO" in df.columns) and ("FeO" in df.columns):
        # should update this to be if there's both iron and magnesium species
        df.pyrochem.add_MgNo()

    df = zero_to_nan(df)
    df = tuple_reindex(df)
    return df


def import_tables(pth, kelvin=False):
    """
    Import tables from a directory.

    Parameters
    -----------
    kelvin : :class:`bool`
        Whether to keep temperatures in kelvin.

    Returns
    --------
    system : :class:`pandas.DataFrame`

    phases : :class:`pandas.DataFrame`
    """
    # system table
    system = read_melts_table(pth / "System_main_tbl.txt", skiprows=3, kelvin=kelvin)
    system["step"] = np.arange(system.index.size)  # generate the step index
    system["mass%"] = system["mass"] / system["mass"].values[0]
    system["volume%"] = system["volume"] / system["volume"].values[0]
    system = system.reindex(
        columns=["step"] + [i for i in system.columns if i != "step"]
    )

    phase = read_alphamelts_table_phases(pth / "Phase_main_tbl.txt", kelvin=kelvin)

    # bulk composition
    bulk = read_melts_table(pth / "Bulk_comp_tbl.txt", skiprows=3, kelvin=kelvin)
    bulk["phase"] = "bulk"
    # solid composition
    solid = read_melts_table(pth / "Solid_comp_tbl.txt", skiprows=3, kelvin=kelvin)
    solid["phase"] = "solid"
    solid = solid.loc[solid["mass"] > 0.0, :]  # drop where no solids present
    # integrated solids for fractionation
    cumulate = integrate_solids(solid)
    cumulate["phase"] = "cumulate"
    # traces could be imported here

    for tb in [bulk, solid, cumulate]:
        phase = phase.append(tb, sort=False)

    phase["step"] = system.loc[phase.index, "step"]
    phase = phase.reindex(columns=["step"] + [i for i in phase.columns if i != "step"])

    phase["mass%"] = phase["mass"] / system.loc[phase.index, "mass"].values[0] * 100
    phase["volume%"] = phase["volume"] / system.loc[phase.index, "volume"].values[0]
    return system, phase


def import_batch_config(filepath):
    """
    Import a batch configuration file.

    Parameters
    -----------
    filepath : :class:`str` | :class:`pathlib.Path`

    Returns
    ---------
    :class:`dict`
        Configuration dictionary indexed by hashes.
    """

    filepath = Path(filepath)
    if filepath.is_dir():
        # find config
        cfgpath = filepath / "meltsBatchConfig.json"
    else:
        cfgpath = filepath.with_suffix("json")

    with open(str(cfgpath), "r") as f:
        cfg = json.loads(f.read())
    return cfg


def aggregate_tables(lst, kelvin=False):
    """
    Aggregate a number of melts tables to a single dataframe.

    Parameters
    ------------
    lst : :class:`str` | :class:`pathlib.Path` | :class:`list`
        Directory, list of directories or list of 2-dataframe tuples.
    kelvin : :class:`bool`
        Whether to keep temperatures in kelvin.

    Parameters
    ------------
    system : :class:`pandas.DataFrame`
        System aggregate table.
    phases : :class:`pandas.DataFrame`
        Phases aggregate table.
    """
    # if the input is a directory, aggregate subfolders
    if isinstance(lst, (str, Path)):
        lst = [x for x in Path(lst).rglob("*") if x.is_dir()]
    system, phases = pd.DataFrame(), pd.DataFrame()
    if isinstance(lst[0], (str, Path)):
        # if the list is of filenames, aggregate the tables one by one
        for d in lst:
            S, P = import_tables(d, kelvin=kelvin)
            # ensure the experiment name is incorporated
            S["experiment"] = d.name
            P["experiment"] = d.name

            system = system.append(S, sort=False)
            phases = phases.append(P, sort=False)
    elif isinstance(lst[0], (list, tuple)) and isinstance(lst[0][0], (pd.DataFrame)):
        # if the list is of tuples of dataframes,
        # aggregate them to a single table
        Sagg, Pagg = pd.DataFrame(), pd.DataFrame()
        for ix, d in enumerate(lst):
            S, P = d
            # ensure the experiment index is incorporated
            S["experiment"] = ix
            P["experiment"] = ix

            system = system.append(S, sort=False)
            phases = phases.append(P, sort=False)
    else:
        raise NotImplementedError

    system = system.reindex(
        columns=["experiment"] + [i for i in system.columns if i != "experiment"]
    )
    phases = phases.reindex(
        columns=["experiment"] + [i for i in phases.columns if i != "experiment"]
    )
    return system, phases
