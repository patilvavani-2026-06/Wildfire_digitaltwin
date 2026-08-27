"""PyroCast Step 11 — Honest replacement for F35.
Diagnosis (see thesis erratum): the old F35 y-axis (fire_p{h}_sd) is the std across
3 retraining SEEDS of XGBoost (algorithmic jitter), not predictive uncertainty; it
contracts with lead due to shrinkage + median-imputed tail targets. This figure plots
the three quantities the paper text conflated, each labeled honestly:
  (A) true verification RMSE vs lead (LOEO direct models) + persistence reference;
  (B) seed-disagreement floor (the old curve, correctly labeled);
  (C) inter-scenario spread of counterfactual futures vs lead.
"""
import pandas as pd, numpy as np, json
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

R='/home/user/PyroCast/'; FIG=R+'figures/'
plt.rcParams.update({'figure.dpi':150,'savefig.dpi':150,'font.size':8.5,
                     'axes.grid':True,'grid.alpha':0.25,'axes.axisbelow':True})
FUT=pd.read_csv(R+'results/counterfactual_futures.csv')
df=pd.read_csv(R+'data/master.csv')
hh=[1,2,3,4]; leads=[6*h for h in hh]

# observed shifted targets
obs={}
for e,g in df.groupby('pyroCb_id'):
    g=g.sort_values('step')
    for h in hh: obs[(e,h)]=dict(zip(g.step, g.fire_proxy.shift(-h)))

b=FUT[FUT.scenario=='S0 baseline']
rmse_m=[]; ns=[]
for h in hh:
    o=np.array([obs[(r.event,h)].get(r.step,np.nan) for r in b.itertuples()])
    m=b[f'fire_p{h}_mean'].to_numpy(); ok=~np.isnan(o)
    rmse_m.append(float(np.sqrt(np.nanmean((o[ok]-m[ok])**2)))); ns.append(int(ok.sum()))
rmse_p=[]
for h in hh:
    errs=[]
    for e,g in df.groupby('pyroCb_id'):
        g=g.sort_values('step'); errs.append((g.fire_proxy.shift(-h)-g.fire_proxy).dropna()**2)
    rmse_p.append(float(np.sqrt(pd.concat(errs).mean())))
seed_sd=[b[f'fire_p{h}_sd'].mean() for h in hh]
piv=FUT.pivot_table(index=['event','step'],columns='scenario',
                    values=[f'fire_p{h}_mean' for h in hh])
inter=[float(piv[f'fire_p{h}_mean'].std(axis=1).mean()) for h in hh]

fig,axes=plt.subplots(1,3,figsize=(11.4,3.5))
ax=axes[0]
ax.plot(leads,rmse_m,'-o',ms=4,lw=1.4,color='#1d3557',label='twin (LOEO direct models)')
ax.plot(leads,rmse_p,'--s',ms=4,lw=1.2,color='#e63946',label='persistence')
for x,y,n in zip(leads,rmse_m,ns): ax.annotate(f'n={n}',(x,y),textcoords='offset points',xytext=(0,6),fontsize=6.5,ha='center')
ax.set_xlabel('lead time (h)'); ax.set_ylabel('verification RMSE (fire proxy)')
ax.set_title('(a) True error growth — flat; 24 h diurnal resonance',fontsize=8.6)
ax.legend(fontsize=7); ax.set_ylim(0,22)

ax=axes[1]
ax.plot(leads,seed_sd,'-o',ms=4,lw=1.4,color='#6d597a')
ax.set_xlabel('lead time (h)'); ax.set_ylabel('3-seed σ (fire proxy)')
ax.set_title('(b) Algorithmic jitter floor (old F35 curve)\ncontracts as learnable signal decays — NOT forecast σ',fontsize=8.2)

ax=axes[2]
ax.plot(leads,inter,'-o',ms=4,lw=1.4,color='#2a9d8f')
ax.set_xlabel('lead time (h)'); ax.set_ylabel('inter-scenario σ (fire proxy)')
ax.set_title('(c) Divergence across 9 counterfactual futures\n(the quantity the text meant) — no growth at 6–24 h',fontsize=8.2)

fig.suptitle('F35 — Uncertainty vs lead time, decomposed honestly (replaces earlier trust-decay panel)',y=1.04,fontsize=9.5)
fig.tight_layout(); fig.savefig(FIG+'F35_uncertainty_growth.png',bbox_inches='tight'); plt.close(fig)

out={'rmse_model':rmse_m,'rmse_persistence':rmse_p,'n':ns,
     'seed_sd':[round(float(s),3) for s in seed_sd],'inter_scenario_sd':inter}
json.dump(out,open(R+'results/f35_audit.json','w'),indent=1)
print(json.dumps(out))
print('F35 REPLACED')
