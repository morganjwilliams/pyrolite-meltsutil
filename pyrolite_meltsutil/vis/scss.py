import numpy as np
import pyrolite_meltsutil as melts
from pyrolite.util.plot import get_twins, share_axes
from pyrolite.geochem.magma import SCSS


def plot_sulfur_saturation_point(liquidcomp, ax=None, start=1000, xvar="mass%"):
    """
    Plot a perfectly incompatbile trend for sulfur in a melt, and
    indicate the point at which it crosses a previously-calculated
    sulfur saturation point.
    """
    s_wtpct = start / liquidcomp["mass%"] / 10000.0
    satpoint = np.argmax(s_wtpct > liquidcomp.SCSS)  # will return where first true
    satabund = s_wtpct[satpoint]

    ax2 = get_twins(ax)
    if not ax2:
        ax2 = ax.twinx()
    else:
        ax2 = ax2[0]
    # plot the SCSS
    ax.plot(liquidcomp[xvar], liquidcomp["SCSS"], color="k", zorder=-1)
    # plot the sulfur abundance in the melt
    # this will follow SCSS after sulfide saturation
    s_melt = np.zeros_like(s_wtpct)
    s_melt[s_wtpct >= liquidcomp.SCSS] = liquidcomp.SCSS[s_wtpct >= liquidcomp.SCSS]
    s_melt[s_wtpct < liquidcomp.SCSS] = s_wtpct[s_wtpct < liquidcomp.SCSS]
    ax.plot(s_melt, s_melt, ls="--", label="Sulfur Content ({} ppm)".format(start))
    # plot the excess sulfur abundnace
    s_free = np.zeros_like(s_wtpct)
    s_free[s_wtpct >= liquidcomp.SCSS] = (
        s_wtpct[s_wtpct >= liquidcomp.SCSS]
        - liquidcomp.SCSS[s_wtpct >= liquidcomp.SCSS]
    )
    ax2.plot(liquidcomp[xvar], s_free, color=lines[0].get_color())
    # annotate the (first) saturation point
    ax.annotate(
        "{:.4g} @ {} ppm".format(liquidcomp[xvar][satpoint], start),
        xytext=(liquidcomp[xvar][satpoint], 1.5 * s_wtpct[satpoint]),
        xy=(liquidcomp[xvar][satpoint], s_wtpct[satpoint]),
        rotation=70,
        fontsize=10,
        ha="center",
        va="bottom",
        arrowprops=dict(shrink=0.2, width=1, headwidth=1),
    )
    share_axes([ax, ax2], which="xy")
    return ax
