"""
data_sources.py
----------------
Handles all data acquisition for MeteorScope-AI:
  • Fetch live near-Earth object (NEO) data from NASA’s NeoWs API.
  • Cache results locally to avoid API rate limits (1,000/hour).
  • Optionally fetch precise orbital elements from NASA’s SBDB API.
"""

import os
import time
import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from config.settings import NASA_API_KEY, LOCAL_NEO_PATH

# -------------------------------------------------------------
#  Global cache config
# -------------------------------------------------------------
CACHE_TTL_HOURS = 6
CACHE_PATH = os.path.join("data", "nasa_neo_cache.csv")
CACHE_META_PATH = os.path.join("data", "nasa_neo_cache.meta")

# -------------------------------------------------------------
# 0️⃣  Optional Streamlit cache wrapper
# -------------------------------------------------------------
@st.cache_data(ttl=3600)
def fetch_nasa_neo_data_cached(use_live=True, limit=50):
    """Cached wrapper for Streamlit UI (1h TTL)."""
    return fetch_nasa_neo_data(use_live=use_live, limit=limit)

# -------------------------------------------------------------
# 1️⃣  Main NEO Fetch Function (with pagination + file caching)
# -------------------------------------------------------------

def fetch_nasa_neo_data(use_live: bool = True, limit: int = 50) -> pd.DataFrame:
    """
    Fetches near-Earth object (NEO) data from NASA's NeoWs API,
    automatically handling pagination so more than 20 results can be fetched.
    Falls back to local cache if API fails.
    """

    if not use_live:
        print("[INFO] Using local NASA sample data...")
        return pd.read_csv(LOCAL_NEO_PATH)

    base_url = "https://api.nasa.gov/neo/rest/v1/neo/browse"
    params = {"api_key": NASA_API_KEY}
    records = []
    fetched = 0
    next_url = base_url

    print("[INFO] Fetching new NASA NEO data from API...")

    try:
        while next_url and fetched < limit:
            resp = requests.get(next_url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()

            neos = data.get("near_earth_objects", [])
            for neo in neos:
                if fetched >= limit:
                    break

                approach_list = neo.get("close_approach_data", [])
                approach = approach_list[0] if approach_list else {}

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
                fetched += 1

            # follow pagination if more pages available
            next_url = data.get("links", {}).get("next", None)

            # prevent hitting API too fast
            if next_url:
                import time
                time.sleep(1)

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
    Fetch orbital elements (Keplerian parameters) for a specific asteroid
    from NASA’s Small-Body Database (SBDB) API.
    """
    url = f"https://ssd-api.jpl.nasa.gov/sbdb.api?sstr={neo_id}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        elements = data.get("orbit", {}).get("elements", [])
        out = {el["name"]: float(el["value"]) for el in elements if "name" in el and "value" in el}
        out["epoch"] = data.get("orbit", {}).get("epoch")
        print(f"[INFO] ✅ Retrieved orbital elements for {neo_id}")
        return out
    except Exception as e:
        print(f"[WARN] Could not fetch orbital data for {neo_id}: {e}")
        return {}
