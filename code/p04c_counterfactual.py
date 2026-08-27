"""PyroCast Step 4c — Counterfactual Futures Engine: 9 scenario operators x 4 horizons x seed
ensemble -> thousands of futures per event. LOEO hold-out. Tornado, risk heat, futures fan."""
import pandas as pd, numpy as np, json, warnings
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import xgboost as xgb
from scipy.stats import norm

R='/home/user/PyroCast/'; FIG=R+'figures/'
df = pd.read_csv(R+'data/master.csv', parse_dates=['time'])
EIDS = sorted(df.pyroCb_id.unique())
FEAT = json.load(open(R+'results/feature_blocks.json')); NOGEO=sum(FEAT.values(),[])
plt.rcParams.update({'figure.dpi':150,'savefig.dpi':150,'font.size':8.5,'axes.grid':True,'grid.alpha':0.25,'axes.axisbelow':True})
g=df.groupby('pyroCb_id', group_keys=False)
for h in [1,2,3,4]:
    df[f'yf_p{h}']=g['fire_proxy'].shift(-h)
    df[f'yp_p{h}']=g['PII'].shift(-h)

NANFILL = {}
def prep(Xtr, Xte):
    med = Xtr.median()
    return Xtr.fillna(med).fillna(0), Xte.fillna(med).fillna(0)

# ---------- scenario operators: (description, function on physical row dict) ----------
def recompute(r):
    """recompute derived features after perturbations (same formulas as master builder)."""
    ws = max(r['wind_speed10'],1e-3)
    r['ventilation']=r['blh']*ws
    r['gust_factor']=r['fg10']/ws
    r['speed_shear']=r['wind250']-ws
    r['buoy_forcing']=r['cape']-abs(r['cin_filled'])
    r['net_hflux']=r['sshf']+r['slhf']
    r['rh_colmean']=np.mean([r['rh_850'],r['rh_750'],r['rh_650']])
    r['rh_lapse']=r['rh_850']-r['rh_650']
    r['dry_air_entrain']=100-r['rh_650']
    return r
SCEN = {
 'S0 baseline'              : lambda r: r,
 'S1 wind +20%'             : lambda r: recompute({**r,'u10':r['u10']*1.2,'v10':r['v10']*1.2,
                                    'fg10':r['fg10']*1.2,'wind250':r['wind250']*1.2,
                                    'wind_speed10':r['wind_speed10']*1.2}),
 'S2 heatwave +5K'          : lambda r: recompute({**r,'t2m':r['t2m']+5,'rh_850':r['rh_850']*0.75,
                                    'rh_750':r['rh_750']*0.75,'rh_650':r['rh_650']*0.75}),
 'S3 drying RH -30%'        : lambda r: recompute({**r,'rh_850':r['rh_850']*0.70,'rh_750':r['rh_750']*0.70,
                                    'rh_650':r['rh_650']*0.70}),
 'S4 rain-out'              : lambda r: recompute({**r,'tp':0.005,'cape':r['cape']*0.3,'blh':r['blh']*0.6,
                                    'sshf':r['sshf']*0.4,'t2m':r['t2m']-3}),
 'S5 deep drought'          : lambda r: recompute({**r,'dry_spell':r['dry_spell']+4,'rh_850':r['rh_850']*0.85,
                                    'rh_750':r['rh_750']*0.85,'rh_650':r['rh_650']*0.85,
                                    'slhf':r['slhf']*0.6,'sshf':r['sshf']*1.2}),
 'S6 relocate: high-relief' : lambda r: recompute({**r,'elevation':3040.0,'slope':29.0,'tpi':4.57,'tri':1.0,
                                    'cvh':0.889,'cvl':0.094,'upslope_idx':0.8}),
 'S7 compound extreme'      : lambda r: recompute({**r,'t2m':r['t2m']+8,'rh_850':r['rh_850']*0.5,
                                    'rh_750':r['rh_750']*0.5,'rh_650':r['rh_650']*0.5,
                                    'wind250':r['wind250']*1.5,'fg10':r['fg10']*1.4,
                                    'cape':max(r['cape'],1500.0),'wind_speed10':r['wind_speed10']*1.4,
                                    'u10':r['u10']*1.4,'v10':r['v10']*1.4}),
 'S8 pyro-feedback ON'      : lambda r: recompute({**r,'blh':r['blh']*1.3,'cape':r['cape']*1.2})
                              if r['fire_proxy']< -90 else r,
}
pd.DataFrame([{'scenario':k,'operator':v.__doc__ or k} for k,v in SCEN.items()]
             ).assign(description=[k for k in SCEN]).to_csv(R+'tables/T24_scenarios.csv', index=False)

# raw physical columns needed to build scenario feature rows
RAWCOLS = [c for c in NOGEO if c in df.columns] + ['wind_speed10']
def rowdict(s): return {c:(float(s[c]) if pd.notna(s[c]) else np.nan) for c in RAWCOLS}

NSEEDS=3
CF={}; futures=[]; n_futures=0
for tev in EIDS:
    tr=df[df.pyroCb_id!=tev]; te=df[df.pyroCb_id==tev]
    te=te.dropna(subset=['yf_p1'])
    models={}
    for h in [1,2,3,4]:
        for tgt,ycol in [('fire',f'yf_p{h}'),('pii',f'yp_p{h}')]:
            X=tr[NOGEO]; y=tr[ycol].fillna(tr[ycol].median())
            Xp,_ = prep(X, X)
            mset=[xgb.XGBRegressor(n_estimators=180,max_depth=3,learning_rate=0.06,subsample=0.85,
                    colsample_bytree=0.8, reg_lambda=2.0, random_state=s, n_jobs=4).fit(Xp,y)
                  for s in range(NSEEDS)]
            models[(tgt,h)]=mset
    # scenario futures
    rows_out=[]
    for sname, op in SCEN.items():
        P_rows=[]
        for _,s in te.iterrows():
            rd=rowdict(s); rd2={c:rd.get(c,np.nan) for c in RAWCOLS}
            rd2=op(rd2)
            Xs=pd.DataFrame([{c:rd2.get(c,np.nan) for c in NOGEO}])
            Xs= Xs.fillna(tr[NOGEO].median()).fillna(0)
            rec={'event':tev,'scenario':sname,'step':int(s.step)}
            for h in [1,2,3,4]:
                for tgt in ['fire','pii']:
                    preds=np.array([m.predict(Xs)[0] for m in models[(tgt,h)]])
                    rec[f'{tgt}_p{h}_mean']=float(preds.mean()); rec[f'{tgt}_p{h}_sd']=float(preds.std()+1e-6)
            rows_out.append(rec); n_futures+=2*4*NSEEDS
    futures.extend(rows_out)
    print('event',tev,'done')
FUT=pd.DataFrame(futures)
FUT.to_csv(R+'results/counterfactual_futures.csv', index=False)
print('TOTAL FUTURE PREDICTIONS SIMULATED:', n_futures)

# ---------- headline deltas vs baseline ----------
base=FUT[FUT.scenario=='S0 baseline'].set_index(['event','step'])
sumrows=[]
for sname in SCEN:
    S=FUT[FUT.scenario==sname].set_index(['event','step'])
    if sname=='S0 baseline': continue
    d_fire=float((S['fire_p4_mean']-base['fire_p4_mean']).mean())
    d_pii =float((S['pii_p4_mean'] -base['pii_p4_mean']).mean())
    # severe-outcome probabilities at h=4 (Gaussian over seed spread)
    thr_fire=-120.0; thr_pii=0.5
    P_fire_base=float(norm.cdf((thr_fire-base['fire_p4_mean'])/base['fire_p4_sd']).mean())
    P_fire_sc  =float(norm.cdf((thr_fire-S['fire_p4_mean'])/S['fire_p4_sd']).mean())
    P_pii_base =float(1-norm.cdf((thr_pii-base['pii_p4_mean'])/base['pii_p4_sd']).mean())
    P_pii_sc   =float(1-norm.cdf((thr_pii-S['pii_p4_mean'])/S['pii_p4_sd']).mean())
    sumrows.append({'scenario':sname,'dFireProxy_24h':round(d_fire,2),'dPII_24h':round(d_pii,4),
                    'P(fire intense) S0':round(P_fire_base,3),'P(fire intense) scenario':round(P_fire_sc,3),
                    'P(PyroCb PII>0.5) S0':round(P_pii_base,3),'P(PyroCb PII>0.5) scenario':round(P_pii_sc,3)})
T25=pd.DataFrame(sumrows); T25.to_csv(R+'tables/T25_counterfactual_results.csv', index=False)
print(T25.to_string(index=False))

# F36 tornado ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.4,3.9))
T25s=T25.sort_values('dPII_24h')
ax.barh(T25s.scenario, T25s.dPII_24h, color=['#e63946' if v>0 else '#457b9d' for v in T25s.dPII_24h], edgecolor='k', lw=0.4)
ax.axvline(0,color='k',lw=0.8); ax.set_xlabel('Δ predicted PII at +24 h (scenario − baseline)')
ax.set_title('F36 — Counterfactual tornado: which interventions move the future?')
fig.tight_layout(); fig.savefig(FIG+'F36_cf_tornado.png', bbox_inches='tight'); plt.close(fig)

# F37 futures fan for event 253 ----------------------------------------------
e=253
fig, axes = plt.subplots(1,2, figsize=(9.8,3.9), sharex=True)
hh=[1,2,3,4]
show=['S0 baseline','S1 wind +20%','S2 heatwave +5K','S4 rain-out','S7 compound extreme','S8 pyro-feedback ON']
colmap={'S0 baseline':'#1d3557','S1 wind +20%':'#457b9d','S2 heatwave +5K':'#f4a261',
        'S4 rain-out':'#2a9d8f','S7 compound extreme':'#e63946','S8 pyro-feedback ON':'#6d597a'}
for ax,tgt,lab in zip(axes,['fire','pii'],['fire proxy','PII']):
    d0=FUT[FUT.event==e].groupby('scenario')
    for sname in show:
        dd=FUT[(FUT.event==e)&(FUT.scenario==sname)]
        m=[dd[f'{tgt}_p{h}_mean'].mean() for h in hh]
        sd=[dd[f'{tgt}_p{h}_sd'].mean() for h in hh]
        ax.plot([6*h for h in hh], m, '-o', ms=3, lw=1.4, color=colmap[sname], label=sname.replace('S','S').split(' ',1)[0])
        if sname in ('S0 baseline','S7 compound extreme'):
            ax.fill_between([6*h for h in hh], np.array(m)-1.28*np.array(sd), np.array(m)+1.28*np.array(sd),
                            color=colmap[sname], alpha=0.12)
    ax.set_xlabel('lead time (h)'); ax.set_ylabel(lab); ax.legend(fontsize=6.3, ncol=2)
    ax.set_title(f'{lab} — event 253 (Florida): scenario futures', fontsize=8.6)
fig.suptitle('F37 — Counterfactual futures fan (band = ±80% over model-seed ensemble)', y=1.02)
fig.tight_layout(); fig.savefig(FIG+'F37_cf_fan.png', bbox_inches='tight'); plt.close(fig)

# F38 risk heatmap scenario x event ------------------------------------------
thr_pii=0.5
risk=np.zeros((len(EIDS), len(SCEN)-1))
for i,e in enumerate(EIDS):
    b=FUT[(FUT.event==e)&(FUT.scenario=='S0 baseline')]
    for j,sname in enumerate([s for s in SCEN if s!='S0 baseline']):
        S=FUT[(FUT.event==e)&(FUT.scenario==sname)]
        pS=float((1-norm.cdf((thr_pii-S['pii_p4_mean'])/S['pii_p4_sd'])).mean())
        pB=float((1-norm.cdf((thr_pii-b['pii_p4_mean'])/b['pii_p4_sd'])).mean())
        risk[i,j]=pS-pB
cols=[s.replace('S','S').split(' ',1)[0] for s in SCEN if s!='S0 baseline']
fig, ax = plt.subplots(figsize=(7.6,4.6))
im=ax.imshow(risk, cmap='RdBu_r', vmin=-max(abs(risk.min()),abs(risk.max())), vmax=max(abs(risk.min()),abs(risk.max())), aspect='auto')
ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, fontsize=7.5)
ax.set_yticks(range(len(EIDS))); ax.set_yticklabels([f'event {e}' for e in EIDS], fontsize=7.5)
for i in range(len(EIDS)):
    for j in range(len(cols)):
        ax.text(j,i,f'{risk[i,j]:+.2f}',ha='center',va='center',fontsize=6.4)
ax.set_title('F38 — ΔP(PyroCb PII>0.5 at +24 h) under each counterfactual (red = risk amplification)')
fig.colorbar(im, shrink=0.85); fig.tight_layout(); fig.savefig(FIG+'F38_cf_riskheat.png', bbox_inches='tight'); plt.close(fig)

# F35 (SUPERSEDED by p11_f35_fix.py): this curve is the 3-seed jitter floor, NOT predictive uncertainty.
fig, ax = plt.subplots(figsize=(5.8,3.6))
for sname in show:
    dd=FUT[FUT.scenario==sname]
    sd=[dd.groupby(['event','step'])[f'fire_p{h}_sd'].mean().mean() for h in hh]
    ax.plot([6*h for h in hh], sd, '-o', ms=3, lw=1.3, color=colmap[sname], label=sname.split(' ',1)[0])
ax.set_xlabel('lead time (h)'); ax.set_ylabel('predictive σ (fire proxy)')
ax.set_title('F35 (superseded) — 3-seed ensemble jitter vs lead (NOT forecast uncertainty)')
ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(FIG+'F35_uncertainty_growth.png', bbox_inches='tight'); plt.close(fig)

TWIN=json.load(open(R+'results/metrics_twin.json'))
TWIN['counterfactual_engine']={'n_scenarios':len(SCEN),'n_futures':n_futures,
    'headline_dPII':{r['scenario']:r['dPII_24h'] for _,r in T25.iterrows()}}
json.dump(TWIN, open(R+'results/metrics_twin.json','w'), indent=1)
print('COUNTERFACTUAL ENGINE DONE')
