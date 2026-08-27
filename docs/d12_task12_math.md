# PART VI — TASK 12: Unified Mathematical Formulation

*Notation:* cycle index t ∈ ℤ (Δt = 6 h); spatial support S (single anchor pixel in reference cohort; cell graph under scaling); random world state X⋆(s,t) ∈ ℝ^{n⋆}; twin estimate x(t) ∈ ℝⁿ (n = 52); controls u(t) ∈ ℝ^{n_u}; observations y(t) ∈ ℝ^{m}.

## 12.1 Twin state and observation operator

x(t) = Φ(z(t), m(t), Θ(t)) decomposed as §4.1. Observations:

**y(t) = H x(t) + v(t),  v(t) ~ N(0, R(t))** — H ∈ {0,1}^{m×n} selection (GOES dims with R_GOES = 0.15²σ²I; BLH/CAPE with R_ERA5 = 0.08²σ²I); R(t) adaptive via assimilation appetite (12.6).

## 12.2 State transition (the legal dynamics)

Define the hybrid propagator **F**(x, u; θ):

**x(t+1) = A·x(t) + B·u(t) + G_θ(x(t), m(t)) + w(t),  w ~ N(0, Q(t)),  ρ(A) ≤ 1−ε**

- A, B: physics-kernel blocks (ridge-fitted; spectral clip ρ(A) ≤ 0.97 — guarantees Lyapunov-stable mean dynamics: λ_max(AᵀA) < 1 ⇒ no mean blow-up between cycles);
- G_θ: learned residual (GBM ensemble; GNN node-update under graph scaling §12.7; N-ODE limit §12.8);
- m(t): retrieval-conditioned memory prior entering as an added drift term α·(x̄_donor(t+1) − x(t));
- Q(t): process covariance = Q₀ · a(D(t)) (appetite), Q₀ = Cov[X₁ − AX₀ − Bu] estimated on training folds.

Continuous-time view: dx/dt = f_phys(x,u) + f_θ(x,u,t) with the discrete propagator as its Δt-integrator; the N-ODE upgrade (E4) replaces the integrator by an adjoint-trained ODE net: x(t+Δt) = ODESolve(f_phys + f_θ, x(t), [t, t+Δt]).

## 12.3 Assimilation (synchronization as MAP estimation)

Cycle recursion, stochastic EnKF with ensemble size N:

Forecast: x⁻⁽ⁱ⁾(t+1) = F(x⁺⁽ⁱ⁾(t), u(t)) + w⁽ⁱ⁾
Innovation: r = y(t+1) − H x̄⁻ ; S = H P⁻ Hᵀ + R ; **D(t+1) = rᵀS⁻¹r**
Gain: K = P⁻ Hᵀ S⁻¹
Analysis: x⁺⁽ⁱ⁾ = x⁻⁽ⁱ⁾ + K ( y + ε⁽ⁱ⁾ − Hx⁻⁽ⁱ⁾ ), ε⁽ⁱ⁾ ~ N(0, R)

which is the ensemble form of the Kalman MAP update x⁺ = argmin_x ‖x−x⁻‖²_{P⁻} + ‖y−Hx‖²_R. Trust field: **Θ(t) = σ( c₁ − c₂·D(t)/m − c₃·(1−cov_audit) )**, σ the logistic; bounds issuance rule D3.

## 12.4 Data fusion as a convex-constrained map

Harmonized frame z(t) = argmin_z Σ_s λ_s‖M_s z − o_s‖²  s.t.  C z ≥ 0 (physical ranges), where s indexes sensors, M_s masks/resamples, C encodes physics constraints (RH∈[0,100], blh>0, tp≥0, BT bounds); derived state block x_der = g(z) per the rulebook of Part III. Fused uncertainty: R_fuse = (Σ_s λ_s R_s⁻¹)⁻¹.

## 12.5 Memory (retrieval as nonparametric kernel regression)

Episodic store E = {(κᵢ, Yᵢ, cᵢ)}; query key κ(q). Weights and fused prediction:

**aᵢ = softmax_i( −d(κ(q), κᵢ)/τ ),   ŷ_mem(s) = Σᵢ aᵢ Yᵢ(s),   ŷ = α·ŷ_mem + (1−α)·ŷ_dyn**

with d the standardized profile metric, τ = median(d), α\*(=0.30) selected by nested CV minimizing fused LOEO RMSE. Consolidation update of encoder parameters: θ_E ← argmin L_replay + λ_EWC Σ_i F_i (θ_i − θ_i\*)², F_i the Fisher diagonal — quadratic evidence preservation (no catastrophic forgetting).

## 12.6 Self-calibration and fitness

Conformal band repair on validation half: k = Quantile_{0.9}(|y − q̂_bound|); adjusted [q̂_lo − k_lo, q̂_hi + k_hi] restores nominal coverage (measured 0.65→0.776).
Fitness functional driving slow-loop selection:

**J(θ) = NLL_skill(θ) ↑ − λ₁·|cov − cov*| − λ₂·staleness(θ) − λ₃·Forget(θ, E_archive)**, promote ⟺ J_challenger > J_incumbent in shadow.

## 12.7 Graph formulation (scaled twin)

Cells as nodes: G = (V, E), node states xᵢ(t), edge features eᵢⱼ = [Δterrain, w·Δt advection length, upwind flag]. Message passing (design slot for Channel-L/GNN):

hᵢ^{(k+1)} = φ( hᵢ^{(k)}, ⊕_{j∈N(i)} ψ( hᵢ^{(k)}, h_j^{(k)}, eᵢⱼ ) ),  xᵢ(t+1) = γ(hᵢ^{(K)}, uᵢ(t)) + wᵢ

Fire-spread physics enters as the edge prior: ψ upwind-weighted, Rothermel-consistent sign constraints (spread downwind ≥ upwind) — **physics-informed message passing**. The current cohort degenerates to |V|=1, proving by construction why the arbiter's V♂↦graph upgrade is extension E2, not a present claim.

## 12.8 Loss functions (full objective)

**L = w₁L_fcst + w₂L_phys + w₃L_cal + w₄L_graph + w₅L_contrast + w₆L_cf**

- L_fcst = Σ_h Σ_y ℓ_q(ŷ(h), y(h)) pinball (q∈{0.1,0.5,0.9}) — probabilistic nowcast;
- L_phys = ‖ρ(A) clip residual‖ + flux-sign violations + monotone constraints (e.g. ventilation ∂₂ ≥ 0 in BLH);
- L_cal = (cov − cov\*)² + PIT dispersion term;
- L_graph = KG edge sign agreement with learned coupling matrix A (cross-entropy on sign(A_ij) vs prior);
- L_contrast = InfoNCE over (key, same-regime) pairs in memory encoder;
- L_cf = counterfactual consistency: rollouts under do(ω) must obey operator invariants exactly (e.g. RH scaling conserved by recompute map), penalized deviation.

Optimization: stage-wise (fit A,B → fit G_θ residual → fit memory encoder contrastive → calibrate quantiles → conformal repair); kernel upgrades enter shadow-A/B under J.

## 12.9 Temporal modelling

Beyond VAR: the temporal ontology T = (cycle lattice 6h, Δt-aware propagator F(Δt) via matrix fraction A(Δt) = A₁^{Δt/6h}, diurnal forcing harmonics D(t) = [sin, cos](2πh/24), seasonal S(t)). Memory provides the long term E[·|history >> window]; phase sub-chain P(phase_{t+1}|phase_t, x) provides the discrete skeleton of lifecycle reasoning.

## 12.10 Counterfactual expectation & risk

p( y(h) | do(ω), x(t) ) = ∫ p( y(h) | x(t), u(t..h) = ω(u) ) dP_x(t) ≈ (1/N) Σ_i ŷ⁽ⁱ⁾(h; ω)

operative expectation estimated by the futures ensemble. Risk and robust action:

R(a) = E_ω[L(a,ω)];  **a\* = argmin_a CVaR_α L(a,·) = argmin_a ( ξ + (1−α)⁻¹ E[ (L − ξ)⁺ ] )** (Rockafellar–Uryasev form; ξ = VaR_α; differentiable optimum subproblem).
