import json
import hashlib
from pyrolite.util.text import slugify
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)

__abbrv__ = {"fractionate solids": "frac", "isobaric": "isobar"}


def exp_hash(d, algorithm="sha1", length=10):
    """
    Get the hash of an experiment configuration dictionary.

    Parameters
    ----------
    d : :class:`dict`
        Configuration dictonary.
    algorithm : :class:`str`
        Name of hash algorithm to use.
    length : :class:`int`
        Length of the returned index generated from the hash.

    Returns
    --------
    :class:`str`
        Hash-based index for the configuration.

    Todo
    -------

        * Consider rounding floats to 4-5 decimal places to minimise floating point
            errors and potential differences across systems
    """
    length = length or -0
    hsh = hashlib.new(algorithm)
    hsh.update(json.dumps(d, sort_keys=True, ensure_ascii=False).encode("utf8"))
    hex = hsh.hexdigest()
    length = length or len(hex)
    return hex[:length]


def exp_name(exp):
    """
    Derive an experiment name from an experiment configuration dictionary.

    Parameters
    ------------
    exp : :class:`dict`
        Dictionary of parameters and their specific values to derive an experiment name
        from.

    Todo
    ------

        This is a subset of potential parameters, hash is used to ensure uniqueness of naming.

        To avoid path length limits, we keep only a fraction of the hash length.

        Avoid using odd symbols like @.
    """

    p0, p1, t0, t1 = "", "", "", ""
    if exp.get("Initial Pressure", None) is not None:
        p0 = "{:d}".format(int(exp["Initial Pressure"] / 1000))
    if exp.get("Final Pressure", None) is not None:
        p1 = "{:d}".format(int(exp["Final Pressure"] / 1000))
    if exp.get("Initial Temperature", None) is not None:
        t0 = "{:d}".format(int(exp["Initial Temperature"]))
    if exp.get("Final Temperature", None) is not None:
        t1 = "{:d}".format(int(exp["Final Temperature"]))
    fo2 = exp.get("Log fO2 Path", "")
    fo2d = exp.get("Log fO2 Delta", "")

    titlestr = slugify(exp.get("Title", ""))
    modestr = "".join([__abbrv__.get(m, m) for m in exp.get("modes", [""])])
    pstr = p0 + ["-" + p1, ""][p1 == ""] + ["", "kbar"][p0 + p1 != ""]
    tstr = t0 + ["-" + t1, ""][t1 == ""] + ["", "C"][t0 + t1 != ""]
    fo2str = "{}{}".format(fo2d, fo2)
    chemstr = "-".join(
        ["{}{}".format(k, v) for k, v in exp.get("modifychem", {}).items()]
    )

    suppressstr = "-".join(["no_{}".format(v) for v in exp.get("Suppress", {})])
    hashstr = "{}".format(exp_hash(exp))

    return slugify(
        "".join([titlestr, modestr, pstr, tstr, fo2str, chemstr, suppressstr, hashstr])
    )
