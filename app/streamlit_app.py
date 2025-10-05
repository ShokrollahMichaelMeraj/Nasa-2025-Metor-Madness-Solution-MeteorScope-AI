# UI and Control Flow
# Purpose:
# The front-end brain — everything the user sees and interacts with.
# Runs on Streamlit to provide a fast, interactive, and responsive app.
# Responsibilities:
# Create the sidebar inputs and main layout.
# Allow users to:

    # Select an asteroid or use live data.
    # Adjust size, speed, density, and angle.
    # Pick impact coordinates and target type.
    # Choose mitigation strategies.
# Dynamically call:
    # utils for physics.
    # ai_core for predictions.
    # visuals for rendering.
# Render summary text and tooltips.
# Handle fallback (offline mode).

# Key functions:

# def main():
#     """Streamlit entrypoint: builds UI, handles state, updates outputs."""


# Used by: main.py

# app/streamlit_app.py  (TOP of file)

import os, sys, datetime
import streamlit as st
import pandas as pd

# -------------------------------------------------------------
# Setup import paths
# -------------------------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from config.settings import NASA_API_KEY
from app.data_sources import fetch_nasa_neo_data
from config.settings import BASE_DIR



# -------------------------------------------------------------
# Streamlit Page Config
# -------------------------------------------------------------
st.set_page_config(page_title="MeteorScope AI", layout="wide")

# -------------------------------------------------------------
# Sidebar Header + API Source
# -------------------------------------------------------------
st.sidebar.title("🪐 MeteorScope AI")
using_demo = (NASA_API_KEY == "DEMO_KEY")

st.sidebar.markdown(
    f"**Data Source:** {'🌍 Live NASA API' if not using_demo else '📁 Local CSV / DEMO_KEY'}"
)
if using_demo:
    st.sidebar.warning("⚠️ Using DEMO_KEY (limited rate). Add your NASA key in `.env` or Streamlit Secrets.")

# -------------------------------------------------------------
# Sidebar Controls
# -------------------------------------------------------------
st.sidebar.subheader("Data Settings")
use_live = st.sidebar.toggle("Use live NASA data", value=not using_demo)
limit = st.sidebar.slider("NEO count", min_value=5, max_value=50, value=15, step=5)
refresh = st.sidebar.button("🔄 Refresh live NEOs")

if refresh:
    st.cache_data.clear()  # Clears cached API results

# -------------------------------------------------------------
# Fetch NEO Data
# -------------------------------------------------------------
progress = st.progress(0, text="Fetching NEO data…")

try:
    # the fetch itself
    df = fetch_nasa_neo_data(use_live=use_live, limit=limit)
    # complete the bar after a successful fetch
    progress.progress(1.0, text=f"Fetched {len(df)} NEOs ✅")

except Exception as e:
    # show the error and finish the bar in error state
    st.error(f"Failed to load data: {e}")
    progress.progress(1.0, text="Fetch failed ❌")
    df = pd.DataFrame()
    
# --- Save a dated snapshot only if we have real data ---
if not df.empty:
    import os, datetime
    from config.settings import BASE_DIR

    today = datetime.date.today().isoformat()
    save_dir = os.path.join(BASE_DIR, "data")
    os.makedirs(save_dir, exist_ok=True)  # ensure folder exists

    dated_path = os.path.join(save_dir, f"neo_{today}.csv")

    # Optional: avoid multiple saves on Streamlit reruns
    if not os.path.exists(dated_path):
        df.to_csv(dated_path, index=False)
        st.sidebar.caption(f"📦 Saved snapshot: `data/neo_{today}.csv`")
    else:
        st.sidebar.caption(f"📦 Snapshot already exists for today: `neo_{today}.csv`")
    
    

# -------------------------------------------------------------
# Main App Layout
# -------------------------------------------------------------
st.title("☄️ MeteorScope AI — Asteroid Impact Explorer")

if df.empty:
    st.info("No data loaded yet. Try enabling live NASA data or using local CSV.")
else:
    st.caption("✅ Near-Earth Objects loaded:")
    st.dataframe(df, width="stretch", hide_index=True)

    # ---------------------------------------------------------
    # Asteroid Selector
    # ---------------------------------------------------------
    name_col = "name" if "name" in df.columns else df.columns[0]
    selected_name = st.selectbox("Select an asteroid:", df[name_col].tolist())
    sel_row = df[df[name_col] == selected_name].iloc[0].to_dict()

    # ---------------------------------------------------------
    # Asteroid Summary Metrics
    # ---------------------------------------------------------
    st.subheader("Asteroid Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Diameter (km)", f"{sel_row.get('estimated_diameter_km', '—')}")
    col2.metric("Velocity (km/s)", f"{sel_row.get('relative_velocity_kms', '—')}")
    col3.metric("Miss Distance (LD)", f"{sel_row.get('miss_distance_ld', '—')}")

    # ---------------------------------------------------------
    # Visualization Placeholder (to be linked with visuals.py)
    # ---------------------------------------------------------
    st.divider()
    st.subheader("🛰️ Visualization")
    st.info("🌐 3D map and orbital trajectory will appear here once visuals.py is connected.")