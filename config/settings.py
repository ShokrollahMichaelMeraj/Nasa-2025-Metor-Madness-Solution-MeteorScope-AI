# config/settings.py
# Centralized configuration and constants for MeteorScope AI

from pathlib import Path

# Base project directory (meteorscope-ai/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory paths
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
ASSETS_DIR = BASE_DIR / "assets"

# Data files
NASA_NEO_SAMPLE = DATA_DIR / "nasa_neo_sample.csv"
POP_GRID_SAMPLE = DATA_DIR / "pop_grid_sample.csv"
SYNTHETIC_IMPACTS = DATA_DIR / "synthetic_impacts.csv"

# Model files
THREAT_MODEL_PATH = MODELS_DIR / "threat_model.pkl"
EFFECTS_MODEL_PATH = MODELS_DIR / "effects_model.pkl"

# External NASA API (optional for later use)
JPL_SBDB_URL = "https://ssd-api.jpl.nasa.gov/sbdb.api"
