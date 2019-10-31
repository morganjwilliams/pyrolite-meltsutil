"""
Automating alphaMELTS runs
=============================

pyrolite includes some utilities to help you run alphaMELTS with a little less hassle,
especially for established workflows or repetitive calculations. Here we run multiple
experiments at different conditions for a single MORB composition. Once we have the
data in a :class:`~pandas.DataFrame`, we configure the default alphaMELTS environment
before running the batch of experiments.
"""
import os, sys
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import pyrolite.plot
from pyrolite.geochem.norm import get_reference_composition
from pyrolite_meltsutil.env import MELTS_Env
from pyrolite_meltsutil.automation import MeltsBatch

from pyrolite.util.meta import stream_log
import logging

logger = logging.Logger(__name__)
stream_log(logger)  # print the logging output
########################################################################################
Gale_MORB = get_reference_composition("MORB_Gale2013")
majors = ["SiO2", "Al2O3", "FeO", "MnO", "MgO", "CaO", "Na2O", "TiO2", "K2O", "P2O5"]
MORB = Gale_MORB.comp[majors].reset_index(drop=True)
MORB["Title"] = [
    "{}_{}".format(Gale_MORB.name, ix) for ix in MORB.index.values.astype(str)
]
MORB["Initial Temperature"] = 1300
MORB["Final Temperature"] = 800
MORB["Initial Pressure"] = 5000
MORB["Final Pressure"] = 5000
MORB["Log fO2 Path"] = "FMQ"
MORB["Increment Temperature"] = -5
MORB["Increment Pressure"] = 0
########################################################################################
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
batch = MeltsBatch(
    MORB,
    default_config={
        "Initial Pressure": 7000,
        "Initial Temperature": 1400,
        "Final Temperature": 800,
        "modes": ["isobaric", "fractionate solids"],
    },
    grid={
        "Initial Pressure": [5000],
        "Log fO2 Path": [None, "FMQ"],
        "modifychem": [None, {"H2O": 0.5}],
    },
    env=env,
    logger=logger,
)

batch.run(
    overwrite=True
)  # overwrite=False if you don't want to update existing exp folders
########################################################################################
# .. seealso::
#
#   Examples:
#     `alphaMELTS Environment Configuration <environment.html>`__,
#     `pyrolite-hosted alphaMELTS Installation <localinstall.html>`__,
#     `Handling Outputs from Melts: Tables <tables.html>`__,
#     `Compositional Uncertainty Propagation for alphaMELTS Experiments <montecarlo.html>`__
#
