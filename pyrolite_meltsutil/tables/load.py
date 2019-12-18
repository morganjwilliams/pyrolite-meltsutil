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


def read_phase_table(tab):
    """
    Import a phase table to a dataframe.

    Parameters
    ------------
    tab : :class:`str`
        String containing the table to be imported, with its title.

    Returns
    -------
    :class:`pandas.DataFrame`
        DataFrame with phase table information.
    """
    lines = [i for i in re.split(r"[\n\r]", tab) if i]
    phaseID = lines[0].split()[0].strip()
    buff = io.BytesIO("\n".join(lines[1:]).encode("UTF-8"))
    table = pd.read_csv(buff, sep=" ")
    table["phaseID"] = phaseID
    table["phase"] = phasename(phaseID)
    return table


def read_melts_tablefile(filepath, kelvin=False, **kwargs):
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

    df = convert_thermo_names(df)

    if ("temperature" in df.columns) and not kelvin:
        df["temperature"] -= 273.15
    if ("MgO" in df.columns) and ("FeO" in df.columns):
        # should update this to be if there's both iron and magnesium species
        df.pyrochem.add_MgNo()
    df = zero_to_nan(df)
    df = tuple_reindex(df)
    return df


def phasetable_from_alphameltstxt(filepath, kelvin=False):
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

    Todo
    ------

    * If this file exists and is properly formatted, we can pull in alomst all
        the data here.
    """

    filepath = Path(filepath)
    assert filepath.exists()
    with open(str(filepath), "r") as f:
        df = pd.DataFrame()
        data = f.read().strip()
        tables = re.split("Title: ", data)
        tables = [t for t in re.split(r"Title: .*[\n\r][\n\r]+", data, re.DOTALL) if t]
        phasetbl = [t for t in tables if t[0] == t[0].lower()]
        if len(phasetbl) != 1:
            logger.warning("Imported alphaMELTS_tbl.txt incorrectly formatted.")
            return df  # return empty dataframe
        else:
            phasetbl = phasetbl[0]
            for tab in re.split(r"[\n\r][\n\r]+", phasetbl.strip()):
                tabdf = read_phase_table(tab)
                df = df.append(tabdf, sort=False)

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


def phasetable_from_phasemain(filepath, kelvin=False):
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
            df = df.append(read_phase_table(tab), sort=False)

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
    sysfile, bulkfile, solidfile, alphafile = [
        pth / t
        for t in [
            "System_main_tbl.txt",
            "Bulk_comp_tbl.txt",
            "Solid_comp_tbl.txt",
            "alphaMELTS_tbl.txt",
        ]
    ]
    try:
        for f in [sysfile, bulkfile, solidfile, alphafile]:
            assert f.exists()
    except AssertionError:
        msg = "File missing from {}: {}".format(
            pth, ",".join([i.name for i in pth.iterdir()])
        )
        raise FileNotFoundError(msg)
    # system table
    system = read_melts_tablefile(sysfile, skiprows=3, kelvin=kelvin)
    system["step"] = np.arange(system.index.size)  # generate the step index
    system["mass%"] = (system["mass"] / system["mass"].values[0]) * 100
    system["volume%"] = (system["volume"] / system["volume"].values[0]) * 100
    system = system.reindex(
        columns=["step"] + [i for i in system.columns if i != "step"]
    )

    phase = phasetable_from_alphameltstxt(pth / "alphaMELTS_tbl.txt", kelvin=kelvin)
    bulk = read_melts_tablefile(pth / "Bulk_comp_tbl.txt", skiprows=3, kelvin=kelvin)
    solid = read_melts_tablefile(pth / "Solid_comp_tbl.txt", skiprows=3, kelvin=kelvin)

    bulk["phase"] = "bulk"
    solid["phase"] = "solid"
    solid = solid.loc[solid["mass"] > 0.0, :]  # drop where no solids present
    # integrated solids for fractionation - if the system mass changes significantly
    # could add this threshold as a parameter
    frac = system.mass.max() / system.mass.min() > 1.05
    cumulate = integrate_solids(solid, frac=frac)
    cumulate["phase"] = "cumulate"
    # traces could be imported here

    for tb in [bulk, solid, cumulate]:
        phase = phase.append(tb, sort=False)

    phase["step"] = system.loc[phase.index, "step"]
    phase = phase.reindex(columns=["step"] + [i for i in phase.columns if i != "step"])

    phase["mass%"] = phase["mass"] / system.loc[phase.index, "mass"].values[0] * 100
    phase["volume%"] = (
        phase["volume"] / system.loc[phase.index, "volume"].values[0] * 100
    )
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


def aggregate_tables(
    lst=Path("./"), kelvin=False, validate_path=lambda x: len(x.name) == 10
):
    """
    Aggregate a number of melts tables to a single dataframe.

    Parameters
    ------------
    lst : :class:`str` | :class:`pathlib.Path` | :class:`list`
        Directory, list of directories or list of 2-dataframe tuples.
    kelvin : :class:`bool`
        Whether to keep temperatures in kelvin.
    validate_path :
        Function to validate path names.

    Parameters
    ------------
    system : :class:`pandas.DataFrame`
        System aggregate table.
    phases : :class:`pandas.DataFrame`
        Phases aggregate table.
    """
    if isinstance(lst, (str, Path)):
        # if the input is a directory, aggregate subfolders
        lst = [x for x in Path(lst).rglob("*") if (x.is_dir() and validate_path(x))]

    system, phases = pd.DataFrame(), pd.DataFrame()
    if isinstance(lst[0], (str, Path)):
        # if the list is of filenames, aggregate the tables one by one
        for d in lst:
            try:
                S, P = import_tables(d, kelvin=kelvin)
                # ensure the experiment name is incorporated
                S["experiment"] = d.name
                P["experiment"] = d.name

                system = system.append(S, sort=False)
                phases = phases.append(P, sort=False)
            except Exception as e:
                logger.warning("{} at {}.".format(e, d.name)) # record the error
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
