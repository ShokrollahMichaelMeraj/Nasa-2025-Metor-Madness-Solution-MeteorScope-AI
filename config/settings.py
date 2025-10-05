# config/settings.py
# Centralized configuration and constants for MeteorScope AI

# Constants & Global Configuration
# Purpose:
# Holds all constants and settings in one place.
# Responsibilities:
# Define file paths for data, models, and assets.
# Set default values (density, API keys, Earth radius).
# Define constants for physics or scaling.
# Example:
# DATA_PATH = "data/nasa_neo_sample.csv"
# EARTH_RADIUS_KM = 6371
# DEFAULT_DENSITY = 3000  # kg/m³
# NASA_API_URL = "https://api.nasa.gov/neo/rest/v1/neo/browse"


# config/settings.py
import os
from pathlib import Path

# --- NASA API key resolution: Streamlit Secrets -> env var -> .env -> DEMO ---
NASA_API_KEY = None
try:
    import streamlit as st
    NASA_API_KEY = st.secrets.get("NASA_API_KEY")
except Exception:
    pass

if not NASA_API_KEY:
    NASA_API_KEY = os.getenv("NASA_API_KEY")

if not NASA_API_KEY:
    try:
        from dotenv import load_dotenv
        load_dotenv()
        NASA_API_KEY = os.getenv("NASA_API_KEY")
    except Exception:
        pass

if not NASA_API_KEY:
    NASA_API_KEY = "DEMO_KEY"

def key_prefix() -> str:
    """Return a short, non-sensitive prefix used for debugging in the UI."""
    return "DEMO" if NASA_API_KEY == "DEMO_KEY" else f"{NASA_API_KEY[:6]}…"

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
ASSETS_DIR = BASE_DIR / "assets"

# Files
LOCAL_NEO_PATH = str(DATA_DIR / "nasa_neo_sample.csv")
NASA_NEO_SAMPLE = DATA_DIR / "nasa_neo_sample.csv"
POP_GRID_SAMPLE = DATA_DIR / "pop_grid_sample.csv"
SYNTHETIC_IMPACTS = DATA_DIR / "synthetic_impacts.csv"

THREAT_MODEL_PATH = MODELS_DIR / "threat_model.pkl"
EFFECTS_MODEL_PATH = MODELS_DIR / "effects_model.pkl"

# External
JPL_SBDB_URL = "https://ssd-api.jpl.nasa.gov/sbdb.api"
