"""
BeamformingApp Class - Main Application

The View layer only handles UI events.
It delegates all logic to the Controller.
"""

import dash
from dash import dcc, html, Input, Output, State
from typing import Optional
import numpy as np
import plotly.graph_objects as go

from .system_controller import SystemController
from .visualizer import Visualizer
from .scenario_loader import ScenarioLoader


class BeamformingApp:
    """
    Main application class for the Beamforming Simulator.
    The View layer only handles UI events.
    It delegates all logic to the Controller.
    """

    def __init__(self):
        """Initialize the BeamformingApp."""
        self.app = dash.Dash(__name__)
        self.controller: Optional[SystemController] = None
        self.visualizer = Visualizer()
        
        self.init_layout()
        self.register_callbacks()

    def init_layout(self):
        """Initialize the Dash app layout."""
        self.app.layout = html.Div([
            html.H1("2-D Beamforming Simulator", style={'textAlign': 'center'}),
            
            html.Div([
                html.Div([
                    html.H3("Scenarios"),
                    dcc.Dropdown(
                        id='scenario-selector',
                        options=[
                            {'label': '5G Scenario', 'value': '5g'},
                            {'label': 'Tumor Ablation Scenario', 'value': 'tumor'},
                            {'label': 'Ultrasound Scenario', 'value': 'ultrasound'},
                        ],
                        value='5g',
                        clearable=False
                    ),
                    html.Button('Load Scenario', id='load-scenario-btn', n_clicks=0),
                ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
                
                html.Div([
                    html.H3("Array Controls"),
                    html.Div(id='array-controls-container'),
                ], style={'width': '65%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),
            ]),
            
            html.Div([
                dcc.Graph(id='interference-map'),
            ], style={'width': '100%', 'padding': '10px'}),
            
            html.Div([
                dcc.Graph(id='geometry-plot'),
            ], style={'width': '100%', 'padding': '10px'}),
            
            html.Div([
                dcc.Graph(id='beam-profile'),
            ], style={'width': '100%', 'padding': '10px'}),
        ])

    def register_callbacks(self):
        """Register Dash callbacks for UI interactions."""
        
        @self.app.callback(
            [Output('interference-map', 'figure'),
             Output('geometry-plot', 'figure'),
             Output('beam-profile', 'figure'),
             Output('array-controls-container', 'children')],
            [Input('load-scenario-btn', 'n_clicks'),
             Input('scenario-selector', 'value')],
            prevent_initial_call=True
        )
        def load_scenario(n_clicks, scenario_value):
            """Load a scenario and update visualizations."""
            if scenario_value == '5g':
                self.controller = ScenarioLoader.load_5g_scenario()
            elif scenario_value == 'tumor':
                self.controller = ScenarioLoader.load_tumor_ablation_scenario()
            elif scenario_value == 'ultrasound':
                self.controller = ScenarioLoader.load_ultrasound_scenario()
            else:
                return {}, {}, {}, html.Div()
            
            return self._update_visualizations()
        
        @self.app.callback(
            [Output('interference-map', 'figure', allow_duplicate=True),
             Output('geometry-plot', 'figure', allow_duplicate=True),
             Output('beam-profile', 'figure', allow_duplicate=True)],
            [Input('steer-angle', 'value')],
            prevent_initial_call=True
        )
        def update_steering(angle):
            """Update visualizations when steering angle changes."""
            if self.controller and self.controller.arrays:
                # Update steering for first array (assuming single array scenarios)
                self.controller.arrays[0].steer_beam(angle)
            
            return self._update_visualizations()
        
        # Add more callbacks for array parameter updates as needed

    def _update_visualizations(self):
        """Update all visualizations based on current controller state."""
        if not self.controller:
            empty_fig = go.Figure()
            return empty_fig, empty_fig, empty_fig, html.Div()
        
        # Calculate total field
        field_magnitude = self.controller.calculate_total_field()
        
        # Create interference map
        interference_fig = self.visualizer.plot_constructive_map(
            field_magnitude,
            self.controller.grid_x,
            self.controller.grid_y
        )
        
        # Create geometry plot
        geometry_fig = self.visualizer.plot_geometry(
            self.controller.arrays,
            self.controller.grid_x,
            self.controller.grid_y
        )
        
        # Create beam profile (horizontal slice through center)
        center_y = self.controller.grid_y.shape[0] // 2
        x1, y1 = self.controller.grid_x[0, 0], self.controller.grid_y[center_y, 0]
        x2, y2 = self.controller.grid_x[0, -1], self.controller.grid_y[center_y, -1]
        
        try:
            profile_fig = self.visualizer.plot_beam_profile(
                field_magnitude,
                ((x1, y1), (x2, y2)),
                self.controller.grid_x,
                self.controller.grid_y
            )
        except:
            # Fallback if scipy is not available
            profile_fig = go.Figure()
            profile_fig.update_layout(title="Beam Profile (requires scipy)")
        
        # Create array controls
        controls = html.Div([
            html.Div([
                html.Label(f'Steering Angle (degrees): '),
                dcc.Slider(
                    id='steer-angle',
                    min=-90,
                    max=90,
                    step=1,
                    value=0,
                    marks={i: str(i) for i in range(-90, 91, 30)},
                ),
            ]) if len(self.controller.arrays) > 0 and self.controller.arrays[0].curvature == 0 else html.Div(),
        ])
        
        return interference_fig, geometry_fig, profile_fig, controls

    def run(self, debug: bool = True, host: str = '127.0.0.1', port: int = 8050):
        """
        Run the Dash application.

        Args:
            debug: Enable debug mode
            host: Host address
            port: Port number
        """
        self.app.run_server(debug=debug, host=host, port=port)


if __name__ == '__main__':
    app = BeamformingApp()
    app.run()

