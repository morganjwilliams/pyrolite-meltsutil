"""
Visualisation: Plot Templates
=====================================

pyrolite-meltsutil includes a few plot templates to quickly visualise some melts
experiment results.
"""
########################################################################################
# First let's get a folder with some data in it. Here we use one of the isobaric
# crystallisation experiments from the montecarlo tutorial, and import the tables:
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.tables import import_tables

exp_dir = get_data_example("montecarlo/0ef62e8e55")
system, phases = import_tables(exp_dir)
########################################################################################
# We can quickly visualise the phase volume relationships versus temperature:
#
import matplotlib.pyplot as plt
from pyrolite_meltsutil.vis.templates import plot_phasevolumes

ax = plot_phasevolumes(phases)
plt.show()
########################################################################################
# Similarly, for the phase mass relationships versus temperature:
#
from pyrolite_meltsutil.vis.templates import plot_phasemasses

ax = plot_phasemasses(phases, marker=None)
ax.set_yscale("log")
plt.show()
