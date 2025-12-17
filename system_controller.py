"""
SystemController Class - Single Array Manager
Manages the simulation grid and the single Phased Array.
"""

import numpy as np
from typing import Dict, Any
from phased_array import PhasedArray

class SystemController:
    """
    RESPONSIBILITY: The "World Manager"
    """

    def __init__(self, resolution: int = 200):  # Increased from 150
        self.resolution = resolution
        
        # Match PyQt5 grid: -10 to 10 width, 0 to 20 depth
        x = np.linspace(-10.0, 10.0, self.resolution)
        y = np.linspace(0.0, 20.0, self.resolution)
        self.grid_x, self.grid_y = np.meshgrid(x, y)
        
        # Initialize Array
        self.array = PhasedArray(id=0, num_elements=16)

    def update_parameters(self, params: Dict[str, Any]):
        """
        Update parameters of the active array.
        Handles Spacing Logic (Meters vs Lambda).
        Handles Combined Beamforming (Steer + Focus).
        """
        # --- 1. Update Basic Physics ---
        if 'num_elements' in params:
            self.array.num_elements = params['num_elements']

        if 'frequencies' in params:
            self.array.update_frequencies(params['frequencies'])

        # --- 2. Update Geometry (with Unit Conversion) ---
        if 'curvature' in params or 'spacing_val' in params:
            curvature = params.get('curvature', 0.0)
            spacing_val = params.get('spacing_val', 0.5)
            spacing_unit = params.get('spacing_unit', 'lambda') # 'lambda' or 'meter'

            # Convert Meter input to Wavelength Ratio if necessary
            if spacing_unit == 'meter':
                # Calculate Lambda based on mean frequency
                avg_freq = np.min(self.array.frequencies)
                wavelength = 3e8 / avg_freq
                spacing_ratio = spacing_val / wavelength
            else:
                spacing_ratio = spacing_val

            self.array.generate_geometry(
                spacing_ratio=spacing_ratio,
                curvature=curvature
            )

        # --- 3. Update Phases (Combined Logic) ---
        # We always read both values. If one is missing/inactive, it's None.
        steer_angle = params.get('steer_angle', 0.0)

        # Focus is optional (None if not provided)
        focus_target = params.get('focus_target', None)

        # Compute combined phases
        self.array.compute_phases(steer_angle=steer_angle, focal_point=focus_target)

    def calculate_total_field(self) -> np.ndarray:
        """Calculate electric field magnitude with PyQt5-style logarithmic scaling."""
        # Get the field (now returns real values, not complex)
        field = self.array.get_electric_field(self.grid_x, self.grid_y)
        
        # Take absolute value
        field_abs = np.abs(field)
        
        # Apply logarithmic scaling (log1p = ln(1 + x))
        field_log = np.log1p(field_abs)
        
        # Normalize to [0, 1] range
        field_min = field_log.min()
        field_max = field_log.max()
        
        if field_max - field_min > 1e-10:
            field_normalized = (field_log - field_min) / (field_max - field_min)
        else:
            field_normalized = np.zeros_like(field_log)
        
        return field_normalized