"""
Utilities for reading alphaMELTS table outputs.
"""
import os, sys
import re
import io
import pandas as pd
from pathlib import Path
import pyrolite.geochem
from ..parse import from_melts_cstr
from ..meltsfile import df_to_meltsfiles
from pyrolite.util.pd import zero_to_nan, to_frame, to_ser

from .load import import_tables, aggregate_tables
from ..util.log import Handle

logger = Handle(__name__)
