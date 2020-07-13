"""
Import Batch Configuration
===========================

When importing batches of alphaMELTS experiments which have been run using
the :mod:`pyrolite_meltsutil.automation` interface, you can also import the
batch configuration file which contains the index of hashes, names, configurations
and the environment for the experiments. This can be handy to refer back to
when automatically visualising or searching through your experiments.
"""
########################################################################################
# First let's find a folder with some results. In this case we'll use one of the
# pyrolite-meltsutil example folders which already contains some batch experiment
# results:
#
from pyrolite_meltsutil.util.general import get_data_example

experiment_dir = get_data_example("batch")
########################################################################################
# Now we can import the configuration file and explore it's contents:
#
from pyrolite_meltsutil.tables.load import import_batch_config

cfg = import_batch_config(experiment_dir)
########################################################################################
# The configuration is imported as a dictionary, with keys which correspond to
# experiment hashes, which should line up with the experiment folders:
cfg.keys()
########################################################################################
# The values of the dictionary are tuples containing the experiment title, meltsfile
# configuration and the environment:
exp_name, exp_cfg, exp_env = cfg["363f3d0a0b"]
########################################################################################
exp_name
########################################################################################
exp_cfg
########################################################################################
exp_env
########################################################################################
# .. seealso:: `Loading Melts Tables <tables_load.html>`__,
#              `Aggregating Tables <tables_aggregate.html>`__,
