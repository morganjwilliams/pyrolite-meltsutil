"""
Uncertainties and alphaMELTS Experiments
===========================================

While alphaMELTS is a useful tool for formulating hypotheses around magmatic processes,
analytical uncertainties for compositional parameters are difficult to propagate. Here
I've given an example of taking the composition of average MORB, adding 'noise' to
represent multiple possible realisations under analytical uncertainties, and conducted
replicate alphaMELTS experiments to provide some quantification of the uncertainties in
the results. Note that the 'noise' added here is uncorrelated, and as such may usefully
represent analytical uncertainty. Geological uncertainties are typically strongly
correlated, and the uncertainties associated with e.g. variable mineral assemblages
should be modelled differently.
"""
import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(23)
# sphinx_gallery_thumbnail_number = 2

########################################################################################
# We'll use the major element composition of MORB from Gale et al (2013) for this
# exercise:
#
from pyrolite_meltsutil.util.synthetic import isobaricGaleMORBexample

MORB = isobaricGaleMORBexample(title="Gale2013MORB")
MORB.T

########################################################################################
# As we're going to 'blur' compositions by adding compositional noise to them,
# it'll be handy to have a function to do so. Here's a simple one which
# achieves this and is sufficient for our purpose:
#
from pyrolite.comp.codata import ilr, inverse_ilr


def blur_compositions(df, noise=0.05, scale=100):
    """
    Function to add 'compositional noise' to a set of compositions. In reality, it's
    its best to use measured uncertainties to generate these simulated compositions.
    """
    # transform into compositional space, add noise, return to simplex
    xvals = ilr(df.values)
    xvals += np.random.randn(*xvals.shape) * noise
    return inverse_ilr(xvals) * scale


########################################################################################
# We'll replicate this composition a number of times, and then add gaussian noise
# to each to create a range of plausible compositions:
#
import pyrolite.geochem
from pyrolite.util.text import slugify
from pyrolite.util.pd import accumulate

reps = 10  # increase this to perform more experiments
df = accumulate([MORB] * reps)
df = df.reset_index().drop(columns="index")
df[df.pyrochem.list_oxides] = (
    df.loc[:, df.pyrochem.list_oxides].astype(float).pyrocomp.renormalise()
)
df[df.pyrochem.list_oxides] = blur_compositions(df[df.pyrochem.list_oxides])

df.Title = df.Title + " " + df.index.map(str)  # differentiate titles
df.Title = df.Title.apply(slugify)
########################################################################################
# We can visualise this variation in a ternary space:
#
import pyrolite.plot
import matplotlib.pyplot as plt

ax = df.loc[:, ["CaO", "MgO", "Al2O3"]].pyroplot.scatter(alpha=0.2, c="0.5")
plt.show()
########################################################################################
# Now we can setup an environment for isobaric fractional crystallisation:
#
from pyrolite_meltsutil.env import MELTS_Env

env = MELTS_Env()
env.VERSION = "MELTS"  # crustal processes, < 1GPa/10kbar
env.MODE = "isobaric"
env.DELTAT = -5
env.MINP = 0
env.MAXP = 10000
########################################################################################
# Let's create a directory to run this experiment in - here we use an example folder:
#
from pyrolite_meltsutil.util.general import get_data_example

experiment_dir = get_data_example("montecarlo")
########################################################################################
# Let's also set up logging we can see the progression:
from pyrolite.util.meta import stream_log
import logging

logger = logging.Logger(__name__)
stream_log(logger)
########################################################################################
# Next we setup the alphaMELTS configuration for each of the inputs:
#
from pyrolite_meltsutil.automation import MeltsBatch

batch = MeltsBatch(
    df,
    default_config={
        "Initial Pressure": 5000,
        "Initial Temperature": 1300,
        "Final Temperature": 800,
        "modes": ["isobaric"],
    },
    config_grid={
        # "Initial Pressure": [3000, 7000],
        "Log fO2 Path": [None, "FMQ"],
        # "modifychem": [None, {"H2O": 0.5}],
    },
    env=env,
    fromdir=experiment_dir,
    logger=logger,
)
########################################################################################
# The series of calls to alphaMELTS are now configured, and could be run as follows
# (::code:`overwrite=False` if you don't want to update existing experiment folders).
# Here we've already run the experiment and will load local data for the experiment
# to keep the documentation-building time low.
#

# batch.run(overwrite=False)

########################################################################################
# We can first aggregate and import these results:
#
from pyrolite_meltsutil.tables.load import (
    aggregate_tables,
    import_tables,
    import_batch_config,
)

system, phases = aggregate_tables(experiment_dir)  # let's import the tables
cfg = import_batch_config(experiment_dir)  # and also the configuration
########################################################################################
# And now we can visualse these tables. Let's first look at how the relative phase
# masses change with temperature (i.e. during crystallisation).
#
import matplotlib.pyplot as plt
from pyrolite.util.plot import proxy_line
from pyrolite_meltsutil.vis.style import phaseID_linestyle, phaseID_marker, phase_color

phaselist = ["liquid", "clinopyroxene", "feldspar", "olivine"]

fig, ax = plt.subplots(
    len(phaselist) // 2, 2, sharex=True, sharey=True, figsize=(10, 8)
)
xvar, yvar = "temperature", "mass%"
[a.set_xlabel(xvar) for a in ax[-1, :]]
[a.set_ylabel(yvar) for a in ax[:, 0]]

for p, pax in zip(phaselist, ax.flat):
    pdf = phases.loc[phases.phase == p, :]
    proxies = {}
    for phaseID in pdf.phaseID.unique():
        style = dict(ls=phaseID_linestyle(phaseID), color=phase_color(phaseID))
        for expr in pdf.experiment.unique():
            e_p_df = pdf.loc[((pdf.phaseID == phaseID) & (pdf.experiment == expr)), :]
            pax.plot(e_p_df[xvar], e_p_df[yvar], **style)
            proxies[phaseID] = proxy_line(**style)

    pax.legend(proxies.values(), proxies.keys(), frameon=False, facecolor=None)

########################################################################################
# We can also see how variable the chemistry of these phases might be.
#

fig, ax = plt.subplots(1, figsize=(6, 6))
vars = "FeO", "Al2O3", "MgO"

proxies = {}
for p in phaselist:
    pdf = phases.loc[phases.phase == p, :]
    for phaseID in pdf.phaseID.unique():
        style = dict(
            marker=phaseID_marker(phaseID), c=phase_color(phaseID), markersize=3
        )
        proxies[phaseID] = proxy_line(**style)
        for expr in pdf.experiment.unique():
            e_p_df = pdf.loc[((pdf.phaseID == phaseID) & (pdf.experiment == expr)), :]
            e_p_df.loc[:, vars].pyroplot.scatter(s=3, **style, ax=ax)
proxies = {k: proxies[k] for k in sorted(proxies.keys())}
legend = ax.legend(
    proxies.values(),
    proxies.keys(),
    frameon=False,
    facecolor=None,
    bbox_to_anchor=(1, 1),
    loc="upper left",
)
