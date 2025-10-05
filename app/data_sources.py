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



"""
data_sources.py
----------------
Handles all data acquisition for MeteorScope-AI.

This module lets you:
  • Fetch live near-Earth object (NEO) data from NASA’s NeoWs API.
  • Fall back to a local CSV file if the API call fails or you’re offline.
  • Optionally fetch precise orbital elements from the Small-Body Database (SBDB) for detailed trajectory visualization.

Dependencies:
  requests, pandas, os
"""

import os
import requests
import pandas as pd
from config.settings import NASA_API_KEY, LOCAL_NEO_PATH


# -------------------------------------------------------------
# 1️⃣  Fetch NEO Data (Core)
# -------------------------------------------------------------
def fetch_nasa_neo_data(use_live: bool = True, limit: int = 50) -> pd.DataFrame:
    """
    Fetches recent near-Earth object data from NASA's NeoWs API,
    or falls back to a local CSV file if offline or API fails.

    Parameters
    ----------
    use_live : bool
        If True → fetch from NASA API.
        If False → load from local CSV only.
    limit : int
        Max number of asteroids to load (API pages can be large).

    Returns
    -------
    pandas.DataFrame
        Columns:
          ['id','name','absolute_magnitude_h','estimated_diameter_km',
           'relative_velocity_kms','miss_distance_ld','orbiting_body',
           'is_potentially_hazardous_asteroid']

    Notes
    -----
    • The NeoWs “browse” endpoint returns a list of NEOs with close-approach data.
    • We extract a few representative fields so the rest of the app
      can quickly visualize or run physics on them.
    • If anything fails (no key, network, etc.), the local CSV backup is used.
    """

    if not use_live:
        print("[INFO] Using local NASA sample data...")
        return pd.read_csv(LOCAL_NEO_PATH)

    url = f"https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={NASA_API_KEY}"

    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        # The "near_earth_objects" field is a list of asteroid dicts
        neos = data.get("near_earth_objects", [])[:limit]

        records = []
        for neo in neos:
            # Some NEOs have multiple close_approach_data entries; we pick the first
            approach = neo.get("close_approach_data", [{}])[0]

            record = {
                "id": neo.get("id"),
                "name": neo.get("name"),
                "absolute_magnitude_h": neo.get("absolute_magnitude_h"),
                "estimated_diameter_km": neo.get("estimated_diameter", {})
                    .get("kilometers", {})
                    .get("estimated_diameter_max"),
                "relative_velocity_kms": float(approach.get("relative_velocity", {}).get("kilometers_per_second", 0)),
                "miss_distance_ld": float(approach.get("miss_distance", {}).get("lunar", 0)),
                "orbiting_body": approach.get("orbiting_body", "Earth"),
                "is_potentially_hazardous_asteroid": neo.get("is_potentially_hazardous_asteroid", False)
            }
            records.append(record)

        df = pd.DataFrame(records)
        df.to_csv(LOCAL_NEO_PATH, index=False)
        print(f"[INFO] ✅ Downloaded {len(df)} NEOs from NASA and cached locally.")
        return df

    except Exception as e:
        print(f"[WARN] NASA API failed ({e}); using local CSV fallback.")
        return pd.read_csv(LOCAL_NEO_PATH)


# -------------------------------------------------------------
# 2️⃣  Fetch SBDB Orbital Elements (Optional Detailed Orbits)
# -------------------------------------------------------------
def fetch_sbdb_orbital_elements(neo_id: str) -> dict:
    """
    Fetches orbital elements (Keplerian parameters) for a specific asteroid
    from NASA’s Small-Body Database (SBDB) API.

    Parameters
    ----------
    neo_id : str
        The asteroid’s numeric or alphanumeric identifier
        (e.g., '3542519' or 'Apophis').

    Returns
    -------
    dict
        Keys typically include:
          'a'  : semi-major axis (AU)
          'e'  : eccentricity
          'i'  : inclination (deg)
          'om' : longitude of ascending node (deg)
          'w'  : argument of perihelion (deg)
          'ma' : mean anomaly (deg)
          'epoch' : reference epoch (JD)
          plus any other available metadata.

    Notes
    -----
    • These values define an asteroid’s *orbit shape and position*.
    • You’ll use them later in utils.calc_orbit_points() to render its trajectory.
    • If the API fails, return an empty dict and print a warning instead of crashing.
    """

    url = f"https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={neo_id}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        elements = data.get("orbit", {}).get("elements", [])
        # Convert to dict for convenience
        out = {el["name"]: float(el["value"]) for el in elements if "name" in el and "value" in el}
        out["epoch"] = data.get("orbit", {}).get("epoch")
        print(f"[INFO] ✅ Retrieved orbital elements for {neo_id}")
        return out

    except Exception as e:
        print(f"[WARN] Could not fetch orbital data for {neo_id}: {e}")
        return {}



