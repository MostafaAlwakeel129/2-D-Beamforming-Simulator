"""
AntennaElement class - Represents an individual antenna element within a phased array.
"""

import numpy as np
from typing import Tuple


class AntennaElement:
    """
    Represents an individual antenna element within a phased array.
    
    Attributes:
        x_position (float): X coordinate of the antenna element
        y_position (float): Y coordinate of the antenna element
        frequency (float): Operating frequency of the antenna element
        phase_shift (float): Phase shift applied to the antenna element
    """
    
    def __init__(self, x_position: float, y_position: float, frequency: float, phase_shift: float = 0.0):
        """
        Initialize an antenna element.
        
        Args:
            x_position: X coordinate of the antenna element
            y_position: Y coordinate of the antenna element
            frequency: Operating frequency of the antenna element
            phase_shift: Initial phase shift (default: 0.0)
        """
        self.x_position = x_position
        self.y_position = y_position
        self.frequency = frequency
        self.phase_shift = phase_shift
    
    def set_frequency(self, freq: float) -> None:
        """
        Set the operating frequency of the antenna element.
        
        Args:
            freq: New frequency value
        """
        self.frequency = freq
    
    def set_phase(self, phi: float) -> None:
        """
        Set the phase shift of the antenna element.
        
        Args:
            phi: New phase shift value (in radians or degrees, depending on implementation)
        """
        self.phase_shift = phi
    
    def compute_field_contribution(self, grid_x: np.ndarray, grid_y: np.ndarray) -> np.ndarray:
        """
        Compute the field contribution of this antenna element at each point in the grid.
        
        Args:
            grid_x: X coordinates of the evaluation grid (Matrix)
            grid_y: Y coordinates of the evaluation grid (Matrix)
            
        Returns:
            ComplexMatrix: Complex field values at each grid point
        """
        # Calculate distances from antenna element to each grid point
        dx = grid_x - self.x_position
        dy = grid_y - self.y_position
        distances = np.sqrt(dx**2 + dy**2)
        
        # Avoid division by zero
        distances = np.where(distances == 0, 1e-10, distances)
        
        # Compute field contribution (simplified model)
        # This is a placeholder - actual implementation would use proper antenna radiation pattern
        wavelength = 1.0 / self.frequency if self.frequency > 0 else 1.0
        k = 2 * np.pi / wavelength  # Wave number
        
        # Spherical wave propagation with phase
        amplitude = 1.0 / distances  # Decay with distance
        phase = k * distances + self.phase_shift
        
        # Return complex field
        field = amplitude * np.exp(1j * phase)
        
        return field

