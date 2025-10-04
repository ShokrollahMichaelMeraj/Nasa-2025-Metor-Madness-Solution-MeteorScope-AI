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