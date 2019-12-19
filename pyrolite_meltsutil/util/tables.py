import pandas as pd
import numpy as np
import pyrolite.geochem


def phasename(phaseID):
    """
    Take a phase ID and return the name of the phase.

    Parameters
    ------------
    phaseID : :class:`str`
        ID for the particular phase (e.g. 'olivine_0')

    Returns
    --------
    :class:`str`
        Name of the phase.
    """
    if phaseID.find("_") > 0:
        n = phaseID[: phaseID.find("_")]
    else:
        n = phaseID
    return n


def tuple_reindex(df, columns=["pressure", "temperature"]):
    """
    Create an index based on tuples from multiple columns.

    Parameters
    -----------
    df: :class:`pandas.DataFrame`
        Table DataFrame to reindex.
    columns : :class:`list`
        List of columns to incorporate into the tuple index.

    Returns
    -------
    :class:`pandas.DataFrame`
        Reindexed DataFrame.
    """
    df.index = df.loc[:, columns].astype(int).itertuples(index=False)
    return df


def integrate_solid_composition(df, frac=True):
    """
    Integrate solid compositions to return a 'cumulate' like
    composition. Note that in the case of non-fractional crystallisation
    this will correspond to the solid composition.

    Parameters
    -----------
    df : :class:`pandas.DataFrame`
        DataFrame to integrate.
    frac : :class:`bool`
        Whether the experiment is a fractional crystallisation experiment.

    Returns
    -----------
    df : :class:`pandas.DataFrame`
        DataFrame containing an integrated solid composition.
    """
    slds = df.loc[df.phase == "solid", :]
    if frac:
        chem = slds.loc[
            :, [i for i in slds.pyrochem.list_compositional if i not in ["S", "H", "V"]]
        ]
        chem = chem.apply(pd.to_numeric, errors="coerce")
        increments = slds["mass"].values[:, np.newaxis] * chem.values
        cumulate = pd.DataFrame(columns=slds.columns, index=slds.index)
        cumulate["mass"] = np.cumsum(slds.mass.values)
        cumulate[chem.columns] = np.cumsum(increments, axis=1)
        cumulate[["pressure", "temperature", "step"]] = slds.loc[
            :, ["pressure", "temperature", "step"]
        ]
    else:
        cumulate = slds.copy()
    cumulate.pyrochem.add_MgNo()
    return cumulate

def integrate_solid_proportions(df, frac=True):
    """
    Integrate solid proportions to return a 'cumulates' split by integrated phase
    masses. Note that in the case of non-fractional crystallisation
    this will correspond to the overall solid phase abundances.

    Parameters
    -----------
    df : :class:`pandas.DataFrame`
        DataFrame to integrate.
    frac : :class:`bool`
        Whether the experiment is a fractional crystallisation experiment.

    Returns
    -----------
    df : :class:`pandas.DataFrame`
        DataFrame containing integrated solid phase proportions.
    """
    # another dataframe for integrated minerals
    phases = sorted([pID for pID in df.phaseID.unique() if not pd.isnull(pID)])
    mindf = pd.DataFrame(
        columns=phases, index=df.loc[df.phase == "solid", :].index
    )  # empty dataframe
    for p in phases:  # integrate cumulate mass per phase
        phasemass = df.loc[df.phase == p, "mass"]

    mindf = mindf.apply(np.cumsum, axis=1)  # check the axis

    mindf = mindf.div(
        mindf.apply(np.nansum, axis=0)
    )  # fractioal mass of total cumulate
    return mindf
