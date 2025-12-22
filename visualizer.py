import numpy as np
import plotly.graph_objects as go

class Visualizer:
    # Unified Styling Constants
    STYLE = {
        "font": dict(family="'Exo 2', sans-serif", color='white'),
        "cyan": "#00f2ff",
        "orange": "#ff8c00",
        "grid": "#333",
        "bg_transparent": "rgba(0,0,0,0)"
    }

    @staticmethod
    def plot_heatmap(field_magnitude, grid_x, grid_y, array_obj):
        """Generates the Intensity Heatmap."""
        heatmap = go.Heatmap(
            z=field_magnitude, x=grid_x[0, :], y=grid_y[:, 0],
            colorscale='Inferno', zmin=0, zmax=1, zsmooth='fast',
            colorbar=dict(
                title=dict(text="INTENSITY", font=Visualizer.STYLE["font"]),
                tickfont=dict(color='#ccc', family=Visualizer.STYLE["font"]["family"]),
                thickness=15
            )
        )

        antennas = go.Scatter(
            x=array_obj.x_coords, y=array_obj.y_coords, mode='markers',
            marker=dict(color='blue', size=10, line=dict(color='white', width=2)),
            showlegend=False
        )

        fig = go.Figure(data=[heatmap, antennas])
        fig.update_layout(
            title="FIELD INTENSITY MAP",
            title_font=dict(color=Visualizer.STYLE["cyan"], family=Visualizer.STYLE["font"]["family"], size=18, weight=700),
            template="plotly_dark",
            paper_bgcolor=Visualizer.STYLE["bg_transparent"],
            plot_bgcolor="black",
            xaxis=dict(title="LATERAL POSITION (m)", title_font=Visualizer.STYLE["font"], gridcolor=Visualizer.STYLE["grid"], range=[-10, 10]),
            yaxis=dict(title="DEPTH (m)", title_font=Visualizer.STYLE["font"], gridcolor=Visualizer.STYLE["grid"], range=[0, 20]),
            margin=dict(l=60, r=40, t=50, b=50)
        )
        return fig

    @staticmethod
    def plot_polar_beam_profile(angles_deg, response):
        """Generates the Polar Beam Profile."""
        max_val = np.max(response)
        r_vals = response / max_val if max_val > 1e-9 else np.zeros_like(response)

        trace = go.Scatterpolar(
            r=r_vals, theta=angles_deg + 90, mode='lines', fill='toself',
            line=dict(color=Visualizer.STYLE["orange"], width=3), name='Beam Pattern'
        )

        fig = go.Figure(data=[trace])
        fig.update_layout(
            title="BEAM PROFILE (NORMALIZED)",
            title_font=dict(color=Visualizer.STYLE["orange"], family=Visualizer.STYLE["font"]["family"], size=18, weight=700),
            template="plotly_dark",
            paper_bgcolor=Visualizer.STYLE["bg_transparent"],
            polar=dict(
                sector=[0, 180],
                radialaxis=dict(visible=True, range=[0, 1.1], showticklabels=False, gridcolor=Visualizer.STYLE["grid"]),
                angularaxis=dict(
                    direction="counterclockwise", rotation=0, gridcolor='#444',
                    tickvals=[0, 30, 60, 90, 120, 150, 180],
                    ticktext=["0°", "30°", "60°", "90°", "120°", "150°", "180°"],
                    tickfont=dict(family=Visualizer.STYLE["font"]["family"], size=14)
                ),
                bgcolor=Visualizer.STYLE["bg_transparent"]
            ),
            margin=dict(l=30, r=30, t=40, b=10)
        )
        return fig