"""
Visualisation utilities for working with alphaMELTS table outputs.

Todo
-------

    * Pull out mineral compostional trends
"""
from pyrolite.util.plot import proxy_line
from ..tables.load import import_tables
from .style import phase_color, phaseID_linestyle


def xy_by_phase(df, xvar="temperature", yvar="volume", legend=False):
    """
    Plot selected variables from a table grouped by phases.

    Returns
    ---------
    :class:`matplotlib.axes.Axes`
        Axes on which the table results are plotted.
    """
    ids = sorted(df.phaseID.unique())  # alpha sorting
    p = {ID: dict(color=phase_color(ID), ls=phase_linestyle(ID)) for ID in ids}
    proxies = {ID: proxy_line(**cfg) for ID, cfg in p.items()}  # legend proxies
    if legend:
        ax.legend(
            list(proxies.values()), list(proxies.keys()), frameon=False, facecolor=None
        )
    return ax