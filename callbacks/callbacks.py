# from dash import Input, Output, html, dcc
# from dash.exceptions import PreventUpdate
#
# # Styles for consistency
# NEON_TEAL = "#ffffff"
#
# label_style = {
#     "color": NEON_TEAL,
#     "fontWeight": "bold",
#     "marginBottom": "3px",
#     "fontSize": "13px"
# }
#
#
# def register_callbacks(app):
#     """Register all callbacks for the application"""
#
#     @app.callback(
#         Output('frequency-sliders-container', 'children'),
#         Input('num-transmitters-dropdown', 'value')
#     )
#     def update_frequency_sliders(num_transmitters):
#         """
#         Dynamically generate frequency sliders based on number of transmitters
#
#         Args:
#             num_transmitters: Number of transmitters selected
#
#         Returns:
#             List of Div elements containing frequency sliders
#         """
#         if num_transmitters is None:
#             raise PreventUpdate
#
#         sliders = []
#
#         for i in range(num_transmitters):
#             slider_div = html.Div([
#                 html.Label(f"Transmitter Frequency-{i+1}", style=label_style),
#                 dcc.Slider(
#                     id={'type': 'freq-slider', 'index': i},
#                     min=100,
#                     max=1000,
#                     step=10,
#                     value=500,
#                     tooltip={"placement": "bottom", "always_visible": True},
#                     marks=None
#                 ),
#                 html.Div(style={"marginBottom": "12px"})
#             ])
#             sliders.append(slider_div)
#
#         return sliders

from dash import Input, Output, ALL, html, dcc
import numpy as np
from system_controller import SystemController
from visualizer import Visualizer

controller = SystemController(resolution=1000)


def register_callbacks(app):
    # 1. FREQUENCY SLIDERS
    @app.callback(Output('frequency-sliders-container', 'children'), Input('num-elements-slider', 'value'))
    def update_frequency_inputs(num):
        return [html.Div([
            html.Label(f"Elem {i + 1}",
                       style={"fontSize": "10px", "color": "#aaa", "width": "45px", "display": "inline-block"}),
            html.Div([
                dcc.Slider(
                    id={'type': 'freq-slider', 'index': i},
                    min=0.5, max=5.0, step=0.1, value=1.0,
                    marks={0.5: '0.5', 5: '5'},
                    tooltip={"placement": "right", "always_visible": False}
                )
            ], style={"width": "calc(100% - 55px)", "display": "inline-block", "verticalAlign": "middle"})
        ], style={"marginBottom": "8px"}) for i in range(num)]

    # 2. SCENARIO UI MANAGER
    @app.callback(
        [Output('focus-controls', 'style'), Output('curvature-slider', 'value'), Output('steer-angle-slider', 'value')],
        Input('scenario-dropdown', 'value')
    )
    def update_scenario_ui(scenario):
        if scenario == '5g':
            return {'display': 'none'}, 0.0, 30.0
        elif scenario == 'tumor':
            return {'display': 'block'}, 2.0, 0.0
        else:
            return {'display': 'block'}, 0.0, 0.0

    # 3. SPACING SLIDER RANGE UPDATE (Fixes the "Corruption")
    @app.callback(
        [Output('spacing-slider', 'min'),
         Output('spacing-slider', 'max'),
         Output('spacing-slider', 'value'),
         Output('spacing-slider', 'step'),
         Output('spacing-slider', 'marks')],  # <--- Crucial Fix: Updates step precision
        Input('spacing-unit-radio', 'value')
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

        params = {
            'num_elements': num,
            'curvature': curv,
            'spacing_val': space_val,
            'spacing_unit': space_unit,
            'frequencies': freq_array,
            'steer_angle': angle
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