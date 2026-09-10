"""PyroCast Step 1 — dataset inventory & deep profiling (all 7 uploaded files)."""
import pandas as pd, numpy as np, json, os
U = '/home/user/uploads/'
OUT = '/home/user/PyroCast/'
files = ['pyrocb_GOES_processed.csv','era5_results (1).csv','merged_pyrocb_era5_features[1].csv',
         'complete_era5_veg.csv','merged_with_terrain.csv','merged_with_terrain_dataset.csv',
         'merged_with_pressure_final.csv']
inv = {}
for f in files:
    df = pd.read_csv(U + f)
    tcols = [c for c in df.columns if c.lower() in ('time','timestamp','valid_time')]
    ids = sorted(map(int, df['pyroCb_id'].unique())) if 'pyroCb_id' in df.columns else []
    rec = {'shape': list(df.shape), 'n_rows': len(df), 'n_events': len(ids), 'ids': ids,
           'columns': list(df.columns),
           'dtypes': {c: str(df[c].dtype) for c in df.columns},
           'missing': {c: int(df[c].isna().sum()) for c in df.columns if int(df[c].isna().sum()) > 0}}
    if tcols and 'pyroCb_id' in df.columns:
        t = pd.to_datetime(df[tcols[0]], errors='coerce', format='mixed')
        rec['time_range'] = [str(t.min()), str(t.max())]
        rec['rows_per_event'] = {int(k): int(v) for k, v in df.groupby('pyroCb_id').size().items()}
        # inter-step spacing
        d = df.copy(); d['_t'] = t
        gaps = d.sort_values(['pyroCb_id','_t']).groupby('pyroCb_id')['_t'].diff().dropna().dt.total_seconds()/3600
        rec['step_hours'] = sorted(gaps.unique().tolist())
    inv[f] = rec
    print(f"### {f}\n  shape={rec['shape']} events={rec['n_events']} ids={ids}")
    print(f"  time={rec.get('time_range')} step_hours={rec.get('step_hours')}")
    print(f"  rows/event={rec.get('rows_per_event')}")
    print(f"  missing={rec['missing']}")
json.dump(inv, open(OUT+'results/inventory_full.json','w'), indent=1)
print("\nsaved -> results/inventory_full.json")

# cross-file identity check: are the 'merged*' files the same core table with growing columns?
base = pd.read_csv(U+'complete_era5_veg.csv')
t2 = pd.read_csv(U+'merged_with_terrain_dataset.csv')
common = [c for c in base.columns if c in t2.columns]
eq = base[common].astype(str).equals(t2[common].astype(str))
print("\ncomplete_era5_veg vs merged_with_terrain_dataset on common cols identical:", eq)
mp = pd.read_csv(U+'merged_with_pressure_final.csv')
common2 = [c for c in t2.columns if c in mp.columns]
print("merged_with_terrain_dataset vs merged_with_pressure_final common identical:",
      t2[common2].astype(str).equals(mp[common2].astype(str)))
