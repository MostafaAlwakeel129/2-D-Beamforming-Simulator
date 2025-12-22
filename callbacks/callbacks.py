from dash import Input, Output, ALL, html, dcc
import numpy as np
from system_controller import SystemController
from visualizer import Visualizer
from scenario_loader import ScenarioLoader

controller = SystemController(resolution=200)


def register_callbacks(app):
    # 1. FREQUENCY SLIDERS (Dynamic Generation)
    @app.callback(
        Output('frequency-sliders-container', 'children'),
        [Input('num-elements-slider', 'value'),
         Input('scenario-dropdown', 'value')]
    )
    def update_frequency_inputs(num, scenario):
        # Determine default freq based on scenario

        if scenario == '5g':
            default_val = ScenarioLoader.get_5g_scenario()['default_freq']
        elif scenario == 'tumor' :
            default_val = ScenarioLoader.get_tumor_ablation_scenario()['default_freq']
        elif scenario == 'ultrasound':
            default_val = ScenarioLoader.get_ultrasound_scenario()['default_freq']

        return [html.Div([
            html.Label(f"Elem {i + 1}",
                       style={"fontSize": "10px", "color": "#aaa", "width": "45px", "display": "inline-block"}),
            html.Div([
                dcc.Slider(
                    id={'type': 'freq-slider', 'index': i},
                    min=0.5, max=5.0, step=0.1, value=default_val,
                    marks={0.5: '0.5', 5: '5'},
                    tooltip={"placement": "right", "always_visible": False}
                )
            ], style={"width": "calc(100% - 55px)", "display": "inline-block", "verticalAlign": "middle"})
        ], style={"marginBottom": "8px"}) for i in range(num)]

    # 2. SCENARIO UI MANAGER
    @app.callback(
        [Output('focus-controls', 'style'),
         Output('num-elements-slider', 'value'),
         Output('curvature-slider', 'value'),
         Output('spacing-unit-radio', 'value'),
         Output('spacing-slider', 'value'),
         Output('steer-angle-slider', 'value'),
         Output('focus-x-slider', 'value'),
         Output('focus-y-slider', 'value')],
        Input('scenario-dropdown', 'value')
    )
    def update_scenario_ui(scenario):
        # 1. Fetch parameters dictionary
        if scenario == '5g':
            params = ScenarioLoader.get_5g_scenario()
            style = {'display': 'none'}
        elif scenario == 'tumor':
            params = ScenarioLoader.get_tumor_ablation_scenario()
            style = {'display': 'block'}
        else:  # ultrasound
            params = ScenarioLoader.get_ultrasound_scenario()
            style = {'display': 'block'}

        # 2. Return values in order of Outputs
        return (
            style,
            params['num_elements'],
            params['curvature'],
            params['spacing_unit'],
            params['spacing_val'],
            params['steer_angle'],
            params['focus_x'],
            params['focus_y']
        )

    # 3. SPACING SLIDER RANGE UPDATE
    @app.callback(
        [Output('spacing-slider', 'min'),
         Output('spacing-slider', 'max'),
         Output('spacing-slider', 'value',allow_duplicate=True),
         Output('spacing-slider', 'step'),
         Output('spacing-slider', 'marks')],
        Input('spacing-unit-radio', 'value'),
        prevent_initial_call = True
    )
    def update_spacing_range(unit):
        if unit == 'meter':
            # Range: 1cm to 50cm, Step: 1cm, Default: 15cm
            return 0.01, 0.5, 0.15, 0.01, {0.01: '0.01', 0.5: '0.5'}
        else:
            # Range: 0.1 to 2.0 lambda, Step: 0.1, Default: 0.5
            return 0.1, 2.0, 0.5, 0.1, {0.1: '0.1', 2: '2.0'}

    # 4. MAIN UPDATE LOOP
    @app.callback(
        [Output('interference-map', 'figure'), Output('beam-profile', 'figure')],
        [Input('num-elements-slider', 'value'),
         Input('curvature-slider', 'value'),
         Input('spacing-slider', 'value'),
         Input('spacing-unit-radio', 'value'),
         Input('steer-angle-slider', 'value'),
         Input('focus-x-slider', 'value'),
         Input('focus-y-slider', 'value'),
         Input({'type': 'freq-slider', 'index': ALL}, 'value'),
         Input('scenario-dropdown', 'value')]
    )
    def update_graphs(num, curv, space_val, space_unit, angle, fx, fy, freqs, scenario):

        freq_array = np.array(freqs) * 1e9 if freqs else np.ones(num) * 1e9

        # Fetch hidden physics parameters based on scenario
        if scenario == '5g':
            physics_params = ScenarioLoader.get_5g_scenario()
        elif scenario == 'tumor':
            physics_params = ScenarioLoader.get_tumor_ablation_scenario()
        else:
            physics_params = ScenarioLoader.get_ultrasound_scenario()

        params = {
            'num_elements': num,
            'curvature': curv,
            'spacing_val': space_val,
            'spacing_unit': space_unit,
            'frequencies': freq_array,
            'steer_angle': angle,
            # Add Physics Parameters
            'wave_speed': physics_params['wave_speed'],
            'grid_width': physics_params.get('grid_width', 20.0),
            'grid_depth': physics_params.get('grid_depth', 20.0)
        }

        if scenario != '5g':
            params['focus_target'] = (fx, fy)
        else:
            params['focus_target'] = None

        controller.update_parameters(params)

        field_mag = controller.calculate_total_field()

        fig_map = Visualizer.plot_heatmap(field_mag, controller.grid_x, controller.grid_y, controller.array)

        angles = np.linspace(-90, 90, 361)
        profile = controller.array.calculate_azimuth_profile(angles)
        fig_profile = Visualizer.plot_polar_beam_profile(angles, profile)

        return fig_map, fig_profile