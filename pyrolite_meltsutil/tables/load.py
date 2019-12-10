"""
Functions for loading alphaMELTS tables to :class:`pandas.DataFrame`.

Notes
-------

    * Some variable abbreviations are converted to their names (e.g.
        enthalpy, entropy and volume).
"""
import re
import io
import pandas as pd
import numpy as np
from pathlib import Path
from pyrolite.util.pd import zero_to_nan
from ..parse import from_melts_cstr
from ..util.tables import phasename, tuple_reindex, integrate_solids

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


def read_phasemain(filepath, kelvin=False):
    """
    Read the phasemain file into a single table.

    Parameters
    ------------
    filepath : :class:`str` | :class:`pathlib.Path`
        Filepath to the melts table.
    kelvin : :class:`bool`
        Whether the imported table has temperature listed in kelvin.

    Returns
    -------
    :class:`pandas.DataFrame`
        DataFrame with table information.
    """
    kelvin = False
    df = pd.DataFrame()
    with open(filepath) as f:
        data = f.read().split("\n\n")[1:]
        for tab in data:
            lines = re.split(r"[\n\r]", tab)
            phaseID = lines[0].split()[0].strip()
            table = pd.read_csv(
                io.BytesIO("\n".join(lines[1:]).encode("UTF-8")), sep=" "
            )
            table["phaseID"] = phaseID
            table["phase"] = phasename(phaseID)

            df = df.append(table, sort=False)

    if "formula" in df.columns:
        df.loc[:, "formula"] = df.loc[:, "formula"].apply(from_melts_cstr)

    if ("Temperature" in df.columns) and not kelvin:
        df["Temperature"] -= 273.15

    if ("MgO" in df.columns) and ("FeO" in df.columns):
        # should update this to be if there's both iron and magnesium species
        df.pyrochem.add_MgNo()

    df = zero_to_nan(df)
    df = tuple_reindex(df)
    df = convert_thermo_names(df)
    return df


def import_tables(pth, kelvin=False):
    """
    Import tables from a directory.

    Parameters
    -----------
    kelvin : :class:`bool`
        Whether to keep temperatures in kelvin.
    """
    # system table
    system = read_melts_table(pth / "System_main_tbl.txt", skiprows=3, kelvin=kelvin)
    system["step"] = np.arange(system.index.size)  # generate the step index
    system["mass%"] = system["mass"] / system["mass"].values[0]
    system["volume%"] = system["volume"] / system["volume"].values[0]
    system = system.reindex(
        columns=["step"] + [i for i in system.columns if i != "step"]
    )

    phase = read_phasemain(pth / "Phase_main_tbl.txt", kelvin=kelvin)
    # column management
    non_num = ["step", "structure", "phaseID", "phase", "formula"]
    num = [i for i in phase.columns if i not in non_num]

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
    phase = phase.reindex(columns=["Step"] + [i for i in phase.columns if i != "step"])

    phase[num] = phase[num].apply(pd.to_numeric, errors="coerce")

    phase["mass%"] = phase["mass"] / system.loc[phase.index, "mass"].values[0] * 100
    phase["volume%"] = phase["volume"] / system.loc[phase.index, "volume"].values[0]

    return system, phase
