class ScenarioLoader:
    """
    RESPONSIBILITY: Data Factory for Scenarios
    Returns dictionary of parameters to update UI sliders.
    """

    @staticmethod
    def get_5g_scenario():
        """
        SCENARIO 1: 5G Beamforming (Far-Field)
        - 28 GHz (High Freq)
        - 16 Elements
        - Steered to 30 degrees
        """
        return {
            'num_elements': 16,
            'curvature': 0.0,
            'spacing_unit': 'lambda',
            'spacing_val': 0.5,
            'steer_angle': 30.0,
            'focus_x': 0.0,  # Ignored in 5G mode
            'focus_y': 0.5,
            'default_freq': 5.0,
            'wave_speed': 3e8,
            'grid_width': 20.0,  # 20 Meters wide
            'grid_depth': 20.0  # 20 Meters deep
        }

    @staticmethod
    def get_tumor_ablation_scenario():
        """
        SCENARIO 2: Tumor Ablation / HIFU (Near-Field)
        - 1 MHz (Low Freq)
        - Curved Array (Focused physically)
        - Focused electronically at (0, 5)
        """
        return {
            'num_elements': 32,
            'curvature': 2.0,
            'spacing_unit': 'lambda',
            'spacing_val': 0.5,
            'steer_angle': 0.0,
            'focus_x': 0.0,
            'focus_y': 0.12,  # Focus at 12cm depth
            'default_freq': 1.0,
            'wave_speed': 1540,
            'grid_width': 0.30,  # 30 cm wide
            'grid_depth': 0.30  # 30 cm deep
        }

    @staticmethod
    def get_ultrasound_scenario():
        """
        SCENARIO 3: Medical Imaging (Linear Probe)
        - 5 MHz
        - Flat Array
        - Scanning straight ahead
        """
        return {
            'num_elements': 64,
            'curvature': 0.0,
            'spacing_unit': 'lambda',
            'spacing_val': 0.5,
            'steer_angle': 0.0,
            'focus_x': 0.0,
            'focus_y': 0.10,  # Focus at 10cm
            'default_freq': 2.5,
            'wave_speed': 1540,
            'grid_width': 0.20,  # 20 cm wide
            'grid_depth': 0.20  # 20 cm deep
        }