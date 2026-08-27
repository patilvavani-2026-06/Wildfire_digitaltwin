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
39. **F35_uncertainty_growth.png** — Predictive σ vs lead time per scenario: trust decay made quantitative.
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
