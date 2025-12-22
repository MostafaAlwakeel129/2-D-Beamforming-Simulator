import numpy as np
from typing import Dict, Any
from phased_array import PhasedArray

class SystemController:
    """Manages the simulation grid and coordinate systems."""

    def __init__(self, resolution: int = 200):
        self.resolution = resolution
        self._grid_width = 20.0
        self._grid_depth = 20.0
        self._initialize_grid()
        self.array = PhasedArray(id=0, num_elements=16)

    @property
    def grid_width(self):
        return self._grid_width

    @grid_width.setter
    def grid_width(self, value):
        self._grid_width = value
        self._initialize_grid()

    @property
    def grid_depth(self):
        return self._grid_depth

    @grid_depth.setter
    def grid_depth(self, value):
        self._grid_depth = value
        self._initialize_grid()

    def _initialize_grid(self):
        """Regenerate the meshgrid based on current dimensions."""
        x = np.linspace(-self._grid_width / 2, self._grid_width / 2, self.resolution)
        y = np.linspace(0.0, self._grid_depth, self.resolution)
        self.grid_x, self.grid_y = np.meshgrid(x, y)

    def update_parameters(self, params: Dict[str, Any]):
        """Update active array parameters using property setters."""

        if 'wave_speed' in params:
            self.array.wave_speed = params['wave_speed']

        # Updating these triggers _initialize_grid automatically via setters
        if 'grid_width' in params:
            self.grid_width = params['grid_width']
        if 'grid_depth' in params:
            self.grid_depth = params['grid_depth']

        if 'num_elements' in params:
            self.array.num_elements = params['num_elements']

        if 'frequencies' in params:
            self.array.frequencies = params['frequencies']

        if 'curvature' in params or 'spacing_val' in params:
            spacing_val = params.get('spacing_val', 0.5)
            if params.get('spacing_unit') == 'meter':
                wavelength = self.array.wave_speed / np.min(self.array.frequencies)
                spacing_ratio = spacing_val / wavelength
            else:
                spacing_ratio = spacing_val

            self.array.generate_geometry(spacing_ratio, params.get('curvature', 0.0))

        self.array.compute_phases(
            steer_angle=params.get('steer_angle', 0.0),
            focal_point=params.get('focus_target')
        )

    def calculate_total_field(self) -> np.ndarray:
        field_log = np.log1p(np.abs(self.array.get_electric_field(self.grid_x, self.grid_y)))
        f_min, f_max = field_log.min(), field_log.max()
        
        if f_max - f_min > 1e-10:
            return (field_log - f_min) / (f_max - f_min)
        return np.zeros_like(field_log)