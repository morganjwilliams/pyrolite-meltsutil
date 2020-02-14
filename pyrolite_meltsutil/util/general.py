import psutil
import subprocess
from pyrolite.util.meta import get_module_datafolder
from ..util.log import Handle

logger = Handle(__name__)

def check_perl():
    """
    Checks whether perl is installed on the system.

    Returns
    -------
    :class:`bool`
        Boolean indication of whether there is an executable perl installation.
    """
    try:
        p = subprocess.check_output(["perl", "-v"])
        returncode = 0
    except subprocess.CalledProcessError as e:
        output = e.output
        returncode = e.returncode
    except FileNotFoundError:
        returncode = 1

    return returncode == 0

def get_process_tree(process, levels_up=1):
    """
    Get a process tree from an active process or process ID.

    Parameters
    -----------
    process : :class:`int` | :class:`psutil.Process`
        Process to search for.
    levels_up : :class:`int`
        How many levels up the tree to search for parent processes.

    Returns
    -------
    :class:`list`
        List of processes associated with the given process tree.
    """
    if isinstance(process, int):
        top = psutil.Process(process)
    elif isinstance(process, psutil.Process):
        top = process
    for i in range(levels_up):
        if top.parent() is not None:
            top = top.parent()
        else:
            break
    return [top, *top.children(recursive=True)]


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
