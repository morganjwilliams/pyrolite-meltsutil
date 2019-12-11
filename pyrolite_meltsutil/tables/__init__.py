"""
Utilities for reading alphaMELTS table outputs.
"""
import os, sys
import re
import io
import logging
import pandas as pd
from pathlib import Path
import pyrolite.geochem
from ..parse import from_melts_cstr
from ..meltsfile import df_to_meltsfiles
from pyrolite.util.pd import zero_to_nan, to_frame, to_ser

from .load import import_tables, aggregate_tables

logging.getLogger(__name__).addHandler(logging.NullHandler())
logger = logging.getLogger(__name__)
