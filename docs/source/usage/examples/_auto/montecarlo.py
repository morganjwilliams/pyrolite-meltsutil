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
import pyrolite.geochem
import pyrolite.plot
from pyrolite.comp.codata import ilr, inverse_ilr
from pyrolite.util.meta import stream_log
import logging
# sphinx_gallery_thumbnail_number = 2
logger = logging.Logger(__name__)
stream_log(logger)  # print the logging output


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
# We'll use the major element composition of MORB from Gale et al (2013) for this
# exercise:
#
from pyrolite.geochem.norm import get_reference_composition

Gale_MORB = get_reference_composition("MORB_Gale2013")
MORB = Gale_MORB.comp.pyrochem.oxides.reset_index(drop=True)
########################################################################################
MORB["Title"] = Gale_MORB.name
MORB["Initial Temperature"] = 1300
MORB["Final Temperature"] = 800
MORB["Initial Pressure"] = 5000
MORB["Final Pressure"] = 5000
MORB["Log fO2 Path"] = "FMQ"
MORB["Increment Temperature"] = -5
MORB["Increment Pressure"] = 0
########################################################################################
# We'll replicate this composition a number of times, and then add gaussian noise
# to each to create a range of plausible compositions:
#
from pyrolite.util.text import slugify
from pyrolite.util.pd import accumulate

reps = 3  # increase this to perform more experiments
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
ax = df.loc[:, ["CaO", "MgO", "Al2O3"]].pyroplot.ternary(alpha=0.2, c="0.5")
ax.figure
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
# Next we setup the alphaMELTS configuration for each of the inputs:
#
from pyrolite_meltsutil.automation import MeltsBatch

# create a directory to run this experiment in
tempdir = Path("./") / "montecarlo"

batch = MeltsBatch(
    df,
    default_config={
        "Initial Pressure": 5000,
        "Initial Temperature": 1300,
        "Final Temperature": 800,
        "modes": ["isobaric"],
    },
    grid={
        # "Initial Pressure": [3000, 7000],
        "Log fO2 Path": [None, "FMQ"],
        # "modifychem": [None, {"H2O": 0.5}],
    },
    env=env,
    logger=logger,
    fromdir=tempdir,
)

batch.grid  # [{}, {'Log fO2 Path': 'FMQ'}]
########################################################################################
# The series of calls to alphaMELTS are now configured, and can be run as follows:
#
batch.run(
    overwrite=False
)  # overwrite=False if you don't want to update existing exp folders

########################################################################################
# We can aggregate and import these results for simple visualisations:
#
from pathlib import Path
from pyrolite_meltsutil.tables import get_experiments_summary
from pyrolite_meltsutil.plottemplates import table_by_phase

tempdir = Path("./") / "montecarlo"

summary = get_experiments_summary(tempdir / "isobar5kbar1300-800C", kelvin=False)
fig = table_by_phase(summary, table="phasemass", plotswide=2, figsize=(10, 8))
