"""PyroCast Step 4a-2 — delta-target skill, conformal self-calibration, within-event skill."""
import pandas as pd, numpy as np, json, warnings
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import xgboost as xgb
from sklearn.metrics import mean_squared_error, r2_score

R='/home/user/PyroCast/'; FIG=R+'figures/'
df = pd.read_csv(R+'data/master.csv', parse_dates=['time'])
RES = json.load(open(R+'results/metrics_core.json'))
EIDS = sorted(df.pyroCb_id.unique())
FEAT_BLOCKS = json.load(open(R+'results/feature_blocks.json')) if False else None
# rebuild feature list (same as p04a)
FEAT = {
 'GOES':['fire_proxy','cloud_height_proxy','raw_fire_bt','raw_cloud_bt','simulated_green'],
 'ERA5':['t2m','sp','u10','v10','blh','cape','cin_filled','slhf','sshf','fg10','tp'],
 'PRESS':['rh_850','rh_750','rh_650','wind250','dir_shear_deg','speed_shear'],
 'DERIVED':['ventilation','gust_factor','bowen','net_hflux','buoy_forcing','trigger_idx',
            'rh_colmean','rh_lapse','dry_air_entrain','upslope_idx','dry_spell',
            'd_blh','d_cape','d_ventilation'],
 'IDX':['injection_potential','PII','capped_flag'],
 'TERRAIN':['elevation','slope','tpi','tri','cvh','cvl'],
 'TEMP':['age_h','diurnal_sin','diurnal_cos','season_sin','season_cos'],
 'RATE':['d_fire_proxy','d_cloud_height_proxy','d_raw_cloud_bt']}
NOGEO = sum(FEAT.values(),[])
import json as _j; _j.dump(FEAT, open(R+'results/feature_blocks.json','w'))

def xgb_reg(seed=7):
    return xgb.XGBRegressor(n_estimators=220, max_depth=3, learning_rate=0.06, subsample=0.85,
                            colsample_bytree=0.8, reg_lambda=2.0, reg_alpha=0.4, min_child_weight=3,
                            random_state=seed, n_jobs=4)

# ---- 1) delta-targets: does the twin predict CHANGE better than "no change"? ----
DELTAS = {'Δfire proxy (+6h)':('y_fire_proxy_p1','fire_proxy'),
          'ΔPII (+6h)':('y_pii_p1','PII')}
drows=[]
for name,(ycol,base) in DELTAS.items():
    d = df.dropna(subset=[ycol]).copy()
    d['dy'] = d[ycol]-d[base]
    d = d.dropna(subset=['dy'])
    yh = np.full(len(d), np.nan)
    for e in EIDS:
        tr, te = d[d.pyroCb_id!=e], d[d.pyroCb_id==e]
        Xtr=tr[NOGEO].fillna(tr[NOGEO].median()).fillna(0); Xte=te[NOGEO].fillna(tr[NOGEO].median()).fillna(0)
        yh[d.index.get_indexer(te.index)] = xgb_reg().fit(Xtr,tr['dy']).predict(Xte)
    mfin = np.isfinite(yh)
    rm0 = float(mean_squared_error(d['dy'],np.zeros_like(d['dy']))**0.5)
    rm1 = float(mean_squared_error(d['dy'][mfin],yh[mfin])**0.5)
    r2  = float(r2_score(d['dy'][mfin],yh[mfin]))
    RES[name]={'twin':{'RMSE':round(rm1,4),'R2':round(r2,3)},
               'no-change baseline':{'RMSE':round(rm0,4),'R2':0.0},
               'skill improvement %':round(100*(1-rm1/rm0),1)}
    drows.append((name,rm0,rm1))
    print(name, 'no-change RMSE', round(rm0,3), 'twin', round(rm1,3), 'improvement %', round(100*(1-rm1/rm0),1))

fig, ax = plt.subplots(figsize=(6.4,3.4))
x=np.arange(len(drows)); w=0.36
ax.bar(x-w/2,[r[1] for r in drows],w,label='"no-change" baseline',color='#8d99ae')
ax.bar(x+w/2,[r[2] for r in drows],w,label='twin (XGB core)',color='#e63946')
ax.set_xticks(x); ax.set_xticklabels([r[0] for r in drows],fontsize=8)
ax.set_ylabel('LOEO RMSE'); ax.legend()
ax.set_title('F21b — Change-prediction skill: predicting *dynamics*, not levels')
fig.tight_layout(); fig.savefig(FIG+'F21b_delta_skill.png', bbox_inches='tight'); plt.close(fig)

# ---- 2) conformal self-calibration of the 80% PI ----
QP = pd.read_csv(R+'results/quantile_predictions.csv')
# split-half conformal: adjust band half-width via residual quantiles (leave-event-half-out)
QP['lo']=QP.obs-QP.q10; QP['hi']=QP.q90-QP.obs
evs=sorted(QP.pyroCb_id.unique()); half=set(evs[:5])
cal=QP[QP.pyroCb_id.isin(half)]
k_lo=np.quantile(np.maximum(cal.lo,0),0.9); k_hi=np.quantile(np.maximum(cal.hi,0),0.9)
QP['q10_c']=QP.q10-k_lo; QP['q90_c']=QP.q90+k_hi
val=QP[~QP.pyroCb_id.isin(half)]
picp_raw=float(np.mean((QP.obs>=QP.q10)&(QP.obs<=QP.q90)))
picp_cal=float(np.mean((val.obs>=val.q10_c)&(val.obs<=val.q90_c)))
RES['fire_proxy (+6h)']['quantiles_conformal']={'PICP_80_raw':round(picp_raw,3),
     'PICP_80_conformal':round(picp_cal,3),'k_lo':round(float(k_lo),3),'k_hi':round(float(k_hi),3)}
print('conformal:', round(picp_raw,3),'->',round(picp_cal,3))
pd.DataFrame([{'stage':'raw quantile XGB','nominal':0.8,'coverage':round(picp_raw,3)},
              {'stage':'+ conformal self-calibration','nominal':0.8,'coverage':round(picp_cal,3)}]
             ).to_csv(R+'tables/T20b_conformal.csv', index=False)
fig, ax = plt.subplots(figsize=(5.6,3.5))
ax.bar(['raw\nquantile model','after conformal\nself-calibration'],[picp_raw,picp_cal],color=['#8d99ae','#2a9d8f'],width=0.5)
ax.axhline(0.8,color='k',ls='--',lw=0.9); ax.set_ylim(0,1); ax.set_ylabel('coverage of 80% PI')
ax.set_title('F27b — The twin calibrates itself (split-conformal, out-of-event)')
fig.tight_layout(); fig.savefig(FIG+'F27b_conformal.png', bbox_inches='tight'); plt.close(fig)

# ---- 3) within-event standardized skill (removes cross-event level shift) ----
P = pd.read_csv(R+'results/loeo_predictions.csv')
win=[]
for (tgt),grp in P.groupby('target'):
    r2w_x, r2w_p = [],[]
    for e,g in grp.groupby('pyroCb_id'):
        if g.obs.std()<1e-6 or len(g)<6: continue
        r2w_x.append(r2_score(g.obs,g.xgb)); r2w_p.append(r2_score(g.obs,g.persistence))
    win.append({'target':tgt,'within-event R2 twin (median)':round(float(np.median(r2w_x)),3),
                'within-event R2 persistence (median)':round(float(np.median(r2w_p)),3)})
Tw=pd.DataFrame(win); Tw.to_csv(R+'tables/T18_within_event_skill.csv',index=False)
print(Tw.to_string())
RES['within_event_summary']=win
json.dump(RES, open(R+'results/metrics_core.json','w'), indent=1)
print('DONE 4a2')
