"""
Visualising Cumulate Compositions
====================================
"""
########################################################################################
# First we'll import a set of example data tables:
#
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.tables.load import import_tables

# sphinx_gallery_thumbnail_number = 2
hsh = "3149b39eee"  # the hash index of our experiment
batchdir = get_data_example("montecarlo")  # let's use the example batch data for this
system, phases = import_tables(batchdir / hsh)  # let's import the tables
########################################################################################
# The cumulate composition is automatically calculated and added to the phase table:
#
phases.loc[phases.phase == "cumulate", :].head(3).T
########################################################################################
# We can also manually calculate the phase mass proportions for the cumulate pile:
#
from pyrolite_meltsutil.util.tables import integrate_solid_proportions

cumulate_phases = integrate_solid_proportions(phases, frac=False)
cumulate_phases.tail(3).T
########################################################################################
# Ternary diagrams can be useful to visualise how the overal/fractional cumulates
# change during the experiment:
#
import matplotlib.pyplot as plt
import pyrolite.plot
from pyrolite.util.plot.style import mappable_from_values

chemvars = ["MgO", "Al2O3", "FeO"]
cumulate_comp = phases.loc[phases.phase == "cumulate", :]
ax = cumulate_comp.loc[:, chemvars].pyroplot.scatter(
    c=cumulate_comp.temperature, cmap="magma"
)
plt.colorbar(
    mappable_from_values(cumulate_comp.temperature.dropna(), cmap="magma"),
    label="Temperature (C)",
    ax=ax,
    shrink=0.7,
)
plt.show()
########################################################################################
# Similarly, we can plot the phase proportions:
#

phaselist = ["clinopyroxene_0", "clinopyroxene_1", "feldspar_0"]
ax = cumulate_phases.loc[:, phaselist].pyroplot.scatter(
    c=cumulate_phases.temperature, cmap="magma"
)
plt.colorbar(
    mappable_from_values(cumulate_phases.temperature, cmap="magma"),
    label="Temperature (C)",
    ax=ax,
    shrink=0.7,
)
plt.show()
