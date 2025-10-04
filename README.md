# Nasa-2025-Metor-Madness-Solution-MeteorScope-AI

#  MeteorScope AI  
**NASA Space Apps Challenge 2025 Submission**

---

##  Objectives
1. **Interactive visualization & simulation** of asteroid impact scenarios.  
2. **Use real data** (NASA NEO + optional USGS layers).  
3. **Predict consequences** (energy, crater, blast/seismic/tsunami proxies).  
4. **Evaluate mitigation** (deflection strategies; show outcomes).  
5. **Accessible + educational** (tooltips, story mode, clean UI).  
6. **Performance** (snappy; graceful fallbacks).  
7. **Modular & scalable** (add datasets later).  

---

##  MVP Feature List (Built in 24h)

### A. Data Ingest (offline first, live optional)
- Local CSV loader for a small NEO table (`id, name, diam_km, v_kms, moid_au, approach_ld, ecc, inc_deg, Hmag`).  
- Optional live fetch (toggle) from **NASA NeoWs** browse endpoint (first page → 20–50 NEOs).  
- Unit normalization (km ↔ AU ↔ LD).  
- Fallback: if API fails → use local CSV.  

**Acceptance:**  
- Selecting “Use live NASA data” loads a table; turning off reverts to CSV.  
- No crash if offline.  

---

### B. Orbital/Impact Inputs (left sidebar)
- Asteroid selector (dropdown → from NEO DF).  
- Manual override sliders (diameter, velocity, density, entry angle).  
- Impact location controls (lat/lon sliders + map click-to-set).  
- Target type: land/water toggle.  

**Acceptance:**  
- Changing any control updates calculations and visualizations within ~300ms.  

---

### C. Physics & AI Core (instant outputs)
- Mass from diameter+density (sphere approximation).  
- Kinetic energy \( E = \frac{1}{2}mv^2 \) → TNT Mt conversion.  
- Crater diameter (toy scaling).  
- Blast radius (toy factor of crater).  
- AI Threat Badge (Low/Med/High).  
  - v0: rule-based (MOID + energy).  
  - v1 (stretch): scikit-learn classifier trained on heuristics.  

**Acceptance:**  
- Outputs update instantly and are numerically plausible.  

---

### D. Visualizations
- 3D globe (orthographic) with:  
  - Impact point marker  
  - Crater ring  
  - Blast ring  
- Animated pulse when impact changes.  
- Legend + units.  

**Acceptance:**  
- Circles render correctly at chosen lat/lon; resizing feels smooth.  

---

### E. Mitigation Mode (“Deflect with Light / Kinetic”)
- Strategy dropdown: None / Kinetic Impactor / Laser Ablation.  
- Lead time slider (years).  
- Δv estimate (toy): proportional miss distance \( \text{miss\_km} \propto \Delta v \times \text{lead\_years} \).  
- Outcome label: “Miss”, “Grazing pass”, or “Still impacts”.  

**Acceptance:**  
- Increasing lead time expands predicted miss distance and can flip outcome to “Miss.”  

---

### F. Educational UX
- Tooltips on key terms (eccentricity, MOID, kinetic energy, Δv).  
- AI-generated plain-language summary:  
  > “Moderate threat. 250m stony asteroid at 19 km/s. If impacting near Vancouver: crater 3.1 km; severe damage in 15 km. With 5 years lead, kinetic impactor likely prevents impact.”  

**Acceptance:**  
- Hover shows simple, correct definitions; summary updates dynamically.  

---

## 🌊 Optional “Plus” Features
1. **Population Risk Overlay**  
   - Pre-baked CSV grid of city centroids + populations.  
   - Sum population within blast radius.  

2. **USGS Elevation / Tsunami Proxy**  
   - Qualitative “tsunami risk” if impact within X km of coasts.  

3. **Orbit Similarity Clustering (Unsupervised)**  
   - K-means on orbital parameters → “asteroid families.”  

4. **Story Mode: Impactor-2025**  
   - Guided 3-step scenario walkthrough.  

---

## System Architecture
```
meteorscope-ai/
├── app/
│   ├── ai_core.py                  # AI threat prediction & crater modeling
│   ├── streamlit_app.py            # Main Streamlit UI app
│   ├── utils.py                    # Physics equations & helper functions
│   ├── visuals.py                  # Plotly globe & map rendering
│   ├── data_sources.py             # NASA NEO API fetch + CSV loader
│
├── config/
│   └── settings.py                 # Constants & global config
│
├── data/
│   ├── nasa_neo_sample.csv         # Sample asteroid data
│   ├── pop_grid_sample.csv         # Population data for impact overlay
│   └── synthetic_impacts.csv       # Simulated impact dataset
│
├── docs/
│   ├── pitch_slides.pdf            # Presentation slides
│   ├── architecture_diagram.png    # System diagram
│   └── challenge_mapping.txt       # Challenge mapping documentation
│
├── models/
│   ├── threat_model.pkl            # ML threat classification model
│   └── effects_model.pkl           # ML impact effects regressor
│
├── notebooks/
│   ├── 01_prepare_data.ipynb       # Data prep
│   ├── 02_train_threat_model.ipynb # Train classifier
│   └── 03_train_effects_model.ipynb# Train regressor
│
├── tests/
│   └── test_utils.py               # Unit tests for core functions
│
├── assets/
│   ├── logo.png                    # Logo
│   └── demo_video.mp4              # Demo recording
│
├── requirements.txt                # Dependencies
├── main.py                         # CLI entry to run the app
├── README.md                       # Overview & setup instructions
├── LICENSE                         # MIT license
└── .gitignore                      # Ignore compiled files & models

```


**Data Flow:**  
`streamlit_app` → loads DataFrame → passes asteroid params to `ai_core` → returns effects → `visuals` renders globe → `utils` does math.

---

## Algorithm Details (MVP)
- **Mass**: \( m = \rho \cdot \frac{4}{3}\pi (D/2)^3 \), \( \rho \approx 3000 \text{ kg/m}^3 \)  
- **Energy**: \( E = ½mv^2 \)  
- **TNT equivalent**: \( E / 4.184×10^{15} = \text{Mt} \)  
- **Crater diameter**: \( D_c ≈ 0.07⋅E^{1/4} \) (km)  
- **Blast radius**: \( R_b ≈ 5⋅D_c \) (km)  
- **Threat heuristic**:  
  - High → MOID < 0.01 AU & (diam_km × v_kms > 5)  
  - Medium → MOID < 0.05 AU & (diam_km × v_kms > 2)  
  - Else → Low  
- **Mitigation toy**: \( \text{miss\_km} ∝ \Delta v × \text{lead\_years} \)

---

##  User Stories
- As a **teacher**, I can pick a real asteroid and visualize its impact near my city.  
- As a **policymaker**, I can toggle deflection and see if early action averts disaster.  
- As a **scientist**, I can vary parameters and get instant impact metrics.  

---

##  Test Plan
| Component | Test | Expected |
|------------|------|-----------|
| config/settings.py | Imports successfully | Prints valid paths |
| utils.py | Energy/TNT math | Within known scale |
| ai_core.py | classify_threat() | “Low”, “Med”, or “High” |
| visuals.py | draw_impact_map() | Plotly Figure with ≥3 traces |
| streamlit_app.py | Live slider update | Numbers + rings update instantly |

---

##  UI Layout
**Sidebar:**  
- Asteroid selector  
- Manual overrides: D, v, ρ, angle, target  
- Mitigation: strategy, lead time  

**Main Panel:**  
- 3D globe + crater & blast rings  
- Metrics card (energy, crater, blast, threat)  
- Summary with tooltips  

---

##  Build Order (Hackathon Timeline)
| Time | Task |
|------|------|
| T0–T1 | Config + Utils setup |
| T1–T3 | AI fallback + Visuals |
| T3–T6 | Streamlit UI base |
| T6–T8 | Mitigation Panel |
| T8–T10 | Educational polish |
| T10–T12 | (Stretch) Live NeoWs or Pop overlay |
| T12–T14 | (Stretch) Train classifier/regressor |

---

##  Feature Checklist
- [ ] CSV loader + NASA NeoWs fetch  
- [ ] Sidebar controls (D, v, ρ, angle, target, lat/lon)  
- [ ] Physics outputs (mass, energy, TNT Mt, crater, blast)  
- [ ] AI threat badge (rule-based / ML later)  
- [ ] Plotly globe with crater/blast rings  
- [ ] Mitigation mode (strategy + Δv)  
- [ ] Tooltips + plain-language summary  
- [ ] (Stretch) population affected  
- [ ] (Stretch) live data toggle  
- [ ] (Stretch) ML surrogate & classifier  

---

##  Credits
Built for **NASA Space Apps Challenge 2025** by  
**Team:** MeteorScope AI  
**Mission:** Make asteroid risk understandable, actionable, and inspiring 🚀  

