from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# --- Custom Styles ---
# Defines the neon teal color and card borders to match your design
NEON_TEAL = "#ffffff"  # Approximate color from your image
DARK_BG = "#1e1e1e"

card_style = {
    "border": f"2px solid {NEON_TEAL}",
    "borderRadius": "15px",
    "backgroundColor": "transparent",
    "marginBottom": "15px",
    "padding": "10px"
}

label_style = {
    "color": NEON_TEAL,
    "fontWeight": "bold",
    "marginBottom": "3px",
    "fontSize": "13px"
}

# --- Helper Functions for Placeholder Graphs ---
def get_empty_map_figure():
    """Returns a placeholder figure for the Heatmap (Constructive/Destructive Map)"""
    fig = go.Figure()
    fig.update_layout(
        title="Constructive/Destructive Map",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis={"visible": True, "showgrid": False},
        yaxis={"visible": True, "showgrid": False},
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

def get_empty_polar_figure():
    """Returns a placeholder figure for the Beam Profile"""
    fig = go.Figure()
    fig.update_layout(
        title="Beam Profile Viewer",
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            radialaxis=dict(visible=True, showline=False),
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig


# --- Layout Components ---

def create_sidebar():
    """Creates the left sidebar with all controls"""
    return html.Div([

        # CARD 1: Beamforming Parameters
        html.Div([
            html.H5("Beamforming Parameters", style={
                "color": NEON_TEAL,
                "textAlign": "center",
                "marginTop": "-22px",
                "backgroundColor": "#060606",
                "width": "fit-content",
                "margin": "-10px auto 8px auto",
                "padding": "0 10px",
                "fontSize": "15px"
            }),

            # Number of Transmitters Dropdown (moved to top)
            html.Label("Transmitters Number:", style=label_style),
            dcc.Dropdown(
                id='num-transmitters-dropdown',
                options=[{'label': str(i), 'value': i} for i in range(1, 17)],
                value=2,
                style={'color': 'black', 'fontSize': '13px'}
            ),
            html.Div(style={"marginBottom": "15px"}),

            # Dynamic Frequency Sliders Container
            html.Div(id='frequency-sliders-container'),

            # Phase Shift Slider
            html.Label("Phase Shift (°):", style=label_style),
            dcc.Slider(
                id='phase-slider',
                min=-180, max=180, step=1, value=0,
                tooltip={"placement": "bottom", "always_visible": True},
                marks=None
            ),
            html.Div(style={"marginBottom": "12px"}),

            # Transmitter Position Slider
            html.Label("Transmitter Position:", style=label_style),
            dcc.Slider(
                id='pos-slider',
                min=0, max=1, step=0.01, value=0.10,
                tooltip={"placement": "bottom", "always_visible": True},
                marks=None
            ),
            html.Div(style={"marginBottom": "12px"}),

            # Curvature Slider
            html.Label("Curvature:", style=label_style),
            dcc.Slider(
                id='curve-slider',
                min=-1, max=1, step=0.1, value=0.0,
                tooltip={"placement": "bottom", "always_visible": True},
                marks=None
            ),
            html.Div(style={"marginBottom": "8px"}),

        ], style=card_style),

        # CARD 2: Scenario Selection
        html.Div([
            html.H5("Scenario", style={
                "color": NEON_TEAL,
                "textAlign": "center",
                "marginTop": "-22px",
                "backgroundColor": "#060606",
                "width": "fit-content",
                "margin": "-10px auto 8px auto",
                "padding": "0 10px",
                "fontSize": "15px"
            }),
            html.Label("Select Scenario:", style=label_style),
            dcc.Dropdown(
                id='scenario-dropdown',
                options=[
                    {'label': 'Default Mode', 'value': 'default'},
                    {'label': '5G Beam Steering', 'value': '5g'},
                    {'label': 'Ultrasound Focus', 'value': 'ultrasound'},
                    {'label': 'Tumor Ablation', 'value': 'ablation'}
                ],
                value='default',
                style={'color': 'black', 'fontSize': '13px'}
            )
        ], style=card_style),

    ], style={"padding": "15px"})


def create_graphs_area():
    """Creates the right side with graphs"""
    return html.Div([
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='map-graph',
                    figure=get_empty_map_figure(),
                    style={'height': '45vh'}
                )
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='beam-profile-graph',
                    figure=get_empty_polar_figure(),
                    style={'height': '45vh'}
                )
            ], width=12)
        ])
    ], style={"padding": "20px"})


def create_layout():
    """Main layout function that combines all components"""
    return dbc.Container([
        dbc.Row([
            # Left Sidebar (Takes up 3 out of 12 columns)
            dbc.Col(create_sidebar(), width=3, style={
                "backgroundColor": "#060606",
                "minHeight": "100vh"
            }),

            # Right Graphs (Takes up 9 out of 12 columns)
            dbc.Col(create_graphs_area(), width=9, style={
                "backgroundColor": "#121212"
            })
        ], className="g-0")  # g-0 removes default gutters/spacing between cols
    ], fluid=True, style={"padding": "0px"})