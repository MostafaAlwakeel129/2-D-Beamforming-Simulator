import numpy as np
from typing import Dict, Any
from phased_array import PhasedArray, SPEED_OF_LIGHT

class SystemController:
    """Manages the simulation grid and coordinate systems."""

    def __init__(self, resolution: int = 200):
        self.resolution = resolution
        x = np.linspace(-10.0, 10.0, self.resolution)
        y = np.linspace(0.0, 20.0, self.resolution)
        self.grid_x, self.grid_y = np.meshgrid(x, y)
        self.array = PhasedArray(id=0, num_elements=16)

    def update_parameters(self, params: Dict[str, Any]):
        """Update active array parameters and unit conversions."""
        if 'num_elements' in params:
            self.array.num_elements = params['num_elements']

        if 'frequencies' in params:
            self.array.update_frequencies(params['frequencies'])

        if 'curvature' in params or 'spacing_val' in params:
            spacing_val = params.get('spacing_val', 0.5)
            # Convert meter to lambda ratio if unit is 'meter'
            if params.get('spacing_unit') == 'meter':
                wavelength = SPEED_OF_LIGHT / np.min(self.array.frequencies)
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