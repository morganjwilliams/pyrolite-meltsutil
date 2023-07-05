"""
Visualisation utilities for working with alphaMELTS table outputs.

Todo
-------

    * Pull out mineral compostional trends
"""
from pyrolite.util.plot.legend import proxy_line

from ..tables.load import import_tables
from ..util.log import Handle
from . import templates
from .style import phase_color, phaseID_linestyle

logger = Handle(__name__)
