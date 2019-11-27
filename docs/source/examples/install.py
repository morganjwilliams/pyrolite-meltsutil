"""
Local Installation of alphaMELTS
----------------------------------

pyrolite can download and manage its own version of alphaMELTS (without any real
'installation', *per-se*), and use this for :mod:`~pyrolite.util.alphamelts.automation`
purposes.

"""
from pyrolite.util.meta import stream_log
from pyrolite_meltsutil.download import install_melts
from pyrolite_meltsutil.util import pyrolite_meltsutil_datafolder

########################################################################################
# Here we can do a conditonal install - only downloading alphamelts if it doesnt exist:
#
if not (pyrolite_meltsutil_datafolder(subfolder="localinstall")).exists():
    stream_log("pyrolite-meltsutil", level="INFO")  # logger for output info
    install_melts(local=True)  # install a copy of melts to pyrolite data folder

########################################################################################
# .. warning:: This 'local install' method still requires that you have Perl installed,
#           as it uses the Perl :code:`run_alphamelts.command` script. If you're on
#           Windows, you can use `Strawberry Perl <http://strawberryperl.com/>`__
#           for this purpose.
#
# .. seealso::
#
#   Examples:
#     `alphaMELTS Environment Configuration <environment.html>`__,
#     `Automating alphaMELTS Runs <automation.html>`__,
#     `Handling Outputs from Melts: Tables <tables.html>`__,
#     `Compositional Uncertainty Propagation for alphaMELTS Experiments <montecarlo.html>`__
