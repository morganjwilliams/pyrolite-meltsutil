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


def tuple_reindex(df, columns=["Pressure", "Temperature"]):
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


def integrate_solids(df, frac=True):
    """
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
        cumulate[["Pressure", "Temperature", "step"]] = slds.loc[
            :, ["Pressure", "Temperature", "step"]
        ]
    cumulate.pyrochem.add_MgNo()
    return cumulate
