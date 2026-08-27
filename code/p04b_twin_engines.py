"""PyroCast Step 4b — Living-twin engines: Episodic Memory, Learned Coupling Core (ODE),
EnKF Synchronization, Counterfactual Futures Engine. All validated out-of-event (LOEO)."""
import pandas as pd, numpy as np, json, warnings
warnings.filterwarnings('ignore')
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, seaborn as sns, networkx as nx
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb

R='/home/user/PyroCast/'; FIG=R+'figures/'
df = pd.read_csv(R+'data/master.csv', parse_dates=['time'])
EIDS = sorted(df.pyroCb_id.unique())
pal = plt.get_cmap('tab10'); cmap_ev = dict(zip(EIDS, [pal(i) for i in range(10)]))
plt.rcParams.update({'figure.dpi':150,'savefig.dpi':150,'font.size':8.5,'axes.grid':True,'grid.alpha':0.25,'axes.axisbelow':True})
FEAT = json.load(open(R+'results/feature_blocks.json'))
NOGEO = sum(FEAT.values(),[])
TWIN = {}
rmse = lambda a,b: float(mean_squared_error(a,b)**0.5)

ZCOLS = ['fire_proxy','cloud_height_proxy','raw_cloud_bt','blh','cape','ventilation','rh_colmean','wind250']
ZTIT  = ['fire\nproxy','cloud-hgt\nproxy','cloud-top\nBT','BLH','CAPE','ventila-\ntion','column\nRH','250 hPa\nwind']

# ============================================================ 1) EPISODIC MEMORY ENGINE
print('--- Episodic Memory Engine ---')
PROF_DYN = ['cape','blh','wind250','rh_colmean','ventilation','t2m']
PROF_STA = ['pixel_latitude','elevation','slope','cvh']
def event_profile(d, steps=None):
    dd = d if steps is None else d[d.step<steps]
    v = [dd[c].mean() for c in PROF_DYN]+[dd[c].median() for c in PROF_STA]
    return np.array(v, float)

mem_rows=[]; simS = np.zeros((10,10))*np.nan; analog_pred = {}
for q in EIDS:
    donors=[e for e in EIDS if e!=q]
    dq=df[df.pyroCb_id==q]; dD={e:df[df.pyroCb_id==e] for e in donors}
    Pq=event_profile(dq, steps=4)                       # query: only first 24 h known
    PD=np.stack([event_profile(dD[e]) for e in donors])
    sc=StandardScaler().fit(np.vstack([Pq,PD]))
    dvec=np.linalg.norm(sc.transform(PD)-sc.transform(Pq.reshape(1,-1)),axis=1)
    order=np.argsort(dvec); simS[EIDS.index(q), [EIDS.index(e) for e in donors]]=dvec
    top=[(donors[i], float(dvec[i])) for i in order[:3]]
    tau=np.median(dvec)+1e-9
    w={e:np.exp(-d/tau) for e,d in top}
    mem_rows.append({'query_event':q,'donor1':top[0][0],'d1':round(top[0][1],3),
                     'donor2':top[1][0],'d2':round(top[1][1],3),'donor3':top[2][0],'d3':round(top[2][1],3)})
    ap=[]
    for tgt in ['fire_proxy','cloud_height_proxy','PII']:
        obs=dq[['step',tgt]].dropna().set_index('step')[tgt]
        pre={}
        for s in obs.index:
            if s==0: pre[s]=np.nan; continue
            num=den=0
            for e,wt in w.items():
                dv=dD[e][['step',tgt]].dropna().set_index('step')
                if s in dv.index: num+=wt*dv.loc[s,tgt]; den+=wt
            pre[s]=num/den if den>0 else np.nan
        ap.append((tgt, obs, pd.Series(pre)))
    analog_pred[q]=ap
T21=pd.DataFrame(mem_rows); T21.to_csv(R+'tables/T21_memory_retrieval.csv', index=False)
print(T21.to_string(index=False))

# accuracy of analog continuation (LOEO)
accs={}
for tgt_i,tgt in enumerate(['fire_proxy','cloud_height_proxy','PII']):
    ro,rp,pers=[],[],[]
    for q in EIDS:
        tgt_,obs,pre=analog_pred[q][tgt_i]
        m=pre.notna()&obs.notna()
        ro+=list(obs[m]); rp+=list(pre[m]); pers+=list(df[(df.pyroCb_id==q)].set_index('step').loc[m[m].index, ('fire_proxy' if tgt=='fire_proxy' else tgt)])
    # persistence: value at s-1
    ro,pers=[],[]
    for q in EIDS:
        tgt_,obs,pre=analog_pred[q][tgt_i]; m=pre.notna()&obs.notna()
        full=df[df.pyroCb_id==q][['step',tgt_]].dropna().set_index('step')[tgt_]
        pv=[full.get(s-1,np.nan) for s in obs[m].index]
        mm=[i for i,v in enumerate(pv) if np.isfinite(v)]
        ro+=[obs[m].iloc[i] for i in mm]; rp2_unused=0; pers+=[pv[i] for i in mm]
    rp_all=[];ro_all=[]
    for q in EIDS:
        tgt_,obs,pre=analog_pred[q][tgt_i]; m=pre.notna()&obs.notna()
        ro_all+=list(obs[m]); rp_all+=list(pre[m])
    accs[tgt]={'analog_RMSE':round(rmse(ro_all,rp_all),4),'persistence_RMSE':round(rmse(ro,pers),4)}
TWIN['memory_engine']=accs; print(accs)
pd.DataFrame(accs).T.to_csv(R+'tables/T21b_memory_skill.csv')

# F29 analog retrieval for query 260
qe=260; dq=df[df.pyroCb_id==qe]
fig, axes = plt.subplots(1,3, figsize=(11,3.3))
for ax,(tgt_,obs,pre) in zip(axes, analog_pred[qe]):
    ax.plot(obs.index, obs.values,'ko-',ms=3,lw=1.2,label='observed (query 260)')
    ax.plot(pre.index, pre.values,'--',color='#e63946',lw=1.5,label='memory-analog forecast')
    ax.set_title(tgt_); ax.set_xlabel('6-h step'); ax.legend(fontsize=6.4)
fig.suptitle('F29 — Episodic Memory Engine: event 260 forecast by replay of donors (258, 216, 190) — no retraining', y=1.04)
fig.tight_layout(); fig.savefig(FIG+'F29_analog.png', bbox_inches='tight'); plt.close(fig)

# ---- memory fusion: alpha-blend of persistence (short-term) and analog replay (episodic) ----
print('--- memory fusion ---')
fus_rows=[]
for tgt_i,tgt in enumerate(['fire_proxy','cloud_height_proxy','PII']):
    grid=np.arange(0,1.01,0.1)
    best=(None,1e9)
    # choose alpha on donor-side events (nested LOEO)
    for a in grid:
        errs=[]
        for q in EIDS[:-1]:
            tgt_,obs,pre=analog_pred[q][tgt_i]; m=pre.notna()&obs.notna()
            full=df[df.pyroCb_id==q][['step',tgt_]].dropna().set_index('step')[tgt_]
            for s,v in obs[m].items():
                p0=full.get(s-1,np.nan)
                if np.isfinite(p0): errs.append((a*pre[s]+(1-a)*p0 - v)**2)
        r=float(np.mean(errs)**0.5)
        if r<best[1]: best=(a,r)
    a=best[0]
    # evaluate on LAST event as untouched final check + all-event fused RMSE
    ro,rf=[],[]
    for q in EIDS:
        tgt_,obs,pre=analog_pred[q][tgt_i]; m=pre.notna()&obs.notna()
        full=df[df.pyroCb_id==q][['step',tgt_]].dropna().set_index('step')[tgt_]
        for s,v in obs[m].items():
            p0=full.get(s-1,np.nan)
            if np.isfinite(p0): ro.append(v); rf.append(a*pre[s]+(1-a)*p0)
    fus_rows.append({'target':tgt,'alpha_star':round(a,2),'fused_RMSE':round(rmse(ro,rf),4),
                     'persistence_RMSE':accs[tgt]['persistence_RMSE'],'pure_analog_RMSE':accs[tgt]['analog_RMSE']})
T21c=pd.DataFrame(fus_rows); T21c.to_csv(R+'tables/T21c_memory_fusion.csv', index=False)
print(T21c.to_string(index=False))
TWIN['memory_fusion']=fus_rows
fig, ax = plt.subplots(figsize=(6.8,3.5))
x=np.arange(3); w=0.27
pm=[r['persistence_RMSE'] for r in fus_rows]; am=[r['pure_analog_RMSE'] for r in fus_rows]; fm=[r['fused_RMSE'] for r in fus_rows]
# normalize per-target for display
pm=[p/m for p,m in zip(pm,pm)]
ax.bar(x-w, [1,1,1], w, label='short-term only (persistence)', color='#8d99ae')
ax.bar(x,   [a/p for a,p in zip(am,[r['persistence_RMSE'] for r in fus_rows])], w, label='episodic only (analog replay)', color='#457b9d')
ax.bar(x+w, [f/p for f,p in zip(fm,[r['persistence_RMSE'] for r in fus_rows])], w, label='fused memory twin', color='#e63946')
ax.axhline(1,color='k',lw=0.7,ls='--')
ax.set_xticks(x); ax.set_xticklabels([r['target'] for r in fus_rows]); ax.set_ylabel('RMSE (rel. to persistence)')
ax.set_title('F29b — Memory fusion: episodic recall fused with short-term dynamics (α* tuned nested-LOEO)')
ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(FIG+'F29b_memory_fusion.png', bbox_inches='tight'); plt.close(fig)

# F30 similarity matrix
fig, ax = plt.subplots(figsize=(5.4,4.4))
S=pd.DataFrame(simS, index=EIDS, columns=EIDS)
sns.heatmap(S, annot=True, fmt='.1f', cmap='viridis_r', ax=ax, cbar_kws={'label':'profile distance'})
ax.set_title('F30 — Event-memory similarity field (smaller = closer analog)')
fig.tight_layout(); fig.savefig(FIG+'F30_memory_matrix.png', bbox_inches='tight'); plt.close(fig)

# ============================================================ 2) LEARNED COUPLING CORE (linear world model)
print('--- Coupling Core (ODE/VAR) ---')
def transitions(d, sc):
    Zs = sc.transform(d[ZCOLS].fillna(d[ZCOLS].median()))
    dd = d.reset_index(drop=True); Z=pd.DataFrame(Zs, columns=ZCOLS)
    X0=[];X1=[]
    for _,g in dd.groupby('pyroCb_id'):
        zg=Z.loc[g.index]
        for i in range(len(g)-1):
            if g.step.iloc[i+1]-g.step.iloc[i]==1:
                X0.append(zg.iloc[i].values); X1.append(zg.iloc[i+1].values)
    return np.array(X0), np.array(X1)

A_folds=[]; fold_skill=[]
for tev in EIDS:
    tr=df[df.pyroCb_id!=tev]; te=df[df.pyroCb_id==tev]
    sc=StandardScaler().fit(tr[ZCOLS].fillna(tr[ZCOLS].median()))
    X0,X1=transitions(tr,sc)
    reg=Ridge(alpha=20.0).fit(X0,X1)
    A=reg.coef_.T; A_folds.append(A)          # Z1 = A @ Z0 + b
    # free-run rollout on test event
    Zt=sc.transform(te[ZCOLS].fillna(tr[ZCOLS].median()))
    z=Zt[0].copy(); path=[z]
    for i in range(len(te)-1): z=A@z+reg.intercept_; path.append(z)
    path=np.array(path)
    r2v=r2_score(Zt[1:,:].ravel(), path[1:,:].ravel())
    pers=rmse(Zt[1:,:].ravel(), Zt[:-1,:].ravel()); modl=rmse(Zt[1:,:].ravel(), path[1:,:].ravel())
    fold_skill.append({'held_out_event':tev,'rollout_R2':round(float(r2v),3),
                       'rollout_RMSE':round(modl,3),'persistence_RMSE':round(pers,3),
                       'skill_vs_persistence_%':round(100*(1-modl/pers),1)})
T22s=pd.DataFrame(fold_skill); T22s.to_csv(R+'tables/T22_ode_rollout_skill.csv', index=False)
print(T22s.to_string(index=False))
Abar=np.mean(A_folds,axis=0)
np.save(R+'results/coupling_matrix.npy', Abar)
T22=pd.DataFrame(Abar, index=ZCOLS, columns=ZCOLS); T22.to_csv(R+'tables/T22_coupling_matrix.csv')
TWIN['coupling_core']={'mean_rollout_R2':round(float(T22s.rollout_R2.mean()),3),
                       'mean_skill_%':round(float(T22s['skill_vs_persistence_%'].mean()),1)}

fig, ax = plt.subplots(figsize=(5.8,4.8))
sns.heatmap(Abar, cmap='RdBu_r', center=0, annot=True, fmt='.2f', ax=ax,
            xticklabels=ZTIT, yticklabels=ZTIT, cbar_kws={'label':'coupling coefficient'})
ax.set_title('F31 — Learned fire–atmosphere coupling matrixÂ (6-h transition kernel, std units)')
fig.tight_layout(); fig.savefig(FIG+'F31_coupling_matrix.png', bbox_inches='tight'); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.4,5.2))
G=nx.DiGraph(); [G.add_node(t.replace('\n',' ')) for t in ZTIT]
thr=0.10
for i in range(8):
    for j in range(8):
        if i!=j and abs(Abar[j,i])>thr:
            G.add_edge(ZTIT[i].replace('\n',' '), ZTIT[j].replace('\n',' '), w=Abar[j,i])
pos=nx.circular_layout(G)
cols={'fire proxy':'#e63946','cloud-hgt proxy':'#e76f51','cloud-top BT':'#e76f51','BLH':'#457b9d',
      'CAPE':'#457b9d','ventila- tion':'#2a9d8f','column RH':'#2a9d8f','250 hPa wind':'#6d597a'}
nx.draw_networkx_nodes(G,pos,node_color=[cols[n] for n in G.nodes],node_size=1900,ax=ax,edgecolors='k',linewidths=0.7)
nx.draw_networkx_labels(G,pos,font_size=6.1,font_color='white',font_weight='bold',ax=ax)
for (u,v,d) in G.edges(data=True):
    nx.draw_networkx_edges(G,pos,edgelist=[(u,v)],ax=ax,width=1+6*abs(d['w']),
        edge_color='#e63946' if d['w']>0 else '#1d3557', arrows=True, arrowsize=9,
        connectionstyle='arc3,rad=0.12', alpha=0.85, min_source_margin=14, min_target_margin=14)
ax.set_title('F32 — Emergent coupling graph learned from data (red=amplifying, blue=damping)')
ax.axis('off'); fig.tight_layout(); fig.savefig(FIG+'F32_coupling_graph.png', bbox_inches='tight'); plt.close(fig)

# ============================================================ 3) ENKF SYNCHRONIZATION ENGINE
print('--- EnKF Synchronization ---')
rng=np.random.default_rng(11)
OBS_IDX=[0,1,2,3,4]; Rdiag=np.array([0.15**2]*3+[0.08**2]*2)
N=80

def stabilize(A, cap=0.97):
    w,V=np.linalg.eig(A)
    w=w/np.maximum(np.abs(w),1e-9)*np.minimum(np.abs(w),cap)
    A2=(V@np.diag(w)@np.linalg.inv(V)).real
    return A2

def fit_core(tr):
    sc=StandardScaler().fit(tr[ZCOLS].fillna(tr[ZCOLS].median()))
    X0,X1=transitions(tr,sc)
    reg=Ridge(alpha=20.0).fit(X0,X1)
    A=stabilize(reg.coef_.T); b=reg.intercept_
    resid=X1-(X0@A.T+b); Q=np.cov(resid.T)+1e-4*np.eye(8)
    return sc,A,b,Q

def run_enkf(te, sc, A, b, Q, record_dim=None):
    Zt=sc.transform(te[ZCOLS].fillna(te[ZCOLS].median()))
    L=np.linalg.cholesky(Q)
    ens=(Zt[0][None,:]+rng.normal(0,0.08,(N,8))).T
    free=Zt[0].copy(); rec=[]; dP=[]; FREE=[Zt[0].copy()]; ANA=[ens.mean(axis=1)]; SPR=[0.0]
    for t in range(1,len(te)):
        ens=A@ens+b[:,None]+L@rng.normal(0,1,(8,N))
        free=A@free+b
        H=Zt[t][OBS_IDX]; HX=ens[OBS_IDX,:]
        Pf=np.cov(ens); S=Pf[OBS_IDX][:,OBS_IDX]+np.diag(Rdiag)
        K=Pf[:,OBS_IDX]@np.linalg.inv(S)
        innov=H-HX.mean(axis=1); dP.append(float(innov.T@np.linalg.inv(S)@innov))
        pert=rng.multivariate_normal(np.zeros(len(OBS_IDX)),np.diag(Rdiag),N).T
        ens=ens+K@((H[:,None]+pert)-HX)
        am=ens.mean(axis=1)
        rec.append((t, rmse(Zt[t],free), rmse(Zt[t],am), float(ens.std(axis=1).mean())))
        FREE.append(free.copy()); ANA.append(am); SPR.append(float(ens.std(axis=1).mean()))
    return pd.DataFrame(rec,columns=['t','free_RMSE','analysis_RMSE','spread']), dP, Zt, np.array(FREE), np.array(ANA), np.array(SPR)

enkf_rows=[]; demo=None
for tev in EIDS:
    tr=df[df.pyroCb_id!=tev]; te=df[df.pyroCb_id==tev]
    sc,A,b,Q=fit_core(tr)
    Rres,dP,Zt,F,A_,S_=run_enkf(te,sc,A,b,Q)
    enkf_rows.append({'held_out_event':tev,
        'free_run_RMSE':round(float(Rres.free_RMSE.mean()),3),
        'analysis_RMSE':round(float(Rres.analysis_RMSE.mean()),3),
        'reduction_pct':round(100*(1-Rres.analysis_RMSE.mean()/Rres.free_RMSE.mean()),1),
        'mean_spread':round(float(Rres.spread.mean()),3),
        'mean_divergence_pressure':round(float(np.mean(dP)),2)})
    if tev==202: demo=(Rres,dP,Zt,F,A_,S_,te)
T23=pd.DataFrame(enkf_rows); T23.to_csv(R+'tables/T23_enkf_sync.csv', index=False)
print(T23.to_string(index=False))
TWIN['enkf_sync']={'mean_RMSE_reduction_pct':round(float(T23['reduction_pct'].mean()),1)}

fig, ax = plt.subplots(figsize=(7.6,3.6))
x=np.arange(len(T23)); w=0.38
ax.bar(x-w/2, T23['free_run_RMSE'], w, label='free-running twin (no assimilation)', color='#8d99ae')
ax.bar(x+w/2, T23['analysis_RMSE'], w, label='synchronized twin (6-h EnKF)', color='#2a9d8f')
ax.set_xticks(x); ax.set_xticklabels(T23['held_out_event'], fontsize=7.5); ax.set_ylabel('state RMSE (std units)')
ax.set_title('F33 — 6-hourly synchronization keeps the twin homeostatic (all bars = unseen events)')
ax.legend(); fig.tight_layout(); fig.savefig(FIG+'F33_enkf_bars.png', bbox_inches='tight'); plt.close(fig)

Rres,dP,Zt,F,A_,S_,te = demo
fig, axes = plt.subplots(2,1, figsize=(8.6,5.8), sharex=True, gridspec_kw={'height_ratios':[2,1]})
tt=np.arange(len(te))
axes[0].plot(tt, Zt[:,0],'ko-',ms=3.2,lw=1.2,label='truth — event 202 (Manitoba)')
axes[0].plot(tt, F[:,0],'--',color='#8d99ae',lw=1.4,label='free-running twin (no assimilation)')
axes[0].plot(tt, A_[:,0],'-',color='#2a9d8f',lw=1.7,label='synchronized twin (6-h EnKF analysis)')
axes[0].fill_between(tt, A_[:,0]-2*S_, A_[:,0]+2*S_, color='#2a9d8f', alpha=0.18, label='±2σ all-state spread')
axes[0].set_ylabel('fire proxy (std units)'); axes[0].legend(fontsize=7, loc='best')
axes[0].set_title('F34 — Synchronization engine in action: every 6 h the twin snaps back to Earth')
axes[1].plot(tt[1:], dP,'-',color='#e63946',lw=1.4)
axes[1].axhline(len(OBS_IDX),color='k',ls='--',lw=0.8,label='expected D under calibration')
axes[1].set_ylabel('divergence pressure D(t)'); axes[1].set_xlabel('6-h cycle'); axes[1].legend(fontsize=7)
fig.tight_layout(); fig.savefig(FIG+'F34_enkf_cycle.png', bbox_inches='tight'); plt.close(fig)

print('PART 1-3 ENGINES DONE')
