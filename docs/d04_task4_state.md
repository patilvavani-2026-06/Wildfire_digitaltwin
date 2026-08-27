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
