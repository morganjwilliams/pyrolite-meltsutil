"""
Loading Melts Tables
=============================
"""
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.tables.load import import_tables

experiment_dir = get_data_example(
    "batch/363f3d0a0b"
)  # let's use the example batch data for this
system, phases = import_tables(experiment_dir)  # let's import the tables
########################################################################################
# The system table contains intensive variables and 'whole of system' measures.
#
system.head(3).T
########################################################################################
# The phases table contains information about individual components. In this case this
# includes the liquid, and also other aggregate measures such as 'bulk' and 'solid'.
#
phases.head(3).T
########################################################################################
# This can be extended to generate a 'cumulate' composiiton of integrated
# solids (for fractional crystallisation experiments):
