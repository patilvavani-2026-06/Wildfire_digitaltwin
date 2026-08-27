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
 