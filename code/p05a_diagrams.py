"""PyroCast Step 5a — architecture diagrams D40-D50 (publication flowcharts)."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import networkx as nx, numpy as np
R='/home/user/PyroCast/'; FIG=R+'figures/'
plt.rcParams.update({'figure.dpi':150,'savefig.dpi':150,'font.size':8,'font.family':'DejaVu Sans'})
C = {'phys':'#3d405b','obs':'#457b9d','atm':'#2a9d8f','fus':'#8d99ae','core':'#e63946',
     'mem':'#6d597a','pred':'#e76f51','cf':'#f4a261','dec':'#606c38','fb':'#118ab2','kg':'#b56576'}

def box(ax, x, y, w, h, text, fc, fs=7.4, tc='white', lw=0.8, style='round,pad=0.02,rounding_size=0.035', weight='bold'):
    ax.add_patch(FancyBboxPatch((x,y), w, h, boxstyle=style, fc=fc, ec='black', lw=lw*0.6, mutation_aspect=1))
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=fs, color=tc, weight=weight)
def arrow(ax, p1, p2, color='#222', style='-|>', lw=1.4, rad=0.0, ls='-'):
    ax.add_patch(FancyArrowPatch(p1,p2,arrowstyle=style,mutation_scale=11,color=color,lw=lw,
                                 connectionstyle=f'arc3,rad={rad}',linestyle=ls))
def canvas(w=8.4,h=11.4):
    fig, ax = plt.subplots(figsize=(w,h)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off'); return fig,ax
def save(fig,name):
    fig.savefig(FIG+name,bbox_inches='tight',facecolor='white'); plt.close(fig); print('saved',name)

# ---------------- D40 MASTER ARCHITECTURE ----------------
fig,ax=canvas()
ax.text(0.5,0.985,'PyroCast–MORPHEUS: Mnemotic, Observationally-coupled, Recursive,\nPHysics-informed, Episodic, Uncertainty-calibrated, Self-learning Twin',
        ha='center',va='top',fontsize=9.3,weight='bold')
layers=[
 ('PHYSICAL WORLD','Wildfire ⊗ Atmosphere ⊗ Terrain ⊗ Vegetation\ntrue coupled dynamical system (unknown, stochastic)',C['phys'],0.845),
 ('SATELLITE OBSERVATION LAYER','GOES-16/17 ABI: B07 3.9µm, B14 11.2µm, B16 13.3µm, B01–B03\nfire proxy, cloud-height proxy, simulated green; 6-h swath sync',C['obs'],0.745),
 ('ATMOSPHERIC LAYER','ERA5: t2m, sp, u10/v10, BLH, CAPE, CIN, tp, SLHF, SSHF, fg10\npressure-level RH(850/750/650), u/v(250 hPa); terrain&veg rasters',C['atm'],0.645),
 ('DATA FUSION LAYER','harmonization • QC • unit audit • gridding • derived physics\n(ventilation, shear, buoyancy forcing, RH structure, upslope index)',C['fus'],0.545),
 ('DIGITAL TWIN CORE','homeostatic state machine x(t)∈Rⁿ  +  trust field Θ(t)\nEnKF synchronization every 6 h • divergence pressure D(t)',C['core'],0.445),
 ('KNOWLEDGE GRAPH','Event–Regime–Driver–Mechanism entities\ncausal edges learned from coupling matrix + literature priors',C['kg'],0.360),
 ('STATE MEMORY','sensory → short-term → episodic (event schemas) → semantic\ncontrastive retrieval • consolidation replay • anti-forgetting',C['mem'],0.275),
 ('PREDICTION ENGINE','physics-guided MIMO forecaster (VAR kernel + XGB residual +\nneural-ODE design slot) multi-horizon h∈{6,12,18,24 h}',C['pred'],0.190),
 ('COUNTERFACTUAL SIMULATION','do-operators on forcing: wind+20%, +5 K, RH−30%, rain-out,\nrelocation, compound extremes — 46,224 futures / cohort',C['cf'],0.105),
 ('DECISION INTELLIGENCE','risk integrals • CVaR scenario ranking • action utility\nalerting, asset pre-positioning, burn windows, observation tasking',C['dec'],0.020),
]
for name,desc,col,y in layers:
    box(ax,0.06,y,0.62,0.082,'',col)
    ax.text(0.10,y+0.062,name,fontsize=7.8,weight='bold',color='white')
    ax.text(0.10,y+0.030,desc,fontsize=6.2,color='white',va='center')
for i in range(len(layers)-1):
    y0=layers[i][3]; y1=layers[i+1][3]
    arrow(ax,(0.37,y0),(0.37,y1+0.082),color='#111',lw=1.6)
    arrow(ax,(0.62,y1+0.041),(0.62,y0+0.041),color='#888',lw=1.0,ls='--')
# right rail: cross-cutting organs
rail=[('UNCERTAINTY & TRUST FIELD Θ',0.80),('AUTONOMY / ACTIVE LEARNING',0.62),('SCENARIO LIBRARY ω∈Ω',0.44),('HUMAN-IN-THE-LOOP CONSOLE',0.26)]
for name,y in rail:
    box(ax,0.72,y,0.24,0.09,name,'#1d3557',fs=6.6)
    for _,_,_,ly in layers:
        if abs(ly+0.041-y-0.045)<0.10:
            arrow(ax,(0.72,y+0.045),(0.68,y+0.045),color='#1d3557',lw=0.8)
ax.text(0.37,0.002,'↑ downward = information flow (ingest→decide)   ↑ dashed = feedback/tasking (decide→observe)',ha='center',fontsize=6.4,color='#333')
save(fig,'D40_architecture_master.png')

# ---------------- D41 TWIN STATE SCHEMA ----------------
fig,ax=canvas(8.6,6.4)
ax.text(0.5,0.97,'D41 — The MORPHEUS Twin State x(t): six-state partition',ha='center',fontsize=9.5,weight='bold')
parts=[('xᶠ fire state','fire proxy • raw t07 • dist_km\nderived: intensity trend',C['core'],0.03,0.52),
       ('xᵖ plume state','cloud-top BT • cloud-height proxy\nderived: growth/mature/decay phase',C['pred'],0.35,0.52),
       ('xᵃ atmosphere','t2m,sp,wind,BLH,CAPE,CIN,RH(p)\nfluxes, gusts, tp',C['atm'],0.67,0.52),
       ('xˡ land & terrain','elevation,slope,aspect,TPI,TRI\ncvh/cvl, tvh/tvl, dry spell',C['dec'],0.03,0.12),
       ('xᵐ memory latent','event embedding z∈Rᵈ\nretrieval keys κ, regime priors',C['mem'],0.35,0.12),
       ('xᵘ uncertainty','ensemble covariance P(t)\ntrust field Θ(t), divergence D(t)',C['kg'],0.67,0.12)]
for name,desc,col,x,y in parts:
    box(ax,x,y,0.29,0.30,'',col)
    ax.text(x+0.145,y+0.25,name,ha='center',fontsize=8,weight='bold',color='white')
    ax.text(x+0.145,y+0.12,desc,ha='center',fontsize=6.4,color='white')
for (a,b) in [(0,1),(1,2),(0,3),(2,3),(0,4),(1,4),(3,5),(4,5)]:
    arrow(ax,(parts[a][3]+0.145,parts[a][4]+0.15),(parts[b][3]+0.145,parts[b][4]+0.15),color='#444',lw=1.0,style='<|-|>')
ax.text(0.5,0.045,'x(t) = [ xᶠ | xᵖ | xᵃ | xˡ | xᵐ | xᵘ ]ᵀ  — observable block via y(t)=H·x(t)+v(t);  memory & uncertainty are first-class state, not metadata',
        ha='center',fontsize=6.8)
save(fig,'D41_state_schema.png')

# ---------------- D42 SYNCHRONIZATION SEQUENCE ----------------
fig,ax=canvas(8.6,6.8)
ax.text(0.5,0.97,'D42 — The 6-hour synchronization cycle (the twin heartbeat)',ha='center',fontsize=9.5,weight='bold')
actors=[('Satellite',0.06),('Fusion',0.26),('Twin Core',0.46),('Memory',0.66),('Engines',0.86)]
for name,x in actors:
    box(ax,x,0.86,0.14,0.06,name,'#1d3557',fs=7.2); ax.plot([x+0.07,x+0.07],[0.10,0.86],ls=':',color='#999',lw=0.8)
msgs=[(0,0.80,'t₀+00: GOES ABI swath → ABI features (t07,t14,t16,b01–03)',1),
      (2,0.735,'t₀+01: propagate ensemble forecast x⁻ = A x + b + w',0),
      (1,0.675,'t₀+02: ERA5 analysis + pressure levels → derived physics',2),
      (2,0.615,'t₀+03: innovation r = y − H x⁻ ; divergence D = rᵀS⁻¹r',0),
      (3,0.555,'t₀+04: retrieve top-k analog events (κ-match)',2),
      (2,0.495,'t₀+05: EnKF update x⁺ = x⁻ + K(y − Hx⁻); trust Θ ← f(P,D)',0),
      (3,0.435,'t₀+06: consolidate episode → episodic store (EWC guard)',2),
      (4,0.375,'t₀+07: prediction engine rolls h∈{6..24h} ahead',2),
      (4,0.315,'t₀+08: counterfactual futures under do-operators ω∈Ω',2),
      (4,0.255,'t₀+09: risk integrals, CVaR ranks, action utilities',2),
      (0,0.195,'t₀+10: tasking: next-look request if D > threshold',1),
      (2,0.135,'t₀+11: self-audit: coverage check → conformal recalibration',0)]
for src,y,txt,dst in msgs:
    x1=actors[src][1]+0.07; x2=actors[dst][1]+0.07
    arrow(ax,(x1,y),(x2,y),color='#e63946' if dst==2 else '#2a9d8f',lw=1.2)
    ax.text(min(x1,x2)+0.005,y+0.012,txt,fontsize=6.0)
save(fig,'D42_sync_sequence.png')

# ---------------- D43 MEMORY ARCHITECTURE ----------------
fig,ax=canvas(8.6,6.2)
ax.text(0.5,0.96,'D43 — Mnemotic memory stack: from sensation to wisdom',ha='center',fontsize=9.5,weight='bold')
box(ax,0.04,0.72,0.20,0.16,'SENSORY STORE\n6-h observation window\n(raw features, seconds-scale TTL)',C['obs'],fs=6.6)
box(ax,0.28,0.72,0.20,0.16,'SHORT-TERM\nWORKING MEMORY\nrecent k=8 cycles, rates,\nphase estimate',C['atm'],fs=6.6)
box(ax,0.52,0.72,0.20,0.16,'EPISODIC STORE\nconsolidated event schemas\n(trajectory + context + outcome)',C['mem'],fs=6.6)
box(ax,0.76,0.72,0.20,0.16,'SEMANTIC STORE\nregime archetypes, coupling\npriors, KG constraints',C['kg'],fs=6.6)
for x in [0.24,0.48,0.72]: arrow(ax,(x,0.80),(x+0.04,0.80),lw=1.5)
box(ax,0.28,0.36,0.44,0.22,'CONSOLIDATION ENGINE (offline "replay")\n• re-encode episodes with updated encoder\n• merge/split schemas, update regime centroids\n• EWC/Fisher-weighted fine-tuning → no catastrophic forgetting\n• surprise-driven priority (|innovation|, max PII)',C['core'],fs=6.6)
arrow(ax,(0.62,0.72),(0.50,0.58),lw=1.5)
box(ax,0.04,0.06,0.44,0.20,'RETRIEVAL PATHWAY\nq = encoder(current window)\na_i = softmax(−d(q,κ_i)/τ)\nŷ_mem = Σ a_i · (donor continuation)',C['pred'],fs=6.6)
box(ax,0.52,0.06,0.44,0.20,'WRITE PATHWAY\nsalience s = λ₁·surprise + λ₂·severity + λ₃·novelty\nif s > θ: commit episode; else decay\nprovenance: every memory links to raw rows',C['dec'],fs=6.6)
arrow(ax,(0.38,0.36),(0.30,0.26),lw=1.3); arrow(ax,(0.60,0.36),(0.72,0.26),lw=1.3)
ax.text(0.5,0.02,'Biological analogy: hippocampal fast-write / neocortical slow-consolidation (CLS theory) re-cast for geophysical twins.',ha='center',fontsize=6.4)
save(fig,'D43_memory_architecture.png')

# ---------------- D44 KNOWLEDGE GRAPH SCHEMA ----------------
fig,ax=canvas(8.2,6.0)
ax.text(0.5,0.96,'D44 — PyroCast Knowledge Graph schema (nodes & typed relations)',ha='center',fontsize=9.5,weight='bold')
G=nx.DiGraph()
ents={'PyroCbEvent':'#e63946','FireRegime':'#e76f51','Driver(BLH)':'#457b9d','Driver(RH)':'#457b9d',
      'Driver(CAPE)':'#457b9d','Mechanism(invigoration)':'#2a9d8f','Mechanism(entrainment)':'#2a9d8f',
      'Outcome(injection)':'#6d597a','Observation(GOES)':'#8d99ae','Reanalysis(ERA5)':'#8d99ae',
      'Counterfactual(ω)':'#f4a261','Action(tasking)':'#606c38'}
G.add_nodes_from(ents)
edges=[('PyroCbEvent','FireRegime','belongs_to'),('Driver(BLH)','Mechanism(invigoration)','ventilates'),
       ('Driver(CAPE)','Mechanism(invigoration)','energizes'),('Driver(RH)','Mechanism(entrainment)','drys'),
       ('Mechanism(invigoration)','Outcome(injection)','amplifies'),('Mechanism(entrainment)','Outcome(injection)','suppresses'),
       ('PyroCbEvent','Outcome(injection)','produces'),('Observation(GOES)','PyroCbEvent','observes'),
       ('Reanalysis(ERA5)','Driver(BLH)','supplies'),('Counterfactual(ω)','Driver(CAPE)','do()'),
       ('Counterfactual(ω)','Driver(RH)','do()'),('Action(tasking)','Observation(GOES)','requests')]
for u,v,l in edges: G.add_edge(u,v,label=l)
pos=nx.spring_layout(G,seed=5,k=1.4)
nx.draw_networkx_nodes(G,pos,node_color=[ents[n] for n in G.nodes],node_size=2300,ax=ax,edgecolors='k',linewidths=0.6)
nx.draw_networkx_labels(G,pos,font_size=5.6,font_color='white',font_weight='bold',ax=ax)
nx.draw_networkx_edges(G,pos,ax=ax,arrows=True,arrowsize=9,edge_color='#555',connectionstyle='arc3,rad=0.06',min_source_margin=16,min_target_margin=16)
nx.draw_networkx_edge_labels(G,pos,{ (u,v):d['label'] for u,v,d in G.edges(data=True)},font_size=5.4,ax=ax,label_pos=0.55)
ax.axis('off'); save(fig,'D44_knowledge_graph.png')

# ---------------- D45 PREDICTION ENGINE ----------------
fig,ax=canvas(8.6,5.6)
ax.text(0.5,0.96,'D45 — Physics-guided hybrid prediction engine (three channels + arbiter)',ha='center',fontsize=9.5,weight='bold')
box(ax,0.03,0.60,0.26,0.24,'CHANNEL P\nPHYSICS KERNEL\nVAR/ODE coupling core A\nstable, interpretable\n(caps: spectral radius<1)',C['atm'],fs=6.6)
box(ax,0.37,0.60,0.26,0.24,'CHANNEL L\nLEARNED RESIDUAL\nXGB/GNN on nonlinear\nresidual y − Ax\n(captures thresholds)',C['core'],fs=6.6)
box(ax,0.71,0.60,0.26,0.24,'CHANNEL M\nMEMORY CONTINUATION\nα*-weighted analog replay\n(regime-aware transfer)',C['mem'],fs=6.6)
box(ax,0.21,0.24,0.58,0.20,'ARBITER (stacked meta-model)\nŷ(h) = β₀(h) + β₁·ŷ_P + β₂·ŷ_L + β₃·ŷ_M\nβ fitted on LOEO residuals;  uncertainty: quantile + ensemble + conformal',C['pred'],fs=6.8)
for x in [0.16,0.50,0.84]: arrow(ax,(x,0.60),(0.50,0.44),lw=1.4)
box(ax,0.21,0.03,0.58,0.14,'MULTI-HORIZON OUTPUT h ∈ {6,12,18,24 h}\nfire proxy • cloud-height proxy • Δcloud-top BT • PII • lifecycle phase probs',C['dec'],fs=6.8)
arrow(ax,(0.50,0.24),(0.50,0.17),lw=1.4)
save(fig,'D45_prediction_engine.png')

# ---------------- D46 COUNTERFACTUAL DAG ----------------
fig,ax=canvas(8.4,5.8)
ax.text(0.5,0.96,'D46 — Counterfactual futures engine: do-calculus over twin transitions',ha='center',fontsize=9.5,weight='bold')
box(ax,0.34,0.80,0.32,0.12,'twin state x(t), trust Θ(t)',C['core'],fs=7)
box(ax,0.03,0.52,0.28,0.20,'SCENARIO LIBRARY ω\nmarginal do-ops (do(rh×0.7))\ncompound ops (heatwave)\nstructural ops (relocate)',C['cf'],fs=6.4)
box(ax,0.36,0.52,0.28,0.20,'COUNTERFACTUAL KERNEL\nE[f(x(t+h)) | do(ω)]\nrollout via arbiter ensemble\nnoise: seeds × obs-error',C['pred'],fs=6.4)
box(ax,0.69,0.52,0.28,0.20,'FUTURE MEASURES\nP(severe | ω, h)\nΔrisk(ω), tornado(ω)\nfutures fan {μ(h), σ(h)}',C['mem'],fs=6.4)
box(ax,0.20,0.20,0.28,0.18,'SCENARIO MINER\nsearches ω* maximizing\nΔrisk (vulnerability audit)',C['kg'],fs=6.4)
box(ax,0.53,0.20,0.28,0.18,'DECISION HOOK\na* = argmin CVaR_α[L(a,ω)]\nranked robust actions',C['dec'],fs=6.4)
arrow(ax,(0.50,0.80),(0.50,0.72)); arrow(ax,(0.17,0.72),(0.44,0.72))
arrow(ax,(0.50,0.52),(0.50,0.44));  arrow(ax,(0.83,0.52),(0.60,0.44))
arrow(ax,(0.34,0.38),(0.60,0.38))
arrow(ax,(0.30,0.52),(0.30,0.38),style='<|-|>')
ax.text(0.5,0.08,'cohort demo: 9 operators × 10 events × 4 horizons × 3 seeds × 2 targets = 46,224 simulated futures',ha='center',fontsize=6.6)
save(fig,'D46_counterfactual_dag.png')

# ---------------- D47 DECISION INTELLIGENCE ----------------
fig,ax=canvas(8.4,5.6)
ax.text(0.5,0.96,'D47 — Decision intelligence: from futures to ranked, risk-averse actions',ha='center',fontsize=9.5,weight='bold')
box(ax,0.03,0.70,0.27,0.18,'FUTURES ENSEMBLE\n{ x̂(ω,h), P(severe|ω,h) }',C['pred'],fs=6.6)
box(ax,0.36,0.70,0.27,0.18,'RISK INTEGRAL\nR(a) = ∫ L(a,ω) dP(ω)\nL = exposure × vulnerability',C['kg'],fs=6.6)
box(ax,0.69,0.70,0.27,0.18,'ROBUST SELECTOR\na* = argmin CVaR_α[L]\ns.t. budget, feasibility',C['dec'],fs=6.6)
box(ax,0.10,0.36,0.36,0.22,'ACTION LIBRARY\nalert escalation • crew pre-positioning\nair-tanker windows • Rx-burn go/no-go\nsatellite tasking • mesh densification',C['atm'],fs=6.4)
box(ax,0.54,0.36,0.36,0.22,'EXPLANATION LAYER\nwhich ω dominate the CVaR tail\nwhich features drive Δrisk (SHAP)\nwhich analog events justify the alert',C['mem'],fs=6.4)
box(ax,0.28,0.06,0.44,0.16,'OUTPUT: ranked action card\n{action, expected loss, CVaR₀.₉ loss, confidence, rationale}',C['core'],fs=6.8)
arrow(ax,(0.30,0.70),(0.30,0.58)); arrow(ax,(0.69,0.70),(0.69,0.58))
arrow(ax,(0.28,0.36),(0.40,0.22)); arrow(ax,(0.72,0.36),(0.60,0.22))
save(fig,'D47_decision_intelligence.png')

# ---------------- D48 LIVING TWIN DUAL LOOP ----------------
fig,ax=canvas(8.6,5.8)
ax.text(0.5,0.96,'D48 — The living twin: fast homeostatic loop ⊗ slow evolutionary loop',ha='center',fontsize=9.5,weight='bold')
box(ax,0.06,0.62,0.40,0.26,'FAST LOOP (every 6 h)\nobserve → propagate → innovate → update\ntrust Θ, divergence D, self-calibration\nhomeostat: keep ‖x_twin − x_earth‖ bounded',C['core'],fs=6.6)
box(ax,0.54,0.62,0.40,0.26,'SLOW LOOP (offline, dream phase)\nconsolidate episodes → refine encoders\nretrain kernels (EWC-guarded)\nupdate scenarios, archetypes, KG edges',C['mem'],fs=6.6)
arrow(ax,(0.46,0.75),(0.54,0.75),style='<|-|>',lw=1.6)
ax.text(0.5,0.78,'episodes ⇄ parameters',ha='center',fontsize=6.2)
box(ax,0.06,0.30,0.26,0.20,'SELF-CORRECTION\ncoverage audit → conformal fix\nbias audit → recalibration map',C['fb'],fs=6.6)
box(ax,0.37,0.30,0.26,0.20,'SELF-EXPANSION\nsurprise triggers tasking:\nrequest denser sampling,\nnew variables (e.g. d2m, fapar)',C['fb'],fs=6.6)
box(ax,0.68,0.30,0.26,0.20,'SELF-EVALUATION\nshadow-mode A/B kernels\nretire kernels whose D-stat\ndegrades across seasons',C['fb'],fs=6.6)
box(ax,0.24,0.04,0.52,0.16,'FITNESS METRIC (evolution pressure)\nJ = skill − λ₁·miscalibration − λ₂·staleness − λ₃·forgetting',C['dec'],fs=6.8)
for x in [0.19,0.50,0.81]: arrow(ax,(x,0.30),(0.50,0.20),lw=1.1)
save(fig,'D48_living_loops.png')

# ---------------- D49 MULTI-AGENT ORG ----------------
fig,ax=canvas(8.6,5.4)
ax.text(0.5,0.96,'D49 — Twin organs as cooperating agents (socio-technical governance)',ha='center',fontsize=9.5,weight='bold')
box(ax,0.34,0.78,0.32,0.14,'CONDUCTOR\nscheduler, SLA, kill-switch,\naudit log, policy gates',C['phys'],fs=6.8)
agents=[('OBSERVER\nsatellite/ERA5 ingest',C['obs']), ('FUSER\nQC + derived physics',C['fus']),
        ('SYNCHRONIZER\nEnKF heartbeat',C['core']), ('MNEMONIST\nmemory + retrieval',C['mem']),
        ('PROPHET\nmulti-horizon forecast',C['pred']), ('DREAMER\ncounterfactual futures',C['cf']),
        ('STRATEGIST\ndecision intelligence',C['dec']), ('CRITIC\nred-team audits (T18)',C['kg'])]
for i,(name,col) in enumerate(agents):
    x=0.03+(i%4)*0.245; y=0.42-(i//4)*0.26
    box(ax,x,y,0.21,0.18,name,col,fs=6.4)
    arrow(ax,(0.50,0.78),(x+0.105,y+0.18),lw=0.9,color='#666')
ax.text(0.5,0.03,'Agents communicate via versioned twin-state topics (pub/sub); every write carries provenance & uncertainty.',ha='center',fontsize=6.4)
save(fig,'D49_multiagent.png')

# ---------------- D50 DEPLOYMENT PIPELINE ----------------
fig,ax=canvas(8.8,4.6)
ax.text(0.5,0.96,'D50 — Deployment pipeline: from nightly batch to mission-critical ops',ha='center',fontsize=9.5,weight='bold')
stages=[('INGEST\nGOES/ERA5 watchers\n6-h cron',C['obs']),('VALIDATE\nschema, unit audit,\nQC gates',C['fus']),('SYNC\ntwin core EnKF\n(state store)',C['core']),
        ('FORECAST\narbiter + futures\n(GPU pool)',C['pred']),('DECIDE\nrisk + action cards',C['dec']),('SERVE\ndashboard/API\n(STAC/WMS/tiles)',C['atm'])]
for i,(name,col) in enumerate(stages):
    x=0.03+i*0.163
    box(ax,x,0.55,0.14,0.26,name,col,fs=6.2)
    if i<5: arrow(ax,(x+0.14,0.68),(x+0.163,0.68),lw=1.4)
box(ax,0.03,0.22,0.30,0.20,'shadow mode\n(challenger kernels score silently)',C['kg'],fs=6.4)
box(ax,0.36,0.22,0.30,0.20,'drift sentinels\n(PSI on features, coverage alarms)',C['kg'],fs=6.4)
box(ax,0.69,0.22,0.28,0.20,'rollback & twin-snapshot registry\n(UTC-versioned state)',C['kg'],fs=6.4)
save(fig,'D50_deployment.png')
print('diagrams done')
