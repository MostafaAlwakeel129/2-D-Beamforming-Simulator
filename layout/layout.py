# from dash import dcc, html
# import dash_bootstrap_components as dbc
#
# # --- THEME CONFIGURATION ---
# NEON_TEAL = "#00f2ff"
# DARK_BG = "#0f0f13"
#
# # --- UX: GLASSMORPHISM CARD STYLE ---
# GLASS_STYLE = {
#     "border": f"1px solid rgba(0, 242, 255, 0.3)",
#     "borderRadius": "12px",
#     "backgroundColor": "rgba(20, 20, 25, 0.7)",
#     "backdropFilter": "blur(10px)",
#     "boxShadow": "0 8px 32px 0 rgba(0, 0, 0, 0.37)",
#     "marginBottom": "20px",
#     "padding": "20px"
# }
#
# # --- UX: TYPOGRAPHY ---
# LABEL_STYLE = {
#     "color": "#e0e0e0",
#     "fontFamily": "'Exo 2', sans-serif",
#     "fontSize": "12px",  # Increased slightly
#     "letterSpacing": "1px",
#     "textTransform": "uppercase",
#     "marginBottom": "8px",
#     "fontWeight": "600",  # Made bolder
#     "display": "block"
# }
#
# HEADER_STYLE = {
#     "color": NEON_TEAL,
#     "fontFamily": "'Exo 2', sans-serif",
#     "textAlign": "center",
#     "letterSpacing": "3px",
#     "textShadow": f"0 0 10px {NEON_TEAL}",
#     "fontSize": "24px",
#     "fontWeight": "700",
#     "marginBottom": "20px",
#     "marginTop": "10px"
# }
#
#
# def create_sidebar():
#     return html.Div([
#         # Title Area
#         html.H2("BEAMLAB", style=HEADER_STYLE),
#         html.Hr(style={"borderColor": NEON_TEAL, "opacity": "0.5"}),
#
#         # 1. SCENARIO CARD
#         # FIX: Added zIndex and position relative so dropdown floats ABOVE other cards
#         html.Div([
#             html.Label("SCENARIO PRESET", style=LABEL_STYLE),
#             dcc.Dropdown(
#                 id='scenario-dropdown',
#                 options=[
#                     {'label': '📡 5G Beam Steering', 'value': '5g'},
#                     {'label': '🏥 Ultrasound Imaging', 'value': 'ultrasound'},
#                     {'label': '🎯 Tumor Ablation', 'value': 'tumor'}
#                 ],
#                 value='5g',
#                 clearable=False,
#                 style={
#                     'fontSize': '14px',
#                     'color': 'black',
#                     'fontFamily': "'Exo 2', sans-serif"
#                 }
#             )
#         ], style={**GLASS_STYLE, "zIndex": "10", "position": "relative"}),
#
#         # 2. ARRAY CONFIG CARD
#         html.Div([
#             html.Div([
#                 html.Label("ELEMENTS COUNT (N)", style=LABEL_STYLE),
#                 dcc.Slider(
#                     id='num-elements-slider',
#                     min=2, max=16, step=1, value=8,
#                     marks={2: '2', 8: '8', 16: '16'},
#                     tooltip={"placement": "bottom", "always_visible": False}
#                 ),
#             ], style={"marginBottom": "25px"}),
#
#             html.Div([
#                 html.Label("ARRAY CURVATURE", style=LABEL_STYLE),
#                 dcc.Slider(
#                     id='curvature-slider',
#                     min=0, max=5, step=0.1, value=0,
#                     marks={0: 'FLAT', 5: 'MAX'},
#                     tooltip={"placement": "bottom", "always_visible": False}
#                 ),
#             ], style={"marginBottom": "25px"}),
#
#             html.Hr(style={"borderColor": "#444"}),
#
#             html.Label("SPACING UNIT", style=LABEL_STYLE),
#             dcc.RadioItems(
#                 id='spacing-unit-radio',
#                 options=[
#                     {'label': ' Lambda (λ)', 'value': 'lambda'},
#                     {'label': ' Meters (m)', 'value': 'meter'}
#                 ],
#                 value='lambda',
#                 labelStyle={
#                     'display': 'inline-block',
#                     'marginRight': '20px',
#                     'color': '#bbb',
#                     'fontSize': '12px',
#                     'fontFamily': "'Exo 2', sans-serif"
#                 },
#                 inputStyle={"marginRight": "5px"}
#             ),
#
#             html.Div([
#                 html.Label("SPACING VALUE", style=LABEL_STYLE),
#                 dcc.Slider(
#                     id='spacing-slider',
#                     min=0.1, max=2.0, step=0.1, value=0.5,
#                     marks={0.1: '0.1', 2: '2.0'},
#                     tooltip={"placement": "bottom", "always_visible": False}
#                 ),
#             ], style={"marginTop": "15px"}),
#
#         ], style={**GLASS_STYLE, "zIndex": "5", "position": "relative"}),
#
#         # 3. FREQUENCIES CARD
#         html.Div([
#             html.Label("ELEMENT FREQUENCIES (GHz)", style=LABEL_STYLE),
#             html.Div(
#                 id='frequency-sliders-container',
#                 style={
#                     'maxHeight': '180px',
#                     'overflowY': 'auto',
#                     'paddingRight': '5px',
#                     'scrollbarWidth': 'thin'
#                 }
#             )
#         ], style={**GLASS_STYLE, "zIndex": "4", "position": "relative"}),
#
#         # 4. BEAM CONTROL CARD
#         html.Div([
#             html.Div([
#                 html.Label("STEERING ANGLE (°)", style=LABEL_STYLE),
#                 dcc.Slider(
#                     id='steer-angle-slider',
#                     min=-90, max=90, step=1, value=0,
#                     marks={-90: '-90', 0: '0', 90: '90'},
#                     tooltip={"placement": "bottom", "always_visible": False}
#                 ),
#             ]),
#
#             html.Div(id='focus-controls', children=[
#                 html.Hr(style={"borderColor": "#444", "marginTop": "20px"}),
#
#                 html.Label("FOCUS TARGET X (Lateral)", style=LABEL_STYLE),
#                 dcc.Slider(
#                     id='focus-x-slider', min=-1, max=1, step=0.1, value=0,
#                     marks={-1: '-1m', 0: '0', 1: '1m'},
#                     tooltip={"placement": "bottom", "always_visible": False}
#                 ),
#
#                 html.Div(style={"height": "20px"}),
#
#                 html.Label("FOCUS TARGET Y (Depth)", style=LABEL_STYLE),
#                 dcc.Slider(
#                     id='focus-y-slider', min=0, max=2, step=0.1, value=0.5,
#                     marks={0: '0m', 2: '2m'},
#                     tooltip={"placement": "bottom", "always_visible": False}
#                 ),
#             ], style={'display': 'none'})
#
#         ], style={**GLASS_STYLE, "zIndex": "3", "position": "relative"}),
#
#     ], style={
#         "padding": "25px",
#         "height": "100vh",
#         "overflowY": "auto",
#         "backgroundColor": "#050505",
#         "borderRight": "1px solid #333"
#     })
#
#
# def create_graphs_area():
#     return html.Div([
#         # Row 1: The Main Heatmap
#         dbc.Row([
#             dbc.Col([
#                 html.Div([
#                     dcc.Graph(id='interference-map', style={'height': '50vh'})  # Reduced slightly to give space
#                 ], style={"border": "1px solid #333", "borderRadius": "12px", "overflow": "hidden"})
#             ], width=12)
#         ], style={"marginBottom": "20px"}),
#
#         # Row 2: The Azimuth Beam Profile
#         dbc.Row([
#             dbc.Col([
#                 html.Div([
#                     # FIX: Increased height significantly for the Polar Plot
#                     dcc.Graph(id='beam-profile', style={'height': '45vh'})
#                 ], style={"border": "1px solid #333", "borderRadius": "12px", "overflow": "hidden"})
#             ], width=12)
#         ])
#     ], style={"padding": "30px"})
#
#
# def create_layout():
#     return dbc.Container([
#         dbc.Row([
#             dbc.Col(create_sidebar(), width=3, style={"padding": "0"}),
#             dbc.Col(create_graphs_area(), width=9, style={"backgroundColor": DARK_BG})
#         ], className="g-0")
#     ], fluid=True, style={"fontFamily": "'Exo 2', sans-serif"})
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# --- Custom Styles (From your snippet) ---
NEON_TEAL = "#ffffff"  # Using the white/bright color from your code
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
    """Returns a placeholder figure for the Heatmap"""
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

            # 1. Number of Elements (Updated to Slider to match backend)
            html.Label("Number of Elements:", style=label_style),
            dcc.Slider(
                id='num-elements-slider',
                min=2, max=16, step=1, value=8,
                marks={2: '2', 8: '8', 16: '16'},
                tooltip={"placement": "bottom", "always_visible": False}
            ),
            html.Div(style={"marginBottom": "15px"}),

            # 2. Curvature
            html.Label("Curvature:", style=label_style),
            dcc.Slider(
                id='curvature-slider',
                min=0, max=5, step=0.1, value=0.0,
                marks={0: 'Flat', 5: 'Max'},
                tooltip={"placement": "bottom", "always_visible": False}
            ),
            html.Div(style={"marginBottom": "15px"}),

            # 3. Spacing Controls (Added Component)
            html.Label("Element Spacing Unit:", style=label_style),
            dcc.RadioItems(
                id='spacing-unit-radio',
                options=[
                    {'label': ' Lambda (λ)', 'value': 'lambda'},
                    {'label': ' Meters (m)', 'value': 'meter'}
                ],
                value='lambda',
                labelStyle={'display': 'inline-block', 'marginRight': '15px', 'color': 'white', 'fontSize': '12px'}
            ),
            html.Label("Spacing Value:", style=label_style),
            dcc.Slider(
                id='spacing-slider',
                min=0.1, max=2.0, step=0.1, value=0.5,
                marks={0.1: '0.1', 2: '2.0'},
                tooltip={"placement": "bottom", "always_visible": False}
            ),
            html.Div(style={"marginBottom": "15px"}),

            # 4. Dynamic Frequency Sliders
            html.Label("Frequencies (GHz):", style=label_style),
            html.Div(id='frequency-sliders-container', style={'maxHeight': '150px', 'overflowY': 'auto'}),
            html.Div(style={"marginBottom": "15px"}),

            # 5. Steering Angle (Replaces Phase Shift)
            html.Label("Steering Angle (°):", style=label_style),
            dcc.Slider(
                id='steer-angle-slider',
                min=-90, max=90, step=1, value=0,
                marks={-90: '-90', 0: '0', 90: '90'},
                tooltip={"placement": "bottom", "always_visible": False}
            ),

            # 6. Focus Controls (Hidden by default, used for Tumor/US)
            html.Div(id='focus-controls', children=[
                html.Div(style={"marginBottom": "12px"}),
                html.Label("Focus X (m):", style=label_style),
                dcc.Slider(
                    id='focus-x-slider', min=-1, max=1, step=0.1, value=0,
                    marks={-1: '-1', 0: '0', 1: '1'},
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
                html.Label("Focus Y (m):", style=label_style),
                dcc.Slider(
                    id='focus-y-slider', min=0, max=2, step=0.1, value=0.5,
                    marks={0: '0', 2: '2'},
                    tooltip={"placement": "bottom", "always_visible": False}
                ),
            ], style={'display': 'none'}),

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
                    {'label': '5G Beam Steering', 'value': '5g'},
                    {'label': 'Ultrasound Focus', 'value': 'ultrasound'},
                    {'label': 'Tumor Ablation', 'value': 'tumor'}
                ],
                value='5g',
                clearable=False,
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
                    id='interference-map',  # Updated ID for callback
                    figure=get_empty_map_figure(),
                    style={'height': '45vh'}
                )
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='beam-profile',  # Updated ID for callback
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