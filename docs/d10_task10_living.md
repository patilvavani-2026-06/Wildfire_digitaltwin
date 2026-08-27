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
