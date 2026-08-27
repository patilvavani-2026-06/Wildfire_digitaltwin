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

Uncertainty vs lead time, stated honestly (`F35`, erratum): the three quantities that are easy to conflate must be separated. *(i)* True verification error of the LOEO direct models is **flat, not growing** — RMSE 17.5 / 18.6 / 18.7 / 16.7 at +6/+12/+18/+24 h — with a shallow minimum at +24 h: the 6-hourly cadence makes +24 h a *diurnal-resonant* lead (same phase of the fire-proxy diurnal cycle is predicted), so classical error growth is not observed on this cohort; persistence attains 16.7 / 16.2 / 16.6 / 14.4, i.e. the parametric learner does not beat persistence on level prediction — the regime-transfer theorem of §6. *(ii)* The seed ensemble's dispersion (3-seed σ = 1.64 → 1.18) is an *algorithmic-jitter floor*, not forecast uncertainty; it **contracts** with lead because learnable signal decays while XGBoost shrinkage (depth 3, η = 0.06, λ = 2) pulls all seeds toward the climatological mean, an effect amplified by median-imputed tail targets (target variance after imputation falls 291 → 252 from h = 1 to 4). *(iii)* The divergence across the nine counterfactual futures — the quantity "uncertainty across futures" properly refers to — is ≈ 2.0–2.2 σ(fire proxy) and likewise flat over 6–24 h. Risk heat (`F38`) shows the twin's *event-dependent* sensitivity (e.g. 253's subtropical CAPE regime responds opposite to boreal 216 for the same operator).

## 8.4 Scaling to "thousands of futures"

The engine is embarrassingly parallel over (event, step, ω, seed); reference run: 46,224 futures in 118 s on one CPU (`T33`). The production design swaps XGB channels for the GNN/N-ODE kernels and runs Latin-hypercube over continuous operator manifolds (ω as vectors, not bookmarks), with importance-sampling concentrated on tail-ω — the scenario-miner of `D46`.
