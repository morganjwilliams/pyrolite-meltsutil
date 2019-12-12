"""
Aggregating Tables
=============================
"""
from pyrolite_meltsutil.tables.load import aggregate_tables, import_batch_config

experiment_dir = get_data_example("batch")  # let's use the example batch data for this
system, phases = aggregate_tables(experiment_dir)  # let's import the tables
cfg = import_batch_config(experiment_dir)
