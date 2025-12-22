import numpy as np

class PhasedArray:
    """
    Represents the physical array of antennas.
    Handles Geometry generation and Physics calculations (Steering/Focusing).
    """

    def __init__(self, id: int, num_elements: int, curvature: float = 0.0,wave_speed = 3e8):
        self.id = id
        self.num_elements = num_elements
        self.curvature = curvature
        self.WAVE_SPEED = wave_speed
        self.x_coords = np.zeros(num_elements)
        self.y_coords = np.zeros(num_elements)
        self.phases = np.zeros(num_elements)
        
        # Initialize frequencies and cached wavenumbers (k = 2*pi*f/c)
        self.frequencies = np.ones(num_elements) * 1e9
        
        self._update_k_vec()

    def _update_k_vec(self):
        """Internal helper to cache wavenumbers."""
        self.k_vec = 2 * np.pi * self.frequencies / self.WAVE_SPEED

    def set_speed_of_wave(self, speed: float):
        """Update propagation speed (Light vs Sound) and refresh wavenumbers."""
        self.WAVE_SPEED = speed
        self._update_k_vec()

    def update_frequencies(self, freq_list):
        """Update frequency for each element and refresh wavenumbers."""
        if len(freq_list) != self.num_elements:
            val = freq_list[0] if len(freq_list) > 0 else 1e9
            self.frequencies = np.ones(self.num_elements) * val
        else:
            self.frequencies = np.array(freq_list)
        self._update_k_vec()

    def generate_geometry(self, spacing_ratio: float, curvature: float):
        """Generate (x,y) coordinates based on spacing ratio of min wavelength."""
        self.curvature = curvature
        min_freq = np.min(self.frequencies) if self.frequencies.size > 0 else 1e9
        nominal_lambda = self.WAVE_SPEED / min_freq
        d = spacing_ratio * nominal_lambda

        if curvature == 0:
            indices = np.arange(self.num_elements)
            self.x_coords = (indices - (self.num_elements - 1) / 2) * d
            self.y_coords = np.zeros(self.num_elements)
        else:
            R = 1.0 / curvature
            arc_length = (self.num_elements - 1) * d
            angles = np.linspace(- (arc_length / R) / 2, (arc_length / R) / 2, self.num_elements)
            self.x_coords = R * np.sin(angles)
            self.y_coords = R * (1 - np.cos(angles))

    def compute_phases(self, steer_angle: float, focal_point: tuple = None):
        """Calculates and combines phase shifts: Total = Phase_Steer + Phase_Focus"""
        total_phases = np.zeros(self.num_elements)

        if steer_angle is not None:
            angle_rad = np.deg2rad(steer_angle)
            total_phases += -self.k_vec * self.x_coords * np.sin(angle_rad)

        if focal_point is not None:
            tx, ty = focal_point
            dists = np.sqrt((self.x_coords - tx) ** 2 + (self.y_coords - ty) ** 2)
            total_phases += self.k_vec * (np.max(dists) - dists)

        self.phases = total_phases

    def get_electric_field(self, grid_x, grid_y):
        """Calculate Total Electric Field magnitude using real sine waves."""
        field = np.zeros_like(grid_x, dtype=float)
        max_freq = np.max(self.frequencies)
        
        for i in range(self.num_elements):
            r = np.sqrt((grid_x - self.x_coords[i])**2 + (grid_y - self.y_coords[i])**2)
            r = np.maximum(r, 1e-6)
            freq_scaling = self.frequencies[i] / max_freq
            field += (freq_scaling / (r**0.3)) * np.sin(self.k_vec[i] * r + self.phases[i])
        return field

    def calculate_azimuth_profile(self, angles_deg):
        """Simulate Far-Field Response vs Angle."""
        angles_rad = np.deg2rad(angles_deg)
        response = np.zeros_like(angles_rad, dtype=complex)

        for i in range(self.num_elements):
            geo_phase = self.k_vec[i] * (self.x_coords[i] * np.sin(angles_rad))
            response += np.exp(1j * (geo_phase + self.phases[i]))

        return np.log1p(np.abs(response))