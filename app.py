"""
Beamforming Simulator - Main Application File
Run this file to start the Dash application
"""

import dash
import dash_bootstrap_components as dbc
from layout.layout import create_layout
from callbacks.callbacks import register_callbacks

# --- UX IMPROVEMENT: Add Google Font (Exo 2) ---
# We use 'Exo 2' for a futuristic, technical look.
FONT_URL = "https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;700&display=swap"

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG, FONT_URL],
    title="BeamLab Sim" # Browser Tab Title
)

# Set the layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

# Server instance for deployment
server = app.server

if __name__ == '__main__':
    app.run(debug=True)