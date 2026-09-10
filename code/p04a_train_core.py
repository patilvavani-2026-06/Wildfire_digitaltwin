"""PyroCast Step 4a — Twin Core training: LOEO-CV nowcast models, uncertainty, ablation, classification."""
import pandas as pd, numpy as np, json, warnings, joblib
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, seaborn as sns
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, roc_auc_score, f1_score, confusion_matrix, roc_curve, precision_recall_curve
import xgboost as xgb

R='/home/user/PyroCast/'; FIG=R+'figures/'
df = pd.read_csv(R+'data/master.csv', parse_dates=['time'])
plt.rcParams.update({'figure.dpi':150,'savefig.dpi':150,'font.size':8.5,'axes.grid':True,'grid.alpha':0.25,'axes.axisbelow':True})
EIDS = sorted(df.pyroCb_id.unique())

# ---------------- feature blocks ----------------
FEAT = {
 'GOES':  ['fire_proxy','cloud_height_proxy','raw_fire_bt','raw_cloud_bt','simulated_green'],
 'ERA5':  ['t2m','sp','u10','v10','blh','cape','cin_filled','slhf','sshf','fg10','tp'],
 'PRESS': ['rh_850','rh_750','rh_650','wind250','dir_shear_deg','speed_shear'],
 'DERIVED':['ventilation','gust_factor','bowen','net_hflux','buoy_forcing','trigger_idx',
            'rh_colmean','rh_lapse','dry_air_entrain','upslope_idx','dry_spell',
            'd_blh','d_cape','d_ventilation'],
 'IDX':   ['injection_potential','PII','capped_flag'],
 'TERRAIN':['elevation','slope','tpi','tri','cvh','cvl'],
 'TEMP':  ['age_h','diurnal_sin','diurnal_cos','season_sin','season_cos'],
 'GEO':   ['pixel_latitude','pixel_longitude'],
 'RATE':  ['d_fire_proxy','d_cloud_height_proxy','d_raw_cloud_bt'],
}
FULL = sum([FEAT[k] for k in ['GOES','ERA5','PRESS','DERIVED','IDX','TERRAIN','TEMP','GEO','RATE']],[])
NOGEO = [c for c in FULL if c not in FEAT['GEO']]

TARGETS = {'fire_proxy (+6h)':'y_fire_proxy_p1','cloud-height proxy (+6h)':'y_chp_p1',
           'cloud-top BT change (+6h)':'y_cbt_chg_p1','PII (+6h)':'y_pii_p1'}

def xgb_reg(seed=7):
    return xgb.XGBRegressor(n_estimators=220, max_depth=3, learning_rate=0.06, subsample=0.85,
                            colsample_bytree=0.8, reg_lambda=2.0, reg_alpha=0.4, min_child_weight=3,
                            random_state=seed, n_jobs=4)

def loeo_split(d, ycol):
    d = d.dropna(subset=[ycol]).copy()
    return [(d[d.pyroCb_id!=e], d[d.pyroCb_id==e]) for e in sorted(d.pyroCb_id.unique())]

RESULTS = {}
preds_store = {}

for tname, ycol in TARGETS.items():
    feats = NOGEO
    d = df.dropna(subset=[ycol])
    yhat = {'persistence':np.full(len(d),np.nan), 'ridge':np.full(len(d),np.nan), 'xgb':np.full(len(d),np.nan)}
    base_col = {'y_fire_proxy_p1':'fire_proxy','y_chp_p1':'cloud_height_proxy',
                'y_cbt_chg_p1':None,'y_pii_p1':'PII'}[ycol]
    for tr, te in loeo_split(d, ycol):
        Xtr = tr[feats].fillna(tr[feats].median()).fillna(0); Xte = te[feats].fillna(tr[feats].median()).fillna(0)
        sc = StandardScaler().fit(Xtr)
        pers = te[base_col] if base_col else pd.Series(0.0, index=te.index)
        yhat['persistence'][d.index.get_indexer(te.index)] = pers.fillna(tr[ycol].mean())
        m = Ridge(alpha=5.0).fit(sc.transform(Xtr), tr[ycol])
        yhat['ridge'][d.index.get_indexer(te.index)] = m.predict(sc.transform(Xte))
        mx = xgb_reg().fit(Xtr, tr[ycol])
        yhat['xgb'][d.index.get_indexer(te.index)] = mx.predict(Xte)
    y = d[ycol].values
    res = {}
    for k in yhat:
        p = yhat[k]; mfin = np.isfinite(p) & np.isfinite(y)
        res[k] = {'RMSE': float(mean_squared_error(y[mfin],p[mfin])**0.5),
                  'MAE': float(mean_absolute_error(y[mfin],p[mfin])),
                  'R2': float(r2_score(y[mfin],p[mfin]))}
    RESULTS[tname] = res
    preds_store[ycol] = pd.DataFrame({'pyroCb_id':d.pyroCb_id.values,'step':d.step.values,'obs':y,
                                      'persistence':yhat['persistence'],'ridge':yhat['ridge'],'xgb':yhat['xgb']})
    print(tname, json.dumps({k:{m:round(v,3) for m,v in r.items()} for k,r in res.items()}))

# metrics table
rows=[]
for tname, res in RESULTS.items():
    for k,v in res.items(): rows.append({'target':tname,'model':k,**{m:round(v,4) for m,v in v.items()}})
T16 = pd.DataFrame(rows); T16.to_csv(R+'tables/T16_metrics_regression.csv', index=False)
pd.concat({k:v for k,v in preds_store.items()}, names=['target']).to_csv(R+'results/loeo_predictions.csv')

# F21 predicted vs observed ------------------------------------------------
fig, axes = plt.subplots(2,2, figsize=(8.6,7.6))
for ax,(tname,ycol) in zip(axes.ravel(), TARGETS.items()):
    P = preds_store[ycol]
    ax.scatter(P.obs, P.xgb, s=14, alpha=0.7, c='#e63946', label='MORPHEUS-XGB', edgecolors='none')
    ax.scatter(P.obs, P.persistence, s=10, alpha=0.35, c='#8d99ae', label='persistence', edgecolors='none')
    lim = [np.nanmin([P.obs.min(),P.xgb.min()]), np.nanmax([P.obs.max(),P.xgb.max()])]
    ax.plot(lim, lim, 'k--', lw=0.8)
    r2 = RESULTS[tname]['xgb']['R2']; r2p = RESULTS[tname]['persistence']['R2']
    ax.set_title(f'{tname}  (R²={r2:.2f} vs pers. {r2p:.2f})', fontsize=8.5)
    ax.set_xlabel('observed'); ax.set_ylabel('predicted'); ax.legend(fontsize=6.5)
fig.suptitle('F21 — Leave-one-event-out nowcast skill (trained twin core)', y=0.995)
fig.tight_layout(); fig.savefig(FIG+'F21_pred_vs_obs.png', bbox_inches='tight'); plt.close(fig)

# F22 residuals ------------------------------------------------------------
fig, axes = plt.subplots(2,2, figsize=(8.6,6.6))
for ax,(tname,ycol) in zip(axes.ravel(), TARGETS.items()):
    P = preds_store[ycol]
    ax.hist(P.obs-P.xgb, bins=24, alpha=0.75, color='#457b9d', label='twin', edgecolor='w', lw=0.3)
    ax.hist(P.obs-P.persistence, bins=24, alpha=0.45, color='#e76f51', label='persistence', edgecolor='w', lw=0.3)
    ax.axvline(0,color='k',lw=0.8); ax.set_title(tname, fontsize=8.5); ax.legend(fontsize=6.5)
    ax.set_xlabel('residual (obs − pred)')
fig.suptitle('F22 — Residual structure: twin vs persistence', y=0.995)
fig.tight_layout(); fig.savefig(FIG+'F22_residuals.png', bbox_inches='tight'); plt.close(fig)

# ---- ablation (feature-block study on two headline targets) --------------
ABL = {'GOES only':FEAT['GOES'], 'GOES+ERA5':FEAT['GOES']+FEAT['ERA5'],
       'GOES+ERA5+PRESS':FEAT['GOES']+FEAT['ERA5']+FEAT['PRESS'],
       '+derived physics':FEAT['GOES']+FEAT['ERA5']+FEAT['PRESS']+FEAT['DERIVED']+FEAT['RATE'],
       'FULL (twin state)':NOGEO,
       'FULL + geography':FULL}
abl_rows=[]
for aname, feats in ABL.items():
    for tname, ycol in [('fire_proxy (+6h)','y_fire_proxy_p1'), ('PII (+6h)','y_pii_p1')]:
        d = df.dropna(subset=[ycol]); phat=np.full(len(d),np.nan)
        for tr,te in loeo_split(d,ycol):
            Xtr=tr[feats].fillna(tr[feats].median()).fillna(0); Xte=te[feats].fillna(tr[feats].median()).fillna(0)
            phat[d.index.get_indexer(te.index)] = xgb_reg().fit(Xtr,tr[ycol]).predict(Xte)
        abl_rows.append({'config':aname,'target':tname,'RMSE':round(mean_squared_error(d[ycol],phat)**0.5,4),
                         'R2':round(r2_score(d[ycol],phat),4)})
T19 = pd.DataFrame(abl_rows); T19.to_csv(R+'tables/T19_ablation.csv',index=False)
print(T19.to_string())
fig, ax = plt.subplots(figsize=(7.6,3.8))
Pv = T19.pivot(index='config', columns='target', values='RMSE').loc[list(ABL.keys())]
Pv.plot(kind='bar', ax=ax, color=['#e63946','#1d3557'])
ax.set_ylabel('LOEO RMSE'); ax.set_title('F24 — Physics-ablation ladder (feature-block contribution)')
ax.tick_params(axis='x', rotation=25)
fig.tight_layout(); fig.savefig(FIG+'F24_ablation.png', bbox_inches='tight'); plt.close(fig)

# ---- feature importance (full-data fit, gain + permutation) ---------------
from sklearn.inspection import permutation_importance
dl = df.dropna(subset=['y_fire_proxy_p1'])
Xf = dl[NOGEO].fillna(dl[NOGEO].median()).fillna(0); yf = dl['y_fire_proxy_p1']
mfull = xgb_reg().fit(Xf, yf)
joblib.dump(mfull, R+'results/model_fire_p1_full.joblib')
imp = pd.Series(mfull.feature_importances_, index=NOGEO).sort_values(ascending=False).head(15)
perm = permutation_importance(mfull, Xf, yf, n_repeats=12, random_state=7, scoring='neg_root_mean_squared_error')
permS = pd.Series(perm.importances_mean, index=NOGEO).sort_values(ascending=False).head(15)
fig, axes = plt.subplots(1,2, figsize=(10,4.6))
imp.sort_values().plot.barh(ax=axes[0], color='#2a9d8f'); axes[0].set_title('Gain importance (XGB)')
permS.sort_values().plot.barh(ax=axes[1], color='#e76f51'); axes[1].set_title('Permutation importance (ΔRMSE)')
fig.suptitle('F23 — What the twin attends to (target: fire proxy +6h)')
fig.tight_layout(); fig.savefig(FIG+'F23_importance.png', bbox_inches='tight'); plt.close(fig)
pd.DataFrame({'gain':imp,'permutation':permS}).to_csv(R+'tables/T_importance_fire.csv')

# F25 per-event RMSE -------------------------------------------------------
fig, axes = plt.subplots(1,2, figsize=(9.6,3.6), sharey=False)
for ax,ycol in zip(axes, ['y_fire_proxy_p1','y_pii_p1']):
    P = preds_store[ycol]
    rows=[]
    for e in EIDS:
        Pe=P[P.pyroCb_id==e]
        if len(Pe)<3: continue
        rows.append((str(e), mean_squared_error(Pe.obs,Pe.xgb)**0.5, mean_squared_error(Pe.obs,Pe.persistence)**0.5))
    Me = pd.DataFrame(rows, columns=['event','twin','persistence']).set_index('event')
    Me.plot(kind='bar', ax=ax, color=['#e63946','#8d99ae'])
    ax.set_title(ycol.replace('y_','').replace('_p1',' +6h'), fontsize=8.5); ax.set_ylabel('RMSE')
    ax.tick_params(axis='x', rotation=0)
fig.suptitle('F25 — Per-event transfer skill (each bar = a wholly unseen fire)', y=1.02)
fig.tight_layout(); fig.savefig(FIG+'F25_per_event.png', bbox_inches='tight'); plt.close(fig)

# ---- probabilistic nowcast: quantile XGB on fire proxy --------------------
YC='y_fire_proxy_p1'; d = df.dropna(subset=[YC])
qs=[0.1,0.5,0.9]; qhat={q:np.full(len(d),np.nan) for q in qs}
for tr,te in loeo_split(d,YC):
    Xtr=tr[NOGEO].fillna(tr[NOGEO].median()).fillna(0); Xte=te[NOGEO].fillna(tr[NOGEO].median()).fillna(0)
    for q in qs:
        m=xgb.XGBRegressor(objective='reg:quantileerror', quantile_alpha=q, n_estimators=220, max_depth=3,
                           learning_rate=0.06, subsample=0.85, colsample_bytree=0.8, random_state=7, n_jobs=4)
        qhat[q][d.index.get_indexer(te.index)] = m.fit(Xtr,tr[YC]).predict(Xte)
y=d[YC].values
picp=float(np.mean((y>=qhat[0.1])&(y<=qhat[0.9])))
sharp=float(np.mean(qhat[0.9]-qhat[0.1]))
pin10=float(np.mean(np.where(y<qhat[0.1],2*(qhat[0.1]-y),0.2*(y-qhat[0.1]))))
RESULTS['fire_proxy (+6h)']['quantiles']={'PICP_80':round(picp,3),'sharpness':round(sharp,3),'pin10_proxy':round(pin10,3)}
print('quantiles', picp, sharp)
pd.DataFrame({'pyroCb_id':d.pyroCb_id,'step':d.step,'obs':y,'q10':qhat[0.1],'q50':qhat[0.5],'q90':qhat[0.9]}
             ).to_csv(R+'results/quantile_predictions.csv', index=False)
T20=pd.DataFrame([{'target':'fire_proxy (+6h)','nominal':0.80,'PICP':round(picp,3),'sharpness':round(sharp,3),
                   'miscalibration':round(abs(0.80-picp),3)}])
# add 50% band
qs5=[0.25,0.75]; q5={q:np.full(len(d),np.nan) for q in qs5}
for tr,te in loeo_split(d,YC):
    Xtr=tr[NOGEO].fillna(tr[NOGEO].median()).fillna(0); Xte=te[NOGEO].fillna(tr[NOGEO].median()).fillna(0)
    for q in qs5:
        m=xgb.XGBRegressor(objective='reg:quantileerror', quantile_alpha=q, n_estimators=180, max_depth=3,
                           learning_rate=0.06, random_state=7, n_jobs=4)
        q5[q][d.index.get_indexer(te.index)] = m.fit(Xtr,tr[YC]).predict(Xte)
picp50=float(np.mean((y>=q5[0.25])&(y<=q5[0.75])))
T20.loc[1]=['fire_proxy (+6h)',0.50,round(picp50,3),round(float(np.mean(q5[0.75]-q5[0.25])),3),round(abs(0.5-picp50),3)]
T20.to_csv(R+'tables/T20_calibration.csv', index=False)

# F26 quantile fan for event 253 -------------------------------------------
QP = pd.read_csv(R+'results/quantile_predictions.csv')
e=253; dq=QP[QP.pyroCb_id==e].sort_values('step')
fig, ax = plt.subplots(figsize=(7.8,3.9))
ax.fill_between(dq.step, dq.q10, dq.q90, color='#457b9d', alpha=0.30, label='80% prediction interval')
ax.plot(dq.step, dq.q50, '-', color='#1d3557', lw=1.6, label='twin median')
ax.plot(dq.step, dq.obs, 'o-', color='#e63946', lw=1.4, label='observed (event 253, Florida)')
ax.set_xlabel('6-h step'); ax.set_ylabel('fire proxy (+6h)')
ax.set_title('F26 — Probabilistic twin trajectory for a wholly unseen event (LOEO)')
ax.legend(); fig.tight_layout(); fig.savefig(FIG+'F26_quantile_fan.png', bbox_inches='tight'); plt.close(fig)

# F27 calibration summary ---------------------------------------------------
fig, ax = plt.subplots(figsize=(4.6,3.9))
ax.bar(['50% PI','80% PI'], [picp50, picp], color=['#2a9d8f','#457b9d'], width=0.5)
ax.plot([-0.4,1.4],[0.5,0.5],'k--',lw=0.9); ax.plot([-0.4,1.4],[0.8,0.8],'k--',lw=0.9)
ax.set_xticks([0,1]); ax.set_xticklabels(['50% PI','80% PI']); ax.set_ylim(0,1)
ax.set_ylabel('observed coverage'); ax.set_title('F27 — Uncertainty calibration (out-of-event)')
fig.tight_layout(); fig.savefig(FIG+'F27_calibration.png', bbox_inches='tight'); plt.close(fig)

# ---- lifecycle intensification classifier ----------------------------------
YC='y_intensify_p1'; d=df.dropna(subset=[YC]); phat=np.full(len(d),np.nan); pscore=np.full(len(d),np.nan)
for tr,te in loeo_split(d,YC):
    Xtr=tr[NOGEO].fillna(tr[NOGEO].median()).fillna(0); Xte=te[NOGEO].fillna(tr[NOGEO].median()).fillna(0)
    mc=xgb.XGBClassifier(n_estimators=200, max_depth=3, learning_rate=0.06, subsample=0.85,
                         colsample_bytree=0.8, reg_lambda=2.0, random_state=7, n_jobs=4, eval_metric='logloss')
    mc.fit(Xtr, tr[YC].astype(int))
    pscore[d.index.get_indexer(te.index)] = mc.predict_proba(Xte)[:,1]
    phat[d.index.get_indexer(te.index)] = mc.predict(Xte)
y=d[YC].astype(int).values
auc=float(roc_auc_score(y,pscore)); f1=float(f1_score(y,phat))
cm=confusion_matrix(y,phat)
RESULTS['lifecycle intensification (+6h)']={'xgb':{'AUC':round(auc,3),'F1':round(f1,3)},
    'majority':{'AUC':0.5,'F1':round(float(f1_score(y,np.zeros_like(y))),3)}}
print('classifier', auc, f1, cm.tolist())
pd.DataFrame([{'target':'lifecycle intensification (+6h)','model':'twin-xgb','AUC':round(auc,3),'F1':round(f1,3)},
              {'target':'lifecycle intensification (+6h)','model':'majority','AUC':0.5,
               'F1':round(float(f1_score(y,np.zeros_like(y))),3)}]).to_csv(R+'tables/T17_classification.csv', index=False)
fig, axes = plt.subplots(1,3, figsize=(11,3.4))
fpr,tpr,_=roc_curve(y,pscore); axes[0].plot(fpr,tpr,color='#e63946',label=f'AUC={auc:.2f}')
axes[0].plot([0,1],[0,1],'k--',lw=0.8); axes[0].legend(); axes[0].set_title('ROC'); axes[0].set_xlabel('FPR'); axes[0].set_ylabel('TPR')
pr,rc,_=precision_recall_curve(y,pscore); axes[1].plot(rc,pr,color='#457b9d'); axes[1].set_title('Precision–Recall'); axes[1].set_xlabel('recall'); axes[1].set_ylabel('precision')
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[2], cbar=False,
            xticklabels=['decay/no-change','intensify'], yticklabels=['decay/no-change','intensify'])
axes[2].set_title('Confusion matrix'); axes[2].set_ylabel('true'); axes[2].set_xlabel('pred')
fig.suptitle('F28 — Lifecycle intensification classifier (LOEO)', y=1.04)
fig.tight_layout(); fig.savefig(FIG+'F28_classifier.png', bbox_inches='tight'); plt.close(fig)

# F39 twin vital-signs radar -------------------------------------------------
def radar(ax, vals, labels, color, title):
    ang=np.linspace(0,2*np.pi,len(labels),endpoint=False).tolist(); ang+=ang[:1]
    v=list(vals)+[vals[0]]
    ax.plot(ang, v, color=color, lw=1.6); ax.fill(ang, v, color=color, alpha=0.25)
    ax.set_xticks(ang[:-1]); ax.set_xticklabels(labels, fontsize=6.8); ax.set_ylim(0,1); ax.set_title(title, fontsize=8)
cat = pd.read_csv(R+'tables/T_event_catalog.csv').set_index('pyroCb_id')
def vitals(e):
    r=cat.loc[e]
    I = 1-(r['fire_peak']-cat.fire_peak.min())/(cat.fire_peak.max()-cat.fire_peak.min()+1e-9)  # intensity
    E = (r['cape_max']-cat.cape_max.min())/(cat.cape_max.max()-cat.cape_max.min()+1e-9)        # convective energy
    V = (r['blh_max']-cat.blh_max.min())/(cat.blh_max.max()-cat.blh_max.min()+1e-9)            # ventilation
    C = (r['inj_max']-cat.inj_max.min())/(cat.inj_max.max()-cat.inj_max.min()+1e-9)            # coupling
    return [float(x) for x in [I,E,V,C]]
labs=['V1 fire\nintensity','V2 convective\nenergy','V3 ventilation /\nmoisture','V4 fire–atmos\ncoupling']
fig, axes = plt.subplots(1,3, subplot_kw={'projection':'polar'}, figsize=(9.6,3.4))
for ax,e,col in zip(axes,[202,253,258],['#e63946','#f4a261','#457b9d']):
    radar(ax, vitals(e), labs, col, f'event {e}')
fig.suptitle('F39 — Twin "vital signs" monitor: each event treated as a living system', y=1.06)
fig.tight_layout(); fig.savefig(FIG+'F39_vitals.png', bbox_inches='tight'); plt.close(fig)

json.dump(RESULTS, open(R+'results/metrics_core.json','w'), indent=1)
print('CORE TRAINING COMPLETE')
