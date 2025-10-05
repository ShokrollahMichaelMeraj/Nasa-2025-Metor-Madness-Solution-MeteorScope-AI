# Core AI + threat logic

# Purpose:
# Implements the reasoning layer — turns raw asteroid and environmental data into interpretations and predictions.
# Responsibilities:
# Load trained ML models (if present) or fall back to rule-based heuristics.
# Compute risk classification (Low/Med/High) using input parameters.
# Predict crater size, blast radius, or energy effects.
# Handle mitigation simulation (Δv, lead time → miss distance).

# Key functions/classes:
# def classify_threat(neo_row: dict) -> str:
#     """Simple rule-based or ML classifier returning Low/Medium/High threat badge."""
# def predict_effects(diam_km, v_kms, density_gcc, impact_angle_deg) -> dict:
#     """Compute crater size, blast radius, seismic equivalent, and energy."""
# def simulate_deflection(v_kms, lead_years, method='kinetic') -> dict:
#     """Simulate miss distance change (Δv * lead_time) and return new trajectory outcome."""


# Input: processed asteroid parameters
# Output: dictionary of computed effects + threat rating
# Used by: streamlit_app.py


# app/ai_core.py
# ------------------------------------------------------------
# Threat classification + mitigation logic for MeteorScope AI.
# Uses simple, interpretable rules suitable for hackathon speed.
# ------------------------------------------------------------

import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from typing import Tuple, Dict
from app.utils import (
    calc_mass,
    calc_kinetic_energy,
    energy_to_megatons,
    estimate_crater_diameter,
    estimate_blast_radius,
    estimate_miss_distance,
)

AU_TO_KM = 1.496e8


def classify_threat(moid_au: float, diam_km: float, v_kms: float) -> str:
    """
    Simple, explainable rule-based threat label.
    We keep NASA's PHA flag for reference elsewhere; this adds gradation.

    Heuristic:
      score = D * v
      High   if (MOID < 0.01 AU) and (score > 5)
      Medium if (MOID < 0.05 AU) and (score > 2)
      else Low
    """
    score = (diam_km or 0) * (v_kms or 0)
    if (moid_au or 1e9) < 0.01 and score > 5:
        return "🔴 High"
    if (moid_au or 1e9) < 0.05 and score > 2:
        return "🟠 Medium"
    return "🟢 Low"


def predict_effects(
    diam_km: float,
    density_kg_m3: float,
    v_kms: float
) -> Dict[str, float]:
    """
    Fast physics proxy for impact effects.
    Returns mass, energy (J & Mt), crater diameter, and blast radius.
    """
    m = calc_mass(diam_km, density_kg_m3)
    E = calc_kinetic_energy(m, v_kms)
    Mt = energy_to_megatons(E)
    crater_km = estimate_crater_diameter(E)
    blast_km = estimate_blast_radius(crater_km)

    return {
        "mass_kg": m,
        "energy_j": E,
        "energy_mt": Mt,
        "crater_km": crater_km,
        "blast_km": blast_km,
    }


def mitigation_outcome(
    strategy: str,
    delta_v_ms: float,
    lead_years: float,
    moid_au: float
) -> Tuple[str, float]:
    """
    Toy mitigation: miss distance ~ Δv * lead_years * k (k tuned for feel).
    Returns (outcome_label, predicted_miss_km).
    """
    # scale_km_per_dv is a pedagogical factor (not a precise astrodynamics calc)
    miss_km = estimate_miss_distance(delta_v_ms, lead_years, scale_km_per_dv=500.0)
    required_clearance_km = (moid_au or 0) * AU_TO_KM

    if required_clearance_km <= 0:
        # If we don't have MOID, return qualitative result based on miss_km
        if miss_km >= 10000:
            return "✅ Likely misses (qualitative)", miss_km
        if miss_km >= 2000:
            return "⚠️ Grazing pass possible (qualitative)", miss_km
        return "💥 Still impacts (qualitative)", miss_km

    if miss_km >= required_clearance_km:
        return "✅ Missed", miss_km
    if miss_km >= 0.5 * required_clearance_km:
        return "⚠️ Grazing pass", miss_km
    return "💥 Still impacts", miss_km


def summarize_plain_english(
    name: str,
    threat_label: str,
    effects: Dict[str, float],
    v_kms: float,
    diam_km: float,
    moid_au: float,
    strategy: str = "None",
    delta_v_ms: float = 0.0,
    lead_years: float = 0.0,
    mitigation_text: str = ""
) -> str:
    """
    Generates a short, friendly summary suitable for the UI.
    """
    energy_mt = effects.get("energy_mt", 0.0)
    crater_km = effects.get("crater_km", 0.0)
    blast_km = effects.get("blast_km", 0.0)
    moid_ld = moid_au * (AU_TO_KM / 384400.0) if moid_au else None

    lines = []
    lines.append(f"{threat_label} threat for **{name}**.")
    lines.append(
        f"~{diam_km:.0f} m object at {v_kms:.1f} km/s "
        f"→ ~{energy_mt:,.0f} Mt TNT; crater ≈ {crater_km:.1f} km; severe damage within ≈ {blast_km:.1f} km."
    )
    if moid_au:
        lines.append(f"MOID ≈ {moid_au:.3f} AU ({moid_ld:.0f} LD).")
    if strategy != "None":
        lines.append(
            f"Mitigation tried: **{strategy}** (Δv={delta_v_ms} m/s, lead={lead_years} yr). {mitigation_text}"
        )
    return "  \n".join(lines)


# ------------------------------------------------------------
# Self-test / demo block (run: `python3 app/ai_core.py`)
# ------------------------------------------------------------
if __name__ == "__main__":
    # Demo inputs (aligned with your utils demo)
    name = "Demo-NEO-500m"
    diam_km = 0.5          # 500 m
    density = 3000         # kg/m^3
    v_kms = 19.0           # km/s
    moid_au = 0.03         # 0.03 AU (~11.7 LD)
    strategy = "Kinetic Impactor"
    delta_v_ms = 0.002     # 2 mm/s
    lead_years = 5.0

    # Classify threat
    label = classify_threat(moid_au, diam_km, v_kms)

    # Predict effects
    fx = predict_effects(diam_km, density, v_kms)

    # Mitigation
    outcome, miss_km = mitigation_outcome(strategy, delta_v_ms, lead_years, moid_au)
    mit_txt = f"Outcome: {outcome} (predicted miss distance ≈ {miss_km:,.0f} km)."

    # Summary
    summary = summarize_plain_english(
        name=name,
        threat_label=label,
        effects=fx,
        v_kms=v_kms,
        diam_km=diam_km,
        moid_au=moid_au,
        strategy=strategy,
        delta_v_ms=delta_v_ms,
        lead_years=lead_years,
        mitigation_text=mit_txt
    )

    # Print results
    print("[ai_core demo]")
    print(f" Threat label : {label}")
    print(f" Effects      : energy={fx['energy_mt']:.0f} Mt, crater={fx['crater_km']:.2f} km, blast={fx['blast_km']:.2f} km")
    print(f" Mitigation   : {mit_txt}")
    print("\nSummary for UI:\n" + summary)
