import numpy as np
from typing import Dict, Any
from phased_array import PhasedArray

class SystemController:
    """Manages the simulation grid and coordinate systems."""

    def __init__(self, resolution: int = 200):
        self.resolution = resolution
        # Default Grid State (Will be overwritten by Scenario)
        self.grid_width = 20.0
        self.grid_depth = 20.0
        self._initialize_grid()
        self.array = PhasedArray(id=0, num_elements=16)

    def _initialize_grid(self):
        """Regenerate the meshgrid based on current dimensions."""
        x = np.linspace(-self.grid_width / 2, self.grid_width / 2, self.resolution)
        y = np.linspace(0.0, self.grid_depth, self.resolution)
        self.grid_x, self.grid_y = np.meshgrid(x, y)

    def update_parameters(self, params: Dict[str, Any]):
        """Update active array parameters and unit conversions."""

        # --- 1. Update Physics Scale (Speed & Grid) ---
        if 'wave_speed' in params:
            self.array.set_speed_of_wave(params['wave_speed'])

        # Update Grid Size (Dynamic Scaling)
        new_w = params.get('grid_width', self.grid_width)
        new_d = params.get('grid_depth', self.grid_depth)

        if new_w != self.grid_width or new_d != self.grid_depth:
            self.grid_width = new_w
            self.grid_depth = new_d
            self._initialize_grid()

        # --- 2. Update Array Parameters ---
        if 'num_elements' in params:
            self.array.num_elements = params['num_elements']

        if 'frequencies' in params:
            self.array.update_frequencies(params['frequencies'])

        if 'curvature' in params or 'spacing_val' in params:
            spacing_val = params.get('spacing_val', 0.5)
            # Convert meter to lambda ratio if unit is 'meter'
            if params.get('spacing_unit') == 'meter':
                # Use current array wave speed instead of hardcoded SPEED_OF_LIGHT
                wavelength = self.array.WAVE_SPEED / np.min(self.array.frequencies)
                spacing_ratio = spacing_val / wavelength
            else:
                spacing_ratio = spacing_val

            self.array.generate_geometry(spacing_ratio, params.get('curvature', 0.0))

        self.array.compute_phases(
            steer_angle=params.get('steer_angle', 0.0),
            focal_point=params.get('focus_target')
        )

    def calculate_total_field(self) -> np.ndarray:
        """Apply logarithmic scaling and normalization to the electric field."""
        field_log = np.log1p(np.abs(self.array.get_electric_field(self.grid_x, self.grid_y)))
        f_min, f_max = field_log.min(), field_log.max()
        
        if f_max - f_min > 1e-10:
            return (field_log - f_min) / (f_max - f_min)
        return np.zeros_like(field_log)