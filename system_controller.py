# """
# SystemController Class - Single Array Manager
#
# Manages the simulation grid and the single Phased Array.
# """
#
# import numpy as np
# from typing import Dict, Any
# from phased_array import PhasedArray
#
# class SystemController:
#     """
#     RESPONSIBILITY: The "World Manager" (Single Array Version)
#     Manages the simulation grid and controls the single phased array.
#     """
#
#     def __init__(self, resolution: int = 200):
#         """
#         Initialize SystemController.
#
#         Args:
#             resolution: Grid resolution (number of points per dimension)
#         """
#         self.resolution = resolution
#
#         # 1. Initialize Grid
#         self._initialize_grid()
#
#         # 2. Initialize the Single Array
#         self.array = PhasedArray(
#             id=0,
#             frequency=np.array([1e9]), # Default 1 GHz
#             num_elements=16,
#             curvature=0.0
#         )
#
#     def _initialize_grid(self):
#         """Initialize the simulation grid."""
#         # Create a grid from -2 to 2 meters
#         grid_range = 2.0
#         grid = np.linspace(-grid_range, grid_range, self.resolution)
#         self.grid_x, self.grid_y = np.meshgrid(grid, grid)
#
#     def set_grid_resolution(self, res: int):
#         """Set the grid resolution and rebuild grid."""
#         self.resolution = res
#         self._initialize_grid()
#
#     def update_parameters(self, params: Dict[str, Any]):
#         """
#         Update parameters of the single active array.
#
#         Args:
#             params: Dictionary containing any of:
#                     - frequency
#                     - num_elements
#                     - spacing
#                     - curvature
#                     - steer_angle (for Far Field)
#                     - focus_target (tuple x,y for Near Field)
#         """
#         # --- 1. Update Physics (Frequency) ---
#         if 'frequency' in params:
#             self.array.frequency = params['frequency']
#             # Recalculate derived constants
#             self.array.max_freq = np.max(self.array.frequency)
#             self.array.wavelength = self.array.c / self.array.max_freq
#             self.array.k = 2 * np.pi / self.array.wavelength
#
#         # --- 2. Update Geometry ---
#         # If any geometric param is present, we regenerate the positions
#         geom_keys = ['num_elements', 'spacing', 'curvature']
#         if any(key in params for key in geom_keys):
#             # Fetch new values or fallback to existing array state
#             # Note: We default 'spacing' to 0.5 if not provided
#             spacing = params.get('spacing', 0.5)
#             curvature = params.get('curvature', self.array.curvature)
#
#             if 'num_elements' in params:
#                 self.array.num_elements = params['num_elements']
#
#             # Call the array's geometry generator
#             self.array.generate_geometry(spacing=spacing, curvature=curvature)
#
#         # --- 3. Update Beamforming (Steering or Focusing) ---
#         # Case A: Far-Field Steering
#         if 'steer_angle' in params:
#             self.array.steer_beam(params['steer_angle'])
#
#         # Case B: Near-Field Focusing
#         elif 'focus_target' in params:
#             target_x, target_y = params['focus_target']
#             self.array.focus_beam(target_x, target_y)
#
#     def calculate_total_field(self) -> np.ndarray:
#         """
#         Calculate electric field magnitude for the single array.
#
#         Returns:
#             2D array of field magnitudes
#         """
#         # Direct calculation (No summation loop needed for a single array)
#         field_complex = self.array.get_electric_field(self.grid_x, self.grid_y)
#
#         # Return magnitude
#         return np.abs(field_complex)
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

    def __init__(self, resolution: int = 150):
        self.resolution = resolution
        # Grid Setup: -3m to 3m width, 0m to 2m depth
        x = np.linspace(-3.0, 3.0, self.resolution)
        y = np.linspace(0.0, 2.0, self.resolution)
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
        """Calculate electric field magnitude."""
        field_complex = self.array.get_electric_field(self.grid_x, self.grid_y)
        return np.abs(field_complex)