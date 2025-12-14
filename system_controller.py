"""
SystemController class - Manages the phased arrays and overall system logic.
"""

import numpy as np
from typing import List
from .phased_array import PhasedArray


class SystemController:
    """
    Manages the phased arrays and overall system logic.
    
    Attributes:
        arrays (List[PhasedArray]): List of phased arrays in the system
        grid_x (np.ndarray): X coordinates of the evaluation grid (Matrix)
        grid_y (np.ndarray): Y coordinates of the evaluation grid (Matrix)
    """
    
    def __init__(self, grid_x: np.ndarray = None, grid_y: np.ndarray = None):
        """
        Initialize the system controller.
        
        Args:
            grid_x: X coordinates of the evaluation grid (optional, can be set later)
            grid_y: Y coordinates of the evaluation grid (optional, can be set later)
        """
        self.arrays: List[PhasedArray] = []
        self.grid_x = grid_x if grid_x is not None else np.array([])
        self.grid_y = grid_y if grid_y is not None else np.array([])
    
    def create_array_unit(self, param_dict: dict) -> PhasedArray:
        """
        Create a new phased array unit based on parameters.
        
        Args:
            param_dict: Dictionary containing parameters for array creation
                - 'id': Array identifier
                - 'curvature_type': Type of curvature
                - 'elements': List of element parameters (x, y, freq)
                - Other array-specific parameters
        
        Returns:
            PhasedArray: The newly created phased array
        """
        array_id = param_dict.get('id', len(self.arrays))
        curvature_type = param_dict.get('curvature_type', 'linear')
        
        array = PhasedArray(array_id, curvature_type)
        
        # Add elements if provided
        elements = param_dict.get('elements', [])
        for elem_params in elements:
            x = elem_params.get('x', 0.0)
            y = elem_params.get('y', 0.0)
            freq = elem_params.get('freq', 500.0)
            array.add_element(x, y, freq)
        
        self.arrays.append(array)
        return array
    
    def update_element_frequency(self, array_id: int, element_id: int, freq: float) -> None:
        """
        Update the frequency of a specific element in a specific array.
        
        Args:
            array_id: Identifier of the array
            element_id: Index of the element within the array
            freq: New frequency value
        """
        if 0 <= array_id < len(self.arrays):
            array = self.arrays[array_id]
            if 0 <= element_id < len(array.elements):
                array.elements[element_id].set_frequency(freq)
    
    def calculate_total_interference(self) -> np.ndarray:
        """
        Calculate the total interference pattern from all arrays.
        
        Returns:
            Matrix: Total interference pattern (magnitude of combined fields)
        """
        if not self.arrays or self.grid_x.size == 0:
            return np.array([])
        
        # Sum fields from all arrays
        total_field = np.zeros_like(self.grid_x, dtype=complex)
        for array in self.arrays:
            total_field += array.get_total_field(self.grid_x, self.grid_y)
        
        # Return magnitude (interference pattern)
        return np.abs(total_field)

