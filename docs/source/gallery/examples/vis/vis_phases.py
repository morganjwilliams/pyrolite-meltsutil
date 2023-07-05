"""
Visualising Melts Results by Phases
====================================
"""
########################################################################################
# First we'll import a set of example data tables:
#
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.tables.load import import_tables, import_batch_config

# sphinx_gallery_thumbnail_number = 2
hsh = "363f3d0a0b"  # the hash index of our experiment
batchdir = get_data_example("batch")  # let's use the example batch data for this
system, phases = import_tables(batchdir / hsh)  # let's import the tables
name, cfg, env = import_batch_config(batchdir)[hsh]  # and also the configuration
########################################################################################
# Now we can dig into some tables and plot some data for different phases.
#
import pyrolite.plot
import matplotlib.pyplot as plt
from pyrolite.util.plot.legend import proxy_line
from pyrolite_meltsutil.vis.style import phase_color, phaseID_linestyle, phaseID_marker

phasenames = ["olivine", "clinopyroxene", "feldspar", "liquid"]

fig, ax = plt.subplots(1)

proxies = {}  # proxies for creating a legend
for ix, phs in enumerate(phasenames):
    phase_data = phases.loc[phases.phase == phs, :]
    for phaseID, phaseID_data in phase_data.groupby("phaseID"):
        style = dict(c=phase_color(phaseID), marker=phaseID_marker(phaseID))
        ax = phaseID_data.loc[:, ["CaO", "MgO", "Al2O3"]].pyroplot.scatter(
            ax=ax, **style
        )

        proxies[phaseID] = proxy_line(
            ls="-", color=phase_color(phaseID), marker=phaseID_marker(phaseID)
        )
########################################################################################
# Finally we can generate the legend using our legend proxies:
#
ax.legend(
    list(proxies.values()),
    list(proxies.keys()),
    frameon=False,
    facecolor=None,
    bbox_to_anchor=(1, 1),
    loc="upper left",
)
plt.show()
