"""
Visualisation: Distinguishing Phases
=====================================
"""
########################################################################################
# Styling by phase is largely achieved with color, here using the
# :func:`~pyrolite_meltsutil.vis.style.phase_color` function, which will return
# unique colors for each phase:
from pyrolite_meltsutil.vis.style import phase_color

phase_color("olivine")
########################################################################################
# This will also work if given a phase ID:
#
phase_color("olivine_0")
########################################################################################
# Similarly, to differentiate between different generations or endmembers,
# a linestyle or marker can be used, here generated with
# :func:`~pyrolite_meltsutil.vis.style.phaseID_linestyle` which takes the full phaseID:
#
from pyrolite_meltsutil.vis.style import phaseID_linestyle, phaseID_marker

[phaseID_linestyle(ol) for ol in ["olivine_0", "olivine_1", "olivine_2"]]
########################################################################################
[phaseID_marker(ol) for ol in ["olivine_0", "olivine_1", "olivine_2"]]
########################################################################################
# We can now use these when we're plotting to differentiate different phases:
#


########################################################################################
# These are also handy for generating legend proxies:
# 
