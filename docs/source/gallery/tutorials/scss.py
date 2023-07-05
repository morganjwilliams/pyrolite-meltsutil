"""
Visualising SCSS
=================

pyrolite includes a few functions for working with magmatic liquid compositions,
one of which being the Sulfur Content at Sulfur Saturation
(:func:`pyrolite.geochem.magma.SCCS`) function. This is an empirical relationship
derived by Li and Ripley (2009) [#ref_1]_ which enables a better understanding
of relative saturation sulfur saturation state (for both sulfide and sulfate)
and the prediction of sulfur saturation in evolving melts.

Here we use this function to predict sulfur saturation in a fractionally
crystallizing MORB melt with a range of sulfur contents. First we'll import a set of
example data tables:
"""
from pyrolite_meltsutil.tables.load import import_batch_config, import_tables
from pyrolite_meltsutil.util.general import get_data_example

# sphinx_gallery_thumbnail_number = 3
hsh = "363f3d0a0b"  # the hash index of our experiment
batchdir = get_data_example("batch")  # let's use the example batch data for this
system, phases = import_tables(batchdir / hsh, kelvin=False)  # let's import the tables
name, cfg, env = import_batch_config(batchdir)[hsh]  # and also the configuration

########################################################################################
# From this we extract only the liquid composition:
#
liquid = phases.loc[phases.phase == "liquid", :]
########################################################################################
# Now we can calcuate the sulfur saturation at sulfide saturation for this magma.
# This table also includes the relevant temperature and pressure data, noting
# that the temperature here is in degrees Celsius (:code:`kelvin = False`) and the
# pressure is in bars (wheras this function requires kbar, hence the division by 1000):
#
from pyrolite.geochem.magma import SCSS

sulfate, sulfide = SCSS(
    liquid, T=liquid.temperature, P=liquid.pressure / 1000, grid=None, kelvin=False
)
########################################################################################
# To link this back to our chemical data, let's add this measure to the dataframe:
#
liquid.loc[:, "SCSS"] = sulfide
########################################################################################
# Now we can plot this against some of the experiment parameters. Here we plot
# SCSS against the remaining (non-crystallized) mass of the system and color the
# results by temperature:
#
import matplotlib.pyplot as plt
import pyrolite.plot

from pyrolite_meltsutil.vis.scss import plot_sulfur_saturation_point

xvar, colorvar = "mass%", "temperature"

# show the SCSS for the liqud
ax = liquid.loc[:, [xvar, "SCSS"]].pyroplot.scatter(
    c=liquid[colorvar], fontsize=12, figsize=(12, 6)
)
ax.set_ylim(0, 0.35)
########################################################################################
# To this we can add a colorbar for the temperature color mapping:
#
from pyrolite.util.plot.style import mappable_from_values
from pyrolite.util.plot.axes import add_colorbar

plt.colorbar(mappable_from_values(liquid[colorvar]), ax=ax, pad=0.1, label=colorvar)
plt.show()
########################################################################################
# We can clean up these axes a bit by relimiting and rescaling:
#
import numpy as np

ax.set_xlim((np.nanmax(liquid["mass%"]), 0))
########################################################################################
# To this we can also add the saturation points (where sulfur content crosses SCSS)
# and plot the mass of free sulfide liquid expected for a range of initial sulfur
# contents. Note here that the sulfur content in the liquid is plotted with dashed
# lines (linked to left axis), and the free sulfide liquid in solid lines (right axis).
# Once saturation is reached, the sulfur content in the melt will follow the SCSS curve
# unless the system is perturbed or becomes undersaturated again.
#
plot_sulfur_saturation_point(liquid, start=[500, 1000, 1500], xvar=xvar, ax=ax)
plt.show()
########################################################################################
# References
# -----------
# .. [#ref_1] Li, C., and Ripley, E.M. (2009).
#     Sulfur Contents at Sulfide-Liquid or Anhydrite Saturation in Silicate Melts:
#     Empirical Equations and Example Applications. Economic Geology 104, 405–412.
#     doi: `gsecongeo.104.3.405 <https://doi.org/10.2113/gsecongeo.104.3.405>`__
