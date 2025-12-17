"""
Visualizer Class - Plotting Helper
Responsibility: Visualization of simulation results
"""

import numpy as np
import plotly.graph_objects as go
from phased_array import PhasedArray

class Visualizer:

    @staticmethod
    def plot_heatmap(field_magnitude, grid_x, grid_y, array_obj):
        """
        Generates the Heatmap with 'Exo 2' styling.
        """
        v_max = np.percentile(field_magnitude, 98)

        # 1. The Heatmap Trace
        heatmap = go.Heatmap(
            z=field_magnitude,
            x=grid_x[0, :],
            y=grid_y[:, 0],
            colorscale='Jet',
            zmin=0,
            zmax=v_max,
            showscale=True,
            colorbar=dict(
                title=dict(text="INTENSITY", font=dict(color='white', family="'Exo 2', sans-serif")),
                tickfont=dict(color='#ccc', family="'Exo 2', sans-serif"),
                thickness=15
            )
        )

        # 2. Antennas
        antennas = go.Scatter(
            x=array_obj.x_coords,
            y=array_obj.y_coords,
            mode='markers',
            marker=dict(color='white', size=8, line=dict(color='black', width=1)),
            showlegend=False
        )

        fig = go.Figure(data=[heatmap, antennas])
        fig.update_layout(
            title="FIELD INTENSITY MAP",
            title_font=dict(color='#00f2ff', family="'Exo 2', sans-serif", size=18, weight=700),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="black",
            margin=dict(l=60, r=40, t=50, b=50),

            xaxis=dict(
                title="LATERAL POSITION (m)",
                title_font=dict(family="'Exo 2', sans-serif"),
                showgrid=True, gridcolor='#333', range=[-3, 3]
            ),
            yaxis=dict(
                title="DEPTH (m)",
                title_font=dict(family="'Exo 2', sans-serif"),
                showgrid=True, gridcolor='#333', range=[0, 2]
            ),
        )
        return fig

    @staticmethod
    def plot_polar_beam_profile(angles_deg, response):
        """
        Generates the Polar Beam Profile with 'Exo 2' styling.
        """
        max_val = np.max(response)
        if max_val > 1e-9:
            response = response / max_val
        else:
            response = np.zeros_like(response)

        plot_theta = angles_deg + 90

        trace = go.Scatterpolar(
            r=response,
            theta=plot_theta,
            mode='lines',
            fill='toself',
            line=dict(color='#ff8c00', width=3),
            name='Beam Pattern'
        )

        fig = go.Figure(data=[trace])
        fig.update_layout(
            title="BEAM PROFILE (NORMALIZED)",
            title_font=dict(color='#ff8c00', family="'Exo 2', sans-serif", size=18, weight=700),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            # FIX: Minimized margins to make plot HUGE
            margin=dict(l=30, r=30, t=40, b=10),

            polar=dict(
                sector=[0, 180],
                radialaxis=dict(visible=True, range=[0, 1.1], showticklabels=False, gridcolor='#333'),
                angularaxis=dict(
                    direction="counterclockwise",
                    tickvals=[0, 30, 60, 90, 120, 150, 180],
                    ticktext=["0°", "30°", "60°", "90°", "120°", "150°", "180°"],
                    tickfont=dict(family="'Exo 2', sans-serif", size=14), # Larger font
                    gridcolor='#444',
                    rotation=0
                ),
                bgcolor="rgba(0,0,0,0)"
            )
        )
        return fig