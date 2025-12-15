"""
SystemController class - Manages the phased arrays and overall system logic.
"""

import numpy as np
from typing import List, Tuple, Optional
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

    # ==================== PRIVATE HELPERS ====================

    def _is_valid_array_id(self, array_id: int) -> bool:
        """Check if array_id is valid."""
        return 0 <= array_id < len(self.arrays)

    def _is_valid_element_id(self, array_id: int, element_id: int) -> bool:
        """Check if array_id and element_id are both valid."""
        if not self._is_valid_array_id(array_id):
            return False
        return 0 <= element_id < len(self.arrays[array_id].elements)

    def _get_array_settings(self, array: PhasedArray) -> Optional[Tuple[int, float, float]]:
        """
        Extract current settings from an array.

        Args:
            array: The phased array to extract settings from.

        Returns:
            Tuple of (num_elements, frequency, spacing) or None if array is empty.
        """
        if not array.elements:
            return None

        num_elements = len(array.elements)
        frequency = array.elements[0].frequency

        # Calculate spacing from first two elements
        if num_elements >= 2:
            dx = array.elements[1].x_position - array.elements[0].x_position
            dy = array.elements[1].y_position - array.elements[0].y_position
            spacing = np.sqrt(dx**2 + dy**2)
        else:
            spacing = 0.005

        return (num_elements, frequency, spacing)

    # ==================== ARRAY MANAGEMENT ====================

    def create_array_unit(self, param_dict: dict) -> PhasedArray:
        """
        Create a new phased array with auto-generated element positions.

        Args:
            param_dict: Dictionary with keys:
                - 'id': Array identifier (optional)
                - 'curvature_type': "linear", "convex", "concave" (default: "linear")
                - 'num_elements': Number of elements (default: 8)
                - 'frequency': Frequency in Hz (default: 500.0)
                - 'spacing': Element spacing in meters (default: 0.005)
                - 'curvature_params': {'radius': float} for curved arrays (optional)

        Returns:
            PhasedArray: The created phased array.
        """
        array_id = param_dict.get('id', len(self.arrays))
        curvature_type = param_dict.get('curvature_type', 'linear')

        array = PhasedArray(array_id, curvature_type)

        array.set_geometry(
            curvature_type=curvature_type,
            num_elements=param_dict.get('num_elements', 8),
            frequency=param_dict.get('frequency', 500.0),
            spacing=param_dict.get('spacing', 0.005),
            curvature_params=param_dict.get('curvature_params', {})
        )

        self.arrays.append(array)
        return array

    def remove_array(self, array_id: int):
        """Remove an array by index."""
        if self._is_valid_array_id(array_id):
            self.arrays.pop(array_id)
            # Re-index remaining arrays
            for i, arr in enumerate(self.arrays):
                arr.id = i

    def clear_all_arrays(self) -> None:
        """Remove all arrays."""
        self.arrays.clear()

    # ==================== ELEMENT COUNT ====================

    def add_element_to_array(self, array_id: int) -> bool:
        """
        Add one element to an existing array.

        Increases element count by 1 and regenerates positions
        based on current geometry settings.

        Args:
            array_id: Index of the array.

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._is_valid_array_id(array_id):
            return False

        array = self.arrays[array_id]
        settings = self._get_array_settings(array)

        if settings is None:
            return False

        num_elements, frequency, spacing = settings

        array.set_geometry(
            curvature_type=array.curvature_type,
            num_elements=num_elements + 1,
            frequency=frequency,
            spacing=spacing,
            curvature_params=array.curvature_params
        )

        return True

    def set_array_element_count(self, array_id: int, num_elements: int) -> bool:
        """
        Set the number of elements in an array.

        Regenerates positions based on current geometry.

        Args:
            array_id: Index of the array.
            num_elements: New number of elements (minimum 1).

        Returns:
            bool: True if successful, False otherwise.
        """
        if not self._is_valid_array_id(array_id):
            return False

        if num_elements < 1:
            return False

        array = self.arrays[array_id]
        settings = self._get_array_settings(array)

        if settings is None:
            return False

        _, frequency, spacing = settings

        array.set_geometry(
            curvature_type=array.curvature_type,
            num_elements=num_elements,
            frequency=frequency,
            spacing=spacing,
            curvature_params=array.curvature_params
        )

        return True

    # ==================== GEOMETRY ====================

    def update_array_curvature(self, array_id: int, curvature_type: str,
                               curvature_params: dict = None) -> bool:
        """
        Update the curvature/geometry of an array.
        Preserves number of elements and frequency.

        Args:
            array_id: Index of the array to update
            curvature_type: "linear", "convex", or "concave"
            curvature_params: {'radius': float} for curved arrays

        Returns:
            bool: True if successful, False otherwise
        """
        if not self._is_valid_array_id(array_id):
            return False

        array = self.arrays[array_id]
        settings = self._get_array_settings(array)

        if settings is None:
            return False

        num_elements, frequency, spacing = settings

        array.set_geometry(
            curvature_type=curvature_type,
            num_elements=num_elements,
            frequency=frequency,
            spacing=spacing,
            curvature_params=curvature_params
        )

        return True

    # ==================== STEERING ====================

    def steer_array_beam(self, array_id: int, angle: float) -> bool:
        """Steer a specific array's beam."""
        if self._is_valid_array_id(array_id):
            self.arrays[array_id].steer_beam(angle)
            return True
        return False

    # ==================== FREQUENCY ====================

    def update_element_frequency(self, array_id: int, element_id: int, freq: float) -> bool:
        """
        Update the frequency of a specific element in a specific array.

        Args:
            array_id: Identifier of the array
            element_id: Index of the element within the array
            freq: New frequency value
        """
        if self._is_valid_element_id(array_id, element_id):
            self.arrays[array_id].elements[element_id].set_frequency(freq)
            return True
        return False

    def update_array_frequency(self, array_id: int, frequency: float) -> bool:
        """Update frequency for all elements in an array."""
        if not self._is_valid_array_id(array_id):
            return False

        array = self.arrays[array_id]
        for element_id in range(len(array.elements)):
            self.update_element_frequency(array_id, element_id, frequency)
        return True

    # ==================== PHASE ====================

    def update_element_phase(self, array_id: int, element_id: int, phase: float) -> bool:
        """Update phase of a specific element.

        Args:
            array_id: Identifier of the array
            element_id: Index of the element within the array
            phase: New phase value
        """
        if self._is_valid_element_id(array_id, element_id):
            self.arrays[array_id].elements[element_id].set_phase(phase)
            return True
        return False

    def update_array_phases(self, array_id: int, phase: float) -> bool:
        """Update phase for all elements in an array."""
        if not self._is_valid_array_id(array_id):
            return False

        array = self.arrays[array_id]
        for element_id in range(len(array.elements)):
            self.update_element_phase(array_id, element_id, phase)
        return True

    # ==================== CALCULATIONS ====================

    def calculate_total_interference(self) -> np.ndarray:
        """
        Calculate the total interference pattern from all arrays.

        Returns:
            Matrix: Total interference pattern (magnitude of combined fields)
        """
        if not self.arrays or self.grid_x.size == 0:
            return np.array([])

        total_field = np.zeros_like(self.grid_x, dtype=complex)
        for array in self.arrays:
            total_field += array.get_total_field(self.grid_x, self.grid_y)

        return np.abs(total_field)

    def calculate_beam_profile(self, array_ids: List[int] = None,
                               distance: float = 1.0,
                               angles: np.ndarray = None) -> tuple:
        """
        Calculate beam profile (intensity vs angle) at a given distance.

        Returns:
            (angles, intensities) for polar plotting
        """
        if angles is None:
            angles = np.linspace(-np.pi/2, np.pi/2, 360)

        x_points = distance * np.sin(angles)
        y_points = distance * np.cos(angles)

        total_field = np.zeros_like(angles, dtype=complex)

        if array_ids is None:
            arrays_to_use = self.arrays
        else:
            arrays_to_use = [self.arrays[i] for i in array_ids if 0 <= i < len(self.arrays)]

        for array in arrays_to_use:
            total_field += array.get_total_field(x_points, y_points)

        return angles, np.abs(total_field)