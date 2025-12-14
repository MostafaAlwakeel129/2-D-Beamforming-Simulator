"""
BeamformingApp class - Main application class for the beamforming simulator.
"""

import dash
import dash_bootstrap_components as dbc
from .system_controller import SystemController
from .visualizer import Visualizer


class BeamformingApp:
    """
    Main application class for the beamforming simulator.
    
    Attributes:
        app (dash.Dash): Dash application instance
        controller (SystemController): System controller instance
        visualizer (Visualizer): Visualizer instance
    """
    
    def __init__(self, external_stylesheets=None):
        """
        Initialize the beamforming application.
        
        Args:
            external_stylesheets: External stylesheets for Dash (default: CYBORG theme)
        """
        if external_stylesheets is None:
            external_stylesheets = [dbc.themes.CYBORG]
        
        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        self.controller = SystemController()
        self.visualizer = Visualizer()
        
        # Initialize layout
        self.set_layout()
        
        # Register callbacks
        self.register_callbacks()
    
    def set_layout(self) -> None:
        """
        Set the layout of the Dash application.
        This method should be implemented to define the UI layout.
        """
        # Import layout function from the existing layout module
        from layout import create_layout
        self.app.layout = create_layout()
    
    def register_callbacks(self) -> None:
        """
        Register all Dash callbacks for interactivity.
        This method should be implemented to define all callbacks.
        """
        # Placeholder for callback registration
        # Callbacks will be implemented here to connect UI controls
        # to the controller and visualizer
        pass
    
    def run(self, debug: bool = True, **kwargs) -> None:
        """
        Run the Dash application.
        
        Args:
            debug: Enable debug mode (default: True)
            **kwargs: Additional arguments to pass to app.run()
        """
        self.app.run(debug=debug, **kwargs)
    
    @property
    def server(self):
        """Get the Flask server instance for deployment."""
        return self.app.server

