"""
This submodule is a home for templates for quickly
regenerating common visualistions from melts tables.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyrolite.util.meta import subkwargs
from pyrolite.util.plot import proxy_line
from .style import phase_color, phaseID_linestyle, phaseID_marker


def plot_xy_phase_groupby(ax, df, xvar, yvar, legend=True, markersize=3, **kwargs):
    """
    Utility function for plotting phases on an axis.

    Returns
    ---------
    :class:`matplotlib.axes.Axes`
        Axes on which the table results are plotted.
    """

    if "experiment" in df.columns:
        assert len(df.experiment.unique()) == 1
    if ax is None:
        fig, ax = plt.subplots(1)
    phaseIDlist = sorted([i for i in df.phaseID.unique() if not pd.isnull(i)])
    ax.set_xlabel(xvar)
    ax.set_ylabel(yvar)
    proxies = {}
    for phaseID in phaseIDlist:
        phasedf = df.loc[df.phaseID == phaseID, :]
        style = dict(
            ls=phaseID_linestyle(phaseID),
            color=phase_color(phaseID),
            markerfacecolor=phase_color(phaseID),
            marker=phaseID_marker(phaseID),
            markersize=markersize,
        )
        style = {**{k: v for k, v in style.items() if v is not None}, **kwargs}
        proxies[phaseID] = proxy_line(**style)
        ax.plot(phasedf[xvar], phasedf[yvar], **style)

    if legend:
        ax.legend(
            proxies.values(),
            proxies.keys(),
            frameon=False,
            facecolor=None,
            loc="upper left",
            bbox_to_anchor=(1, 1),
        )
    return ax, proxies


def plot_phasevolumes(phasetable, xvar="temperature", legend=True, ax=None, **kwargs):
    """
    """
    ax, proxies = plot_xy_phase_groupby(
        ax, phasetable, xvar, "volume%", legend=legend, **kwargs
    )
    return ax


def plot_phasemasses(phasetable, xvar="temperature", legend=True, ax=None, **kwargs):
    """
    """
    ax, proxies = plot_xy_phase_groupby(
        ax, phasetable, xvar, "mass%", legend=legend, **kwargs
    )
    return ax
