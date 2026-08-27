# PART III (cont.) — TASK 6: Digital Twin Memory (the Mnemotic Stratum)

*(Architecture `D43`; parameters `T32`; measured retrieval `T21/T21b/T21c`, figures `F29/F29b/F30`.)*

## 6.1 Why a twin must remember

Every fire regime is a different planet. On this cohort, out-of-event *levels* prediction collapses toward climatology for any parameter-only learner (pooled R² ≤ 0.10; §IX). The physics reason: fire–atmosphere coupling constants are regime-conditioned (fuel structure, latitude-driven Coriolis/solar geometry, moisture climatology). Parameters can encode an *average* planet; skill on a *new* planet must come from **recalling the most similar known planets**. That is what memory is for.

## 6.2 The four-tier stack

1. **Sensory store** — the current 6-h observation window: raw z(t), TTL one cycle; feeds short-term working memory.
2. **Short-term working memory** — last k=8 cycles: rates, phase estimate, innovation history; supports persistence-channel predictions and D(t) smoothing.
3. **Episodic store** — consolidated *event schemas*: Eᵢ = {κᵢ key, trajectory tensor, context (regime, terrain, season), outcomes (peak intensity, injection, decay mode), provenance}. Write-gated by salience s = λ₁·surprise + λ₂·severity + λ₃·novelty.
4. **Semantic store** — regime archetypes, coupling priors, KG edges: *what kinds of worlds exist and how they work*.

## 6.3 Retrieval and fusion (implemented, measured)

**Query key** κ from the *first 24 h* only (operationally honest): early-window means of {cape, blh, wind250, rh_colmean, ventilation, t2m} + statics {lat, elevation, slope, cvh}, standardized on donor pool. Distance-weighted donor continuation:

aᵢ = exp(−d(q,κᵢ)/τ) / Σⱼ exp(−d(q,κⱼ)/τ),  τ = median(d);  ŷ_mem(s) = Σᵢ aᵢ · yᵢ(s)

**Memory fusion** with short-term dynamics: ŷ = α·ŷ_mem + (1−α)·ŷ_persist, α\* tuned by nested LOEO → **α\* = 0.30 uniformly** (the twin trusts dynamics but listens to experience).

**Measured retrieval sanity (T21):** interior-Alaska events 258/260 are *mutual nearest analogs* (d = 1.56/2.40); Manitoba 202 pulls the boreal set {260, 258, 216}; Johnson 179 pulls Utah 181 (dry high-elevation SW). The `F30` similarity field is block-structured by regime — the twin's geography of experience matches the fire climatologist's.

**Measured skill (T21c):** fused memory beats persistence on all targets — fire proxy RMSE 14.88 vs 16.08 (**−7.5%**), cloud-height proxy 7.47 vs 8.14 (**−8.3%**), PII 0.3295 vs 0.3509 (**−6.1%**) — while pure analog replay alone (21.1/10.36/0.485) is deliberately not trusted unsupervised.

## 6.4 Consolidation (the twin's "sleep")

Offline: (i) re-encode episodes with the current encoder; (ii) merge/split schemas by clustering drift; (iii) fine-tune kernels with Fisher-weighted penalty L = L_task + λ Σ F_i(θ_i − θ_i\*)² (anti-forgetting); (iv) update regime centroids — large shifts flagged as **semantic scars** (requires human countersign — governance rule G2). Experience replay prioritizes high-surprise windows (large |innovation|), the geophysical analog of hippocampal replay bias toward salient experience.

## 6.5 Knowledge accumulation & adaptive learning

Long-horizon growth is *not* weight growth but **memory economy growth**: richer episodic keyspace, sharper regime priors from the KG, scenario-library expansion (S-operators that historical scars proved relevant), and calibrated trust audits per regime. The twin's fitness functional J (Task 10) contains an explicit **forgetting term λ₃** so that adaptation is never free.
