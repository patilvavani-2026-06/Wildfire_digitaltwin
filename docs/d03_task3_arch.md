# PART II (cont.) — TASK 3: Complete Architecture of PyroCast–MORPHEUS

*(Master diagram: figure `D40_architecture_master.png`; organ charts: `D49`; sequence: `D42`; deployment: `D50`.)*

## 3.0 Reading the stack

```
PHYSICAL WORLD            (what is true)
SATELLITE OBSERVATION     (what orbit can see)
ATMOSPHERIC LAYER         (what the atmosphere is doing)
DATA FUSION LAYER         (what can be trusted & harmonized)
DIGITAL TWIN CORE         (the living state machine)
KNOWLEDGE GRAPH           (what the twin *knows about how the world works*)
STATE MEMORY              (what the twin *remembers happening*)
PREDICTION ENGINE         (what comes next)
COUNTERFACTUAL SIMULATION (what could have come instead)
DECISION INTELLIGENCE     (what should be done)
FEEDBACK LOOP             (what must be observed/done differently next)
```

Information flows *down* the ingest path ( Earth→decision) and *up* the tasking path (decision→Earth). The right-hand rail of D40 carries four cross-cutting organs: uncertainty/trust, autonomy/active learning, scenario library, and the human console.

## 3.1 Physical World
**What:** the true coupled system — burning front, plume, boundary layer, free troposphere, terrain, fuels. **Why a formal term:** a digital twin must declare its reference ontology; here it is the coupled reaction–diffusion–convection system with unknown microphysics, treated as a stochastic process Π with partially observable state X⋆(s,t). **Interface:** none digital; only through strata 2–3.

## 3.2 Satellite Observation Layer
**Function:** converts GOES-16/17 ABI radiances into the twin's *observation vector y(t)*: B07/B14/B16 brightness temperatures → `fire_proxy`, `cloud_height_proxy`, `raw_fire_bt`, `raw_cloud_bt`; B01–03 → `simulated_green` smoke texture; geolocation metadata `dist_km`. **Why it exists:** it is the *only* near-real-time sensory organ; it defines H (observation operator) and R (error covariance, r = 0.15σ for GOES-block in our EnKF). **Information out:** y(t) every 6 h + QC flags; **design extensions:** mesoscale sector tasking, GLM lightning feed, VIIRS/MODIS polar cross-calibration (bridges the diurnal sampling gap).

## 3.3 Atmospheric Layer
**Function:** ERA5 single levels (t2m, sp, u10/v10, z, BLH, CAPE, CIN, tp, SLHF, SSHF, fg10) + pressure levels (RH₈₅₀/₇₅₀/₆₅₀, u/v₂₅₀) + static substrates (DEM suite, vegetation cover/type). **Why:** supplies the *environmental control vector u(t)* and the physics residual's explanatory power; also R for analysis fields (r = 0.08σ for BLH, CAPE). **Key choice:** ERA5 *analysis* at 6-h cadence now; HRES/IFS *forecast* fields in forward-mode deployment — the twin treats them as different trust classes.

## 3.4 Data Fusion Layer
**Function:** harmonization (time ontology: 6-h cycles with explicit Δt), QC gates, **unit-audit gate** (§1.5 finding cast into law), gridding, and **derived physics**: ventilation (blh·w₁₀), bulk/directional shear, gust factor, Bowen partition, buoyancy forcing (CAPE−|CIN|), trigger index, RH-column statistics, dry-air entrainment, upslope-wind alignment, dry-spell memory, temporal derivatives. **Why:** physics-shaped features are where small-data regimes buy identifiability; every derived variable is registered in the feature dictionary (T02–T05) with units and lineage. **Output:** the harmonized observation frame z(t) (227 × 82 in the reference build).

## 3.5 Digital Twin Core
**Function:** owns the **state x(t)** (six blocks, Task 4), executes the **heartbeat** (Task 5): propagate ensemble → receive y(t) → innovation r → divergence pressure D → EnKF update → trust field Θ update → state commit (UTC-versioned snapshots). **Why a "core" and not a database:** the twin is a *dynamical system*, not a warehouse; its value is that x(t⁺) is legally comparable to x(t) while Prov(x) is fully traced. **Homeostat:** keeps ‖x−X⋆‖ bounded — measured: EnKF cuts state RMSE **45.0%** mean vs free-run (`T23`, `F33`, `F34`).

## 3.6 Knowledge Graph
**Function:** machine-reasonable store of *working knowledge* — events, regimes, drivers, mechanisms, outcomes, observations, counterfactuals, actions (`T28`, `T29`; schema figure `D44`). Edge signs are *learned* from the coupling kernel (`F31`) and fused with literature priors (e.g. dry mid-levels → entrainment → suppressed updraft). **Why:** it is the twin's *semantic memory* and its explanation substrate — every decision card in Task 9 is a KG subgraph.

## 3.7 State Memory
**Function:** four-tier cognition — sensory → short-term working → episodic event schemas → semantic archetypes; contrastive-key retrieval, α-fusion with short-term dynamics, offline consolidation with anti-forgetting penalty. **Why (evidence):** out-of-event *levels* are unlearnable from parameters alone on this cohort (§IX); memory fusion improves all three targets (`T21c`). **Novelty:** retrieval conditioning the *assimilation* (regime-prior covariances) — memory modulates K, not just forecasts.

## 3.8 Prediction Engine
**Function:** three channels (physics kernel P, learned residual L, memory continuation M) under a stacked **arbiter**; multi-horizon {6,12,18,24 h}; probabilistic via quantile + ensemble + conformal (Task 7 details). **Why three channels:** identifiability (P), nonlinearity (L), and regime transfer (M) are separated concerns on small cohorts; arbiter learns when each is right (β fitted on LOEO residuals).

## 3.9 Counterfactual Simulation
**Function:** applies *do-operators* to the control/initial conditions: marginal (wind×1.2, +5 K, RH×0.7), compound (S7), structural (relocation S6), physical-boundary probes (rain-out S4), and *feedback switches* (pyro-invigoration S8). Rolls the arbiter ensemble forward; returns future measures: P(severe|ω,h), Δrisk tornado, fan distributions. **Why:** decisions are comparisons of worlds, not forecasts of one world. **Delivered:** 46,224 scored futures (`T24/T25`, `F35–F38`).

## 3.10 Decision Intelligence
**Function:** converts the future ensemble into ranked *actions* with risk integrals and CVaR-robust selection; emits explanation bundles (dominant ω, SHAP drivers, analog justifications). **Why:** agencies act; they do not consume RMSE. Risk rubric `T27` binds probability bands to postures.

## 3.11 Feedback Loop
**Function:** (a) *observation tasking* — D(t) > threshold → request mesoscale sector/densified cadence; (b) *self-audit* — coverage/PSI/calibration sentinels trigger conformal recalibration or kernel retrain; (c) *human feedback* — analyst accept/override reinjected as labeled episodes. **Why:** this is the difference between a twin and a dashboard: the system *changes its own future observations*.

## 3.12 Inter-stratum information grammar

| # | Flow | Content | Contract |
|---|---|---|---|
| 1 | 2→4 | ABI proxies + QC | units, timestamps, provenance URI |
| 2 | 3→4 | ERA5/PL/static | same grid ontology |
| 3 | 4→5 | z(t) harmonized frame | schema T30 |
| 4 | 5→6 | committed states | UTC-versioned snapshots |
| 5 | 6↔7 | schemas ↔ edges | key-based, signed |
| 6 | 5,7→8 | x(t), analogs | horizons requested |
| 7 | 8→9 | futures distribution π(ω) | measure, not samples only |
| 8 | 9→10 | P(severe\|ω,h), Δrisk | CVaR-ready |
| 9 | 10→11 | actions + explanations | human-legible cards |
| 10 | 11→2/3/5 | tasking, recalibration | closed loop |
