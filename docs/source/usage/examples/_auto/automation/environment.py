"""
alphaMELTS Environment
------------------------
"""
from pyrolite_meltsutil.env import MELTS_Env

########################################################################################
# Set up an environment for an experiment stepping down temperature from 1350 to 1000
# in 3 degree steps:
#
env = MELTS_Env()
env.MINP = 7000
env.MAXP = 7000
env.MINT = 1000
env.MAXT = 1350
env.DELTAT = -3
########################################################################################
# You can directly export these parameters to an envrionment file:
#
with open("pyrolite_envfile.txt", "w") as f:
    f.write(env.to_envfile(unset_variables=False))
########################################################################################
# You can then pass this to alphamelts using
# :code:`run_alphamelts.command -f pyrolite_envfile.txt`
#
# .. seealso::
#
#   Examples:
#     `pyrolite-hosted alphaMELTS Installation <localinstall.html>`__,
#     `Automating alphaMELTS Runs <automation.html>`__,
#     `Handling Outputs from Melts: Tables <tables.html>`__,
#     `Compositional Uncertainty Propagation for alphaMELTS Experiments <montecarlo.html>`__
#
