"""PyroCast Step 7 — full figure gallery HTML + captions registry (every generated image)."""
import os, json
R='/home/user/PyroCast/'; FIG=R+'figures/'
CAP={
# cohort science
'F01_event_map.png':'Cohort map: 10 PyroCb events, 2021–22 (bubble = max injection potential)',
'F02_traj_fire_proxy.png':'Fire-proxy trajectories per event (6-h steps)',
'F03_traj_cloud_bt.png':'Cloud-top BT trajectories per event (colder = deeper convection)',
'F03b_traj_chp.png':'Cloud-height proxy trajectories per event',
'F04_hovmoller_fire.png':'Event×time Hovmöller — fire proxy',
'F05_hovmoller_cbt.png':'Event×time Hovmöller — cloud-top BT',
'F06_corr_heatmap.png':'28-variable cross-layer correlation structure',
'F07_distributions.png':'Marginal distributions of twin state variables',
'F08_diurnal.png':'Diurnal composites: BLH, SSHF, CAPE, Δ cloud-top BT',
'F09_leadlag.png':'Lead–lag driver×target cross-correlation matrices',
'F10_phase_portrait.png':'Fire–atmosphere phase portrait with 30-h drift arrows',
'F11_windroses.png':'10-m vs 250-hPa directional climatology',
'F12_rh_profiles.png':'Event-mean RH structure (850/750/650 hPa)',
'F13_buoyancy.png':'CAPE–CIN buoyancy phase space (colour PII, size BLH)',
'F14_heatflux_regime.png':'Surface heat-flux diurnal cycle by fire regime',
'F15_terrain_veg.png':'Terrain & vegetation controls per event',
'F16_missing.png':'Missing-data audit (CIN structurally missing)',
'F17_pca.png':'PCA of the joint fire–atmosphere state (events ribbon)',
'F18_gantt.png':'Observation windows Gantt (two fire seasons)',
'F19_severity.png':'Composite event severity ranking',
'F20_regimes.png':'k-means fire-regime archetypes (3 clusters)',
# trained results
'F21_pred_vs_obs.png':'LOEO nowcast: twin vs persistence (4 targets)',
'F21b_delta_skill.png':'Δ-target skill vs "no-change" baseline',
'F22_residuals.png':'Residual structure: twin vs persistence',
'F23_importance.png':'Feature importance (gain + permutation), fire proxy +6h',
'F24_ablation.png':'Physics feature-block ablation ladder',
'F25_per_event.png':'Per-event transfer RMSE (unseen fires)',
'F26_quantile_fan.png':'Probabilistic trajectory — event 253 (80% PI)',
'F27_calibration.png':'Uncertainty calibration before audit',
'F27b_conformal.png':'Conformal self-calibration (0.65→0.776 coverage)',
'F28_classifier.png':'Lifecycle intensification classifier (ROC/PR/confusion)',
'F29_analog.png':'Memory replay: event 260 from donor events',
'F29b_memory_fusion.png':'Memory fusion skill ladder (α*=0.30)',
'F30_memory_matrix.png':'Event-memory similarity field (10×10)',
'F31_coupling_matrix.png':'Learned 8×8 fire–atmosphere coupling matrix',
'F32_coupling_graph.png':'Emergent coupling graph (KG edge evidence)',
'F33_enkf_bars.png':'EnKF synchronization vs free-run, all events (−45.0%)',
'F34_enkf_cycle.png':'Heartbeat: truth vs free-run vs analysis ±2σ, D(t)',
'F35_uncertainty_growth.png':'Erratum: honest uncertainty decomposition vs lead — RMSE vs persistence (flat), seed-jitter floor (artifact), inter-scenario spread (flat)',
'F36_cf_tornado.png':'Counterfactual tornado (ΔPII +24 h)',
'F37_cf_fan.png':'Counterfactual futures fan — event 253',
'F38_cf_riskheat.png':'ΔP(PyroCb) scenario×event risk heatmap',
'F39_vitals.png':'Twin vital-signs radar (V1–V4), events 202/253/258',
# architecture
'D40_architecture_master.png':'Master 11-stratum architecture (Figure 1)',
'D41_state_schema.png':'Six-block twin-state schema (memory+uncertainty as state)',
'D42_sync_sequence.png':'6-hour synchronization sequence grammar',
'D43_memory_architecture.png':'Four-tier memory architecture + consolidation',
'D44_knowledge_graph.png':'Knowledge-graph schema (nodes & typed relations)',
'D45_prediction_engine.png':'Three-channel prediction engine + arbiter',
'D46_counterfactual_dag.png':'Counterfactual futures DAG (do-calculus flow)',
'D47_decision_intelligence.png':'Decision intelligence pipeline (CVaR cards)',
'D48_living_loops.png':'Living twin: fast homeostatic × slow evolutionary loops',
'D49_multiagent.png':'Multi-agent organ chart (incl. CRITIC red-team)',
'D50_deployment.png':'Deployment pipeline (shadow, sentinels, rollback)',
# visualization
'D51_globe_3d.png':'4D globe grammar: terrain ⊗ fire ⊗ plume ⊗ PyroCb',
'globe_plume.gif':'Animated 4D twin (rotating, breathing PyroCb cap)',
'D52_dashboard.png':'Decision dashboard layout (dark mission console)',
'D53_layer_stack.png':'Five composited rendering layer groups',
'D54_timeline.png':'4D time system: ribbons, markers, playhead',
'D55_cf_compare.png':'Counterfactual split-world viewer + Δ-card',
'R01_globe_concept.png':'AI concept render: NASA-grade 4D globe',
'R02_dashboard_concept.png':'AI concept render: decision dashboard UI'}
SEC=[('A — Cohort science (data understanding)',
      ['F01_event_map.png','F02_traj_fire_proxy.png','F03_traj_cloud_bt.png','F03b_traj_chp.png','F04_hovmoller_fire.png','F05_hovmoller_cbt.png','F06_corr_heatmap.png','F07_distributions.png','F08_diurnal.png','F09_leadlag.png','F10_phase_portrait.png','F11_windroses.png','F12_rh_profiles.png','F13_buoyancy.png','F14_heatflux_regime.png','F15_terrain_veg.png','F16_missing.png','F17_pca.png','F18_gantt.png','F19_severity.png','F20_regimes.png']),
     ('B — Trained-twin results (LOEO evidence)',
      ['F21_pred_vs_obs.png','F21b_delta_skill.png','F22_residuals.png','F23_importance.png','F24_ablation.png','F25_per_event.png','F26_quantile_fan.png','F27_calibration.png','F27b_conformal.png','F28_classifier.png','F29_analog.png','F29b_memory_fusion.png','F30_memory_matrix.png','F31_coupling_matrix.png','F32_coupling_graph.png','F33_enkf_bars.png','F34_enkf_cycle.png','F35_uncertainty_growth.png','F36_cf_tornado.png','F37_cf_fan.png','F38_cf_riskheat.png','F39_vitals.png']),
     ('C — Architecture & system diagrams',
      ['D40_architecture_master.png','D41_state_schema.png','D42_sync_sequence.png','D43_memory_architecture.png','D44_knowledge_graph.png','D45_prediction_engine.png','D46_counterfactual_dag.png','D47_decision_intelligence.png','D48_living_loops.png','D49_multiagent.png','D50_deployment.png']),
     ('D — 4D visualization system & concept renders',
      ['D51_globe_3d.png','globe_plume.gif','D52_dashboard.png','D53_layer_stack.png','D54_timeline.png','D55_cf_compare.png','R01_globe_concept.png','R02_dashboard_concept.png'])]
html=['''<!DOCTYPE html><html><head><meta charset="utf-8"><title>PyroCast Figure Gallery — all generated images</title>
<style>
body{background:#0d1117;color:#c9d1d9;font-family:system-ui,sans-serif;margin:0}
h1{font-size:20px;padding:16px 22px 4px;margin:0;color:#fff}
.sub{padding:0 22px 12px;color:#8b949e;font-size:12px;border-bottom:1px solid #30363d}
h2{color:#f4a261;padding:20px 22px 6px;font-size:15px;border-top:1px solid #30363d;margin-top:14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:14px;padding:10px 22px 24px}
.card{background:#161b22;border:1px solid #30363d;border-radius:8px;overflow:hidden}
.card img{width:100%;display:block;background:#fff}
.cap{padding:8px 10px;font-size:11.5px;color:#c9d1d9}
.num{color:#8b949e;font-size:10px}
</style></head><body>''',
'<h1>PyroCast–MORPHEUS — Complete Figure Gallery</h1>',
'<div class="sub">Every image generated by the training pipeline (60 artifacts) · sections: cohort science → trained results → architecture → 4D visualization · all files in <i>figures/</i></div>']
n=0
for title,files in SEC:
    html.append(f'<h2>{title}</h2><div class="grid">')
    for f in files:
        n+=1
        html.append(f'<div class="card"><img src="figures/{f}" loading="lazy"><div class="cap"><span class="num">#{n:02d} · figures/{f}</span><br>{CAP.get(f,f)}</div></div>')
    html.append('</div>')
html.append('</body></html>')
open(R+'PyroCast_Figure_Gallery.html','w').write('\n'.join(html))
json.dump(CAP, open(R+'results/figure_captions.json','w'), indent=1)
print('gallery written with', n, 'figures')
