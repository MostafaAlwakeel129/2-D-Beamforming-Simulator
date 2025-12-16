import numpy as np

class PhasedArray:
    def __init__(self, id: int, frequency: np.ndarray, num_elements: int, curvature: float = 0.0):
        """
        Initialize a PhasedArray.

        Args:
            id: Unique identifier for this array
            frequency: Operating frequency in Hz
            num_elements: Number of elements in the array
            curvature: Curvature parameter (0 for linear, >0 for arc)
        """
        self.id = id
        self.frequency = frequency
        self.num_elements = num_elements
        self.curvature = curvature

        # Internal Vectorized State
        self.x_coords: np.ndarray = np.array([])
        self.y_coords: np.ndarray = np.array([])
        self.phases: np.ndarray = np.array([])

        self.c = 3e8  # Speed of light in m/s
        self.max_freq = np.max(self.frequency)
        self.wavelength = self.c / self.max_freq
        self.k = 2 * np.pi / self.wavelength

    def generate_geometry(self, spacing: float, curvature: float):
        """
        Creates Linear if curvature=0, Circular Arc if curvature>0.

        Args:
            spacing: Element spacing (fraction of wavelength) - typically 0.5
            curvature: Curvature parameter (1/Radius). 0 = Linear.
        """
        # Update internal curvature state
        self.curvature = curvature

        element_spacing_m = spacing * self.wavelength
        
        # 2. Calculate Total Arc Length (Physical width of the array)
        arc_length = (self.num_elements - 1) * element_spacing_m

        # --- CASE A: LINEAR ARRAY ---
        if np.abs(curvature) < 1e-9:
            # Create N points centered at 0
            self.x_coords = np.linspace(
                -arc_length / 2,
                arc_length / 2,
                self.num_elements
            )
            # Y is flat
            self.y_coords = np.zeros(self.num_elements)

        # --- CASE B: CURVED (ARC) ARRAY ---
        else:
            # Radius R = 1 / curvature
            R = 1.0 / curvature
            
            # Total angular spread of the array (theta = ArcLength / Radius)
            total_angle = arc_length * curvature
            
            # Generate angles (alpha) centered around 0
            alpha = np.linspace(
                -total_angle / 2, 
                total_angle / 2, 
                self.num_elements
            )
            
            # Map Polar to Cartesian
            # x = R * sin(alpha)
            self.x_coords = R * np.sin(alpha)
            
            # y = R * cos(alpha) - R
            # The '- R' shifts the apex of the curve to (0,0)
            self.y_coords = (R * np.cos(alpha)) - R


    def steer_beam(self, angle_degrees: float):
        """
        For 5G Scenario (Far-field).
        Steers the beam to a specific angle.
        Uses the general Dot Product rule which works for ANY geometry (Linear, Arc, Random).

        Args:
            angle_degrees: Steering angle in degrees (0 = Broadside/Straight Ahead)
        """
        angle_rad = np.deg2rad(angle_degrees)
        
        # Define the Unit Direction Vector of the target (where we want the beam to go)
        # 0 deg = Straight up (Y-axis)
        # 90 deg = Right (X-axis)
        u_x = np.sin(angle_rad)
        u_y = np.cos(angle_rad)
        
        self.phases = -self.k * (self.x_coords * u_x + self.y_coords * u_y)

    def focus_beam(self, target_x: float, target_y: float):
        """
        For Medical Scenario (Near-field).
        Focuses the beam to a specific target point.

        Args:
            target_x: Target X coordinate in meters
            target_y: Target Y coordinate in meters
        """
        # 1. Calculate Euclidean distance from every element to the target
        distances = np.sqrt((self.x_coords - target_x)**2 + (self.y_coords - target_y)**2)
        
        # 2. Find the longest path (usually the edge elements in a linear array)
        max_distance = np.max(distances)
        
        # 3. Calculate Phase Delays
        self.phases = -self.k * (max_distance - distances)


    def get_electric_field(self, grid_x: np.ndarray, grid_y: np.ndarray) -> np.ndarray:
        """
        Returns E = (A/r) * exp(j(kr + phi))
        Complex electric field at each grid point.

        Args:
            grid_x: X coordinates of grid points (2D array)
            grid_y: Y coordinates of grid points (2D array)

        Returns:
            Complex electric field array (same shape as grid_x/grid_y)
        """
        # Initialize field
        field = np.zeros_like(grid_x, dtype=complex)
        
        # Sum contributions from all elements
        for i in range(self.num_elements):
            # Distance from element i to each grid point
            r = np.sqrt((grid_x - self.x_coords[i])**2 + (grid_y - self.y_coords[i])**2)
            
            # Avoid division by zero
            r = np.maximum(r, 1e-10)
            
            # Amplitude decays as 1/r, phase includes k*r and element phase
            amplitude = 1.0 / r
            phase = self.k * r + self.phases[i]
            
            # Add contribution from this element
            field += amplitude * np.exp(1j * phase)
        
        return field

