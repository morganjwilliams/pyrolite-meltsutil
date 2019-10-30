"""
Utility functions for use with alphaMELTS.
"""
import logging
from collections import OrderedDict
from pyrolite.util.meta import get_module_datafolder

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


def default_data_dictionary():
    """
    Data dictionary with sufficient default values to be passed to MELTS REST services
    for testing purposes.

    Returns
    --------
    :class:`dict`
        Dictionary with some default values.
    """
    d = OrderedDict()
    d["title"] = ("TestREST",)
    d["initialize"] = {
        "SiO2": 48.68,
        "TiO2": 1.01,
        "Al2O3": 17.64,
        "Fe2O3": 0.89,
        "Cr2O3": 0.0425,
        "FeO": 7.59,
        "MnO": 0.0,
        "MgO": 9.10,
        "NiO": 0.0,
        "CoO": 0.0,
        "CaO": 12.45,
        "Na2O": 2.65,
        "K2O": 0.03,
        "P2O5": 0.08,
        "H2O": 0.20,
    }
    d["calculationMode"] = "findLiquidus"
    d["constraints"] = {"setTP": {"initialT": 1200, "initialP": 1000}}
    return d


def pyrolite_meltsutil_datafolder(subfolder=None):
    """
    Returns the path of the pyrolite-meltsutil data folder.

    Parameters
    -----------
    subfolder : :class:`str`
        Subfolder within the pyrolite data folder.

    Returns
    -------
    :class:`pathlib.Path`
    """
    return get_module_datafolder(module="pyrolite_meltsutil", subfolder=subfolder)
