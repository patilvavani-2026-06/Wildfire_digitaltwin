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
