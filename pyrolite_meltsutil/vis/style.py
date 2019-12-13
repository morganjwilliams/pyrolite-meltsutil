from ..util.tables import phasename
import matplotlib.colors as mcolors

COLORS = {
    "aegirine": None,
    "aenigmatite": None,
    "alloy-liquid": None,
    "alloy-solid": None,
    "amphibole": "darkslategrey",
    "apatite": None,
    "biotite": "brown",
    "clinopyroxene": "teal",
    "corundum": None,
    "cristobalite": None,
    "cummingtonite": None,
    "fayalite": None,
    "feldspar": "pink",
    "garnet": "red",
    "hornblende": "darkolivegreen",
    "kalsilite": None,
    "liquid": "black",
    "leucite": None,
    "melilite": None,
    "muscovite": None,
    "nepheline": None,
    "olivine": "green",
    "ortho-oxide": None,
    "orthopyroxene": "darkorange",
    "perovskite": None,
    "quartz": None,
    "rhm-oxide": None,
    "rutile": None,
    "sillimanite": None,
    "sphene": None,
    "spinel": "0.5",
    "tridymite": None,
    "water": "aquamarine",
    "whitlockite": None,
}

def phase_color(phase, rgb=False):
    """
    Method for generating colors for delineating phase names
    (e.g. olivine, clinopyroxene) based on their names.

    Parameters
    ------------
    phase : :class:`str`
        Phase name or phase ID to generate a color for.

    Returns
    --------
    :class:`str`
        Color for the phase.
    """
    c = COLORS.get(phasename(phase), None)
    if rgb:
        c = mcolors.to_rgb(c)  # will error on None
    return c


def phaseID_linestyle(phaseID, linestyles=["-", "--", ":", "-."]):
    """
    Method for generating linestyles for delineating sequential phases
    based on their phase IDs (e.g. olivine_0, olivine_1) .

    Parameters
    -----------
    phasename : :class:`str`
        Phase ID for which to generate a line style.
    linestyles : :class:`list`
        List of line styles for sequential phase ID numbers.
        Added to allow reconfiguraiton where needed.

    Returns
    ---------
    :class:`str`
        Line style for the phase ID.
    """
    if "_" in phaseID:
        return linestyles[int(phaseID[-1])]
    else:
        return linestyles[0]


def phaseID_marker(phaseID, markers=["D", "s", "o", "+", "*"]):
    """
    Method for generating markers for delineating sequential phases
    based on their phase IDs (e.g. olivine_0, olivine_1) .

    Parameters
    -----------
    phasename : :class:`str`
        Phase ID for which to generate a line style.
    markers : :class:`list`
        List of markers for sequential phase ID numbers.
        Added to allow reconfiguraiton where needed.

    Returns
    ---------
    :class:`str`
        Marker for the phase ID.
    """
    if "_" in phaseID:
        return markers[int(phaseID[-1])]
    else:
        return markers[0]
