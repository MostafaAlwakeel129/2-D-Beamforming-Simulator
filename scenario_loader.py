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
            'focus_x': 0.0,          # Ignored in 5G mode
            'focus_y': 0.5,
            'default_freq': 5.0
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
            'num_elements': 16,
            'curvature': 2.0,
            'spacing_unit': 'lambda',
            'spacing_val': 0.5,
            'steer_angle': 0.0,
            'focus_x': 0.0,
            'focus_y': 5.0,
            'default_freq': 1.0
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
            'num_elements': 16,
            'curvature': 0.0,
            'spacing_unit': 'lambda',
            'spacing_val': 0.5,
            'steer_angle': 0.0,
            'focus_x': 0.0,
            'focus_y': 2.0,
            'default_freq': 2.5
        }