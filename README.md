# 2D Beamforming Simulator

A real-time interactive web application for visualizing phased array beamforming with constructive/destructive wave interference patterns and directional beam profiles.

## Overview

This simulator demonstrates how phased arrays work by controlling the phase and timing of multiple antenna elements to steer beams in specific directions or focus energy at precise locations. It's useful for understanding applications in:

- **5G/Wireless Communications** - Beam steering for directional transmission
- **Medical Ultrasound** - Focused imaging and scanning
- **HIFU Therapy** - Targeted tumor ablation through focused ultrasound

## Features

- **Real-time visualization** of electromagnetic/acoustic wave interference
- **Multiple scenarios** pre-configured for different applications
- **Interactive controls** for array geometry, frequency, and beam steering
- **Dual visualizations**: 2D intensity heatmap and polar beam profile
- **Flexible array configurations**: Linear or curved array geometries

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/MostafaAlwakeel129/2-D-Beamforming-Simulator.git
   cd 2-D-Beamforming-Simulator
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install dash dash-bootstrap-components plotly numpy
   ```

## Running the Application

Start the application with:

```bash
python app.py
```

Then open your web browser and navigate to:
```
http://127.0.0.1:8050
```

## Usage

1. **Select a Scenario** - Choose from 5G, Ultrasound, or Tumor Ablation presets
2. **Adjust Parameters** - Modify array configuration, element count, spacing, and curvature
3. **Control the Beam** - Use steering angle and focus controls to direct the beam
4. **Observe Results** - Watch real-time updates in the heatmap and beam profile

## Project Structure

```
2-D-Beamforming-Simulator/
│
├── app.py                      # Main application entry point
├── __init__.py                 # Package initialization
│
├── callbacks/
│   └── callbacks.py            # Dash callback functions for UI interactivity
│
├── layout/
│   └── layout.py               # UI layout and styling definitions
│
├── phased_array.py             # Phased array physics and geometry engine
├── system_controller.py        # Simulation grid and parameter management
├── scenario_loader.py          # Pre-configured scenario templates
├── visualizer.py               # Plotly figure generation for heatmap and polar plots
│
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
└── README.md                   # Project documentation
```