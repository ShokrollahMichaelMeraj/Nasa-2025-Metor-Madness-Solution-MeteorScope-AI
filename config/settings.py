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

from dotenv import load_dotenv; load_dotenv()

import os

from pathlib import Path

# Create a free NASA API key: https://api.nasa.gov
NASA_API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")  # Replace later

# Path for offline NEO cache
LOCAL_NEO_PATH = os.path.join("data", "nasa_neo_sample.csv")

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
