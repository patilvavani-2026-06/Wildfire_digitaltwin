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
