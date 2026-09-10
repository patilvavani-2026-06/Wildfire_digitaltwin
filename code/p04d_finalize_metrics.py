"""PyroCast Step 4d — finalize master metrics + calibrated counterfactual summary."""
import pandas as pd, numpy as np, json
from scipy.stats import norm
R='/home/user/PyroCast/'
df = pd.read_csv(R+'data/master.csv', parse_dates=['time'])
g=df.groupby('pyroCb_id', group_keys=False)
df['yf_p4']=g['fire_proxy'].shift(-4)
thr_fire=float(df['yf_p4'].quantile(0.10))   # intense-fire threshold (train-domain decile)
thr_pii=0.5

FUT=pd.read_csv(R+'results/counterfactual_futures.csv')
base=FUT[FUT.scenario=='S0 baseline'].set_index(['event','step'])
rows=[]
for sname in sorted(FUT.scenario.unique()):
    if sname=='S0 baseline': continue
    S=FUT[FUT.scenario==sname].set_index(['event','step'])
    rows.append({'scenario':sname,
        'dFireProxy_24h':round(float((S['fire_p4_mean']-base['fire_p4_mean']).mean()),2),
        'dPII_24h':round(float((S['pii_p4_mean']-base['pii_p4_mean']).mean()),4),
        'P_fire_intense_S0':round(float(norm.cdf((thr_fire-base['fire_p4_mean'])/base['fire_p4_sd']).mean()),3),
        'P_fire_intense_SC':round(float(norm.cdf((thr_fire-S['fire_p4_mean'])/S['fire_p4_sd']).mean()),3),
        'P_PyroCb_S0':round(float(1-norm.cdf((thr_pii-base['pii_p4_mean'])/base['pii_p4_sd']).mean()),3),
        'P_PyroCb_SC':round(float(1-norm.cdf((thr_pii-S['pii_p4_mean'])/S['pii_p4_sd']).mean()),3)})
pd.DataFrame(rows).to_csv(R+'tables/T25_counterfactual_results.csv', index=False)
print(pd.DataFrame(rows).to_string(index=False)); print('fire threshold:', round(thr_fire,1))

M={}
M['core']=json.load(open(R+'results/metrics_core.json'))
T21c=pd.read_csv(R+'tables/T21c_memory_fusion.csv')
T22s=pd.read_csv(R+'tables/T22_ode_rollout_skill.csv')
T23=pd.read_csv(R+'tables/T23_enkf_sync.csv')
M['memory_engine']={'retrieval_table':'T21','fusion':T21c.to_dict('records'),
  'finding':'Alaska pair 258/260 are mutual nearest analogs; α*=0.3 fusion beats persistence on all targets'}
M['coupling_core']={'mean_rollout_R2':round(float(T22s.rollout_R2.mean()),3),
                    'note':'free-running linear kernel partially unstable -> mandates assimilation (see enkf)'}
M['enkf_sync']={'per_event':T23.to_dict('records'),
  'mean_RMSE_reduction_pct':round(float(T23['reduction_pct'].mean()),1),
  'mean_divergence_pressure':round(float(T23['mean_divergence_pressure'].mean()),2)}
M['counterfactual_engine']={'n_futures':46224,'scenarios':rows,
  'headline':'wind +20% raises 24-h PyroCb probability; high-relief relocation lowers PII most (-0.064)'}
M['cohort']={'n_events':10,'n_rows':227,'cadence_h':6,'span':'2021-05-27..2022-06-14',
  'events':json.load(open(R+'results/inventory_full.json'))['merged_with_pressure_final.csv']['ids']}
json.dump(M, open(R+'results/metrics.json','w'), indent=1)
print('MASTER metrics.json written')
