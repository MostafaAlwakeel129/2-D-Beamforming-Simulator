import numpy as np

class PhasedArray:
    """
    Represents the physical array of antennas.
    Handles Geometry generation and Physics calculations.
    """

    def __init__(self, id: int, num_elements: int, curvature: float = 0.0, wave_speed: float = 3e8):
        self.id = id
        self._num_elements = num_elements
        self._curvature = curvature
        self._wave_speed = wave_speed
        
        # Initialize internal arrays
        self.x_coords = np.zeros(num_elements)
        self.y_coords = np.zeros(num_elements)
        self.phases = np.zeros(num_elements)
        self._frequencies = np.ones(num_elements) * 1e9
        
        self._update_k_vec()

    # --- GETTERS & SETTERS ---

    @property
    def wave_speed(self):
        return self._wave_speed

    @wave_speed.setter
    def wave_speed(self, value: float):
        """Automatically updates wavenumbers when speed changes."""
        self._wave_speed = value
        self._update_k_vec()

    @property
    def frequencies(self):
        return self._frequencies

    @frequencies.setter
    def frequencies(self, freq_list):
        """Ensures frequency array matches element count and updates wavenumbers."""
        if isinstance(freq_list, (list, np.ndarray)):
            if len(freq_list) != self._num_elements:
                val = freq_list[0] if len(freq_list) > 0 else 1e9
                self._frequencies = np.ones(self._num_elements) * val
            else:
                self._frequencies = np.array(freq_list)
        else:
            self._frequencies = np.ones(self._num_elements) * freq_list
        self._update_k_vec()

    @property
    def num_elements(self):
        return self._num_elements

    @num_elements.setter
    def num_elements(self, value: int):
        self._num_elements = value
        # Resize arrays to match new element count
        self.x_coords = np.zeros(value)
        self.y_coords = np.zeros(value)
        self.phases = np.zeros(value)
        self.frequencies = self._frequencies[0] # Reset to a scalar default to trigger array expansion

    # --- INTERNAL LOGIC ---

    def _update_k_vec(self):
        """Internal helper to cache wavenumbers (k = 2*pi*f/c)."""
        self.k_vec = 2 * np.pi * self._frequencies / self._wave_speed

    def generate_geometry(self, spacing_ratio: float, curvature: float):
        self._curvature = curvature
        min_freq = np.min(self._frequencies) if self._frequencies.size > 0 else 1e9
        nominal_lambda = self._wave_speed / min_freq
        d = spacing_ratio * nominal_lambda

        if curvature == 0:
            indices = np.arange(self._num_elements)
            self.x_coords = (indices - (self._num_elements - 1) / 2) * d
            self.y_coords = np.zeros(self._num_elements)
        else:
            R = 1.0 / curvature
            arc_length = (self._num_elements - 1) * d
            angles = np.linspace(- (arc_length / R) / 2, (arc_length / R) / 2, self._num_elements)
            self.x_coords = R * np.sin(angles)
            self.y_coords = R * (1 - np.cos(angles))

    def compute_phases(self, steer_angle: float, focal_point: tuple = None):
        total_phases = np.zeros(self._num_elements)
        if steer_angle is not None:
            angle_rad = np.deg2rad(steer_angle)
            total_phases += -self.k_vec * self.x_coords * np.sin(angle_rad)
        if focal_point is not None:
            tx, ty = focal_point
            dists = np.sqrt((self.x_coords - tx) ** 2 + (self.y_coords - ty) ** 2)
            total_phases += self.k_vec * (np.max(dists) - dists)
        self.phases = total_phases

    def get_electric_field(self, grid_x, grid_y):
        field = np.zeros_like(grid_x, dtype=float)
        max_freq = np.max(self._frequencies)
        for i in range(self._num_elements):
            r = np.sqrt((grid_x - self.x_coords[i])**2 + (grid_y - self.y_coords[i])**2)
            r = np.maximum(r, 1e-6)
            freq_scaling = self._frequencies[i] / max_freq
            field += (freq_scaling / (r**0.3)) * np.sin(self.k_vec[i] * r + self.phases[i])
        return field

    def calculate_azimuth_profile(self, angles_deg):
        angles_rad = np.deg2rad(angles_deg)
        response = np.zeros_like(angles_rad, dtype=complex)
        for i in range(self._num_elements):
            geo_phase = self.k_vec[i] * (self.x_coords[i] * np.sin(angles_rad))
            response += np.exp(1j * (geo_phase + self.phases[i]))
        return np.log1p(np.abs(response))