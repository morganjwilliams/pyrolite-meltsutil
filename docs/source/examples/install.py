from pyrolite.util.meta import stream_log
from pyrolite_meltsutil.download import install_melts
from pyrolite_meltsutil.util import pyrolite_meltsutil_datafolder

# Here we can do a conditonal install - only downloading alphamelts if it doesnt exist
if not (pyrolite_meltsutil_datafolder(subfolder="localinstall")).exists():
    stream_log("pyrolite.util.alphamelts", level="INFO")  # logger for output info
    install_melts(local=True)  # install a copy of melts to pyrolite data folder
