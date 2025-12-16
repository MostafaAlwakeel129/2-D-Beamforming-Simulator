"""
Beamforming Simulator - Main Application File
Run this file to start the Dash application
"""

import dash
import dash_bootstrap_components as dbc
from layout.layout import create_layout
from callbacks.callbacks import register_callbacks

# Initialize the app with a dark theme (CYBORG closely matches your screenshot)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Set the layout
app.layout = create_layout()

# Register callbacks
register_callbacks(app)

# Server instance for deployment
server = app.server

if __name__ == '__main__':
    app.run(debug=True)