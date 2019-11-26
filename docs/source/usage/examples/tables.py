"""
alphaMELTS Tables
--------------------

To automatically import alphaMELTS tables as :class:`~pandas.DataFrame`s, you can use
:class:`~pyrolite.util.alphamelts.tables.MeltsOutput`, from which you can then
develop plots and interrogate data.
"""
import matplotlib.pyplot as plt
from pyrolite_meltsutil.tables import MeltsOutput

########################################################################################
# If you have a folder containing melts table outputs, you can import them using:
#
output = MeltsOutput(folder, kelvin=False)  # tables in degrees C
########################################################################################
# This object has a number of useful attributes:
output.tables  # list of tables accessible from the object
########################################################################################
output.phasenames  # get the names of phases which appear in the experiment
########################################################################################
output.phases  # dictionary of phasename : phase composition tables (<df>)
########################################################################################
# For example, you can access the phase volume table using:
#
output.phasevol
########################################################################################
# .. seealso::
#
#   Examples:
#     `pyrolite-hosted alphaMELTS Installation <localinstall.html>`__,
#     `alphaMELTS Environment Configuration <environment.html>`__,
#     `Automating alphaMELTS Runs <automation.html>`__,
#     `Compositional Uncertainty Propagation for alphaMELTS Experiments <montecarlo.html>`__
#
