# Physics & Helper Functions
# Purpose:
# All math and formulas live here — physics, geometry, conversions.
# Responsibilities:
# Physics formulas (mass, energy, TNT equivalent, crater diameter).
# Unit conversions (AU ↔ km, km/s ↔ m/s).
# Coordinate/geodesy math for impact mapping.
# Helper constants (Earth radius, density defaults).

# Key functions:


# def calc_mass(d_km, density_kg_m3=3000):
#     """Compute asteroid mass from diameter and density."""

# def calc_kinetic_energy(mass_kg, v_kms):
#     """Compute kinetic energy in Joules."""

# def energy_to_tnt_mt(energy_j):
#     """Convert Joules to megatons of TNT."""

# def estimate_crater_size(energy_mt):
#     """Return approximate crater diameter in km."""

# def estimate_blast_radius(crater_km):
#     """Return estimated blast radius in km."""


# def calc_mass(diam_km: float, density_gcc: float = 3.0) -> float:
#     """Calculate asteroid mass in kg using volume * density."""
# def calc_impact_energy(diam_km: float, v_kms: float, density_gcc: float = 3.0) -> float:
#     """Compute kinetic energy of impact in Joules."""
# def calc_crater_and_blast(E_joules: float) -> tuple[float, float]:
#     """Estimate crater and blast radius using empirical scaling laws."""
# def calc_orbit_points(a, e, i, omega, w, M0, num_points=200) -> np.ndarray:
#     """Compute positions along an elliptical orbit for visualization."""

# Used by: ai_core.py, tests/test_utils.py



# app/utils.py
import math

def calc_mass(diameter_km, density_kg_m3=3000):
    radius_m = (diameter_km * 1000) / 2
    return (4/3) * math.pi * radius_m**3 * density_kg_m3

def calc_kinetic_energy(mass_kg, velocity_kms):
    v_ms = velocity_kms * 1000
    return 0.5 * mass_kg * v_ms**2

def energy_to_megatons(energy_joules):
    return energy_joules / 4.184e15

def estimate_crater_diameter(energy_joules):
    # simple toy model
    return 0.07 * (energy_joules ** 0.25) / 1000  # km

def estimate_blast_radius(crater_km):
    return 5 * crater_km  # km

def estimate_miss_distance(delta_v, lead_years, scale_km_per_dv=500):
    return delta_v * lead_years * scale_km_per_dv


# if __name__ == "__main__":
#     # Quick sanity demo
#     d_km = 0.5
#     rho = 3000
#     v_kms = 19
#     dv = 0.002
#     years = 5

#     m = calc_mass(d_km, rho)
#     E = calc_kinetic_energy(m, v_kms)
#     mt = energy_to_megatons(E)
#     cr_km = estimate_crater_diameter(E)
#     bl_km = estimate_blast_radius(cr_km)
#     miss_km = estimate_miss_distance(dv, years)

#     print("[utils demo]")
#     print(f" mass          : {m:.3e} kg")
#     print(f" energy        : {E:.3e} J  (~{mt:.1f} Mt TNT)")
#     print(f" crater dia    : {cr_km:.2f} km")
#     print(f" blast radius  : {bl_km:.2f} km")
#     print(f" miss distance : {miss_km:.1f} km (toy)")