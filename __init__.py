"""
2-D Beamforming Simulator Package

A simulator for visualizing constructive/destructive interference and beam profiles
for phased arrays (Linear/Curved) with real-time steering control.
"""

__version__ = "1.0.0"

from .beamforming_app import BeamformingApp
from .system_controller import SystemController
from .phased_array import PhasedArray
from .scenario_loader import ScenarioLoader
from .visualizer import Visualizer

__all__ = [
    "BeamformingApp",
    "SystemController",
    "PhasedArray",
    "ScenarioLoader",
    "Visualizer",
]

