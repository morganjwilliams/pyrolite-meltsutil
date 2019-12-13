"""
Utilities for reading and writing .melts files.
"""
import io
import os
import itertools
import numpy as np
import pandas as pd
from pathlib import Path
from pyrolite.util.pd import to_frame, to_ser
from pyrolite.geochem.ind import common_elements, common_oxides
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def dict_to_meltsfile(
    d, linesep=os.linesep, writetraces=True, modes=[], exclude=[], **kwargs
):
    """
    Converts a dictionary to a MELTSfile text representation. It requires 'title'
    and 'initial composition' lines, major elements to be represented as oxides
    in Wt% and trace elements in µg/g.

    Parameters
    ----------
    d : :class:`dict`
        Dictionary to convert to a melts file.
    linesep : :class:`str`
        Line separation character.
    writetraces : :class:`bool`
        Whether to include traces in the output file.
    modes : :class:`list`
        List of modes to use (e.g. 'isobaric', 'fractionate solids').
    exclude : :class:`list`
        List of chemical components to exclude from the meltsfile.

    Returns
    -------
    :class:`str`
        String representation of the meltsfile, which can be immediately written to a
        file object.

    Notes
    -------

        * Some of the parameters are one-to-many, including modes, phase fractionation,
            supression and coexist-limits.

    Todo
    -----
        * Parameter validation.
    """
    # we'll incrementally collect the lines for the melts file from the data dictionary
    lines = []
    # first we add the title
    assert ("Title" in d) or ("title" in d)
    if "Title" in d:
        lines.append("Title: {}".format(d["Title"]))
    else:
        lines.append("Title: {}".format(d["title"]))

    # then we'll collect the composition Parameters
    majors = [
        (k, v) for (k, v) in d.items() if k in common_oxides() and not k in exclude
    ]
    traces = [
        (k, v) for (k, v) in d.items() if k in common_elements() and not k in exclude
    ]
    for k, v in majors:
        if not pd.isnull(v):  # no NaN data in MELTS files
            lines.append("Initial Composition: {} {}".format(k, v))

    if writetraces:
        for k, v in traces:
            if not pd.isnull(v):  # no NaN data in MELTS files
                lines.append("Initial Trace: {} {}".format(k, v))

    # follwed by the pressure and temperature parameters
    PTpars = [
        (" ".join([pre, param]), d.get(" ".join([pre, param]), None))
        for pre, param in itertools.product(
            ["Initial", "Final", "Increment"], ["Temperature", "Pressure"]
        )
    ]

    for (k, v) in PTpars:
        if not pd.isnull(v):  # no NaN data in MELTS files
            lines.append("{}: {}".format(k, v))

    for mfilepar in [
        "dp/dt",
        "Log fO2 Path",
        "Log fO2 Delta",
        "Suppress",
        "Limit coexisting",
        "Fractionate",
    ]:
        par = [(k, v) for (k, v) in d.items() if k.lower() == mfilepar.lower()]
        if par:
            par, v = par[0]
            if isinstance(v, (list, set, tuple)):
                for iv in v:
                    if not pd.isnull(iv):  # no NaN data in MELTS files
                        lines.append(
                            "{}: {}".format(mfilepar, iv)
                        )  # suppress, fractionate
            else:
                if not pd.isnull(v):
                    lines.append("{}: {}".format(mfilepar, v))

    for m in modes:
        lines.append("Mode: {}".format(m))

    # valid_modes = ["Fractionate Solids", "Fractionate"]
    return linesep.join(lines)


def ser_to_meltsfile(
    ser, linesep=os.linesep, writetraces=True, modes=[], exclude=[], **kwargs
):
    """
    Converts a series to a MELTSfile text representation. It requires 'title'
    and 'initial composition' lines, major elements to be represented as oxides
    in Wt% and trace elements in µg/g.

    Parameters
    ----------
    ser : :class:`pandas.Series`
        Series to convert to a melts file.
    linesep : :class:`str`
        Line separation character.
    writetraces : :class:`bool`
        Whether to include traces in the output file.
    modes : :class:`list`
        List of modes to use (e.g. 'isobaric', 'fractionate solids').
    exclude : :class:`list`
        List of chemical components to exclude from the meltsfile.

    Returns
    -------
    :class:`str`
        String representation of the meltsfile, which can be immediately written to a
        file object.

    Todo
    -----
        * Parameter validation.
    """
    lines = []
    ser = to_ser(ser)
    return dict_to_meltsfile(
        ser.to_dict(),
        linesep=linesep,
        writetraces=writetraces,
        modes=modes,
        exclude=exclude,
        **kwargs
    )


def df_to_meltsfiles(df, linesep=os.linesep, **kwargs):
    """
    Creates a number of melts files from a dataframe.

    Parameters
    -----------
    df : :class:`pandas.DataFrame`
        Dataframe from which to take the rows and create melts files.
    linesep : :class:`str`
        Line separation character.

    Returns
    -------
    :class:`list`
        List of strings which can be written to file objects.
    """

    # Type checking such that series will be passed directly to MELTSfiles
    if isinstance(df, pd.DataFrame):
        return [
            ser_to_meltsfile(df.iloc[ix, :], linesep=os.linesep, **kwargs)
            for ix in range(df.index.size)
        ]
    elif isinstance(df, pd.Series):
        return [ser_to_meltsfile(df, linesep=os.linesep, **kwargs)]


def from_meltsfile(filename):
    """
    Read from a meltsfile into a :class:`pandas.DataFrame`.

    Parameters
    -----------
    filename : :class:`str` | :class:`pathlib.Path` | :class:`io.BytesIO`
        Filename, filepath or bytes object to read from.

    Returns
    --------
    :class:`pandas.DataFrame`
        Dataframe containing meltsfile parameters.
    """
    if isinstance(filename, io.BytesIO):
        file = filename.getvalue().decode()
    elif isinstance(filename, io.StringIO):
        file = filename.getvalue()
    else:
        try:  # filepath
            with open(filename) as fh:
                file = fh.read()
        except FileNotFoundError:  # string specification of meltsfile
            file = filename

    lines = [line.split(": ") for line in file.splitlines() if line.strip()]
    fmtlines = []
    for ix, args in enumerate(lines):
        if args[0].strip().lower() in ["initial composition", "initial trace"]:
            fmtlines.append(args[1].strip().split())
        else:
            fmtlines.append([i.strip() for i in args])
    df = (
        pd.DataFrame.from_records(fmtlines)
        .set_index(0, drop=True)
        .apply(pd.to_numeric, errors="ignore")[1]
    )
    return df
