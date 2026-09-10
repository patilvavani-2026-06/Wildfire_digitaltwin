"""PyroCast Step 9 — export all data packs (JSON + inline JS pack) for the web digital twin."""
import pandas as pd, numpy as np, json, warnings
warnings.filterwarnings('ignore')
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
R='/home/user/PyroCast/'; W=R+'webapp/data/'
df=pd.read_csv(R+'data/master.csv', parse_dates=['time'])
EIDS=sorted(df.pyroCb_id.unique())
rmse=lambda a,b: float(mean_squared_error(a,b)**0.5)
NAMES={179:'Johnson (Gila, NM)',180:'Arizona (Telegraph-consistent)',181:'SW Utah',189:'Lava (Mt Shasta, CA)',
       190:'BC heat-dome',202:'Manitoba Interlake',216:'Yukon',253:'South Florida',258:'Alaska A',260:'Alaska B'}
REGIME={179:'high-elevation',180:'arid-continental',181:'plateau',189:'cascade',190:'boreal',
        202:'boreal',216:'subarctic',253:'subtropical',258:'boreal',260:'boreal'}
cat=pd.read_csv(R+'tables/T_event_catalog.csv', parse_dates=['start','end'])

# --- events catalog ---
events=[]
for _,r in cat.iterrows():
    e=int(r.pyroCb_id)
    events.append({'id':e,'name':NAMES[e],'regime':REGIME[e],'lat':float(r.lat),'lon':float(r.lon),
        'start':str(r['start']),'end':str(r['end']),'duration_h':float(r.duration_h),
        'fire_peak':float(r.fire_peak),'cbt_min':float(r.cbt_min),'blh_max':float(r.blh_max),
        'cape_max':float(r.cape_max),'pii_max':float(r.pii_max),'inj_max':float(r.inj_max),
        'elev':float(r.elev),'rhmin':float(r.rhmin),'w250_max':float(r.w250_max)})
json.dump(events, open(W+'events.json','w'), indent=1)

# --- series per event (chart + 4D arrays) ---
SERIES={}
KEEP=['step','time','age_h','hour_utc','fire_proxy','cloud_height_proxy','raw_fire_bt','raw_cloud_bt',
      'simulated_green','t2m','blh','cape','cin_filled','tp','slhf','sshf','fg10','wind_speed10',
      'wind_dir_deg','wind250','wind_dir250','rh_850','rh_750','rh_650','rh_colmean','ventilation',
      'buoy_forcing','PII','injection_potential','phase','phase_name','elevation','slope','upslope_idx']
for e in EIDS:
    d=df[df.pyroCb_id==e].sort_values('step')
    rec={}
    for c in KEEP:
        v=d[c]
        if c=='time': rec[c]=[str(x) for x in v]
        else: rec[c]=[None if pd.isna(x) else (float(x) if not isinstance(x,str) else x) for x in v]
    SERIES[str(e)]=rec
json.dump(SERIES, open(W+'series.json','w'), indent=1)

# --- EnKF sync table + event-202 demo arrays (regenerate deterministically) ---
T23=pd.read_csv(R+'tables/T23_enkf_sync.csv')
enkf={'table':T23.to_dict('records')}
ZCOLS=['fire_proxy','cloud_height_proxy','raw_cloud_bt','blh','cape','ventilation','rh_colmean','wind250']
def transitions(dd, sc):
    Z=pd.DataFrame(sc.transform(dd[ZCOLS].fillna(dd[ZCOLS].median())),columns=ZCOLS)
    X0=[];X1=[]
    base=dd.reset_index(drop=True)
    for _,gr in base.groupby('pyroCb_id'):
        zg=Z.loc[gr.index]
        for i in range(len(gr)-1):
            if gr.step.iloc[i+1]-gr.step.iloc[i]==1: X0.append(zg.iloc[i].values); X1.append(zg.iloc[i+1].values)
    return np.array(X0),np.array(X1)
def stabilize(A,cap=0.97):
    w,V=np.linalg.eig(A); w=w/np.maximum(np.abs(w),1e-9)*np.minimum(np.abs(w),cap)
    return (V@np.diag(w)@np.linalg.inv(V)).real
def run_demo(tev=202, seed=11):
    rng=np.random.default_rng(seed)
    tr=df[df.pyroCb_id!=tev]; te=df[df.pyroCb_id==tev]
    sc=StandardScaler().fit(tr[ZCOLS].fillna(tr[ZCOLS].median()))
    X0,X1=transitions(tr,sc); reg=Ridge(alpha=20.0).fit(X0,X1)
    A=stabilize(reg.coef_.T); b=reg.intercept_; Q=np.cov((X1-(X0@A.T+b)).T)+1e-6*np.eye(8)
    L=np.linalg.cholesky(Q); OBS=[0,1,2,3,4]; Rd=np.array([0.15**2]*3+[0.08**2]*2); Nn=80
    Zt=sc.transform(te[ZCOLS].fillna(te[ZCOLS].median()))
    ens=(Zt[0][None,:]+rng.normal(0,0.08,(Nn,8))).T; free=Zt[0].copy()
    FREE=[free[0]]; ANA=[ens.mean(axis=1)[0]]; SPR=[0.0]; DP=[]
    for t in range(1,len(te)):
        ens=A@ens+b[:,None]+L@rng.normal(0,1,(8,Nn)); free=A@free+b
        H=Zt[t][OBS]; HX=ens[OBS,:]; Pf=np.cov(ens); S=Pf[OBS][:,OBS]+np.diag(Rd); K=Pf[:,OBS]@np.linalg.inv(S)
        innov=H-HX.mean(axis=1); DP.append(float(innov.T@np.linalg.inv(S)@innov))
        pert=rng.multivariate_normal(np.zeros(5),np.diag(Rd),Nn).T
        ens=ens+K@((H[:,None]+pert)-HX)
        FREE.append(float(free[0])); ANA.append(float(ens.mean(axis=1)[0])); SPR.append(float(ens.std(axis=1).mean()))
    return {'truth':[float(v) for v in Zt[:,0]],'free':FREE,'analysis':ANA,'spread':SPR,'divergence':DP}
enkf['demo']=run_demo()
json.dump(enkf, open(W+'enkf.json','w'), indent=1)

# --- memory packs ---
T21=pd.read_csv(R+'tables/T21_memory_retrieval.csv')
memory={'retrieval':T21.to_dict('records'),
        'fusion':pd.read_csv(R+'tables/T21c_memory_fusion.csv').to_dict('records')}
json.dump(memory, open(W+'memory.json','w'), indent=1)

# --- coupling matrix ---
cm=pd.read_csv(R+'tables/T22_coupling_matrix.csv', index_col=0)
json.dump({'labels':list(cm.index),'matrix':[[float(v) for v in row] for row in cm.values]}, open(W+'coupling.json','w'), indent=1)

# --- futures aggregated (scenario x horizon means/sd per event) ---
FUT=pd.read_csv(R+'results/counterfactual_futures.csv')
agg={}
for (e,scen),grp in FUT.groupby(['event','scenario']):
    rec={}
    for h in [1,2,3,4]:
        rec[f'fire_p{h}']=[float(grp[f'fire_p{h}_mean'].mean()), float(grp[f'fire_p{h}_sd'].mean())]
        rec[f'pii_p{h}']=[float(grp[f'pii_p{h}_mean'].mean()), float(grp[f'pii_p{h}_sd'].mean())]
    agg.setdefault(str(int(e)),{})[scen]=rec
json.dump({'scenarios':sorted(FUT.scenario.unique()),'by_event':agg}, open(W+'futures.json','w'), indent=1)

# --- scenario operators + T25 summary + risk rubric ---
T25=pd.read_csv(R+'tables/T25_counterfactual_results.csv')
json.dump({'operators':pd.read_csv(R+'tables/T24_scenarios.csv').scenario.tolist(),
           'summary':T25.to_dict('records')}, open(W+'counterfactual.json','w'), indent=1)

# --- metrics core ---
json.dump(json.load(open(R+'results/metrics.json')), open(W+'metrics.json','w'), indent=1)
json.dump(json.load(open(R+'results/metrics_core.json')), open(W+'metrics_core.json','w'), indent=1)
json.dump(json.load(open(W+'../models/spec.json')), open(W+'feature_spec.json','w'), indent=1)

# --- per-event raw feature rows for live inference endpoint ---
def _v(v):
    import pandas as _pd
    if _pd.isna(v): return None
    if isinstance(v, _pd.Timestamp): return str(v)
    if isinstance(v, (str,bool,np.bool_)): return str(v)
    return float(v)
rows={}
for e in EIDS:
    d=df[df.pyroCb_id==e].sort_values('step')
    rows[str(e)]=[{c:_v(v) for c,v in r.items()} for _,r in d.iterrows()]
json.dump(rows, open(W+'rows.json','w'), indent=1)

# --- inline JS pack (offline fallback: window.PYROCAST_DATA) ---
pack={}
for f in ['events','series','enkf','memory','coupling','futures','counterfactual','metrics','metrics_core']:
    pack[f]=json.load(open(W+f+'.json'))
js='const PYROCAST_DATA = '+json.dumps(pack)+';'
open(W+'pack.js','w').write(js)
print('data packs exported:', sorted(__import__("os").listdir(W)))
