"""
Utilities for reading alphaMELTS table outputs.
"""
import io
import os
import re
import sys
from pathlib import Path

import pandas as pd
import pyrolite.geochem
from pyrolite.util.pd import to_frame, to_ser, zero_to_nan

from ..meltsfile import df_to_meltsfiles
from ..parse import from_melts_cstr
from ..util.log import Handle
from .load import aggregate_tables, import_tables

logger = Handle(__name__)
