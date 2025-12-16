from dash import Input, Output, html, dcc
from dash.exceptions import PreventUpdate

# Styles for consistency
NEON_TEAL = "#ffffff"

label_style = {
    "color": NEON_TEAL,
    "fontWeight": "bold",
    "marginBottom": "3px",
    "fontSize": "13px"
}


def register_callbacks(app):
    """Register all callbacks for the application"""
    
    @app.callback(
        Output('frequency-sliders-container', 'children'),
        Input('num-transmitters-dropdown', 'value')
    )
    def update_frequency_sliders(num_transmitters):
        """
        Dynamically generate frequency sliders based on number of transmitters
        
        Args:
            num_transmitters: Number of transmitters selected
            
        Returns:
            List of Div elements containing frequency sliders
        """
        if num_transmitters is None:
            raise PreventUpdate
        
        sliders = []
        
        for i in range(num_transmitters):
            slider_div = html.Div([
                html.Label(f"Transmitter Frequency-{i+1}", style=label_style),
                dcc.Slider(
                    id={'type': 'freq-slider', 'index': i},
                    min=100, 
                    max=1000, 
                    step=10, 
                    value=500,
                    tooltip={"placement": "bottom", "always_visible": True},
                    marks=None
                ),
                html.Div(style={"marginBottom": "12px"})
            ])
            sliders.append(slider_div)
        
        return sliders