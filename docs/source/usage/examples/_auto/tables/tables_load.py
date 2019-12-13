"""
Loading Melts Tables
=============================

pyrolite-meltsutil includes utilites to import the information from
alphaMELTS-generated tables such that they can be more readily used for
further interrogation and visualiastion.

This example shows how you would typically import a single experiment from
the experiment directory. In this case we point you to a pyrolite-meltsutil
example folder which already contains some table files. Note that the function
returns two tables - one for :code:`system` variables and one for :code:`phases`,
which contains information pertaining to individual phases or aggregates (e.g.
'olivine_0', 'bulk', 'liquid' etc).
"""
from pyrolite_meltsutil.util.general import get_data_example
from pyrolite_meltsutil.tables.load import import_tables

# let's use the example batch data for this
experiment_dir = get_data_example("batch/363f3d0a0b")
system, phases = import_tables(experiment_dir)  # let's import the tables
########################################################################################
# The system table contains intensive variables and 'whole of system' measures.
#
system.head(3).T
########################################################################################
# The phases table contains information about individual components. In this case this
# includes the liquid, and also other aggregate measures such as 'bulk' and 'solid'.
#
phases.sample(3).T
########################################################################################
# The standard MELTS tables are extended to generate a 'cumulate' composiiton of
# integrated solids (for fractional crystallisation experiments) from the `phases`
# table:
cumulate = phases.loc[phases.phase == "cumulate", :]
########################################################################################
# Some of the thermodynamic variables will necessarily be missing for now, but most
# other relevant variables are present:
cumulate.sample(3).dropna(how="all", axis="columns").T
########################################################################################
# These cumulate compositions are generated with the
# :func:`~pyrolite_meltsutil.util.tables.integrate_solids` function (along with a few
# additions provided in :func:`~pyrolite_meltsutil.tables.load.import_tables` which
# reindex and calcuate relative percentages using the system table). You should get
# similar results with:
from pyrolite_meltsutil.util.tables import integrate_solids

cumulate = integrate_solids(phases)
########################################################################################
# .. seealso:: `Aggregating Tables <tables_aggregate.html>`__,
#              `Import Batch Configuration <tables_config.html>`__,
