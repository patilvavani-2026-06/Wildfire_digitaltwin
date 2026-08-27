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
