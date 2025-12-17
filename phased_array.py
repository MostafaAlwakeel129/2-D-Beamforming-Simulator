# import numpy as np
#
# class PhasedArray:
#     def __init__(self, id: int, frequency: np.ndarray, num_elements: int, curvature: float = 0.0):
#         """
#         Initialize a PhasedArray.
#
#         Args:
#             id: Unique identifier for this array
#             frequency: Operating frequency in Hz
#             num_elements: Number of elements in the array
#             curvature: Curvature parameter (0 for linear, >0 for arc)
#         """
#         self.id = id
#         self.frequency = frequency
#         self.num_elements = num_elements
#         self.curvature = curvature
#
#         # Internal Vectorized State
#         self.x_coords: np.ndarray = np.array([])
#         self.y_coords: np.ndarray = np.array([])
#         self.phases: np.ndarray = np.array([])
#
#         self.c = 3e8  # Speed of light in m/s
#         self.max_freq = np.max(self.frequency)
#         self.wavelength = self.c / self.max_freq
#         self.k = 2 * np.pi / self.wavelength
#
#     def generate_geometry(self, spacing: float, curvature: float):
#         """
#         Creates Linear if curvature=0, Circular Arc if curvature>0.
#
#         Args:
#             spacing: Element spacing (fraction of wavelength) - typically 0.5
#             curvature: Curvature parameter (1/Radius). 0 = Linear.
#         """
#         # Update internal curvature state
#         self.curvature = curvature
#
#         element_spacing_m = spacing * self.wavelength
#
#         # 2. Calculate Total Arc Length (Physical width of the array)
#         arc_length = (self.num_elements - 1) * element_spacing_m
#
#         # --- CASE A: LINEAR ARRAY ---
#         if np.abs(curvature) < 1e-9:
#             # Create N points centered at 0
#             self.x_coords = np.linspace(
#                 -arc_length / 2,
#                 arc_length / 2,
#                 self.num_elements
#             )
#             # Y is flat
#             self.y_coords = np.zeros(self.num_elements)
#
#         # --- CASE B: CURVED (ARC) ARRAY ---
#         else:
#             # Radius R = 1 / curvature
#             R = 1.0 / curvature
#
#             # Total angular spread of the array (theta = ArcLength / Radius)
#             total_angle = arc_length * curvature
#
#             # Generate angles (alpha) centered around 0
#             alpha = np.linspace(
#                 -total_angle / 2,
#                 total_angle / 2,
#                 self.num_elements
#             )
#
#             # Map Polar to Cartesian
#             # x = R * sin(alpha)
#             self.x_coords = R * np.sin(alpha)
#
#             # y = R * cos(alpha) - R
#             # The '- R' shifts the apex of the curve to (0,0)
#             self.y_coords = (R * np.cos(alpha)) - R
#
#
#     def steer_beam(self, angle_degrees: float):
#         """
#         For 5G Scenario (Far-field).
#         Steers the beam to a specific angle.
#         Uses the general Dot Product rule which works for ANY geometry (Linear, Arc, Random).
#
#         Args:
#             angle_degrees: Steering angle in degrees (0 = Broadside/Straight Ahead)
#         """
#         angle_rad = np.deg2rad(angle_degrees)
#
#         # Define the Unit Direction Vector of the target (where we want the beam to go)
#         # 0 deg = Straight up (Y-axis)
#         # 90 deg = Right (X-axis)
#         u_x = np.sin(angle_rad)
#         u_y = np.cos(angle_rad)
#
#         self.phases = -self.k * (self.x_coords * u_x + self.y_coords * u_y)
#
#     def focus_beam(self, target_x: float, target_y: float):
#         """
#         For Medical Scenario (Near-field).
#         Focuses the beam to a specific target point.
#
#         Args:
#             target_x: Target X coordinate in meters
#             target_y: Target Y coordinate in meters
#         """
#         # 1. Calculate Euclidean distance from every element to the target
#         distances = np.sqrt((self.x_coords - target_x)**2 + (self.y_coords - target_y)**2)
#
#         # 2. Find the longest path (usually the edge elements in a linear array)
#         max_distance = np.max(distances)
#
#         # 3. Calculate Phase Delays
#         self.phases = -self.k * (max_distance - distances)
#
#
#     def get_electric_field(self, grid_x: np.ndarray, grid_y: np.ndarray) -> np.ndarray:
#         """
#         Returns E = (A/r) * exp(j(kr + phi))
#         Complex electric field at each grid point.
#
#         Args:
#             grid_x: X coordinates of grid points (2D array)
#             grid_y: Y coordinates of grid points (2D array)
#
#         Returns:
#             Complex electric field array (same shape as grid_x/grid_y)
#         """
#         # Initialize field
#         field = np.zeros_like(grid_x, dtype=complex)
#
#         # Sum contributions from all elements
#         for i in range(self.num_elements):
#             # Distance from element i to each grid point
#             r = np.sqrt((grid_x - self.x_coords[i])**2 + (grid_y - self.y_coords[i])**2)
#
#             # Avoid division by zero
#             r = np.maximum(r, 1e-10)
#
#             # Amplitude decays as 1/r, phase includes k*r and element phase
#             amplitude = 1.0 / r
#             phase = self.k * r + self.phases[i]
#
#             # Add contribution from this element
#             field += amplitude * np.exp(1j * phase)
#
#         return field
#

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
        """Calculate Total Electric Field at every pixel."""
        field = np.zeros_like(grid_x, dtype=complex)
        k_vec = 2 * np.pi * self.frequencies / self.c

        for i in range(self.num_elements):
            r = np.sqrt((grid_x - self.x_coords[i]) ** 2 + (grid_y - self.y_coords[i]) ** 2)
            r = np.maximum(r, 1e-6)  # Avoid singularity
            field += (1.0 / r) * np.exp(1j * (k_vec[i] * r + self.phases[i]))

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