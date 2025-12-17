import numpy as np

class PhasedArray:
    """
    PhasedArray Class
    Represents the physical array of antennas.
    Handles Geometry generation and Physics calculations (Steering/Focusing).
    """

    def __init__(self, id: int, num_elements: int, curvature: float = 0.0):
        """
        Initialize PhasedArray.
        """
        self.id = id
        self.num_elements = num_elements
        self.curvature = curvature

        # State
        self.frequencies = np.ones(num_elements) * 1e9
        self.x_coords = np.zeros(num_elements)
        self.y_coords = np.zeros(num_elements)
        self.phases = np.zeros(num_elements)

        # Physics Constants
        self.c = 3e8

    def update_frequencies(self, freq_list):
        """Update frequency for each element individually."""
        if len(freq_list) != self.num_elements:
            val = freq_list[0] if len(freq_list) > 0 else 1e9
            self.frequencies = np.ones(self.num_elements) * val
        else:
            self.frequencies = np.array(freq_list)

    def generate_geometry(self, spacing_ratio: float, curvature: float):
        """
        Generate (x,y) coordinates.
        spacing_ratio: Spacing as fraction of min wavelength.
        """
        self.curvature = curvature

        # Calculate nominal wavelength
        min_freq = np.min(self.frequencies) if len(self.frequencies) > 0 else 1e9
        nominal_lambda = self.c / min_freq
        d = spacing_ratio * nominal_lambda

        # 1. Linear Geometry
        if curvature == 0:
            indices = np.arange(self.num_elements)
            self.x_coords = (indices - (self.num_elements - 1) / 2) * d
            self.y_coords = np.zeros(self.num_elements)

        # 2. Curved (Arc) Geometry
        else:
            R = 1.0 / curvature
            arc_length = (self.num_elements - 1) * d
            total_angle = arc_length / R
            angles = np.linspace(-total_angle / 2, total_angle / 2, self.num_elements)
            self.x_coords = R * np.sin(angles)
            self.y_coords = (R * np.cos(angles)) - R

    def compute_phases(self, steer_angle: float, focal_point: tuple = None):
        """
        Calculates and combines phase shifts for both Steering and Focusing.
        Total Phase = Phase_Steer + Phase_Focus
        """
        k_vec = 2 * np.pi * self.frequencies / self.c
        total_phases = np.zeros(self.num_elements)

        # 1. Add Steering Component (Linear Phase Gradient)
        # phi = -k * x * sin(theta)
        if steer_angle is not None:
            angle_rad = np.deg2rad(steer_angle)
            steering_phases = -k_vec * self.x_coords * np.sin(angle_rad)
            total_phases += steering_phases

        # 2. Add Focusing Component (Quadratic/Distance Correction)
        # phi = k * distance_to_focal_point
        if focal_point is not None:
            tx, ty = focal_point
            # Calculate distance from each element to target
            dists = np.sqrt((self.x_coords - tx) ** 2 + (self.y_coords - ty) ** 2)
            # Time-of-flight compensation: delay closer elements
            # We reference to the furthest element to keep phases positive/causal
            max_dist = np.max(dists)
            focusing_phases = k_vec * (max_dist - dists)
            total_phases += focusing_phases

        self.phases = total_phases

    def get_electric_field(self, grid_x, grid_y):
        """Calculate Total Electric Field - PyQt5 Style (Real sine waves, no 1/r decay)"""
        field = np.zeros_like(grid_x, dtype=float)  # Changed to float
        k_vec = 2 * np.pi * self.frequencies / self.c
        
        # Get max frequency for scaling
        max_freq = np.max(self.frequencies)
        
        for i in range(self.num_elements):
            # Distance from element i to each grid point
            r = np.sqrt((grid_x - self.x_coords[i]) ** 2 + (grid_y - self.y_coords[i]) ** 2)
            r = np.maximum(r, 1e-6)  # Avoid singularity
            
            # Frequency scaling (normalize by max frequency)
            frequency_scaling = self.frequencies[i] / max_freq
            
            # Real sine wave WITHOUT 1/r amplitude decay
            field += frequency_scaling * np.sin(k_vec[i] * r + self.phases[i])
        
        return field

    def calculate_azimuth_profile(self, angles_deg):
        """Simulate Far-Field Response vs Angle."""
        angles_rad = np.deg2rad(angles_deg)
        k_vec = 2 * np.pi * self.frequencies / self.c
        response = np.zeros_like(angles_rad, dtype=complex)

        for i in range(self.num_elements):
            # Geometric phase difference
            geo_phase = k_vec[i] * (self.x_coords[i] * np.sin(angles_rad))
            # Add element contribution
            response += np.exp(1j * (geo_phase + self.phases[i]))

        return np.abs(response)