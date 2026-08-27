# PART IV (cont.) — TASK 9: Decision Intelligence

*(Pipeline `D47`; rubric `T27`; worked example `T26`.)*

## 9.1 From futures to choices

Decision intelligence consumes the future measure π(ω,h) produced by the dreaming engine and returns **ranked, risk-averse, explainable actions**. Formally (full development in Part VI):

- **Loss of inaction/action a under world ω:** L(a, ω) = exposure(ω) × vulnerability × failure(a, ω) − benefit(a).
- **Risk of action:** R(a) = ∫_Ω L(a,ω) dπ(ω) (scenario expectation).
- **Robust selection (implemented ranking rule):** a\* = argmin_a  CVaR_α[L(a,·)]  =  argmin_a  E[ L | L ≥ VaR_α(L) ], α=0.9 — optimize the *average bad tail*, not the mean: in life-safety domains the expectation is a lie the tail tells.
- **Uncertainty conditioning:** confidence on a card = f(Θ(t), scenario concentration, analog support); low Θ caps alert level regardless of point risk (rule D3).
- **Scenario ranking:** ω ranked by Δrisk(ω) = R(a*,ω) − R(a*,S0) — drives the tornado (`F36`) and the heat (`F38`) views; decision-relevant ranking ≠ sensitivity ranking.

## 9.2 Action library & rubric

Alerts (L2→L4 escalation), crew/air asset pre-positioning, Rx-burn go/no-go windows, satellite tasking (mesoscale sector, cadence up), and mesh densification. Binding to probability bands in `T27`: P(PyroCb) ≥ 0.50 → CRITICAL posture; 0.25–0.50 HIGH; 0.10–0.25 ELEVATED; else ROUTINE (bands tunable per agency; defaults conservative).

## 9.3 Worked example (reference twin, event 253 — subtropical CAPE regime)

`T26` ranks the operators by P(PyroCb|ω,+24 h): S0 0.019 baseline; S1 0.022 (wind) tops the amplification list; S7 collapses PyroCb odds to 0.004 while intensifying fire — *the engine therefore recommends heightened fire-ground readiness with lowered aviation/aviation-SIGMET priority under compound-extreme outlooks, and the opposite under strengthening-shear outlooks*. Every card carries: E[·], σ(·), P(·), Θ, dominant ω, driving features (importance renal `F23`), and the analog events that justify it (for 253: 189/180/202 by retrieval `T21`).

## 9.4 Explanation as a first-class output

Each action card is a **KG instantiation**: Action —justified_by→ Outcome —amplified_by→ Mechanism ←driven_by— Driver —do()→ Counterfactual, with the analog subgraph (ANALOG_OF edges) attached. If the explanation cannot be generated, the action cannot be issued (rule D5: *no unexplained alerts*).

## 9.5 Uncertainty estimation — the three-layer stack

(1) **aleatoric**: quantile heads + ensemble spread (`F26`, `F35`); (2) **epistemic**: seed/kernel diversity + LOEO transfer gaps reported per event (`F25`); (3) **distributional**: conformal self-audit adjusts bands (`F27b`), trust Θ gates issuance (rule D3). Risk is never a scalar: cards report (E, σ, tail, Θ).
