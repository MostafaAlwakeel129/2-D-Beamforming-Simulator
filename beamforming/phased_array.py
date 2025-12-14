"""
PhasedArray class - Represents a single phased array, composed of multiple antenna elements.
"""

import numpy as np
from typing import List
from .antenna_element import AntennaElement


class PhasedArray:
    """
    Represents a single phased array, composed of multiple antenna elements.
    
    Attributes:
        id (int): Unique identifier for the phased array
        elements (List[AntennaElement]): List of antenna elements in the array
        curvature_type (str): Type of curvature applied to the array
    """
    
    def __init__(self, array_id: int, curvature_type: str = "linear"):
        """
        Initialize a phased array.
        
        Args:
            array_id: Unique identifier for the phased array
            curvature_type: Type of curvature (e.g., "linear", "circular", "convex", "concave")
        """
        self.id = array_id
        self.elements: List[AntennaElement] = []
        self.curvature_type = curvature_type
    
    def add_element(self, x: float, y: float, freq: float) -> None:
        """
        Add an antenna element to the phased array.
        
        Args:
            x: X coordinate of the element
            y: Y coordinate of the element
            freq: Operating frequency of the element
        """
        element = AntennaElement(x, y, freq)
        self.elements.append(element)
    
    def steer_beam(self, angle: float) -> None:
        """
        Steer the beam by adjusting phase shifts of all elements.
        
        Args:
            angle: Steering angle (in radians or degrees, depending on implementation)
        """
        # Calculate phase shifts for beam steering
        # This is a simplified implementation
        wavelength = 1.0 / self.elements[0].frequency if self.elements else 1.0
        k = 2 * np.pi / wavelength
        
        for i, element in enumerate(self.elements):
            # Calculate phase shift based on element position and steering angle
            # This is a simplified model - actual implementation would consider array geometry
            phase_shift = k * (element.x_position * np.cos(angle) + element.y_position * np.sin(angle))
            element.set_phase(phase_shift)
    
    def get_total_field(self, grid_x: np.ndarray, grid_y: np.ndarray) -> np.ndarray:
        """
        Calculate the total field contribution from all elements in the array.
        
        Args:
            grid_x: X coordinates of the evaluation grid (Matrix)
            grid_y: Y coordinates of the evaluation grid (Matrix)
            
        Returns:
            ComplexMatrix: Total complex field from all elements
        """
        if not self.elements:
            return np.zeros_like(grid_x, dtype=complex)
        
        # Sum contributions from all elements
        total_field = np.zeros_like(grid_x, dtype=complex)
        for element in self.elements:
            total_field += element.compute_field_contribution(grid_x, grid_y)
        
        return total_field
