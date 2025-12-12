"""
Beamforming Simulator - Main Application File
Run this file to start the Dash application
"""

import dash
import dash_bootstrap_components as dbc
from layout import create_layout

# Initialize the app with a dark theme (CYBORG closely matches your screenshot)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

# Set the layout
app.layout = create_layout()

# Import callbacks here (when you create them)
# import callbacks

# Server instance for deployment
server = app.server

if __name__ == '__main__':
    # print("Starting Beamforming Simulator...")
    # print("Open your browser and navigate to: http://127.0.0.1:8050")
    app.run(debug=True)