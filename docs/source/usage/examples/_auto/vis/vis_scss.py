"""
Visualising SCSS
=================
"""
########################################################################################
# First we'll import a set of example data tables:
#
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.tables.load import import_tables, import_batch_config

# sphinx_gallery_thumbnail_number = 3
hsh = "363f3d0a0b"  # the hash index of our experiment
batchdir = get_data_example("batch")  # let's use the example batch data for this
system, phases = import_tables(batchdir / hsh, kelvin=False)  # let's import the tables
name, cfg, env = import_batch_config(batchdir)[hsh]  # and also the configuration

########################################################################################
# From this we just take the liquid composition:
#
liquid = phases.loc[phases.phase == "liquid", :]
########################################################################################
# Now we can calcuate the sulfur saturation at sulfide saturation for this magma:
#
from pyrolite.geochem.magma import SCSS

sulfate, sulfide = SCSS(
    liquid, T=liquid.temperature, P=liquid.pressure / 1000, grid=None, kelvin=False
)
########################################################################################
# To link this back to our data, let's add it to the dataframe:
#
liquid["SCSS"] = sulfide
########################################################################################
# Now we can plot this against some of the experiment parameters:
#
import matplotlib.pyplot as plt
import pyrolite.plot
from pyrolite_meltsutil.vis.scss import plot_sulfur_saturation_point

xvar, colorvar = "mass%", "temperature"

# show the SCSS for the liqud
ax = liquid.loc[:, [xvar, "SCSS"]].pyroplot.scatter(
    c=liquid[colorvar], fontsize=12, figsize=(12, 6)
)
########################################################################################
# We can clean up these axes a bit by relimiting and rescaling:
#
import numpy as np
xlims = {
    "temperature": (
        1400,  # np.nanmax(liquid["Temperature"]),
        np.nanmin(liquid["temperature"]),
    ),
    "mass%": (np.nanmax(liquid["mass%"]), 0),
}
ax.set_xlim(xlims[xvar])
########################################################################################
# To this we can add the saturation points:
#
plot_sulfur_saturation_point(liquid, start=[500, 1000, 1500], xvar=xvar, ax=ax)

plt.show()
########################################################################################
# Finally, let's add a colorbar:
#
from pyrolite.util.plot import mappable_from_values, add_colorbar

plt.colorbar(mappable_from_values(liquid[colorvar]), ax=ax, pad=0.1, label=colorvar)
ax.figure
