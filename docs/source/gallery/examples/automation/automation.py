"""
Automating alphaMELTS runs
=============================

pyrolite includes some utilities to help you run alphaMELTS with a little less hassle,
especially for established workflows or repetitive calculations. Here we run multiple
experiments at different conditions for a single MORB composition. Once we have the
data in a :class:`~pandas.DataFrame`, we configure the default alphaMELTS environment
before running the batch of experiments.
"""
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pyrolite_meltsutil.automation import MeltsBatch

########################################################################################
from pyrolite_meltsutil.util.synthetic import isobaricGaleMORBexample

MORB = isobaricGaleMORBexample(title="Gale2013MORB")
MORB.T
########################################################################################
from pyrolite_meltsutil.env import MELTS_Env

env = MELTS_Env()
env.VERSION = "MELTS"
env.MODE = "isobaric"
env.MINP = 5000
env.MAXP = 10000
env.MINT = 500
env.MAXT = 1500
env.DELTAT = -10
env.DELTAP = 0
########################################################################################
# Let's create a directory to run this experiment in - here we use an example folder:
#
from pyrolite_meltsutil.util.general import get_data_example

experiment_dir = get_data_example("batch")
########################################################################################
# Now we can set up the experiment. We're going to run a
# :class:`~pyrolite_meltsutil.automation.MeltsBatch`, and we'll provide:
#   * The dataframe of compositions
#   * The default configuration
#   * The configuration grid with lists of parameter values -
#     which overrides the default.
#   * The :class:`~pyrolite_meltsutil.env.MELTS_Env` or environment file to be used
#   * The directory to be used (defaults to the current working directory)
#   * Optionally, specify a logger for output
#
batch = MeltsBatch(
    MORB,
    default_config={  # things that won't change between experiments
        "Initial Temperature": 1400,
        "Final Temperature": 800,
        "modes": ["isobaric", "fractionate solids"],
    },
    config_grid={  # things that change between experiments
        "Initial Pressure": [5000, 7000],
        "Log fO2 Path": [None, "FMQ"],
        "modifychem": [None, {"H2O": 0.5}],
    },
    env=env,
    fromdir=experiment_dir,
)
########################################################################################
# Now the experiment is configured, we can run it:
#

batch.run(overwrite=False)  # overwrite=True if you want to update existing exp folders
########################################################################################
# .. seealso::
#
#   Examples:
#     `alphaMELTS Environment Configuration <environment.html>`__,
#     `pyrolite-hosted alphaMELTS Installation <install.html>`__,
#     `Handling Outputs from Melts: Tables <tables_load.html>`__,
#     `Compositional Uncertainty Propagation for alphaMELTS Experiments <../tutorials/montecarlo.html>`__
#
