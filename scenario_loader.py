"""
ScenarioLoader Class - Factory for Scenarios

Satisfies "Equip simulator with at least three scenarios"
Compatible with Single-Array SystemController
"""

from system_controller import SystemController
import numpy as np

class ScenarioLoader:
    """
    RESPONSIBILITY: Factory for Scenarios
    Satisfies "Equip simulator with at least three scenarios"
    """

    @staticmethod
    def load_5g_scenario() -> SystemController:
        """
        SCENARIO 1: 5G Beamforming (Far-Field)
        - High Frequency (28 GHz mmWave)
        - Linear Array (Curvature 0)
        - Steered Beam (Directional communication)
        """
        controller = SystemController(resolution=200)
        
        # Configure the single array for 5G
        controller.update_parameters({
            'frequency': 28e9,       # 28 GHz
            'num_elements': 16,      # Standard small cell array
            'spacing': 0.5,          # Half-wavelength
            'curvature': 0.0,        # Linear
            'steer_angle': 30.0      # Steer 30 degrees to the right
        })
        
        return controller

    @staticmethod
    def load_tumor_ablation_scenario() -> SystemController:
        """
        SCENARIO 2: Tumor Ablation / HIFU (Near-Field)
        - Low Frequency (1 MHz) for deep penetration
        - Highly Curved Array (HIFU Transducer)
        - Focused Beam (Converges on a specific point)
        """
        controller = SystemController(resolution=200)
        
        # Configure for Focused Ultrasound
        # We use a highly curved array (Arc) to create a natural geometric focus
        controller.update_parameters({
            'frequency': 1e6,        # 1 MHz
            'num_elements': 32,      # More elements for better focusing energy
            'spacing': 0.5,
            'curvature': 2.0,        # Radius = 0.5m (Significant curve)
            
            # Focus at a point 40cm in front of the array (0, 0.4)
            # Since the array is centered at (0,0), this shoots "up/forward"
            'focus_target': (0.0, 0.4) 
        })
        
        return controller

    @staticmethod
    def load_ultrasound_scenario() -> SystemController:
        """
        SCENARIO 3: Medical Imaging (Linear Probe)
        - Medium Frequency (5 MHz)
        - Linear Array (Standard handheld probe)
        - Broadside Beam (Scanning straight ahead)
        """
        controller = SystemController(resolution=200)
        
        # Configure for Standard Diagnostic Ultrasound
        controller.update_parameters({
            'frequency': 5e6,        # 5 MHz
            'num_elements': 64,      # High density for imaging
            'spacing': 0.5,
            'curvature': 0.0,        # Flat linear probe
            'steer_angle': 0.0       # Look straight ahead
        })
        
        return controller