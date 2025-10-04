# NASA & Local Data Loader
# Purpose:
# Fetches and formats all asteroid and environmental data.
# Responsibilities:
# Fetch live asteroid data from NASA NeoWs REST API.
# Parse JSON → pandas DataFrame.
# Normalize units (e.g., AU → km).
# Provide local fallback CSVs if offline.
# (Optionally) join with other datasets (e.g., population or USGS).

# Key functions:

# def load_local_data(path=data/nasa_neo_sample.csv):
#     Load local sample dataset as pandas DataFrame.

# def fetch_nasa_neo_data(use_live=True) -> pd.DataFrame:
#     """Fetches recent near-Earth objects from the NASA NeoWs API or loads fallback CSV."""

# def fetch_sbdb_orbital_elements(neo_id: str) -> dict:
#     """Fetches Keplerian orbital elements for a specific asteroid using the JPL SBDB API."""

# def normalize_units(df):
#     Ensure all relevant numeric units are consistent. -


