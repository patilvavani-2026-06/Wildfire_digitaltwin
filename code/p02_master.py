"""PyroCast Step 2 — master state builder + physics-derived variables (the twin's derived layer)."""
import pandas as pd, numpy as np, json

U = '/home/user/uploads/merged_with_pressure_final.csv'
OUT = '/home/user/PyroCast/'

df = pd.read_csv(U)
df['time'] = pd.to_datetime(df['time'], format='mixed')
df = df.sort_values(['pyroCb_id','time']).reset_index(drop=True)

# ---------- temporal coordinates ----------
g = df.groupby('pyroCb_id', group_keys=False)
df['step'] = g.cumcount()
t0 = g['time'].transform('min')
df['age_h'] = (df['time'] - t0).dt.total_seconds()/3600.0
df['hour_utc'] = df['time'].dt.hour
df['doy'] = df['time'].dt.dayofyear
df['diurnal_sin'] = np.sin(2*np.pi*df['hour_utc']/24); df['diurnal_cos'] = np.cos(2*np.pi*df['hour_utc']/24)
df['season_sin']  = np.sin(2*np.pi*df['doy']/365.25); df['season_cos']  = np.cos(2*np.pi*df['doy']/365.25)

# ---------- upper-air derived ----------
df['wind250'] = np.sqrt(df['u_250']**2 + df['v_250']**2)
dir250 = (np.degrees(np.arctan2(-df['u_250'], -df['v_250'])) + 360) % 360     # meteorological "from"
df['wind_dir250'] = dir250
shear_dir = np.abs(((df['wind_dir250'] - df['wind_dir_deg'] + 180) % 360) - 180)
df['dir_shear_deg'] = shear_dir                                             # directional shear sfc->250 hPa
df['speed_shear'] = df['wind250'] - df['wind_speed10']                      # bulk speed shear
df['gust_factor'] = df['fg10'] / df['wind_speed10'].replace(0, np.nan)

# ---------- boundary-layer / energy ----------
df['ventilation'] = df['blh'] * df['wind_speed10']                          # m^2/s smoke dilution
df['bowen'] = df['sshf'] / df['slhf'].replace(0,np.nan).abs()               # dry-vs-moist heating partition
df['net_hflux'] = df['sshf'] + df['slhf']
df['buoy_forcing'] = df['cape'] - df['cin_filled'].abs()                    # net buoyant energy
df['capped_flag'] = df['capped_flag'].map({True:1,False:0,'TRUE':1,'FALSE':0,1:1,0:0}).astype(float)
df['trigger_idx'] = df['cape'] * (1 - df['capped_flag'].fillna(0))          # uncapped CAPE

# ---------- column moisture structure ----------
df['rh_colmean'] = df[['rh_850','rh_750','rh_650']].mean(axis=1)
df['rh_lapse'] = df['rh_850'] - df['rh_650']                                # moist sfc / dry aloft => +ve
df['dry_air_entrain'] = (100 - df['rh_650'])                                # mid-level dryness (entrainment)

# ---------- terrain-wind alignment (upslope flow) ----------
aspect = np.degrees(np.arctan2(df['aspect_sin'], df['aspect_cos']))         # downslope azimuth
df['upslope_idx'] = np.cos(np.radians(df['wind_dir_deg'] - (aspect+180)%360)) # +1 = wind blows upslope

# ---------- rates of change (temporal derivatives, dt=6h) ----------
def rate(col):
    return g[col].diff()
for c in ['fire_proxy','cloud_height_proxy','raw_cloud_bt','raw_fire_bt','blh','cape','ventilation']:
    df['d_'+c] = rate(c)

# ---------- lifecycle phase (hidden-state observation proxy) ----------
# growth: cloud top cooling (raw_cloud_bt falling); mature: cold & steady; decay: warming / fire_proxy collapse
bt = df['raw_cloud_bt']; db = df['d_raw_cloud_bt'].fillna(0)
df['phase'] = np.where(db < -0.15, 0, np.where(db > 0.15, 2, 1))            # 0 growth,1 mature,2 decay
df['phase_name'] = df['phase'].map({0:'growth',1:'mature',2:'decay'})

# ---------- fuguel moisture proxy (no fuel data uploaded): long-memory dryness proxy ----------
df['dry_spell'] = g['tp'].apply(lambda s: (~(s.fillna(0)>1e-4)).rolling(8,min_periods=1).sum())  # 6-h steps since rain

# ---------- LEAD-1 TARGETS (what the twin must nowcast at t+6h) ----------
lead = lambda col: g[col].shift(-1)
df['y_fire_proxy_p1']   = lead('fire_proxy')
df['y_chp_p1']          = lead('cloud_height_proxy')
df['y_cbt_chg_p1']      = lead('raw_cloud_bt') - df['raw_cloud_bt']         # invigoration (+ = cooling=>growth)
df['y_intensify_p1']    = (lead('cloud_height_proxy') - df['cloud_height_proxy'] > 0).astype(float)
df.loc[df['y_chp_p1'].isna(), 'y_intensify_p1'] = np.nan
df['y_pii_p1']          = lead('PII')

# event-level severity label (for memory retrieval): peak |fire_proxy|, min cloud bt, max blh, max PII
ev = df.groupby('pyroCb_id').agg(
    start=('time','min'), end=('time','max'), n_steps=('step','max'),
    lat=('pixel_latitude','median'), lon=('pixel_longitude','median'),
    fire_peak=('fire_proxy','min'), cbt_min=('raw_cloud_bt','min'),
    blh_max=('blh','max'), cape_max=('cape','max'), pii_max=('PII','max'),
    inj_max=('injection_potential','max'), elev=('elevation','median'),
    rhmin=('rh_colmean','min'), w250_max=('wind250','max'))
ev['duration_h'] = (ev['end']-ev['start']).dt.total_seconds()/3600
ev.to_csv(OUT+'tables/T_event_catalog.csv')
df.to_csv(OUT+'data/master.csv', index=False)
print("master saved:", df.shape)
print("\n=== EVENT CATALOG ===")
print(ev.round(2).to_string())
print("\n=== numeric summary (key cols) ===")
cols=['fire_proxy','cloud_height_proxy','raw_fire_bt','raw_cloud_bt','t2m','sp','blh','cape','cin_filled',
      'tp','slhf','sshf','fg10','wind_speed10','wind250','rh_colmean','rh_lapse','ventilation','bowen',
      'PII','injection_potential','elevation','slope','dist_km']
print(df[cols].describe().T.round(3).to_string())
df[cols].describe().T.round(4).to_csv(OUT+'tables/T_summary_stats.csv')
# correlations with lead targets
num = df.select_dtypes(include=[np.number])
corr = num.corr()
for y in ['y_fire_proxy_p1','y_chp_p1','y_cbt_chg_p1','y_pii_p1']:
    top = corr[y].drop(labels=[y]).abs().sort_values(ascending=False).head(12)
    print(f"\nTop-|corr| with {y}:")
    print(corr[y][top.index].round(3).to_string())
