import logging
from pyrolite.util.meta import get_module_datafolder

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)


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


def get_local_link(name):
    """
    Get the filepath of a local link file installed with alphaMELTS.

    Parameters
    -----------
    name : :class:`str`
        Filename for the link file.

    Returns
    -------
    :class:`pathlib.Path`
    """
    return pyrolite_meltsutil_datafolder("localinstall") / "links" / name


def get_local_example(name):
    """
    Get the filepath of a local example file installed with alphaMELTS.

    Parameters
    -----------
    name : :class:`str`
        Filename for the example file.

    Returns
    -------
    :class:`pathlib.Path`
    """
    return pyrolite_meltsutil_datafolder("localinstall") / "examples" / name


def get_data_example(name):
    """
    Get the filepath of an example data file from pyrolite-meltsutil.

    Parameters
    -----------
    name : :class:`str`
        Filename for the example file.

    Returns
    -------
    :class:`pathlib.Path`
    """
    return pyrolite_meltsutil_datafolder("data_examples") / name
