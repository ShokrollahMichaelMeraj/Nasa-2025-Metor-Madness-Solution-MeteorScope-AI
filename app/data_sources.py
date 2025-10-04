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

# def fetch_nasa_neows(limit=20):
#     Fetch top N NEOs from NASA NeoWs API and format columns.

# def normalize_units(df):
#     Ensure all relevant numeric units are consistent. -


