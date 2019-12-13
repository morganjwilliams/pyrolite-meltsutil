"""
Aggregating Tables
=====================

As one of the main use cases for using pyrolite-meltsutil is executing, interrogating
and visualising multiple experiments, one of the core functionalities is importing
alphaMELTS results and integrating these. Of the key functions to do this is
:func:`~pyrolite_meltsutil.tables.load.aggregate_tables`. This enables you to load
in all the results from an array of experiments within a single folder, enabling
subsequent analysis and visualization.
"""
########################################################################################
# First let's find a folder with some results. In this case we'll use one of the
# pyrolite-meltsutil example folders which already contains some batch experiment
# results:
#
from pyrolite_meltsutil.util.general import get_data_example

experiment_dir = get_data_example("batch")
########################################################################################
# Now we can import the table files from each of the experiments. Note that in the
# same fashion as :func:`~pyrolite_meltsutil.tables.load.import_tables`,
# :func:`~pyrolite_meltsutil.tables.load.aggregate_tables` returns two tables
# - one for :code:`system` variables and one for :code:`phases`,
# which contains information pertaining to individual phases or aggregates (e.g.
# 'olivine_0', 'bulk', 'liquid' etc).
#
from pyrolite_meltsutil.tables.load import aggregate_tables

system, phases = aggregate_tables(experiment_dir)
########################################################################################
# In addition to the variables you'd expect from the tables, the returned dataframes
# also include an 'experiment' column which contains the hash-index of each experiment
# such that they can be easily distinguished:
phases.experiment.unique()
########################################################################################
# As this aggregation process can take a while for larger arrays of experiments, it's
# generally a good idea to save these results to disk such that they can be loaded
# faster:
import pandas as pd

system.to_csv(experiment_dir / "system.csv")
phases.to_csv(experiment_dir / "phases.csv")
########################################################################################
# Then next time you wish to access the data, you could simply load the tables
# back in with:
system, phases = (
    pd.read_csv(experiment_dir / "system.csv"),
    pd.read_csv(experiment_dir / "phases.csv"),
)
########################################################################################
# .. seealso:: `Loading Melts Tables <tables_load.html>`__,
#              `Import Batch Configuration <tables_config.html>`__,
