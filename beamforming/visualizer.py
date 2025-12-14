"""
Visualizer class - Handles the visualization aspects of the application.
"""

import numpy as np
import plotly.graph_objects as go
from typing import List
from .phased_array import PhasedArray


class Visualizer:
    """
    Handles the visualization aspects of the application.
    """
    
    def __init__(self):
        """Initialize the visualizer."""
        pass
    
    def plot_heatmap(self, matrix_data: np.ndarray) -> go.Figure:
        """
        Create a heatmap plot from matrix data.
        
        Args:
            matrix_data: 2D array of data to plot (Matrix)
            
        Returns:
            Figure: Plotly figure object for the heatmap
        """
        fig = go.Figure(data=go.Heatmap(
            z=matrix_data,
            colorscale='Viridis',
            colorbar=dict(title="Intensity")
        ))
        
        fig.update_layout(
            title="Constructive/Destructive Map",
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="X Position"),
            yaxis=dict(title="Y Position"),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig
    
    def plot_geometry(self, arrays_list: List[PhasedArray]) -> go.Figure:
        """
        Create a geometry plot showing the positions of arrays and elements.
        
        Args:
            arrays_list: List of PhasedArray objects to visualize
            
        Returns:
            Figure: Plotly figure object for the geometry plot
        """
        fig = go.Figure()
        
        # Plot each array and its elements
        for array in arrays_list:
            x_positions = [elem.x_position for elem in array.elements]
            y_positions = [elem.y_position for elem in array.elements]
            
            fig.add_trace(go.Scatter(
                x=x_positions,
                y=y_positions,
                mode='markers',
                name=f'Array {array.id}',
                marker=dict(size=10, symbol='circle')
            ))
        
        fig.update_layout(
            title="Array Geometry",
            template="plotly_dark",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(title="X Position"),
            yaxis=dict(title="Y Position", scaleanchor="x", scaleratio=1),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        return fig

