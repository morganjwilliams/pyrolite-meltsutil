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
    idx = (
        df.loc[:, ["pressure", "temperature", "step"]]
        .dropna()
        .drop_duplicates()
        .sort_values("step")
    )
    if frac:
        cumulate = pd.DataFrame(columns=slds.columns, index=idx.index)
        cumulate["mass"] = np.nancumsum(slds.loc[idx.index, "mass"].values)

        chem = slds.loc[
            idx.index,
            [i for i in slds.pyrochem.list_compositional if i not in ["S", "H", "V"]],
        ]
        chem = chem.apply(pd.to_numeric, errors="coerce")
        increments = slds.loc[idx.index, "mass"].values[:, np.newaxis] * chem.values

        cumulate[chem.columns] = np.nancumsum(increments, axis=1)
        cumulate[["pressure", "temperature", "step"]] = slds.loc[
            :, ["pressure", "temperature", "step"]
        ]
    else:
        cumulate = slds.reindex(index=idx.index)
    cumulate.pyrochem.add_MgNo()
    return cumulate


def integrate_solid_proportions(df, frac=True):
    """
    Integrate solid proportions to return a 'cumulate' split by integrated phase
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
    phaseIDs = sorted(
        [
            pID
            for pID in df.phaseID.unique()
            if (not pd.isnull(pID)) and ("liquid" not in pID)
        ]
    )
    idx = (
        df.loc[:, ["pressure", "temperature", "step"]]
        .dropna()
        .drop_duplicates()
        .sort_values("step")
    )
    # empty dataframe
    mindf = pd.DataFrame(
        columns=["pressure", "temperature", "step"] + phaseIDs, index=idx.index
    )
    for p in phaseIDs:  # integrate cumulate mass per phase
        mindf.loc[df.loc[df.phaseID == p, "mass"].index.values, p] = df.loc[
            df.phaseID == p, "mass"
        ].values
    mindf = mindf.loc[idx.index, :]  # sort index
    if frac:
        mindf = mindf.apply(np.nancumsum, axis=0)  # accumulate minerals
    # fractioal mass of total cumulate
    mindf = mindf.div(mindf.sum(axis=1).replace(0, np.nan), axis=0) * 100.0
    PTS = idx
    mindf.loc[idx.index, ["pressure", "temperature", "step"]] = PTS

    mindf = mindf.fillna(0)
    return mindf
