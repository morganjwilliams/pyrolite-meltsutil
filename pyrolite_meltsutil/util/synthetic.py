"""
Generating synthetic data for use with alphaMELTS.
"""
import logging
from collections import OrderedDict
from pyrolite.geochem.norm import get_reference_composition

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


def isobaricGaleMORBexample(T0=1300, T1=800, P0=5000, P1=5000, fO2="FMQ", title=None):
    Gale_MORB = get_reference_composition("MORB_Gale2013")
    majors = [
        "SiO2",
        "Al2O3",
        "FeO",
        "MnO",
        "MgO",
        "CaO",
        "Na2O",
        "TiO2",
        "K2O",
        "P2O5",
    ]
    MORB = Gale_MORB.comp[majors].reset_index(drop=True)
    if title is not None:
        MORB["Title"] = title
    MORB["Initial Temperature"] = T0
    MORB["Final Temperature"] = T1
    MORB["Initial Pressure"] = P0
    MORB["Final Pressure"] = P1
    MORB["Log fO2 Path"] = fO2
    MORB["Increment Temperature"] = -5
    MORB["Increment Pressure"] = 0
    return MORB
