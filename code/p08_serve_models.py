"""PyroCast Step 8 — train full-data serving models for the web twin (post-validation benchmarking).
These are deployment artifacts (LOEO skill already documented in results/)."""
import pandas as pd, numpy as np, json, joblib, warnings
warnings.filterwarnings('ignore')
import xgboost as xgb
R='/home/user/PyroCast/'; W=R+'webapp/'
df=pd.read_csv(R+'data/master.csv', parse_dates=['time'])
FEAT=json.load(open(R+'results/feature_blocks.json')); NOGEO=sum(FEAT.values(),[])
g=df.groupby('pyroCb_id', group_keys=False)
for h in [1,2,3,4]:
    df[f'yf_p{h}']=g['fire_proxy'].shift(-h); df[f'yp_p{h}']=g['PII'].shift(-h)

MAX=df[NOGEO].median()
def X(d): return d[NOGEO].fillna(MAX).fillna(0)
def reg(ycol, seed=7, quant=None):
    kw=dict(n_estimators=220,max_depth=3,learning_rate=0.06,subsample=0.85,colsample_bytree=0.8,
            reg_lambda=2.0,reg_alpha=0.4,min_child_weight=3,random_state=seed,n_jobs=4)
    if quant is not None: kw.update(objective='reg:quantileerror', quantile_alpha=quant)
    d=df.dropna(subset=[ycol])
    m=xgb.XGBRegressor(**kw).fit(X(d), d[ycol])
    return m
models={}
for q in [0.1,0.5,0.9]:
    models[f'fire_p1_q{int(q*100)}']=reg('y_fire_proxy_p1', quant=q)
models['cbt_chg_p1']=reg('y_cbt_chg_p1')
for h in [1,2,3,4]:
    models[f'yf_p{h}']=reg(f'yf_p{h}')
    models[f'yp_p{h}']=reg(f'yp_p{h}')
d=df.dropna(subset=['y_intensify_p1'])
clf=xgb.XGBClassifier(n_estimators=200,max_depth=3,learning_rate=0.06,subsample=0.85,
                      colsample_bytree=0.8,reg_lambda=2.0,random_state=7,n_jobs=4,eval_metric='logloss'
                      ).fit(X(d), d['y_intensify_p1'].astype(int))
models['intensify_clf']=clf
for name,m in models.items(): joblib.dump(m, W+f'models/{name}.joblib')
json.dump({'feature_list':NOGEO,'median_fill':{k:float(v) for k,v in MAX.items()}}, open(W+'models/spec.json','w'), indent=1)
print('saved', len(models), 'serving models')
