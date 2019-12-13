import numpy as np
import matplotlib.pyplot as plt
import pyrolite_meltsutil as melts
from pyrolite.util.plot import get_twins, share_axes
from pyrolite.geochem.magma import SCSS


def plot_sulfur_saturation_point(
    liquid, ax=None, start=1000, xvar="mass%", mode="sulfide"
):
    """
    Plot a perfectly incompatbile trend for sulfur in a melt, and
    indicate the point at which it crosses a previously-calculated
    sulfur saturation point.

    Parameters
    -------------
    liquid : :class:`pandas.DataFrame`
        Liquid composition table.
    ax : :class:`matplotlib.axes.Axes`
        Optionally specify an axis to plot on.
    start : :class:`float` | :class:`list`
        Starting abundance of sulfur in ppm.
    xvar : :class:`str`
        X-variable for the plot.
    mode : :class:`str`
        Where SCSS is missing, add the value from either the `sulfide` saturation or
        `sulfate` saturation model.

    Returns
    -------
    ax : :class:`matplotlib.axes.Axes`
        Axes with saturation points indicated.
    """
    if ax is None:
        fig, ax = plt.subplots(1)
    ax2 = get_twins(ax)
    if not ax2:
        ax2 = ax.twinx()
    else:
        ax2 = ax2[0]
    ax2.set_ylabel("Free S (Mass %)")

    if not "SCSS" in liquid.columns: # add SCSS if its missing
        liquid["SCSS"] = SCSS(
            liquid,
            T=liquid.temperature,
            P=liquid.pressure / 1000,
            grid=None,
            kelvin=False,
        )[mode == "sulfide"]
    # plot the SCSS
    ax.plot(liquid[xvar], liquid["SCSS"], color="k", zorder=-1)
    # plot the sulfur abundance in the melt
    # this will follow SCSS after sulfide saturation
    if isinstance(start, (int, float)):
        start = np.array([start])
    elif isinstance(start, (list, tuple, np.ndarray)):
        start = np.array(start)

    saturation_info = {}
    for xS in start:
        s_wtpct = xS / 10000.0
        s_wtpct /= liquid["mass%"] / liquid["mass%"].values[0]
        satpoint = np.argmax(
            s_wtpct.values > liquid["SCSS"].values
        )  # will return where first true
        satabund = s_wtpct[satpoint]

        s_melt = np.ones_like(s_wtpct) * np.nan
        s_melt[s_wtpct < liquid.SCSS] = s_wtpct[s_wtpct < liquid.SCSS]
        s_melt[s_wtpct >= liquid.SCSS] = liquid.SCSS[s_wtpct >= liquid.SCSS]
        lines = ax.plot(
            liquid[xvar], s_melt, ls="--", label="Sulfur Content ({} ppm)".format(start)
        )
        # plot the excess sulfur abundnace
        s_free = np.ones_like(s_wtpct) * np.nan
        s_free[s_wtpct >= liquid.SCSS] = (
            s_wtpct[s_wtpct >= liquid.SCSS] - liquid.SCSS[s_wtpct >= liquid.SCSS]
        )
        ax2.plot(liquid[xvar], s_free, color=lines[0].get_color())
        saturation_info[xS] = dict(x=liquid[xvar][satpoint], y=s_wtpct[satpoint])

    x0, y0 = liquid[xvar].values[0], liquid["SCSS"].values[0]
    starts_saturated = [k for (k, d) in saturation_info.items() if d["x"] == x0]
    if starts_saturated:
        ax.annotate(
            "Start {} ppm".format(
                "({})".format(",".join([str(s) for s in starts_saturated]))
            ),
            xytext=(
                x0 + (0.05 * (np.nanmax(liquid[xvar]) - np.nanmin(liquid[xvar]))),
                0.5 * y0,
            ),
            xy=(x0, y0),
            rotation=90,
            fontsize=10,
            ha="right",
            va="center",
            arrowprops=dict(shrink=0.05, width=1, headwidth=1),
        )
    for k, d in saturation_info.items():  # annotate the (first) saturation point
        if k not in starts_saturated:
            ax.annotate(
                "{:.4g} @ {} ppm".format(d["x"], k),
                xytext=(d["x"], 1.2 * d["y"]),
                xy=(d["x"], d["y"]),
                rotation=90,
                fontsize=10,
                ha="center",
                va="bottom",
                arrowprops=dict(shrink=0.05, width=1, headwidth=1),
            )
    share_axes([ax, ax2], which="xy")
    return ax
