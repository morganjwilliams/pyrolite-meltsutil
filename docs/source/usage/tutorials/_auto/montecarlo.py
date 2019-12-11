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
# Here we can do a conditonal install - downloading alphamelts if it doesnt exist:
#
from pyrolite_meltsutil.download import install_melts
from pyrolite_meltsutil.util.general import pyrolite_meltsutil_datafolder

if not (pyrolite_meltsutil_datafolder(subfolder="localinstall")).exists():
    stream_log("pyrolite-meltsutil", level="INFO")  # logger for output info
    install_melts(local=True)  # install a copy of melts to pyrolite data folder

########################################################################################
# We'll use the major element composition of MORB from Gale et al (2013) for this
# exercise:
#
from pyrolite_meltsutil.util.synthetic import isobaricGaleMORBexample

MORB = isobaricGaleMORBexample(title="Gale2013MORB")
MORB.T
########################################################################################
# We'll replicate this composition a number of times, and then add gaussian noise
# to each to create a range of plausible compositions:
#
import pyrolite.geochem
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
import pyrolite.plot
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
from pyrolite.util.general import temp_path
from pyrolite_meltsutil.automation import MeltsBatch

# create a directory to run this experiment in
tempdir = temp_path()

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
    logger=logger,
    fromdir=tempdir,
)

batch.configs
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
from pyrolite_meltsutil.vis import xy_by_phase


# TODO
