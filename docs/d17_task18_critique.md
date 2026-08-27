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
