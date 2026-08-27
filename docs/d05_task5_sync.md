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
