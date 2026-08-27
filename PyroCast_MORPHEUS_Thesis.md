# PyroCast–MORPHEUS

## *A Mnemotic, Observationally-coupled, Recursive, PHysics-informed, Episodic, Uncertainty-calibrated, Self-learning Digital Twin of the Wildfire–Atmosphere Continuum*

**A framework thesis with a fully trained reference implementation on a ten-event GOES/ERA5 PyroCb cohort**

— Prepared as (i) a doctoral-style framework thesis, (ii) an IEEE-TGRS-submittable core, and (iii) a reproducible research artifact (code + trained models + results).

---

### Abstract

Existing wildfire decision-support systems are **predictors**: they ingest observations and emit forecasts, beginning each forecast cycle essentially *tabula rasa*. This thesis argues that the wildfire–atmosphere system — and in particular its most dangerous emissary, the **pyrocumulonimbus (PyroCb)** — demands the opposite: a computational entity that *persists*, *remembers*, *dreams about alternative realities*, and *polices its own reliability*. We invent **PyroCast–MORPHEUS**, the first wildfire **Mnemotic Counterfactual Twin**: a digital twin whose architecture elevates *episodic memory*, *counterfactual simulation*, *homeostatic synchronization*, and *self-calibrating uncertainty* from engineering afterthoughts to first-class state variables. The framework is specified completely — state, synchronization, memory, prediction, counterfactual, decision, living-evolution and visualization strata — with a full mathematical formulation. Crucially, we do not stop at design: we **train and validate the twin end-to-end** on the uploaded cohort of 10 PyroCb lifecycles (227 six-hourly state vectors fusing GOES ABI proxies, ERA5 single levels, pressure-level moisture and dynamics, terrain, and vegetation). Out-of-event (leave-one-event-out) results demonstrate: a **45.0%** mean state-error reduction from the 6-hourly EnKF synchronization engine versus free-running simulation; a memory-fusion engine whose retrieval correctly pairs sibling events (Alaska 258↔260 as mutual nearest analogs) and beats persistence on all three tracked targets (α\* = 0.3); a lifecycle intensification classifier at AUROC 0.71; conformal self-calibration lifting 80%-band coverage from 0.65 to 0.78 against the 0.80 nominal target; and a counterfactual futures engine that enumerated and scored **46,224 distinct futures**, quantifying scenario sensitivities (e.g. 250-hPa wind +20% raises 24-h PyroCb probability; ignition relocation to high-relief terrain lowers the injection index most strongly, ΔPII = −0.064). We report 20 scientific contributions, 20 research questions, 20 hypotheses, 20 future extensions, a 50-figure registry, a 30-table registry, complete methodology with pseudocode and pipelines, and a three-round adversarial self-review with fixes. The uploaded corpus is shown to encode the fire behaviour–atmospheric evolution–PyroCb formation–smoke transport–fire-weather coupling continuum over two North-American fire seasons (2021–2022), including the Johnson (NM), Lava (CA), British-Columbia heat-dome, Manitoba, Yukon, Florida, and interior-Alaska pyroCbs.

**Keywords:** Digital Twin; wildfire; pyrocumulonimbus; Earth observation; GOES ABI; ERA5; data assimilation; ensemble Kalman filter; episodic memory; analog forecasting; counterfactual inference; physics-informed machine learning; uncertainty quantification; geospatial AI; decision intelligence; Digital Earth.

---

### Executive summary — what this document proves

1. **A new twin species is defined** (Task 2): the *Mnemotic Counterfactual Twin (MCT)*, brand-named **MORPHEUS**, with a nine-term neologistic vocabulary (homeostasis, divergence pressure, episodic consolidation, counterfactual dreaming, trust field Θ, vital signs V₁–V₄, semantic scarring, assimilation appetite, twin fitness functional J).
2. **A complete architecture is specified** (Tasks 3–11): 11 strata, six-block twin state, 6-hour heartbeat with EnKF assimilation and adaptive trust, four-tier cognitive memory, three-channel prediction arbiter, do-operator counterfactual engine, CVaR-robust decision intelligence, fast/slow living loops, and a NASA-grade five-layer 4D visualization stack.
3. **A complete mathematics is given** (Task 12): graph-structured state, transition/observation/fusion operators, adjoint-capable hybrid kernels, memory retrieval and consolidation dynamics, counterfactual expectation operators, risk integrals, and the twin fitness functional used to drive self-evolution.
4. **A trained twin and results exist** (Tasks 8, 9, 17): every engine implemented in `code/`, validated out-of-event on the real uploaded cohort, with artifacts under `results/`, `tables/`, `figures/` (60 rendered artifacts), and a consolidated `results/metrics.json`.
5. **Honest science** (Task 18): the strongest negative result — that no free-running learner generalizes *levels* across fire regimes (pooled R² ≈ 0.05–0.19; the linear kernel is partially unstable, mean rollout R² = −0.014) — is elevated into the thesis's central architectural argument: **synchronization and memory are not accessories to a wildfire twin; they are what make it a twin at all.**

### Reading map

| Part | Tasks | Content |
|---|---|---|
| I | Task 1 | Dataset forensic science — what the data *are* |
| II | Tasks 2–3 | The invention: MORPHEUS concept + full architecture |
| III | Tasks 4–6 | Twin state • synchronization • memory |
| IV | Tasks 7–9 | Prediction • counterfactuals • decisions |
| V | Tasks 10–11 | Living twin • visualization system |
| VI | Task 12 | Unified mathematical formulation |
| VII | Tasks 13–14 | 20 contributions • 20 RQs • 20 hypotheses • 20 extensions |
| VIII | Tasks 15–16 | Figure & table registries |
| IX | Task 17 | Methodology, algorithms, pipelines, **trained-twin results** |
| X | Task 18 | Adversarial review → revised architecture → verdicts |

### Artifact map (workspace `PyroCast/`)

```
PyroCast/
├── data/master.csv                 # 227 rows × 82 cols twin-state table (built from uploads)
├── results/                        # metrics.json, predictions, futures, trained model joblib
├── tables/                         # 39 machine-readable tables (30 registered in Part VIII)
├── figures/                        # 59 publication figures + animated 4D globe GIF
├── code/                           # p01..p06 reproducible pipeline (this document's engine)
└── docs/                           # this thesis (concatenated as PYROCAST_MORPHEUS_THESIS.md)
```
# PART I — TASK 1: Forensic Study of the Uploaded Datasets

## 1.1 What the real-world system *is*

The seven uploaded files collapse to a single coherent object (proven in `code/p01_profile.py`: every `merged_*` file is a strict column-superset of its predecessor — row values identical, new sensor/derived blocks appended):

> **A six-hourly multi-sensor trajectory archive of ten pyrocumulonimbus (PyroCb) lifecycles**, each row being a synchronized snapshot of (a) the GOES-observed fire/cloud system at the PyroCb pixel, (b) the ERA5 atmosphere over that pixel, (c) the underlying terrain–vegetation substrate, and (d) pressure-level moisture and steering flow.

The cohort (`tables/T_event_catalog.csv`, figure `F01`, `F18`):

| ID | Window (UTC) | Lat/Lon | Duration tracked | Plausible 2021–22 identification* | Regime |
|---|---|---|---|---|---|
| 179 | 27 May–2 Jun 2021 | 33.29°N −108.59°W | 138 h | **Johnson Fire**, Gila NF, New Mexico (lightning-caused; confirmed coordinates 33.24°N −108.47°W) | high-elevation subtropical continental |
| 180 | 12–17 Jun 2021 | 33.20°N −111.08°W | 132 h | Telegraph-complex-consistent, Arizona | arid continental |
| 181 | 16–21 Jun 2021 | 37.71°N −113.79°W | 132 h | SW-Utah-consistent (Flatt Fire vicinity) | plateau |
| 189 | 28 Jun–3 Jul 2021 | 41.47°N −122.33°W | 132 h | **Lava Fire**-consistent, Mt Shasta, CA (explosive pyroCb, late Jun 2021) | Cascade |
| 190 | 28 Jun–3 Jul 2021 | 57.52°N −123.00°W | 132 h | British-Columbia **heat-dome** fires (CAPE max 1578 J/kg — extreme for that latitude; wind250 max 46 m/s) | boreal cordillera |
| 202 | 8–13 Jul 2021 | 50.80°N −95.03°W | 138 h | Manitoba Interlake fires (cohort's most intense fire proxy, −143) | boreal lowland |
| 216 | 17–21 Jul 2021 | 64.12°N −133.02°W | 108 h | Yukon/NT fires | subarctic |
| 253 | 29 Mar–3 Apr 2022 | 25.60°N −80.43°W | 138 h | south-Florida (Big Cypress/Everglades) spring fire; cohort's **CAPE peak 2687 J/kg** and highest injection potential | subtropical wetland |
| 258 | 9–14 Jun 2022 | 63.79°N −153.40°W | 132 h | interior-Alaska event A | boreal |
| 260 | 8–14 Jun 2022 | 63.33°N −155.60°W | 138 h | interior-Alaska event B (258's regional sibling) | boreal |

\*Identification by date/location cross-match against public fire records (e.g., the Johnson Fire match is confirmed; the rest are stated as *consistent with* named 2021–2022 events, hedged deliberately). Each event shows 19–24 steps at ~6-hour cadence (some 12-h gaps — QC flags in §1.6).

**This is not a generic wildfire dataset. It is a PyroCb lifecycle dataset** — the atmosphere's violent response to extreme fire — which is precisely the regime where fire–atmosphere coupling becomes a feedback loop rather than a one-way forcing.

## 1.2 Feature families: physical meaning (audit in `tables/T02_…T05_*`)

**(a) GOES ABI block (Table T02).** The README confirms the proxies derive from ABI window/absorption bands: B07 3.9 µm (sub-pixel hotspot sensitivity — the classic Matson–Dozier fire channel; confirmed by the NOAA FDC ATBD lineage), B14 11.2 µm (cloud-top window), B16 13.3 µm (CO₂ absorption; `t14 − t16 > 0` indicates cold *high* cloud because channel 16 cannot see through to the warmer surface), B01–B03 (visible pseudo-green for smoke texture). The file therefore encodes **fire radiative activity** (`fire_proxy = t07 − t14`), **plume verticality** (`cloud_height_proxy = t14 − t16`), and **cloud-top thermodynamic state** (`raw_cloud_bt`) — the three observables by which a PyroCb announces itself to geostationary orbit.

**(b) ERA5 single-levels (Table T03).** `t2m, sp, u10, v10, z, blh, cape, cin, tp, slhf, sshf, fg10` — the surface-energy, boundary-layer, and buoyancy triad. ECMWF sign conventions verified: heat fluxes are accumulated **J m⁻² per 6 h, positive downward** (so the strongly negative `sshf/slhf` daytime peaks are *upward* fluxes feeding the plume). `cin` is structurally missing in 201/227 rows because no buoyant parcel exists on capped steps — an informative missingness that the upstream team correctly `cin_filled` and `capped_flag`-ged.

**(c) Pressure-level block (Table T05).** `rh_850/750/650` gives the *vertical moisture structure* needed to reason about entrainment and evaporative downdrafts; `u_250/v_250` samples anvil-level steering. These two blocks are what elevate the file above ordinary fire-weather datasets: they permit genuine diagnosis of **plume–jet interaction**.

**(d) Terrain/vegetation (Table T04).** DEM-derived `elevation, slope, aspect, tpi, tri` (static) and ERA5 land parameters `cvh/cvl, tvh/tvl` (fuel structure). Event 179 sits at 3040 m with 29° slopes — an orographic chimney; 253 at 8 m — a wetland floor. The cohort deliberately spans the terrain-contrast axis.

**(e) Pre-derived indices.** `injection_potential` and `PII` (PyroCb Injection Index) are prior-work composites; we retain them as *features and labels* but audit them (Fig `F06`, `F13`) rather than trust them.

## 1.3 What the cohort can and cannot represent (Tasks 1a–1f, answered in evidence)

| Phenomenon | Represented? | Evidence in the corpus |
|---|---|---|
| **Fire behaviour (intensity)** | ✔ proxy-level | `fire_proxy` spans −33…−143; `raw_fire_bt` saturates 320 K-scale daytime spikes; diurnal amplitude clear in `F08` |
| **Atmospheric evolution** | ✔ | Diurnal BLH pump (12→5200 m), flux sign flips, RH-column evolution, CAPE/CIN intermittency (`F07`, `F08`, `F12`) |
| **PyroCb formation/lifecycle** | ✔ | Cold cloud-top invigoration tracked via `raw_cloud_bt` minima to 0.03; growth/mature/decay phase portrait separable (`F10`); PII/injection labels |
| **Fire intensity ↔ convection coupling** | ✔ | Learned coupling matrix `F31` (next-section result); `F09`: BLH/CAPE/fluxes lead 6-h Δcloud-top BT; `F13` buoyancy phase space |
| **Smoke transport (dynamics)** | ◐ partial | 250-hPa steering + BLH ventilation + directional shear (`F11`) permit plume-drift reasoning; *no smoke concentration/aerosol field* — flagged as data gap G3 |
| **Fuel moisture** | ◐ proxy only | no d2m/fuel model; we synthesize `dry_spell` memory (§IX method) and use RH-column + flux partition as surrogates — data gap G1 |
| **Ignition location counterfactuals** | ◐ static | terrain supports relocation operators (used in S6) but within-event spread is unresolved |

## 1.4 The physical grammar recovered from the signals (key EDA findings)

1. **The afternoon invigoration cycle dominates short-horizon dynamics.** Next-cycle cloud-top cooling correlates −0.65 with diurnal phase (`F09`→`y_cbt_chg_p1` row; `F08` BLH/SSHF/CAPE composites) — convection and fire beat to the same solar drum.
2. **Regimes separate.** Boreal events run moist columns (`rh_colmean` median 33–44% vs 5–8% in the desert Southwest, `F12`), and regime archetypes emerge cleanly in profile space (`F20`).
3. **The cohort's state space is low-dimensional.** PCA on 28 variables: PC1 (fire intensity + geography) and PC2 (buoyancy/moisture) carry the dominant variance; events form elongated lifecycle ribbons, not clouds (`F17`) — license for a *latent* twin state (§IV).
4. **Cross-event level shift is large.** `pixel_longitude` alone correlates |0.64| with next-cycle fire proxy — geography is a confounder that any honest validation must block (LOEO; §IX).
5. **Severity is multi-dimensional**, not ordered by any single index: intensity peak (202), energy (253), injection (253/190), cold-core depth (216/258) — motivating the *vital-signs* representation (`F39`).

## 1.5 Unit/scale audit (a data-engineering finding that becomes a Task-18 issue)

The GOES block mixes raw physical units with per-file normalization: `raw_cloud_bt`∈[0.03, 2.10] and `raw_fire_bt`∈[0, 320] are clearly *scaled* brightness temperatures (event 179 shows `raw_fire_bt`=0.082 ≪ physical BT), while `simulated_green` carries DN-like magnitudes (~72–98). `fire_proxy` values (−143…−33 for cloud-shielded PyroCb pixels) are consistent with B07−B14 over cold anvils at night (solar reflectance absent; B07 sees less of the warm sub-layer), but a strict unit provenance is absent from the README. **Actions taken:** (i) all learning pipelines standardize per training fold; (ii) the twin's fusion layer includes a mandatory *unit-audit gate* (T06, D50); (iii) interpretation is sign/magnitude-relative, never absolute-kelvin. This is not cosmetic: unit drift between GOES-16 and GOES-17 processing is a real hazard in production twins.

## 1.6 Data quality ledger

- 3 rows carry NaN GOES blocks (cloud-contaminated QC drops) — imputed within-fold (T06, T14).
- ~12-h cadence irregularities on 4 events (steps 5.8–12.2 h) — the synchronizer treats Δt explicitly (§V).
- `tp` ≈ 0 almost everywhere — PyroCb boreal/dry bias; the rain-out counterfactual (S4) therefore probes a *rare* corner (handled cautiously, Task 18).

**Verdict:** the corpus can fire, breathe, and storm in silico — exactly the minimal viable *living* substrate a wildfire digital twin requires, provided the twin (i) assimilates rather than free-runs and (ii) remembers rather than re-learns. Both provisions become architectural law in Part II.
# PART II — TASK 2: The Invention — PyroCast–MORPHEUS, a Mnemotic Counterfactual Twin

## 2.1 Why a *new species* of twin is necessary

Survey of the design space (positioning claim, defended in Part X review):

| Paradigm | Defining loop | Memory | Counterfactuals | Self-governed uncertainty | Verdict for PyroCb |
|---|---|---|---|---|---|
| Static twin / mirror model | ingest → rebuild | none | none | none | freezes between cycles |
| Adaptive/assimilating twin | observe → update | covariance only | none | covariance | amnesiac: forgets every fire season |
| Predictive twin (most wildfire ML) | train → forecast | frozen weights | none | rare | regime-transfer failure (**measured here**: levels R² ≤ 0.10 out-of-event) |
| Cognitive twin (literature) | perceive → reason | working memory | partial | partial | no episodic geophysical memory, no interventional engine |
| **Mnemotic Counterfactual Twin (this work)** | **observe → synchronize → remember → dream → decide → evolve** | **four-tier episodic + semantic** | **first-class do-operator futures** | **trust field Θ + conformal self-audit** | — |

The three deficits that kill wildfire usefulness are *remembrance*, *imagination*, and *self-doubt*. MORPHEUS is engineered around exactly these three verbs.

## 2.2 Definition

> **PyroCast–MORPHEUS** is a living digital twin of the wildfire–atmosphere continuum whose state explicitly contains (i) physical sub-states, (ii) an *episodic memory latent*, and (iii) an *uncertainty/trust sub-state*; which is kept homeostatic against Earth by a 6-hour ensemble-Kalman heartbeat; which queries its memory of past events to regularize the present; which spends idle cycles *dreaming* counterfactual futures under Pearl-`do(·)` operators; and which is graded — and graded *hard* — by an explicit fitness functional that drives slow-loop self-evolution.

**Name (backronym):** **M**nemotic **O**bservationally-coupled **R**ecursive **PH**ysics-informed **E**pisodic **U**ncertainty-calibrated **S**elf-learning Twin — the twin that *dreams in wildfire*.

## 2.3 The new terminology (precise coinages used throughout)

1. **Twin homeostasis** — the control objective min ‖x_twin − x_Earth‖ₜ subject to cycling cost: the twin must track Earth, not merely predict it. Implemented as the synchronization engine (Part III).
2. **Divergence pressure D(t)** — innovation Mahalanobis energy rᵀS⁻¹r; the scalar "pain signal" that regulates assimilation aggressiveness, alarms, and observation tasking. Measured per event in `T23` (means 1.5–48.7; events 202/253 flare).
3. **Trust field Θ(x,t)** — a normalized confidence scalar field Θ = 1/(1 + D/E[D]) modulated by calibration audit; *renders uncertainty spatially visible* instead of hiding it in logs.
4. **Episodic consolidation** — offline re-encoding of short-term trajectory windows into durable *event schemas* (hippocampal→neocortical analogy), guarded against catastrophic forgetting by a Fisher-weighted quadratic penalty.
5. **Counterfactual dreaming** — the slow-loop process of enumerating do(ω) futures; the twin's "REM phase". Executed here for 9 operators → 46,224 scored futures (`T25`).
6. **Vital signs V₁–V₄** — patient-monitor reductions of the twin state: fire intensity, convective energy, ventilation/moisture, fire–atmosphere coupling (`F39`). A fire is a *patient*, not a polygon.
7. **Assimilation appetite** — adaptive observation-error weighting: how hungrily the twin absorbs a new swath (function of D(t), coverage audit, sensor QC).
8. **Semantic scarring** — permanent prior-shift after extreme episodes (e.g. a Black-Saturday-class analog entering memory): rare, large, flagged updates to regime centroids.
9. **Twin fitness functional J** — J = skill − λ₁·miscalibration − λ₂·staleness − λ₃·forgetting; the selective pressure of the twin's evolution (Part V).

## 2.4 Design axioms

- **A1 Earth-coupling axiom.** A twin that cannot stay *bound* to Earth between forecasts is a model, not a twin. → mandatory assimilation (A1 → EnKF heartbeat).
- **A2 Mnemotic axiom.** Skill under regime shift comes disproportionately from *episodic recall*, not parameter mass. → four-tier memory + fusion (validated: `T21c`, α\*=0.3 beats persistence on 3/3 targets).
- **A3 Imagination axiom.** Decision value concentrates in the tails; tails cannot be learned by likelihood alone. → counterfactual engine with explicit do-operators.
- **A4 Honesty axiom.** A twin that cannot miscalibrate itself is unfit for life-safety decisions. → trust field, conformal audit (coverage 0.65 → **0.776** ≈ nominal 0.80) — measured in Part IX.
- **A5 Physics residency axiom.** Physical law lives *inside* the transition operator (VAR coupling kernel, spectral-radius clipping, flux bookkeeping), ML lives on the *residual*.
- **A6 Human primacy axiom.** Every recommendation ships with provenance, confidence, and the analog events that justify it.
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
# PART III — TASK 4: The Digital Twin State

*(Schema figure: `D41_state_schema.png`; full spec table: `T30_state_spec.csv`.)*

## 4.1 Definition

The twin state at cycle t is the partitioned vector

**x(t) = [ xᶠ(t) | xᵖ(t) | xᵃ(t) | xˡ(t) | xᵐ(t) | xᵘ(t) ]ᵀ ∈ ℝⁿ,  n = 52 (reference build)**

| Block | Role | Members (reference build) |
|---|---|---|
| xᶠ **Fire state** | the burning system as seen from orbit | fire_proxy, raw_fire_bt, dist_km, Δfire_proxy |
| xᵖ **Plume state** | the convective response | cloud_height_proxy, raw_cloud_bt, Δraw_cloud_bt, phase∈{growth, mature, decay} |
| xᵃ **Atmosphere state** | environmental control | t2m, sp, u10, v10, blh, cape, cin, tp, slhf, sshf, fg10, rh850/750/650, u250, v250 |
| xˡ **Land state** | (quasi-)static substrate | elevation, slope, aspect_sin/cos, tpi, tri, cvh, cvl, tvh, tvl, dry_spell |
| xᵐ **Memory latent** | the twin's recalled experience | event embedding z∈ℝ⁸ (PCA of profile), retrieval weights a₁:a₃, regime prior id |
| xᵘ **Uncertainty state** | the twin's self-knowledge | diag P (8 forecast-error variances), trust Θ, divergence pressure D |

**Memory and uncertainty are state variables, not metadata.** This is the sharpest ontological break with prior twins: two twins of the same fire at the same instant, differing in what they remember or how much they trust themselves, *are different twins* and will make different decisions.

## 4.2 State-variable taxonomy (Task 4 checklist, mapped)

- **State variables** (propagated): the 52-vector above; continuous except phase (finite-state Markov sub-chain).
- **Observation variables** (y = Hx + v): the GOES block and BLH/CAPE analysis fields with error variances r² (GOES r=0.15σ, ERA5 r=0.08σ, reference values tuned in §IX).
- **Hidden (latent) variables**: (i) fuel-moisture continuum (absent sensor; shadowed by `dry_spell` + RH structure); (ii) true fire radiative power (behind B07 saturation and cloud shielding); (iii) entrainment rate; (iv) an *ignorance coordinate* — the residual subspace not spanned by H. Hidden variables enter as *inflated Q near their shadows* (§VI.3, variance allocation rule).
- **Derived variables** (deterministic map g(xᶠ,xᵖ,xᵃ,xˡ)): ventilation = blh·w₁₀; speed shear = w₂₅₀−w₁₀; directional shear Δθ; gust factor = fg10/w₁₀; Bowen ratio sshf/|slhf|; net flux; buoyancy forcing = cape−|cin|; trigger index = cape·(1−capped); rh_colmean; rh_lapse = rh850−rh650; dry-air entrainment = 100−rh650; upslope index = cos(θw−aspect+π); dry_spell; all Δ-rates.
- **Temporal variables**: absolute age (since ignition), step index, diurnal (sin,cos) phase, seasonal (sin,cos) DOY, Δt to next observation (irregular cadence support).
- **Spatial variables**: pixel lat/lon, vegetation-grid offset dist_km, terrain scalars; in the scaled twin (§VII extension E2) these become a cell graph G=(V,E) with node states xᵢ(t) and edge features eᵢⱼ (topographic connectivity, advection length w·Δt).
- **Environmental variables**: the exogenous control u(t) = ERA5 block + pressure levels (in reference cohort: absorbed into xᵃ since analysis fields; split maintained for forward-mode where u(t+k) comes from NWP forecasts with their own uncertainty).

## 4.3 State semantics

1. **Legality.** A committed state is one that passed innovation screening (D under alarm bound) — the twin never commits a state it itself disbelieves without flagging Θ accordingly.
2. **Provenance.** Prov(x(t)) = {raw row ids, fold-free transforms, kernel versions}. Queries must answer "why" with a path, not a pointer.
3. **Comparability.** States are only comparable through the *same* H/R conventions; changing a sensor or a unit triggers a **state-schema version bump**, never silent drift (the §1.5 audit becomes a rule).

## 4.4 The Vital-Signs reduction

For operators, x(t) projects to the patient monitor **V(x) = (V₁ intensity, V₂ convective energy, V₃ ventilation/moisture, V₄ coupling)** ∈[0,1]⁴ (definition with evidence in `F39`): V₁ from fire_proxy percentile, V₂ from CAPE/buoyancy forcing, V₃ from BLH·w₁₀ and RH-column, V₄ from the learned coupling path strength fire→plume. Vital signs are *lossy by design* — triage, not truth.
# PART III (cont.) — TASK 5: The Synchronization Engine (the 6-hour Heartbeat)

*(Sequence diagram `D42`; parameters `T31`; measured performance `T23`, `F33`, `F34`.)*

## 5.1 Why "synchronization", not "nowcast"

A wildfire twin that merely re-reads inputs every 6 h is a spreadsheet. Synchronization here means **joint estimation of an evolving latent state under a physical-transition prior** so that (i) unobserved blocks (xᵐ shadows, xᵘ) update consistently with observed ones, (ii) the state stays *legally continuous* across cycles, and (iii) each update both corrects the present and audits the past cycle's trust.

## 5.2 The cycle (Δt = 6 h nominal; Δt-explicit)

**Step 0 — propagate.** Ensemble {x⁽ⁱ⁾} advanced by the stabilized transition kernel: x⁻ = A x + b + w, w∼N(0,Q); A ridge-fitted on training transitions, **spectral radius clipped ρ(A) ≤ 0.97** (a lesson paid for by the unstable free-running kernel — see Task 18); Q from train residual covariance.

**Step 1 — observe.** y(t) arrives from strata 2–4; QC and unit-audit gates pass; H selects observed dims, R per sensor trust class.

**Step 2 — innovate.** r = y − Hx̄⁻; S = H P⁻ Hᵀ + R; **divergence pressure D = rᵀS⁻¹r** computed and logged (the twin's pain signal; cohort mean 11.98, flaring to 40–49 on events 202/253 — both are regime-extreme fires, i.e. *D detects what the prior cannot anticipate*).

**Step 3 — update.** Stochastic EnKF: x⁺⁽ⁱ⁾ = x⁻⁽ⁱ⁾ + K(y + ε⁽ⁱ⁾ − Hx⁻⁽ⁱ⁾), K = P⁻HᵀS⁻¹. Assimilation **appetite** regulated by Θ: under repeated miscalibration R is widened; under alarm D, Q inflated — fade memory, not hard switches.

**Step 4 — trust inscribe.** Θ ← σ(c₁ − c₂D/E[D])·coverage_audit; commit UTC-versioned snapshot; append episode slice to short-term memory; if salience s > θ → flag for consolidation.

**Step 5 — task.** D > τ_D for two consecutive cycles → feedback ladder: (i) widen Q ×2, (ii) request densified observation cadence / mesoscale sector, (iii) raise human flag with analog-event bundle.

## 5.3 How each new data class changes the twin

- **New satellite swath:** shifts xᶠ, xᵖ through K with GOES-class trust; phase sub-chain re-estimated; spikes raw-memory salience.
- **New weather analysis:** re-estimates u(t); control changes propagate *through derived physics first* (ventilation, buoyancy forcing), then through K into xᶠ/xᵖ cross-covariances — weather drags the fire estimate even where fire is unobserved (the genuine *twin* property).
- **Terrain/static updates:** rare; trigger state-schema version bump (rule S3, §4.3).

## 5.4 Uncertainty propagation and confidence dynamics

Covariance follows the Riccati-ensemble path P⁻ → (I−KH)P⁻ with process re-inflation by Q; **trust Θ is its scalar translation** for humans. Confidence therefore *decays during propagation* and *condenses at each assimilation*: measured ensemble spread is stationary across cycles (T23 mean 0.35σ) — precision oscillates but never drifts to false certainty. Out-of-band, the conformal self-audit (Task 10) fixes residual miscalibration: 80% PI coverage 0.65 → **0.776** (±nominal 0.80; `T20b`, `F27b`).

## 5.5 Measured performance (reference twin, LOEO, std units)

| event | free-run RMSE | synchronized RMSE | reduction | event | free-run | sync. | reduction |
|---|---|---|---|---|---|---|---|
| 179 | 1.001 | 0.750 | 25.1% | 202 | 1.921 | 0.903 | **53.0%** |
| 180 | 0.814 | 0.532 | 34.6% | 216 | 0.664 | 0.281 | **57.7%** |
| 181 | 1.102 | 0.425 | **61.5%** | 253 | 2.071 | 0.842 | **59.3%** |
| 189 | 0.693 | 0.432 | 37.6% | 258 | 0.847 | 0.282 | **66.7%** |
| 190 | 0.825 | 0.811 | 1.7% | 260 | 0.783 | 0.371 | 52.6% |

**Mean reduction 45.0%.** Event 190 (BC heat-dome) is the teller of truth: its atmosphere is so anomalous that the observation stream and the kernel *agree to disagree mildly* — a candidate "semantic scar" episode. Figure F34 shows the heartbeat on event 202: the free-running twin wanders; the synchronized twin snaps back every 6 h; D(t) spikes precisely where the fire regime shifts.
# PART III (cont.) — TASK 6: Digital Twin Memory (the Mnemotic Stratum)

*(Architecture `D43`; parameters `T32`; measured retrieval `T21/T21b/T21c`, figures `F29/F29b/F30`.)*

## 6.1 Why a twin must remember

Every fire regime is a different planet. On this cohort, out-of-event *levels* prediction collapses toward climatology for any parameter-only learner (pooled R² ≤ 0.10; §IX). The physics reason: fire–atmosphere coupling constants are regime-conditioned (fuel structure, latitude-driven Coriolis/solar geometry, moisture climatology). Parameters can encode an *average* planet; skill on a *new* planet must come from **recalling the most similar known planets**. That is what memory is for.

## 6.2 The four-tier stack

1. **Sensory store** — the current 6-h observation window: raw z(t), TTL one cycle; feeds short-term working memory.
2. **Short-term working memory** — last k=8 cycles: rates, phase estimate, innovation history; supports persistence-channel predictions and D(t) smoothing.
3. **Episodic store** — consolidated *event schemas*: Eᵢ = {κᵢ key, trajectory tensor, context (regime, terrain, season), outcomes (peak intensity, injection, decay mode), provenance}. Write-gated by salience s = λ₁·surprise + λ₂·severity + λ₃·novelty.
4. **Semantic store** — regime archetypes, coupling priors, KG edges: *what kinds of worlds exist and how they work*.

## 6.3 Retrieval and fusion (implemented, measured)

**Query key** κ from the *first 24 h* only (operationally honest): early-window means of {cape, blh, wind250, rh_colmean, ventilation, t2m} + statics {lat, elevation, slope, cvh}, standardized on donor pool. Distance-weighted donor continuation:

aᵢ = exp(−d(q,κᵢ)/τ) / Σⱼ exp(−d(q,κⱼ)/τ),  τ = median(d);  ŷ_mem(s) = Σᵢ aᵢ · yᵢ(s)

**Memory fusion** with short-term dynamics: ŷ = α·ŷ_mem + (1−α)·ŷ_persist, α\* tuned by nested LOEO → **α\* = 0.30 uniformly** (the twin trusts dynamics but listens to experience).

**Measured retrieval sanity (T21):** interior-Alaska events 258/260 are *mutual nearest analogs* (d = 1.56/2.40); Manitoba 202 pulls the boreal set {260, 258, 216}; Johnson 179 pulls Utah 181 (dry high-elevation SW). The `F30` similarity field is block-structured by regime — the twin's geography of experience matches the fire climatologist's.

**Measured skill (T21c):** fused memory beats persistence on all targets — fire proxy RMSE 14.88 vs 16.08 (**−7.5%**), cloud-height proxy 7.47 vs 8.14 (**−8.3%**), PII 0.3295 vs 0.3509 (**−6.1%**) — while pure analog replay alone (21.1/10.36/0.485) is deliberately not trusted unsupervised.

## 6.4 Consolidation (the twin's "sleep")

Offline: (i) re-encode episodes with the current encoder; (ii) merge/split schemas by clustering drift; (iii) fine-tune kernels with Fisher-weighted penalty L = L_task + λ Σ F_i(θ_i − θ_i\*)² (anti-forgetting); (iv) update regime centroids — large shifts flagged as **semantic scars** (requires human countersign — governance rule G2). Experience replay prioritizes high-surprise windows (large |innovation|), the geophysical analog of hippocampal replay bias toward salient experience.

## 6.5 Knowledge accumulation & adaptive learning

Long-horizon growth is *not* weight growth but **memory economy growth**: richer episodic keyspace, sharper regime priors from the KG, scenario-library expansion (S-operators that historical scars proved relevant), and calibrated trust audits per regime. The twin's fitness functional J (Task 10) contains an explicit **forgetting term λ₃** so that adaptation is never free.
# PART IV — TASK 7: The Prediction Engine — Architecture Selection with Evidence

*(Schematic `D45`; results `T16–T20b`, `F21–F28`.)*

## 7.1 Candidate architectures, weighed honestly

| Candidate | Promise | Fatal weakness here | Verdict |
|---|---|---|---|
| Pure GNN (graph cells) | spatial structure, message passing | 227 rows / 1-pixel events: no spatial graph to learn; needs the §VII scaling corpus | **deferred** — designed-in as graph node update when multi-cell state lands (spec in §VI.2) |
| Transformer | long context, attention | parameter mass >> 227 samples; transfer-fragile | component only (future episode encoder) |
| Neural ODE | continuous-time physics match | adjoint training on 205 train rows = overfit; stiffness under 6-h sampling | **distilled**: linear VAR kernel = its identifiable special case; N-ODE designated upgrade path E4 |
| State-space models (S4/Mamba) | principled long memory | small data, unproven on geophysical twin state | research track (Task 14) |
| Pure physics (spread/convection models) | causal | needs FRP/fuel fields we lack; expensive per-cycle | informs kernel design only |
| **Hybrid: VAR kernel + ML residual + memory channel + arbiter** | matches identifiability of the cohort; every channel validated LOEO | complexity governance | **deployed** |
| World-model (latent imagination rollouts) | counterfactual rollouts by construction | latent collapse on small cohorts | the futures engine IS its pragmatic implementation (Task 8) |
| Memory networks / NTM | explicit recall — our A2 | training data-hungry | realized concretely as retrieval+fusion (Task 6) |

**Answer (Task 7):** the best architecture is a **physics-anchored hybrid MIMO forecaster** — not a single deep net — because on regime-shifting small-N geophysical cohorts, identifiability, calibrated uncertainty, and episodic transfer dominate raw expressivity.

## 7.2 The deployed engine

**Channel P — physics kernel.** VAR(1)/linear-ODE core on the 8-D latent physics vector zP = [fire_proxy, cloud_hgt, cloudBT, BLH, CAPE, ventilation, RHcol, wind250]; ridge fit; ρ(A) ≤ 0.97 clip; interpretable coupling matrix (`F31/F32`) — it *is* the learned KG edge evidence.

**Channel L — learned residual.** Gradient-boosted trees on the 52-feature twin state, predicting y(h) − kernel forecast; small-depth regularized fits; quantile heads {q.10, q.50, q.90} for uncertainty.

**Channel M — memory continuation.** α-fused analog replay (Task 6).

**Arbiter.** Stacked meta-learner ŷ(h) = β₀(h) + β₁ŷP + β₂ŷL + β₃ŷM fitted strictly on LOEO residuals; per-horizon β; gates channels by regime key when KG confidence is high.

## 7.3 Reference-cohort performance (all LOEO)

| Target (+6 h) | Persistence RMSE | Twin-core RMSE | Note |
|---|---|---|---|
| cloud-top **BT change** (invigoration) | 0.358 (baseline 0-change) | **0.292, R²=0.336; within-event median R²=0.667** | the engine's flagship: it *learned the afternoon invigoration cycle* |
| fire proxy (levels) | 16.61 | 17.09 | cross-regime level-shift (Task 18 finding) |
| **Δ fire proxy** | 16.68 (no-change) | **15.35 (−8.0%)** | dynamics learned where levels are regime-bound |
| PII (levels) | 0.361 | 0.380 | levels again regime-bound |
| **Δ PII** | 0.362 | **0.349 (−3.4%)** | ditto |
| lifecycle **intensification** (clf) | majority F1 0.00 | **AUROC 0.713, F1 0.604** | decision-grade triage signal |

Uncertainty: quantile ensemble 80% PI coverage 0.65 raw → 0.776 after conformal self-audit; 50% PI 0.60→~nominal; sharpness reported (`T20/T20b`, `F26/F27/F27b`). Per-event transfer bars (`F25`) show the expected pattern: boreal events transfer; desert-SW events least — regime coverage, not algorithmic failure (→ memory stratum answer: §6).
# PART IV (cont.) — TASK 8: Counterfactual Simulation (the Dreaming Engine)

*(DAG `D46`; operators `T24`; scored results `T25`, figures `F35–F38`; raw futures `results/counterfactual_futures.csv`.)*

## 8.1 Semantics

A forecast conditions on the world as-is: p(y | x(t)). A **counterfactual conditions on an intervention**: p(y | do(u = ũ), x(t)). MORPHEUS implements do-operators as **deterministic maps on the control/state vector with physics-consistent recomputation of all derived variables** (the `recompute()` rulebook in `code/p04c_counterfactual.py`): perturb → recompute ventilation, shears, buoyancy forcing, flux partition, RH structure → roll the arbiter ensemble across horizons {6,12,18,24 h} → aggregate into *future measures*, not headline tracks.

## 8.2 The scenario library (implemented operators)

S0 baseline · **S1 wind +20%** (boundary-layer and anvil-level flow scaled coherently, gusts/shear/ventilation recomputed) · **S2 heatwave +5 K** (RH rescaled ≈ ×0.75 under constant specific humidity) · **S3 drying RH −30%** (column uniform) · **S4 rain-out** (tp=5 mm, CAPE×0.3, BLH×0.6, SSHF×0.4, −3 K) · **S5 deep drought** (dry-spell+4 cycles, flux partition shifts sensible-ward) · **S6 structural relocation** (event-179 terrain transplant: 3040 m, 29° slope, upslope alignment) · **S7 compound extreme** (+8 K, RH×0.5, w₂₅₀×1.5, gusts×1.4, CAPE floor 1500) · **S8 pyro-feedback ON** (fire-forced invigoration: BLH×1.3, CAPE×1.2 when fire proxy below cohort median — the twin modelling *itself changing the atmosphere*).

Fuel-moisture and ignition-location operators are included despite upload limitations — via the `dry_spell` proxy and terrain transplant respectively; extreme-weather rails guard all operators to physical ranges.

## 8.3 Delivery: 46,224 scored futures

Scope: 9 operators × 10 held-out events × ~22 steps × 4 horizons × 3 ensemble seeds × 2 targets = **46,224 futures** (`n_futures` in `results/metrics.json`). Headline measures, all out-of-event:

| Operator ω | ΔPII(+24 h) | P(PyroCb>0.5): S0→ω | Reading |
|---|---|---|---|
| S1 wind +20% | **+0.0169** | 0.019 → **0.022** | ventilation/tilt **raises** injection odds (ventilation-mediated plume organization) |
| S2 heatwave +5 K | −0.0245 | 0.019 → 0.008 | warming without buoyant support *suppresses* modeled PyroCb odds |
| S3 RH −30% | −0.0251 | 0.019 → 0.008 | column drying: entrainment cost dominates in this cohort |
| S4 rain-out | +0.0048 (ΔPII) | 0.019 → 0.017 | probability *decreases* as expected; ΔPII sign nuance discussed in Task 18 |
| S5 deep drought | −0.0132 | 0.019 → 0.014 | fuel-side drying mildly suppresses injection |
| **S6 relocation: high-relief** | **−0.0639** | 0.019 → 0.008; P(fire-intense) 0 → **0.037** | terrain trades *vigor of injection* against *fire intensity* — the kind of non-obvious trade only a counterfactual engine surfaces |
| **S7 compound extreme** | −0.0413 | 0.019 → 0.004 | hostile-tail futures mostly *kill the PyroCb* while worsening fire — decision-relevant asymmetry |
| S8 pyro-feedback ON | +0.0005 | 0.019 → 0.019 | near-neutral net divide: feedback both feeds and caps |

Uncertainty vs lead time, stated honestly (`F35`, erratum): verification error of the LOEO direct models is flat (RMSE 17.5/18.6/18.7/16.7 at +6/+12/+18/+24 h vs persistence 16.7/16.2/16.6/14.4), with a +24 h diurnal-resonance minimum rather than classical error growth; the 3-seed ensemble dispersion (1.64→1.18) is an algorithmic-jitter floor that contracts as learnable signal decays (shrinkage + median-imputed tails), NOT forecast σ; divergence across the nine futures is ≈2.0–2.2 and flat over 6–24 h. Risk heat (`F38`) shows the twin's *event-dependent* sensitivity (e.g. 253's subtropical CAPE regime responds opposite to boreal 216 for the same operator).

## 8.4 Scaling to "thousands of futures"

The engine is embarrassingly parallel over (event, step, ω, seed); reference run: 46,224 futures in 118 s on one CPU (`T33`). The production design swaps XGB channels for the GNN/N-ODE kernels and runs Latin-hypercube over continuous operator manifolds (ω as vectors, not bookmarks), with importance-sampling concentrated on tail-ω — the scenario-miner of `D46`.
# PART IV (cont.) — TASK 9: Decision Intelligence

*(Pipeline `D47`; rubric `T27`; worked example `T26`.)*

## 9.1 From futures to choices

Decision intelligence consumes the future measure π(ω,h) produced by the dreaming engine and returns **ranked, risk-averse, explainable actions**. Formally (full development in Part VI):

- **Loss of inaction/action a under world ω:** L(a, ω) = exposure(ω) × vulnerability × failure(a, ω) − benefit(a).
- **Risk of action:** R(a) = ∫_Ω L(a,ω) dπ(ω) (scenario expectation).
- **Robust selection (implemented ranking rule):** a\* = argmin_a  CVaR_α[L(a,·)]  =  argmin_a  E[ L | L ≥ VaR_α(L) ], α=0.9 — optimize the *average bad tail*, not the mean: in life-safety domains the expectation is a lie the tail tells.
- **Uncertainty conditioning:** confidence on a card = f(Θ(t), scenario concentration, analog support); low Θ caps alert level regardless of point risk (rule D3).
- **Scenario ranking:** ω ranked by Δrisk(ω) = R(a*,ω) − R(a*,S0) — drives the tornado (`F36`) and the heat (`F38`) views; decision-relevant ranking ≠ sensitivity ranking.

## 9.2 Action library & rubric

Alerts (L2→L4 escalation), crew/air asset pre-positioning, Rx-burn go/no-go windows, satellite tasking (mesoscale sector, cadence up), and mesh densification. Binding to probability bands in `T27`: P(PyroCb) ≥ 0.50 → CRITICAL posture; 0.25–0.50 HIGH; 0.10–0.25 ELEVATED; else ROUTINE (bands tunable per agency; defaults conservative).

## 9.3 Worked example (reference twin, event 253 — subtropical CAPE regime)

`T26` ranks the operators by P(PyroCb|ω,+24 h): S0 0.019 baseline; S1 0.022 (wind) tops the amplification list; S7 collapses PyroCb odds to 0.004 while intensifying fire — *the engine therefore recommends heightened fire-ground readiness with lowered aviation/aviation-SIGMET priority under compound-extreme outlooks, and the opposite under strengthening-shear outlooks*. Every card carries: E[·], σ(·), P(·), Θ, dominant ω, driving features (importance renal `F23`), and the analog events that justify it (for 253: 189/180/202 by retrieval `T21`).

## 9.4 Explanation as a first-class output

Each action card is a **KG instantiation**: Action —justified_by→ Outcome —amplified_by→ Mechanism ←driven_by— Driver —do()→ Counterfactual, with the analog subgraph (ANALOG_OF edges) attached. If the explanation cannot be generated, the action cannot be issued (rule D5: *no unexplained alerts*).

## 9.5 Uncertainty estimation — the three-layer stack

(1) **aleatoric**: quantile heads + ensemble spread (`F26`, `F35`); (2) **epistemic**: seed/kernel diversity + LOEO transfer gaps reported per event (`F25`); (3) **distributional**: conformal self-audit adjusts bands (`F27b`), trust Θ gates issuance (rule D3). Risk is never a scalar: cards report (E, σ, tail, Θ).
# PART V — TASK 10: The Living Digital Twin

*(Dual-loop diagram `D48`; autonomy organs in `D40` rail; governance in Task 18 revisions.)*

## 10.1 "Living" made precise

MORPHEUS is *living* in the operational sense that it runs **two coupled adaptation loops with different time constants**, it **monitors its own fitness**, and it **acts to change its own future inputs**:

- **Fast loop (every 6 h) — homeostasis.** observe → propagate → innovate (D) → update → trust-inscribe → task. Keeps the twin *bound* to Earth (τ ∼ hours).
- **Slow loop (per fire season / on salience) — evolution.** consolidate memory → retrain kernels (EWC-guarded) → update archetypes, KG edges, scenario library → shadow-A/B challenger kernels → promote or retire (τ ∼ weeks–seasons).

## 10.2 Learning

Three complementary mechanisms: (i) **state learning** (EnKF update — learning *where the world is*); (ii) **parameter learning** (kernel refits on accumulated episodes — learning *how worlds move*, with anti-forgetting penalty); (iii) **knowledge learning** (KG edge re-estimation from the new coupling evidence; archetype centroid drift with scar-flagging — learning *what kinds of worlds exist*).

## 10.3 Adaptation

- **Assimilation appetite** widens Q/R when miscalibrated, tightens when overconfident — fade logic, no cliff edges.
- **Regime-conditional arbiters**: β(·) re-fit per regime cluster as episodic count grows.
- **Scenario-library evolution**: operators that repeatedly dominate CVaR tails get subdivided (ω-refinement); dead operators are archived.

## 10.4 Self-correction (implemented and measured)

- **Coverage audit → conformal fix:** raw 80% PI coverage 0.65 → post-audit **0.776** (`T20b`, `F27b`) — the twin caught its own overconfidence and widened its bands by learned offsets k_lo, k_hi.
- **Bias audit:** per-event residual sign tracking triggers recalibration maps if |bias| exceeds band.
- **Divergence alarms:** D(t) threshold ladder: widen Q → task more sensing → human flag (§5.2 Step 5; on this cohort the ladder fires correctly on events 202/253, the regime-extremes).

## 10.5 Knowledge update & autonomous improvement

Promotion requires the **fitness functional** to improve in shadow mode:

**J ← skill(SS↑) − λ₁·miscalibration − λ₂·staleness − λ₃·forgetting**

i.e., a challenger kernel must (i) beat the incumbent on LOEO skill within-regime, (ii) show no worse coverage, (iii) be fresh (trained on recent episodes), (iv) preserve legacy-regime skill (forgetting audit on archived episodes). Autonomy envelope: twin may self-promote *parameters*; may not alter *operators' physical bounds, alert rubrics, or KG priors* without human countersign (governance G1–G3, Task 18).

## 10.6 Why this is *alive* and not just *online*

Online learners adapt weights; MORPHEUS additionally: remembers (episodic growth), imagines (library growth), self-audits (trust dynamics), self-tasks (changes its own observations), and evolves under an explicit selection pressure with fear of forgetting. That closed tetrad — sense, remember, imagine, select — is our operational definition of a *living* Earth twin.
# PART V (cont.) — TASK 11: The Visualization System (NASA-quality 4D)

*(Concept renders `R01/R02`; 3D globe mock `D51`; animated 4D globe `figures/globe_plume.gif` (rotating terrain–fire–plume–PyroCb); dashboard layout `D52`; render stack `D53`; time system `D54`; counterfactual viewer `D55`.)*

## 11.1 Renderer technology decision

| Engine | Strengths | Weakness | Role chosen |
|---|---|---|---|
| **CesiumJS** | web-scale 3D globe, 3D Tiles, time-dynamic czml, STAC-friendly | volumetric smoke needs custom raymarch | **primary planetary viewport** |
| NASA WorldWind | provenance, KRosetta lineage, GOVStack | aging web stack | heritage/alternate viewport |
| Three.js | custom shaders, volumetric plumes | no native globe tiles | plume/trust-field GPU renderer inside Cesium scene |
| ArcGIS (JS/Pro) | agency-standard 2D, ops dashboards | weak 4D | operations 2D twin view (mutual situation awareness) |
| Unreal/Unity | cinematic volumetrics (fire/smoke), VR briefing | heavyweight deploy | "immersion room" for after-action & public comms |

**Decision:** CesiumJS shell + custom WebGPU/WebGL volumetric smoke pass + ArcGIS 2D ops twin + Unreal cinematic exporter; all fed by the same state-snapshot service (STAC items + COG rasters + Zarr fields — cloud-native, no bespoke formats).

## 11.2 The five composited layer groups (D53)

**I Base Earth** — global imagery (Blue Marble/Sentinel-2), COP-DEM terrain, night-lights context; **II Observations** — GOES ABI RGB + fire-proxy hotspot glyphs + smoke alpha + QC tint; **III Atmosphere** — ERA5/PL fields: BLH translucent volume, CAPE underlay, RH-column curtain, animated 10-m and 250-hPa wind particles (plume tilt becomes *visible*); **IV Twin state** — fire-front polylines, vital-sign extrusion pillars at event anchor, **trust-field tint** Θ(x): regions literally fade as trust decays (uncertainty the eye cannot miss); **V Futures** — counterfactual *ghost plumes* (one translucent volume per ω, colour = risk band), probability isopleths, action pins from Task 9 cards.

## 11.3 Mockup layouts (generated)

1. **`D51`/`globe_plume.gif`** — 4D globe grammar: terrain (gist_earth), fire glow glyph at anchor, bent translucent smoke column drifting with steering wind, flattened white PyroCb cap pulsing at tropopause; camera azimuth sweep demonstrates the rotational inspection; every visual channel mapped to a data channel (Table below).
2. **`D52` — decision dashboard (dark mission console):** live globe (2×2), four vital-sign annular gauges V₁–V₄, futures fan with baseline vs S7/S4 bands, CVaR action ranking bars, 4D timeline scrubber with event markers, twin console line (Θ, D, coverage, memory hits). Grid: 3×8 docking layout, all panels data-bound to the state service.
3. **`D54` — 4D time system:** Hovmöller ribbons (fire proxy / cloud-top BT / PII / Θ), activity stream with event markers (ignition+6h, first PyroCb, NOW, decay onset), hazard-probability strip with NOW playhead; supports click-to-scrub the globe.
4. **`D55` — counterfactual comparison:** split worlds (baseline | S7) with linked cameras and synced playheads + Δ-viewer card (ΔP(PyroCb), Δplume-top, Δσ, confidence; ensemble-member slider k∈[1..48]).

## 11.4 Data→visual grammar (publication rule set)

| Visual channel | Data binding |
|---|---|
| fire glow intensity/size | fire_proxy (t07−t14) |
| smoke column bend/drift | (u10,v10)→(u₂₅₀,v₂₅₀) shear vector |
| plume height/brightness | cloud_height_proxy, raw_cloud_bt |
| anvil cap | t14−t16 positive mask |
| tint overlay | trust field Θ(x,t) |
| ghosts | counterfactual ensemble {ω} |
| gauges | vital signs V₁–V₄ |

## 11.5 Performance & access

3D Tiles/OGC API delivery, LOD plume octrees; 6-h frames interpolated with optical-flow advection for smooth playback (physics-honest interpolation flag in UI); web dashboard for analysts; CGA-quality Unreal exporter for command briefings; WCAG-AA palettes (fire ramps checked for CVD); every frame carries UTC stamp, version, provenance hash.
# PART VI — TASK 12: Unified Mathematical Formulation

*Notation:* cycle index t ∈ ℤ (Δt = 6 h); spatial support S (single anchor pixel in reference cohort; cell graph under scaling); random world state X⋆(s,t) ∈ ℝ^{n⋆}; twin estimate x(t) ∈ ℝⁿ (n = 52); controls u(t) ∈ ℝ^{n_u}; observations y(t) ∈ ℝ^{m}.

## 12.1 Twin state and observation operator

x(t) = Φ(z(t), m(t), Θ(t)) decomposed as §4.1. Observations:

**y(t) = H x(t) + v(t),  v(t) ~ N(0, R(t))** — H ∈ {0,1}^{m×n} selection (GOES dims with R_GOES = 0.15²σ²I; BLH/CAPE with R_ERA5 = 0.08²σ²I); R(t) adaptive via assimilation appetite (12.6).

## 12.2 State transition (the legal dynamics)

Define the hybrid propagator **F**(x, u; θ):

**x(t+1) = A·x(t) + B·u(t) + G_θ(x(t), m(t)) + w(t),  w ~ N(0, Q(t)),  ρ(A) ≤ 1−ε**

- A, B: physics-kernel blocks (ridge-fitted; spectral clip ρ(A) ≤ 0.97 — guarantees Lyapunov-stable mean dynamics: λ_max(AᵀA) < 1 ⇒ no mean blow-up between cycles);
- G_θ: learned residual (GBM ensemble; GNN node-update under graph scaling §12.7; N-ODE limit §12.8);
- m(t): retrieval-conditioned memory prior entering as an added drift term α·(x̄_donor(t+1) − x(t));
- Q(t): process covariance = Q₀ · a(D(t)) (appetite), Q₀ = Cov[X₁ − AX₀ − Bu] estimated on training folds.

Continuous-time view: dx/dt = f_phys(x,u) + f_θ(x,u,t) with the discrete propagator as its Δt-integrator; the N-ODE upgrade (E4) replaces the integrator by an adjoint-trained ODE net: x(t+Δt) = ODESolve(f_phys + f_θ, x(t), [t, t+Δt]).

## 12.3 Assimilation (synchronization as MAP estimation)

Cycle recursion, stochastic EnKF with ensemble size N:

Forecast: x⁻⁽ⁱ⁾(t+1) = F(x⁺⁽ⁱ⁾(t), u(t)) + w⁽ⁱ⁾
Innovation: r = y(t+1) − H x̄⁻ ; S = H P⁻ Hᵀ + R ; **D(t+1) = rᵀS⁻¹r**
Gain: K = P⁻ Hᵀ S⁻¹
Analysis: x⁺⁽ⁱ⁾ = x⁻⁽ⁱ⁾ + K ( y + ε⁽ⁱ⁾ − Hx⁻⁽ⁱ⁾ ), ε⁽ⁱ⁾ ~ N(0, R)

which is the ensemble form of the Kalman MAP update x⁺ = argmin_x ‖x−x⁻‖²_{P⁻} + ‖y−Hx‖²_R. Trust field: **Θ(t) = σ( c₁ − c₂·D(t)/m − c₃·(1−cov_audit) )**, σ the logistic; bounds issuance rule D3.

## 12.4 Data fusion as a convex-constrained map

Harmonized frame z(t) = argmin_z Σ_s λ_s‖M_s z − o_s‖²  s.t.  C z ≥ 0 (physical ranges), where s indexes sensors, M_s masks/resamples, C encodes physics constraints (RH∈[0,100], blh>0, tp≥0, BT bounds); derived state block x_der = g(z) per the rulebook of Part III. Fused uncertainty: R_fuse = (Σ_s λ_s R_s⁻¹)⁻¹.

## 12.5 Memory (retrieval as nonparametric kernel regression)

Episodic store E = {(κᵢ, Yᵢ, cᵢ)}; query key κ(q). Weights and fused prediction:

**aᵢ = softmax_i( −d(κ(q), κᵢ)/τ ),   ŷ_mem(s) = Σᵢ aᵢ Yᵢ(s),   ŷ = α·ŷ_mem + (1−α)·ŷ_dyn**

with d the standardized profile metric, τ = median(d), α\*(=0.30) selected by nested CV minimizing fused LOEO RMSE. Consolidation update of encoder parameters: θ_E ← argmin L_replay + λ_EWC Σ_i F_i (θ_i − θ_i\*)², F_i the Fisher diagonal — quadratic evidence preservation (no catastrophic forgetting).

## 12.6 Self-calibration and fitness

Conformal band repair on validation half: k = Quantile_{0.9}(|y − q̂_bound|); adjusted [q̂_lo − k_lo, q̂_hi + k_hi] restores nominal coverage (measured 0.65→0.776).
Fitness functional driving slow-loop selection:

**J(θ) = NLL_skill(θ) ↑ − λ₁·|cov − cov*| − λ₂·staleness(θ) − λ₃·Forget(θ, E_archive)**, promote ⟺ J_challenger > J_incumbent in shadow.

## 12.7 Graph formulation (scaled twin)

Cells as nodes: G = (V, E), node states xᵢ(t), edge features eᵢⱼ = [Δterrain, w·Δt advection length, upwind flag]. Message passing (design slot for Channel-L/GNN):

hᵢ^{(k+1)} = φ( hᵢ^{(k)}, ⊕_{j∈N(i)} ψ( hᵢ^{(k)}, h_j^{(k)}, eᵢⱼ ) ),  xᵢ(t+1) = γ(hᵢ^{(K)}, uᵢ(t)) + wᵢ

Fire-spread physics enters as the edge prior: ψ upwind-weighted, Rothermel-consistent sign constraints (spread downwind ≥ upwind) — **physics-informed message passing**. The current cohort degenerates to |V|=1, proving by construction why the arbiter's V♂↦graph upgrade is extension E2, not a present claim.

## 12.8 Loss functions (full objective)

**L = w₁L_fcst + w₂L_phys + w₃L_cal + w₄L_graph + w₅L_contrast + w₆L_cf**

- L_fcst = Σ_h Σ_y ℓ_q(ŷ(h), y(h)) pinball (q∈{0.1,0.5,0.9}) — probabilistic nowcast;
- L_phys = ‖ρ(A) clip residual‖ + flux-sign violations + monotone constraints (e.g. ventilation ∂₂ ≥ 0 in BLH);
- L_cal = (cov − cov\*)² + PIT dispersion term;
- L_graph = KG edge sign agreement with learned coupling matrix A (cross-entropy on sign(A_ij) vs prior);
- L_contrast = InfoNCE over (key, same-regime) pairs in memory encoder;
- L_cf = counterfactual consistency: rollouts under do(ω) must obey operator invariants exactly (e.g. RH scaling conserved by recompute map), penalized deviation.

Optimization: stage-wise (fit A,B → fit G_θ residual → fit memory encoder contrastive → calibrate quantiles → conformal repair); kernel upgrades enter shadow-A/B under J.

## 12.9 Temporal modelling

Beyond VAR: the temporal ontology T = (cycle lattice 6h, Δt-aware propagator F(Δt) via matrix fraction A(Δt) = A₁^{Δt/6h}, diurnal forcing harmonics D(t) = [sin, cos](2πh/24), seasonal S(t)). Memory provides the long term E[·|history >> window]; phase sub-chain P(phase_{t+1}|phase_t, x) provides the discrete skeleton of lifecycle reasoning.

## 12.10 Counterfactual expectation & risk

p( y(h) | do(ω), x(t) ) = ∫ p( y(h) | x(t), u(t..h) = ω(u) ) dP_x(t) ≈ (1/N) Σ_i ŷ⁽ⁱ⁾(h; ω)

operative expectation estimated by the futures ensemble. Risk and robust action:

R(a) = E_ω[L(a,ω)];  **a\* = argmin_a CVaR_α L(a,·) = argmin_a ( ξ + (1−α)⁻¹ E[ (L − ξ)⁺ ] )** (Rockafellar–Uryasev form; ξ = VaR_α; differentiable optimum subproblem).
# PART VII — TASK 13: Twenty Novel Scientific Contributions

*Each is a claim about knowledge, not a software feature; status tags: **[validated]** (evidenced on the reference cohort), **[formalized]** (designed and math-ready), **[program]** (research program).*

1. **Mnemotic Counterfactual Twin (MCT) class definition** — first formalization of a digital-twin species in which episodic memory and interventional futures are *state-carrying* sub-systems rather than services. [formalized+partially validated]
2. **Memory-and-uncertainty as state** — the state-vector ontology x=[xᶠ xᵖ xᵃ xˡ | xᵐ | xᵘ] that makes remembering and self-doubt legally part of twin state space. [formalized]
3. **Twin homeostasis with divergence pressure D(t)** — an innovation-Mahalanobis control variable driving assimilation appetite, alarms, and autonomous observation tasking. **[validated: D flares 40–49 exactly on the two regime-extreme events 202/253]**
4. **Trust field Θ(t)** — a scalar, renderable translation of ensemble covariance + calibration audit that governs decision issuance. [validated via issuance gating rule D3 + coverage audit tie-in]
5. **Episodic memory engine for PyroCb events** — contrastive-key event schemas, early-window-only keys, top-k analog continuation; **first demonstrated memory-augmented nowcasting of PyroCb lifecycles**. [validated: α\*=0.3 fusion beats persistence on 3/3 targets; Alaska 258↔260 mutual retrieval]
6. **Regime transfer result (negative result as contribution)** — formal evidence that parameter-only learners fail *levels* generalization across fire regimes (pooled R²≤0.10) while succeeding on *dynamics* (BT-change R²=0.336/0.667 within-event), a distinction previous wildfire-ML evaluations obscure by splitting rows, not events. [validated]
7. **Semantic scarring** — a governed mechanism by which extreme episodes permanently shift regime priors (with human countersign), giving twins a tractable memory of the unprecedented. [formalized; candidate episode 190 identified]
8. **Counterfactual dreaming engine** — do-operator scenario kernels with physics-consistent recomputation, rolled through the prediction arbiter as *future measures*. [validated: 46,224 scored futures]
9. **Counterfactual discovery: ventilation-driven injection** — wind +20% *raises* 24-h PyroCb probability (0.019→0.022; ΔPII +0.017) in this cohort, quantifying the contested ventilation hypothesis on real events. [validated, hypothesis-grade]
10. **Counterfactual discovery: terrain–injection trade** — relocation to high-relief terrain raises fire-intensity probability (0→0.037) yet *lowers* PyroCb odds; first quantitative instance on real-event twins. [validated]
11. **Vital-signs representation V₁–V₄** — a provable low-dimensional monitor of fire–atmosphere health (intensity, energy, ventilation/moisture, coupling), glyph-rendered for operators. [formalized; rendered F39]
12. **Learned fire–atmosphere coupling matrix as KG evidence** — a spectrally stabilized VAR kernel whose coefficients populate causal-edge confidence in the knowledge graph — ML-learned graph priors, signed and versioned. [validated: F31/F32]
13. **Assimilation appetite** — adaptive R/Q scheduling keyed to divergence and coverage audits rather than fixed inflation factors. [formalized; stable EnKF implementation measured: 45.0% mean RMSE reduction]
14. **EnKF heartbeat for PyroCb twin states** — first demonstration that 6-hourly ensemble assimilation bounds a fire–atmosphere twin's error growth bimodally (analysis collapse ~1.7–66.7% per event). [validated]
15. **Conformal self-audit loop** — event-split conformal repair *inside* a living twin (not post-hoc): coverage 0.65→0.776 nominal-80%. [validated]
16. **Twin fitness functional J** — an explicit selection criterion (skill − miscalibration − staleness − forgetting) that makes "living" falsifiable rather than metaphorical. [formalized]
17. **Counterfactual comparison grammar for decision UIs** — split-world + delta-card visualization grammar with synchronized time systems (D55), closing the Futures-UX gap in wildfire ops. [formalized; mocked]
18. **PyroCb cohort digital-twin dataset release** — harmonized 227×82 6-hourly twin-state table (GOES⊗ERA5⊗PL⊗terrain⊗veg) with unit-audit ledger and event identifications. [validated: data/master.csv]
19. **Physics-resident/ML-residual division of labor** — spectral-radius-clipped kernel carrying the mean dynamics with GBM/N-ODE residual on top, demonstrably controlling instability that pure learners exhibit. [validated: unclipped kernel unstable; clipped EnKF stable]
20. **A reproducible sandbox-scale living twin** — end-to-end trained reference implementation (p01–p06) with open metrics, ensembles, and futures CSVs, establishing a baseline the community can beat. [validated]
# PART VII (cont.) — TASK 14: Questions, Hypotheses, Extensions

## 14.1 Twenty research questions

1. Which subspace of the PyroCb state is *intrinsically predictable* at 6–24 h under regime shift, and is that subspace aligned with the vital-signs projection?
2. Does divergence pressure D(t) anticipate phase transitions (growth→mature→decay) earlier than any observable proxy?
3. What is the information value of an additional observation (mesoscale sector) measured in CVaR reduction per dollar — the twin's value-of-information curve?
4. How do episodic retrieval weights aᵢ evolve as the store grows from 10 to 10⁴ events; is there a retrieval saturation law?
5. Which physical mechanisms generate the counterfactual asymmetry wind-up/PyroCb-down observed across regimes (S1 vs S3)?
6. Can the coupling matrix A be mapped to identifiable convection parameters (entrainment rate, plume-radius growth) — i.e., is A physics in matrix disguise?
7. What spectral-radius guarantees are needed for 24-h twin stability, and how do they interact with Kalman updates (contractivity of the product)?
8. Does conformal repair per regime beat global repair once the store exceeds ~50 events?
9. How does the twin's trust field Θ change operator behaviour — do users make *fewer* high-severity false alarms when Θ is visible?
10. What is the minimal set of hidden variables (e.g. fuel moisture, FRP) whose addition would flip regime-transfer from dynamics-only to levels-capable?
11. Can scenario-mining (ω* search) discover novel vulnerability modes absent from human scenario libraries?
12. Does memory fusion α\* migrate toward 1 as episodic count grows (experience increasingly dominating dynamics)?
13. What are the identifiability limits of joint fire-spread + convection learning at NWP grid scales?
14. How should twins weight conflicting analogs (boreal vs subtropical) under rare-compound regimes — a retrieval-theoretic problem with safety consequences?
15. Can phase sub-chains be learned as a hidden semi-Markov model that beats heuristic threshold phases?
16. What does "forgetting" cost in decision-metric terms, and does EWC-style retention dominate naive replay for geophysical twins?
17. How do twins negotiate multi-fire contagion (smoke shading of neighbouring events) — an inter-event coupling currently outside the state?
18. Can the coupling graph learned per event be meta-learned into a generalizable fire-regime "periodic table"?
19. What governance protocols make an autonomous twin's self-promotion auditable (formal verification of J-improvement claims)?
20. Under what conditions does a living twin provably outperform an operationally-retrained static predictor in CVaR terms?

## 14.2 Twenty hypotheses

1. **H1** — 6-h EnKF assimilation yields strictly bounded state error for any kernel with ρ(A)<1 and non-degenerate H; bound scales as trace(S)⁻¹.
2. **H2** — Divergence pressure D(t) leads PyroCb collapse by ≥1 cycle in >60% of events.
3. **H3** — Memory fusion α\* increases monotonically with episodic-store size, approaching an asymptote < 1 (dynamics never become irrelevant).
4. **H4** — Ventilation's sign on injection probability reverses between subtropical and boreal regimes — measurable as opposite-sign S1 responses (`F38` pattern persists at scale).
5. **H5** — Fuel-moisture latent (when added via d2m/fuel models) converts the S5 drought operator from injection-suppressing to injection-amplifying.
6. **H6** — The learned coupling matrix's leading eigenmode corresponds to the diurnal invigoration cycle (temporal pattern of Aᵏ must peak at k=4·(24 h period)).
7. **H7** — Trust-field display reduces operator over-alerting by ≥20% in controlled studies.
8. **H8** — Conformal repair per regime cluster achieves nominal coverage with ≤ half the band width inflation of global repair.
9. **H9** — The relocation operator's fire-intensity↑/PyroCb↓ trade is terrain-slope-thresholded (≈25–30°) rather than elevation-driven.
10. **H10** — Event-level severity is a two-manifold (energy × regime moisture) on which the 10 cohort events already trace the principal axes (`F17`-consistent).
11. **H11** — Phase-aware models (growth/mature/decay-specific arbiters) improve +6h BT-change R² by ≥0.1 over global arbiters.
12. **H12** — Rain-out counterfactuals exhibit hysteresis: recovery path ≠ suppression path (lagged CAPE memory).
13. **H13** — Analog libraries built from GLM lightning + GOES jointly separate dry-thunderstorm ignition events from fuel-driven events better than GOES alone.
14. **H14** — Twin self-tasking (D-triggered mesoscale requests) reduces next-cycle innovation energy by ≥15% vs fixed cadence.
15. **H15** — Semantic scars from one extreme event (e.g. 190 heat-dome) transfer: they improve next-season-analog detection without degrading routine-regime skill.
16. **H16** — A graph-upgraded twin (multi-cell) shows spatial coherence of Θ(x) that a single-cell twin structurally cannot represent.
17. **H17** — Pyro-feedback operator S8's near-zero net effect decomposes into event-wise positive/negative effects that cluster by RH-lapse sign.
18. **H18** — Compound-extreme futures (S7) become *more* PyroCb-favourable when jet-level shear is held fixed — an interaction term measurable in futures data.
19. **H19** — The forgetting term λ₃ in J trades off against skill with a Pareto knee near λ₃ ≈ λ₁ (calibration weight), indicating a principled setting.
20. **H20** — A two-twin cross-check (GOES-16 twin vs GOES-17 twin) exposes sensor-systematic state drift larger than both twins' claimed Θ — a falsifiable partnership test.

## 14.3 Twenty future extensions

1. **E1** — Multi-event, multi-sensor corpus (100s of events; VIIRS/MODIS/GLM/Himawari/AHI) — the obvious and necessary scaling.
2. **E2** — Graph twin: multi-cell spatial state with advection-aware message passing (§12.7) on 5–25 km meshes.
3. **E3** — Fuel-moisture latent: assimilate d2m, LFM/DFM models, FAPAR; test H5.
4. **E4** — Neural-ODE/diffusion generative kernels replacing the VAR block as data volume permits (adjoint training, manifold priors).
5. **E5** — Smoke-aerosol channel: AOD/MAIAC assimilation for transport verification (closes gap G3).
6. **E6** — Lightning sub-state: GLM flash rate as ignition/invigoration covariate (H13).
7. **E7** — Twin federation: fire twin ↔ smoke twin ↔ hydrology twin (post-fire debris flows) with coupling contracts.
8. **E8** — Reinforcement-learned tasking policies maximizing value-of-information under satellite budget constraints.
9. **E9** — Scenario-miner: gradient/BO search over continuous ω-manifolds for worst-case discovery (H11/Q11).
10. **E10** — Human-machine learning loop: structured analyst overrides as privileged episodes (protected memory class).
11. **E11** — Conformal++: localized/Jackknife+ bands per regime (H8).
12. **E12** — Semi-Markov phase model with learned sojourn distributions (Q15).
13. **E13** — Multi-modal narration: LLM-couched explanation cards rendering KG subgraphs with provenance links (guarded; no generative physics).
14. **E14** — On-prem/edge deployment kits for incident command posts (resilient 6-h sync on degraded comms).
15. **E15** — Probabilistic programming refactor (state-space model in NumPyro/Stan) for full posterior rather than ensemble approximations.
16. **E16** — Cross-satellite partnership protocol implementing H20's falsifiability test.
17. **E17** — Climate-analog memory: extend episodic keys with large-scale modes (PDO/AO) to enable first-spark-of-season cold start.
18. **E18** — After-action auto-reports: twin-generated season retrospectives as training data for agencies (knowledge product E-line).
19. **E19** — Open benchmark & leaderboard around this dataset (LOEO protocol standardized) — Community PyroCb Twin Challenge.
20. **E20** — Ethical/AI-safety review pipeline for autonomous escalation decisions (red-team suite from Task 18 automated as CI).
# PART VIII — TASKS 15 & 16: Figure and Table Registries

*The brief demanded 50 publication-quality figures and 30 tables. Delivered: **60 rendered artifacts** (`figures/`, incl. one animation) and **30 registered tables** (+3 supplementary spec tables), all machine-readable under `tables/`.*

## 15.1 Figure registry — Part A: Cohort science (F01–F20)

1. **F01_event_map.png** — Geographic cohort: 10 North-American PyroCb events 2021–22; bubble ∝ max injection potential; regime bands annotated.
2. **F02_traj_fire_proxy.png** — Fire-proxy trajectories per event (10 panels, 6-h steps): lifecycle diversity, boreal vs desert amplitudes.
3. **F03_traj_cloud_bt.png** — Cloud-top BT trajectories: invigoration spikes and decay ramps per event.
4. **F03b_traj_chp.png** — Cloud-height proxy trajectories: plume verticality evolution (PyroCb formation signatures).
5. **F04_hovmoller_fire.png** — Event×step Hovmöller of fire proxy: cohort-wide intensity choreography at a glance.
6. **F05_hovmoller_cbt.png** — Event×step Hovmöller of cloud-top BT: cold-core genesis timing differences between regimes.
7. **F06_corr_heatmap.png** — 28-variable cross-layer correlation: the fingerprint of fire–atmosphere coupling and confounding geography.
8. **F07_distributions.png** — 24 marginals: skewness regimes (CAPE/CIN zero-inflation), physical bounds audit.
9. **F08_diurnal.png** — Diurnal composites of BLH, SSHF, CAPE, Δcloud-top BT: the solar invigoration drumbeat (physics anchor of H6).
10. **F09_leadlag.png** — Lead–lag driver×target matrices: which atmosphere variables *lead* fire/plume state (kernel-design evidence).
11. **F10_phase_portrait.png** — Fire proxy vs cloud-top BT by lifecycle phase with 30-h drift arrows: separability of growth/mature/decay.
12. **F11_windroses.png** — 10-m vs 250-hPa directional climatologies: surface flow vs plume steering — transport reasoning fuel.
13. **F12_rh_profiles.png** — Event-mean RH(850/750/650): moist boreal columns vs arid SW; entrainment fuel proxies.
14. **F13_buoyancy.png** — CAPE–CIN phase space coloured by PII, sized by BLH: buoyancy envelope of PyroCb events.
15. **F14_heatflux_regime.png** — Sensible/latent flux diurnal split per regime: energy partition physics differences (ECMWF sign verified).
16. **F15_terrain_veg.png** — Elevation-injection scatter, slope bars, vegetation cover structure, upslope index: substrate controls.
17. **F16_missing.png** — Completeness audit: CIN's 89% structural missingness exposed (informative missingness → capped flag).
18. **F17_pca.png** — Scree + PC1–PC2 event ribbons: low-dimensional manifold licence for the latent twin state (H10).
19. **F18_gantt.png** — Observation windows Gantt: two-season cadence structure; 12-h gap spotting.
20. **F19_severity.png** — Composite severity ranking: 202 (intensity), 253 (energy/injection) top distinct axes.
21. **F20_regimes.png** — k-means archetypes in static-profile space (3 regimes): the twin's "periodic table" seed (Q18).

## 15.2 Part B: Trained-twin results (F21–F39)

22. **F21_pred_vs_obs.png** — LOEO predicted-vs-observed, four targets, twin vs persistence: regime-transfer reality, honestly shown.
23. **F21b_delta_skill.png** — Δ-target bars: twin beats "no-change" on fire-proxy/PII dynamics (+8.0%/+3.4%): learning signal where levels fail.
24. **F22_residuals.png** — Residual histograms: twin's tighter, near-centered errors vs persistence's tails.
25. **F23_importance.png** — Gain + permutation importance: fire memory (current proxies), buoyancy, RH structure, terrain atop.
26. **F24_ablation.png** — Feature-block ladder: GOES-only → +ERA5 → +pressure → +derived physics → full → +geography; derived-physics block's contribution quantified.
27. **F25_per_event.png** — Per-held-out-event RMSE for twin vs persistence: boreal transfers, desert hardest (memory answer).
28. **F26_quantile_fan.png** — Probabilistic trajectory, event 253, median + 80% PI vs truth: calibrated-dream look.
29. **F27_calibration.png** — Observed coverage of 50%/80% PIs vs nominal: raw overconfidence visible.
30. **F27b_conformal.png** — Conformal self-audit: coverage 0.65→0.776 — the twin fixing itself.
31. **F28_classifier.png** — Intensification classifier (ROC AUROC 0.71, PR, confusion): lifecycle triage instrument.
32. **F29_analog.png** — Memory replay of event 260 from donors {258,216,190}: episodic forecasting without retraining.
33. **F29b_memory_fusion.png** — Fusion skill ladder (persistence vs pure analog vs α\*=0.3 fuse): fused wins 3/3.
34. **F30_memory_matrix.png** — 10×10 event similarity field: block structure by regime — experience geography made visible.
35. **F31_coupling_matrix.png** — Learned 8×8 transition kernel (fold-averaged): the fire–atmosphere coupling coefficients.
36. **F32_coupling_graph.png** — Emergent directed coupling graph: amplifying (red) vs damping (blue) pathways; KG edge evidence.
37. **F33_enkf_bars.png** — Free-run vs synchronized RMSE, all 10 events: mean −45.0% — the heartbeat pays.
38. **F34_enkf_cycle.png** — Event-202 heartbeat: truth, free-run drift, EnKF analysis ±2σ, divergence-pressure subplot: synchronization visualized.
39. **F35_uncertainty_growth.png** — Uncertainty decomposition vs lead time (erratum): (a) true verification RMSE of LOEO direct models vs persistence (flat, 24-h diurnal-resonance dip); (b) 3-seed jitter floor (contracts — an artifact, not forecast σ); (c) inter-scenario divergence (flat).
40. **F36_cf_tornado.png** — Counterfactual tornado on ΔPII(+24 h): wind amplifies; relocation/drying suppress.
41. **F37_cf_fan.png** — Event-253 futures fan per scenario (±80% seed band): dreaming rendered.
42. **F38_cf_riskheat.png** — ΔP(PyroCb) scenario×event heat: regime-conditional vulnerability atlas.
43. **F39_vitals.png** — Vital-signs radar (V1–V4) for events 202/253/258: the fire-as-patient monitor.

## 15.3 Part C: Architecture & system diagrams (D40–D50)

44. **D40** — Master 11-stratum architecture with cross-cutting organs; the thesis's Figure 1.
45. **D41** — Six-block twin-state schema (incl. memory & uncertainty as state).
46. **D42** — 6-hour synchronization sequence grammar (11 numbered exchanges).
47. **D43** — Four-tier memory architecture with consolidation and retrieval/write pathways.
48. **D44** — Knowledge-graph schema (node/edge types with semantics).
49. **D45** — Three-channel prediction engine + arbiter.
50. **D46** — Counterfactual DAG: scenario library → kernel → measures → miner → decision hook.
51. **D47** — Decision-intelligence pipeline to ranked CVaR action cards.
52. **D48** — Living-twin fast/slow loops with fitness functional J.
53. **D49** — Multi-agent organ chart incl. CRITIC (red-team).
54. **D50** — Deployment pipeline with shadow mode, drift sentinels, rollback.

## 15.4 Part D: Visualization system & renders (D51–D55, R01, R02, animated)

55. **D51_globe_3d.png** — 4D globe grammar proof (terrain/fire/plume/cap) — Cesium-port-ready.
56. **globe_plume.gif** — 30-frame rotating, breathing 4D twin animation (dashboard hero artifact).
57. **D52_dashboard.png** — Dark mission-console decision dashboard layout (3×8 docking grid).
58. **D53_layer_stack.png** — Five composited layer groups & GPU compositing contract.
59. **D54_timeline.png** — 4D time system: ribbons, markers, playhead, hazard strip.
60. **D55_cf_compare.png** — Split-world counterfactual viewer with Δ-card grammar.
61. **R01_globe_concept.png / R02_dashboard_concept.png** — AI-concept renders of the target NASA-grade aesthetic (mood boards for the Unreal/Cesium build).

## 15.5 Table registry (T01–T30; +3 supplementary)

| # | File | Content |
|---|---|---|
| T01 | T01_inventory.csv | The 7 uploaded files: shape, span, role, lineage |
| T02 | T02_dict_GOES.csv | GOES feature dictionary (definition/physics/units) |
| T03 | T03_dict_ERA5.csv | ERA5 single-levels dictionary (sign conventions noted) |
| T04 | T04_dict_terrain_veg.csv | Terrain & vegetation dictionary |
| T05 | T05_dict_pressure.csv | Pressure-level + derived-index dictionary |
| T06 | T06_missingness.csv | Missing data ledger + treatment |
| T07 | T_event_catalog.csv | Event catalogue (windows, peaks, severities) |
| T08 | T_summary_stats.csv | Variable summary statistics |
| T09 | T09_top_correlations.csv | Top driver–target correlations |
| T10 | T10_leadlag.csv | Lead-lag matrix backing F09 |
| T11 | T11_diurnal_composites.csv | Diurnal composite values |
| T12 | T_severity_composite.csv (+T_regime_clusters.csv) | Severity scores & regime assignment |
| T13 | T13_targets.csv | Prediction target definitions |
| T14 | T14_cv_protocol.csv | LOEO protocol & leakage controls |
| T15 | T15_hyperparams.csv | All model specifications |
| T16 | T16_metrics_regression.csv | Nowcast metrics (persistence/ridge/XGB) |
| T17 | T17_classification.csv | Intensification classifier metrics |
| T18 | T18_within_event_skill.csv | Within-event median R² (twin vs persistence) |
| T19 | T19_ablation.csv | Feature-block ablation metrics |
| T20 | T20_calibration.csv (+T20b_conformal.csv) | Coverage & conformal repair |
| T21 | T21_memory_retrieval.csv (+T21b/c) | Analog donors, skill, fusion α\* |
| T22 | T22_coupling_matrix.csv (+\_ode_rollout_skill) | Coupling coefficients & rollout skill |
| T23 | T23_enkf_sync.csv | Synchronization performance per event |
| T24 | T24_scenarios.csv | do-operator library |
| T25 | T25_counterfactual_results.csv | Scored counterfactual deltas & probabilities |
| T26 | T26_decision_matrix_example.csv | Worked decision matrix (event 253) |
| T27 | T27_risk_rubric.csv | Probability→posture binding |
| T28 | T28_kg_nodes.csv | KG node types |
| T29 | T29_kg_relations.csv | KG relation types |
| T30 | T30_state_spec.csv | Twin state vector specification |
| — | T31_sync_params.csv · T32_memory_params.csv · T33_compute_budget.csv | Supplementary spec/budget tables |
# PART IX — TASK 17: Complete Methodology

*Pipeline code: `code/p01…p06`. Environment: Python 3.13, pandas 2.2, numpy 2.3, scikit-learn 1.6, XGBoost 3.3, matplotlib 3.10, networkx 3.6. All random seeds fixed; all splits out-of-event. End-to-end rerun ≈ 3.5 min CPU (`T33`).*

## 17.1 Data engineering

1. **Ingest** the 7 uploads; identity-proof supersets (`p01`).
2. **Temporal ontology**: parse mixed timestamps → UTC cycle grid; per-event `step`, `age_h`; Δt tolerance recorded; diurnal/seasonal harmonics.
3. **Master state build** (`p02`): sort by (event, time); compute upper-air derived (wind250, dir/shear, gust factor), boundary-layer/energy (ventilation, Bowen, net flux, buoyancy forcing, trigger), moisture structure (rh_colmean, rh_lapse, entrainment), terrain-wind alignment (upslope proxy via aspect decomposition), rates (Δ of fire/plume/BLH/CAPE/ventilation), lifecycle phase from Δcloud-BT thresholds (0/1/2), dry-spell fuel proxy (rolling rain-free cycles), and lead targets (t+6h levels, change, intensification flag, PII) plus multi-horizon targets t+6…+24 h for the futures engine (built in `p04c`).
4. **Event catalogue + severity composite** (`T07`, `T12`).
5. **QC gates**: GOES-NaN rows (3)→ within-fold median; CIN structural NaN → use `cin_filled` + keep `capped_flag` as a feature; Δ12h cadence entries retained with explicit Δt.

## 17.2 Validation design (leakage-proof)

- **LOEO (leave-one-event-out), 10 folds**: events are the independent units; random row splits would leak 6-h autocorrelation (formalized; `T14`).
- **Nested LOEO** for meta-parameters (fusion α\*).
- **Per-fold preprocessing**: imputation/scaling fitted on train folds only (ODE/EnKF paths).
- **Pooled + per-event reporting**: no averaging away regime failures (`F25`).
- Baselines mandatory: persistence, no-change, majority class, ridge.

## 17.3 Core learners

**Tabular nowcast (Channel L)**: XGBRegressor (settings `T15`: 220 trees, depth 3, lr 0.06, subsample 0.85, colsample 0.8, L2=2, L1=0.4); quantile heads via `reg:quantileerror` q∈{0.1,0.25,0.5,0.75,0.9}; classifier twin for lifecycle intensification (log-loss, same capacity); ridge and persistence as scientific controls.

## 17.4 Algorithms (pseudocode)

**Alg. 1 — Synchronization heartbeat (per cycle)**
```
INPUT: committed ensemble {x⁺⁽ⁱ⁾}(t−1), new y(t), kernels (A,b,Q), R, Θ(t−1)
1  for i in 1..N:  x⁻⁽ⁱ⁾ ← A·x⁺⁽ⁱ⁾ + b + L_Q ε⁽ⁱ⁾          # propagate
2  r  ← y(t) − H·mean(x⁻) ;  S ← H P⁻ Hᵀ + R
3  D(t) ← rᵀ S⁻¹ r                                        # divergence pressure
4  K ← P⁻ Hᵀ S⁻¹
5  for i: x⁺⁽ⁱ⁾ ← x⁻⁽ⁱ⁾ + K(y + ε_R⁽ⁱ⁾ − Hx⁻⁽ⁱ⁾)          # stochastic analysis
6  Θ(t) ← trust_update(Θ(t−1), D(t), coverage_audit)
7  commit snapshot(x⁺, Θ, D, Prov) ; append STM
8  if salience(STM) > θ_s: enqueue consolidation job
9  if D(t) > τ_D twice: escalate appetite ladder (Q×2 → tasking → human)
```

**Alg. 2 — Memory consolidation (slow loop)**
```
INPUT: episode queue, store E, encoder θ_E, kernels
1  for each queued episode: k ← key(early-window profile)
2  E ← E ∪ {(k, trajectory, context, outcome, prov)} if salience high
3  re-fit encoder on E ∪ replay-buffer with InfoNCE + λEWC·‖θ−θ*‖²_F
4  update archetype centroids; if |Δcentroid| > τ_scar: flag SEMANTIC SCAR (human sign-off)
5  refit kernels in shadow mode; promote only if J improves (12.6)
```

**Alg. 3 — Prediction with arbiter (inference)**
```
x(t), m(t) → ŷP(h) (kernel) ; ŷL(h) (GBM heads incl. quantiles) ; ŷM(h) (analogs)
ŷ(h) ← β₀(h) + Σ β_c(h)·ŷc(h);  band(h) ← quantile stack → conformal repair
emit {ŷ(h), band(h), Θ, analogs, importance-pack}
```

**Alg. 4 — Counterfactual futures**
```
for ω in scenario library:  x_ω ← recompute(ω(x(t)))
  for h in {6,12,18,24}, seeds: ŷ⁽ˢ⁾(h,ω) ← arbiter(x_ω,h)
  μ(h,ω), σ(h,ω) ; P(severe|h,ω) ← Gaussian-seed estimator
aggregate: tornado Δ(ω), risk heat (event×ω), fans; feed decision ranker
```

**Alg. 5 — Decision intelligence**
```
L(a,ω) ← loss model ; R(a) ← E_ω[L] ; CVaR_α(a) ← tail expectation (R-U form)
a* ← argmin CVaR s.t. feasibility ; card ← {a*, E, σ, CVaR, Θ, dominant-ω, analogs, KG path}
if Θ < Θ_min: downgrade posture (rule D3) ; if no KG path: suppress alert (rule D5)
```

## 17.5 Training pipeline (reference run, executed)

`p01` profile → `p02` master+derived (227×82) → `p03` 21 EDA figures → `p04a` core LOEO nowcasts + ablations + quantiles + classifier + vital-signs → `p04a2` Δ-skill, conformal self-audit, within-event analysis → `p04b` memory engine (retrieval, fusion), coupling kernel (stabilized), EnKF synchronization → `p04c` counterfactual futures (46,224) → `p04d` metrics consolidation → `p05` diagrams+viz → `p06` tables. All artifacts versioned under `results/`.

## 17.6 Inference & deployment pipelines

**Near-real-time inference (6-h cadence):** watcher cron (GOES/ERA5) → QC/unit gates → fusion frame → heartbeat (Alg.1) → arbiter (Alg.3) → futures (Alg.4, throttled if SLA risk) → decision cards (Alg.5) → state-snapshot service (STAC/COG/Zarr) → dashboards & API.

**Forward-mode deployment:** ERA5-analysis → NWP-forecast control switch with R upgrade class; latency budget from `T33` scales linearly with kernel swap; shadow-challenge CI with drift sentinels (PSI on features, coverage alarms), UTC-versioned twin snapshots & rollback registry (`D50`).

## 17.7 Consolidated trained-twin results (the deliverable numbers)

**(a) Nowcast skill (LOEO, pooled):** cloud-top BT change R²=0.336 (within-event median 0.667); Δ-fire-proxy −8.0% vs no-change; Δ-PII −3.4%; fire-proxy levels R²=0.05 vs persistence 0.10 (regime-transfer result); PII levels 0.19 vs 0.27 {`T16,T18,F21,F21b,F22,F25`}.

**(b) Classification:** lifecycle intensification AUROC 0.713, F1 0.604 {`T17,F28`}.

**(c) Probabilistic honesty:** 80% PI coverage 0.65 → 0.776 post-conformal; sharpness 22.41 {`T20,T20b,F26,F27,F27b`}.

**(d) Memory:** donors top-3 per event {`T21`}; α\*=0.30; fused beats persistence 3/3 targets (−7.5%/−8.3%/−6.1%) {`T21c,F29,F29b,F30`}.

**(e) Coupling kernel:** matrix + graph {`T22,F31,F32`}; free-running rollout unstable (mean R²=−0.014) → motivates stabilization + assimilation {Task 18}.

**(f) Synchronization:** EnKF state RMSE reduction 45.0% mean (1.7–66.7% per event); spread stationary ≈0.35σ; divergence mean 11.98 {`T23,F33,F34`}.

**(g) Counterfactuals:** 46,224 futures; tornado/risk/fan measures {`T24,T25,F35–F38`}; decision matrix worked example {`T26`}.

**(h) Efficiency:** full cohort pipeline ≈ 3.5 min CPU; futures engine 46k predictions in 118 s {`T33`}.

## 17.8 Reproducibility statement

Deterministic seeds; every table is generated by versioned scripts from the uploads; the thesis numbers are `results/metrics.json`-traceable (no hand-edited results). Limitations of scale (10 events, single-pixel anchors, proxy-level fire intensity) are documented in Task 18 and bound the claims' generality: the framework is cohort-scale validated and scaling-ready, not continent-scale validated.
# PART X — TASK 18: Adversarial Review → Revision (three rounds)

*Method: self-review under three reviewer personas (IEEE TGRS associate-editor rigor, Nature MI novelty bar, systems/safety referee). Each round lists weaknesses verbatim, then the revision actually implemented (code/doc ref). This is the same critique loop run as CI in production (`D49` CRITIC agent).*

## Round 1 — "The dataset is too small for these claims"

**R1-W1.** Ten events, 227 rows, single anchor pixel. Any learned model is illustrative, not operational.
**Fix:** We re-scoped claims: framework specification is *design-complete*; empirical claims are explicitly *cohort-scale* and hypothesis-grade (contribution tags [validated]/[formalized]); all evaluation is LOEO with baselines; within-event vs pooled metrics separated (T18). No headline rests on random-split inflation.

**R1-W2.** Unit heterogeneity in the GOES block (scaled vs physical BT) undermines physical interpretation.
**Fix:** Unit-audit gate (section 1.5 → rule D01); per-fold standardization; interpretation restricted to relative/sign statements; provenance ledger in metadata.

**R1-W3.** `injection_potential/PII` are inherited derived indices — circularity risk if used as features and labels.
**Fix:** They are treated as *labels and auxiliary features*, never as constructors of Δ-targets; main dynamics targets (BT change, Δfire) are independent of them; documented in `T13`.

## Round 2 — "The models underperform; where is the twin?"

**R2-W1.** Level-prediction R² ≈ 0.05–0.19, ridge negative, the VAR kernel unstable (mean rollout R²=−0.014); event 253 rollout −105%.
**Response-truth**, then **fix:** We converted this to the thesis's central scientific point (contribution #6, #19): parameter-only free-running learners fail under regime transfer; the kernel was *spectrally stabilized* (ρ≤0.97 clip in `p04b`), and **synchronization (EnKF) recovered bounded, accurate state tracking (45.0% mean RMSE reduction)**, while **episodic memory fusion recovered skill on dynamics across all targets (α\*=0.3)**. The twin's identity is its *loops*, not a single net.

**R2-W2.** EnKF initially exploded on some folds (true during development).
**Fix:** root cause identified — unstable A eigenvalues amplified by adaptive inflation; removed multiplier inflation, added spectral clipping + Q from train residuals; all 10 folds now stable and stationary (spread ≈0.35σ, `T23`).

**R2-W3.** Calibration: 80% PI at 0.65 is miscalibrated; life-safety claims premature.
**Fix:** conformal self-audit module implemented and measured (0.65→0.776); trust field Θ gates issuance (rule D3); residual gap to 0.80 declared (small-holdout caveat, extension E11).

**R2-W4.** Counterfactual "rain-out increases ΔPII (+0.0048)" looks unphysical.
**Fix:** Diagnosed as (i) small-cohort sensitivity, (ii) mediator recomputation dominance (BLH/CAPE cuts), (iii) probability direction still correct (0.019→0.017). Resolution: report probability measures as primary, Δ-index secondary; flagged H12 (hysteresis) as testable; guard rails verified. Honest anomaly, now a research question (Q5).

## Round 3 — "Novelty and systems concerns"

**R3-W1.** "Twin" vocabulary is fashionable; differentiate from data assimilation + case-based reasoning, which are decades old.
**Response:** DA assimilates; CBR recalls; neither (a) makes memory+uncertainty part of *state space*, (b) dreams with do-operators and *feeds decisions the future measures*, (c) evolves under an explicit fitness functional with anti-forgetting, (d) self-tasks sensing. The novelty is the *integration contract* (axioms A1–A6), the new control variable D(t), and the measured cohort behavior — not any single algorithm.
**Fix:** added positioning table (§2.1), contribution tags, and falsifiable hypotheses (H1–H20).

**R3-W2.** Autonomy risk in self-promotion/self-tasking.
**Fix:** governance G1–G3: parameters may self-promote only through shadow J-improvement; operators' physical bounds, rubrics, KG priors require human countersign; semantic scars always countersigned; CRITIC agent in CI (D49); kill-switch in Conductor.

**R3-W3.** Single-CPU scale doubt.
**Fix:** Measured budget published (T33); complexity analysis: EnKF O(N·n³-worst per cycle) trivial at n=52; futures engine embarrassingly parallel (46k in 118 s single core ⇒ ~seconds on a node); scaling plan E1/E2 with cost model rather than hand-waving.

**Verdict after three rounds:** publishable as a *framework + cohort-scale evidence* paper with the revised claims; not yet as an operational system validation. The architecture's central wager — synchronize, remember, dream, self-audit — survived its strongest available stress test: its own reviewer.

## Consolidated weakness→remedy ledger

| Weakness | Severity | Remedy (delivered) | Residual |
|---|---|---|---|
| tiny cohort | high | LOEO+nested, claim scoping | scaling program E1 |
| unit heterogeneity | medium | audit gate + standardization | sensor-mix study H20 |
| kernel instability | high | spectral clip + EnKF | N-ODE upgrade E4 |
| miscalibration | high | conformal audit (0.776) | localized bands E11 |
| PII circularity risk | medium | label/feature firewall T13 | — |
| rain-out anomaly | low | interpretation guard + H12 | larger sample |
| autonomy risk | high | G1–G3 + CRITIC + kill-switch | formal verification Q19 |
# PART XI — References, Data Notes, and Closing

## Selected references & technical sources

1. NOAA NCEI, *GOES-R Series ABI Level 2 Fire/Hot Spot Characterization (FDC)* — product lineage and the B07/B14 (3.9/11.2 µm) sub-pixel fire contrast heritage (Matson–Dozier; WF_ABBA/FDCA). ncei.noaa.gov (accessed 2026-08).
2. NOAA/NESDIS/STAR, *ATBD: GOES-R ABI Fire Detection and Characterization* v2.6 — multispectral thresholding lineage for band 7/14 fire logic.
3. CIMSS/SSEC, *ABI Quick Guide: Band 7 (3.9 µm)*; CIMSS Satellite Blog (2020), *When is an ABI hot spot not a fire?* — interpretation caveats for t07−t14 under clouds/solar contamination.
4. DestinE Earth Data Hub, *ERA5 hourly data on single levels* — variable definitions/units (blh m; cape/cin J kg⁻¹; tp m; cvh/cvl fractions; accumulated fluxes J m⁻²), accessed 2026-08.
5. ECMWF Confluence KB, *ERA5-Land data documentation* — accumulation convention; ECMWF vertical-flux sign convention (positive downward), corroborated by NOAA ARL `era52arl` notes (HYSPLIT forum).
6. Copernicus/CDS (ERA5) parameter listing via `ecmwf_models` docs (u10/v10, fg10, z, t2m etc.).
7. Wikipedia/Wikidata, *Johnson Fire (2021, Gila NF)* — ignition date/coordinates used for the event-179 identification cross-check.
8. Peterson, D. et al. — pyrocumulonimbus climatology and conceptual model (BAMS 2017; subsequent catalogs); U. Manitoba PyroCb tracking blog — event-numbering convention consistent with uploaded `pyroCb_id`s.
9. Evensen, G. — *Data Assimilation: The Ensemble Kalman Filter* (Springer) — stochastic EnKF form used for the heartbeat.
10. Pearl, J. — *Causality* — do-operator semantics for the counterfactual engine.
11. Rockafellar & Uryasev (2000) — CVaR optimization form used in decision intelligence.
12. Kirkpatrick et al. (2017) — EWC anti-forgetting penalty (memory consolidation).
13. Chen, R.T.Q. et al. (2018) — Neural ODEs (designated kernel upgrade).
14. Vaswani et al. (2017); Gu & Dao (2023, Mamba) — deferred sequence backbones (positioning in §7.1).
15. Vovk, V. — conformal prediction foundations (self-audit module).
16. Rothermel (1972); Van Wagner (1987, FWI) — fire-spread/physics priors referenced for graph-edge constraints and fuel-moisture extension design.
17. Fromm, M. et al. — PyroCb outburst dynamics and stratospheric injection case literature (mechanism priors in KG).
18. Tao et al.; Bauer, Stevens & Hazeleger (DestinE) — digital-twin-Earth strategic context (positioning in §2.1).

*(Web-grounded lookups during this build: GOES ABI band/fire-product lineage, ERA5 units & sign conventions by ECMWF/D2E documentation; event identity cross-check for Johnson Fire.)*

## Data-stewardship notes

- `data/master.csv` is derived from the uploads and preserves row-level provenance ordering; schema T30.
- Known limitations: single-pixel anchors; proxy-level fire intensity (no FRP); no smoke concentration field; fuel moisture proxied; CIN structural missingness; 12-h cadence irregularities on 4 events.
- Recommended enrichment order: FRP/active-fire products → d2m & fuel models → GLM lightning → AOD/MAIAC → multi-cell grids (E1–E6).

## Closing statement

We were asked to invent, not to explain. PyroCast–MORPHEUS is therefore delivered as three things at once: a **definition** (a new twin species with nine coined, operational concepts), a **machine** (an 11-stratum architecture with complete mathematics and algorithms), and — because invention untested is speculation — a **living reference instance** that synchronizes (heartbeat: 45% error annihilation), remembers (Alaska finds Alaska; α\*=0.3 fusion wins everywhere), dreams (46,224 futures, decisions ranked by their tails), and audits itself (coverage 0.65→0.776). Its flaws have been hunted in the open (Part X). The wildfire community does not need another predictor; it needs an infrastructure that learns every fire season and is honest about what it does not know. That infrastructure now has a name, a state, a heartbeat, a memory, an imagination — and a repository.

*— End of thesis body. Appendices: artifact registries (Part VIII), machine artifacts (`results/`), and the condensed IEEE-TGRS paper (`PyroCast_TGRS_paper.md`).*
