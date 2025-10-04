# Visualization Layer
# Purpose:
# Renders the visual representation of asteroid impacts and trajectories.
# Responsibilities:
# Create interactive 3D globe (Plotly or pydeck).
# Plot:
    # Impact point.
    # Crater and blast rings.
    # Optional orbit/trajectory path.
# Support animations (impact pulse).
# Color-code severity and mitigation status.

# Key functions:



# def draw_globe_with_impact(lat, lon, crater_km, blast_km, orbit_points=None):
#     """Render Earth and overlays crater/blast rings, plus orbit path if provided."""
# def animate_deflection(before_path, after_path):
#     """Show beam deflection and changed orbit path overlay."""

# Input: values from ai_core
# Output: a Plotly Figure object for Streamlit to render.





# app/visuals.py
import plotly.graph_objects as go

def draw_impact_scene(earth_lat, earth_lon, asteroid_trajectory, impact_data, mitigation_data=None):
    """
    Build a 3D scene showing Earth, the asteroid's trajectory, an impact marker,
    and (optionally) a mitigation/deflection vector.

    Params
    -------
    earth_lat, earth_lon : float
        For centering the globe (visual convenience).
    asteroid_trajectory : dict
        {'x': [..], 'y': [..], 'z': [..]} positions in a simple Earth-centered frame.
        (For hackathon demo you can generate a straight segment or small arc.)
    impact_data : dict
        {'lat': float, 'lon': float, 'crater_km': float, 'blast_km': float}
        Only 'lat'/'lon' are used in this 3D scene; rings are better on 2D globe.
    mitigation_data : dict | None
        {'start_x': float,'start_y': float,'start_z': float,'dx': float,'dy': float,'dz': float}
        Vector to visualize deflection (optional).

    Returns
    -------
    fig : plotly.graph_objects.Figure
    """
    fig = go.Figure()

    # Earth marker (schematic). For a full globe texture you’d switch to a 2D geo map or pydeck.
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers",
        marker=dict(size=10, symbol="circle", opacity=0.9),
        name="Earth"
    ))

    # Asteroid trajectory (3D line)
    if asteroid_trajectory and all(k in asteroid_trajectory for k in ("x","y","z")):
        fig.add_trace(go.Scatter3d(
            x=asteroid_trajectory["x"],
            y=asteroid_trajectory["y"],
            z=asteroid_trajectory["z"],
            mode="lines",
            line=dict(width=6),
            name="Asteroid Path"
        ))

    # Impact point (projected as a 3D marker near Earth center for demo)
    if impact_data and "lat" in impact_data and "lon" in impact_data:
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode="markers+text",
            text=["Impact zone"],
            textposition="top center",
            marker=dict(size=4),
            name="Impact"
        ))

    # Optional mitigation vector (as a 3D cone/arrow)
    if mitigation_data and all(k in mitigation_data for k in ("start_x","start_y","start_z","dx","dy","dz")):
        fig.add_trace(go.Cone(
            x=[mitigation_data["start_x"]],
            y=[mitigation_data["start_y"]],
            z=[mitigation_data["start_z"]],
            u=[mitigation_data["dx"]],
            v=[mitigation_data["dy"]],
            w=[mitigation_data["dz"]],
            sizemode="absolute",
            sizeref=5,
            anchor="tail",
            showscale=False,
            name="Deflection"
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data",
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
    )
    return fig
