"""PyroCast EDA figure factory — ~20 publication figures into figures/"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.patches import FancyArrowPatch

R = '/home/user/PyroCast/'
df = pd.read_csv(R+'data/master.csv', parse_dates=['time'])
ev = pd.read_csv(R+'tables/T_event_catalog.csv', parse_dates=['start','end'])
FIG = R+'figures/'
plt.rcParams.update({'figure.dpi':150,'savefig.dpi':150,'font.size':8.5,'axes.titlesize':9.5,
                     'axes.labelsize':8.5,'font.family':'DejaVu Sans','axes.grid':True,
                     'grid.alpha':0.25,'axes.axisbelow':True})
C = dict(fire='#e63946', plume='#457b9d', atm='#2a9d8f', warn='#f4a261', dark='#1d3557')
EIDS = sorted(df.pyroCb_id.unique())
pal = sns.color_palette('tab10', 10); cmap_ev = dict(zip(EIDS, pal))
LBL = {179:'179 Johnson (NM)',180:'180 Arizona',181:'181 Utah',189:'189 Lava (CA)',190:'190 BC heat-dome',
       202:'202 Manitoba',216:'216 Yukon',253:'253 Florida',258:'258 Alaska-A',260:'260 Alaska-B'}

def save(fig, name):
    fig.savefig(FIG+name, bbox_inches='tight', facecolor=fig.get_facecolor()); plt.close(fig)
    print('saved', name)

# F01 event map -----------------------------------------------------------
fig, ax = plt.subplots(figsize=(9,4.6))
sev = ev.set_index('pyroCb_id')['inj_max']
for _,r in ev.iterrows():
    ax.scatter(r.lon, r.lat, s=60+700*abs(r.inj_max), c=[cmap_ev[r.pyroCb_id]], alpha=0.85,
               edgecolors='k', linewidths=0.6, zorder=3)
    ax.annotate(str(int(r.pyroCb_id)), (r.lon, r.lat), textcoords='offset points', xytext=(7,4), fontsize=8, weight='bold')
ax.set_xlim(-180,-40); ax.set_ylim(15,75)
ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude')
ax.set_title('F01 — PyroCast event cohort: North-American PyroCb events 2021–2022 (bubble ∝ max injection potential)')
ax.axhspan(60,75,color='b',alpha=0.04); ax.text(-178,70,'boreal / subarctic regime',fontsize=8,style='italic')
ax.axhspan(20,40,color='r',alpha=0.04); ax.text(-178,22,'subtropical / continental regime',fontsize=8,style='italic')
save(fig,'F01_event_map.png')

# F02/F03 trajectory small multiples --------------------------------------
def smallmult(col, ylab, name, title):
    fig, axes = plt.subplots(2,5, figsize=(11.5,4.6), sharex=True)
    for ax, e in zip(axes.ravel(), EIDS):
        d = df[df.pyroCb_id==e]
        ax.plot(d.age_h, d[col], '-o', ms=2.5, lw=1.1, color=cmap_ev[e])
        ax.axhline(0, color='k', lw=0.6, alpha=0.5)
        ax.set_title(LBL[e], fontsize=7.5)
        ax.tick_params(labelsize=6.5)
    for ax in axes[-1]: ax.set_xlabel('event age (h)')
    for ax in axes[:,0]: ax.set_ylabel(ylab)
    fig.suptitle(title, y=1.0)
    fig.tight_layout(); save(fig, name)
smallmult('fire_proxy','fire proxy (BT07–BT14)','F02_traj_fire_proxy.png','F02 — Fire-proxy 6-hourly trajectories per event')
smallmult('raw_cloud_bt','cloud-top BT (norm.)','F03_traj_cloud_bt.png','F03 — Cloud-top brightness-temperature trajectories (lower = colder/deeper convection)')
smallmult('cloud_height_proxy','cloud-height proxy','F03b_traj_chp.png','F03b — Cloud-height proxy trajectories per event')

# F04/F05 Hovmoller --------------------------------------------------------
def hov(col, name, title, cmap):
    piv = df.pivot_table(index='pyroCb_id', columns='step', values=col)
    fig, ax = plt.subplots(figsize=(9,3.6))
    im = ax.imshow(piv.values, aspect='auto', cmap=cmap, interpolation='nearest')
    ax.set_yticks(range(len(piv.index))); ax.set_yticklabels([LBL[i] for i in piv.index], fontsize=7)
    ax.set_xlabel('6-h step since event start'); ax.set_title(title)
    fig.colorbar(im, ax=ax, shrink=0.9)
    save(fig, name)
hov('fire_proxy','F04_hovmoller_fire.png','F04 — Event × time Hovmöller of fire proxy','RdYlBu_r')
hov('raw_cloud_bt','F05_hovmoller_cbt.png','F05 — Event × time Hovmöller of cloud-top BT','viridis')

# F06 correlation heatmap -------------------------------------------------
cols = ['fire_proxy','cloud_height_proxy','raw_fire_bt','raw_cloud_bt','simulated_green','t2m','sp','blh',
        'cape','cin_filled','slhf','sshf','fg10','wind_speed10','wind250','speed_shear','dir_shear_deg',
        'ventilation','gust_factor','rh_colmean','rh_lapse','dry_air_entrain','buoy_forcing','PII',
        'injection_potential','elevation','slope','upslope_idx','age_h']
corr = df[cols].corr()
fig, ax = plt.subplots(figsize=(9.4,8))
sns.heatmap(corr, cmap='RdBu_r', center=0, ax=ax, square=True, cbar_kws={'shrink':0.7},
            xticklabels=True, yticklabels=True, annot=False)
ax.set_title('F06 — Cross-layer Pearson correlation structure (GOES ⊗ ERA5 ⊗ terrain ⊗ derived physics)')
save(fig,'F06_corr_heatmap.png')

# F07 distributions grid ---------------------------------------------------
dcols=['fire_proxy','cloud_height_proxy','raw_fire_bt','raw_cloud_bt','t2m','blh','cape','cin_filled',
       'slhf','sshf','fg10','wind_speed10','wind250','ventilation','rh_colmean','rh_lapse','PII',
       'injection_potential','elevation','slope','upslope_idx','age_h','gust_factor','dist_km']
fig, axes = plt.subplots(4,6, figsize=(12,7.4))
for ax,c in zip(axes.ravel(), dcols):
    ax.hist(df[c].dropna(), bins=26, color=C['plume'], alpha=0.8, edgecolor='w', lw=0.3)
    ax.set_title(c, fontsize=7.5); ax.tick_params(labelsize=6)
fig.suptitle('F07 — Marginal distributions of the twin state variables (n = 227 event-steps)')
fig.tight_layout(); save(fig,'F07_distributions.png')

# F08 diurnal composites ---------------------------------------------------
fig, axes = plt.subplots(2,2, figsize=(8.2,5.6))
for ax,(c,lab) in zip(axes.ravel(), [('blh','BLH (m)'),('sshf','SSHF (J m$^{-2}$/6h)'),
                                     ('cape','CAPE (J kg$^{-1}$)'),('d_raw_cloud_bt','Δ cloud-top BT / 6h')]):
    g = df.groupby('hour_utc')[c].agg(['mean','sem'])
    ax.errorbar(g.index, g['mean'], yerr=1.96*g['sem'], marker='o', ms=3.5, color=C['atm'], capsize=2)
    ax.set_xlabel('UTC hour'); ax.set_ylabel(lab); ax.set_title(lab, fontsize=8.5)
fig.suptitle('F08 — Diurnal composites across all events: the afternoon fire–convection invigoration cycle')
fig.tight_layout(); save(fig,'F08_diurnal.png')

# F09 lead-lag skill -------------------------------------------------------
drivers = ['blh','cape','ventilation','rh_colmean','wind250','slhf','sshf','fire_proxy','raw_cloud_bt']
targets = {'next-step fire proxy':'y_fire_proxy_p1','next-step cloud-height proxy':'y_chp_p1'}
fig, axes = plt.subplots(1,2, figsize=(9.4,3.8))
for ax,(tlab,ycol) in zip(axes, targets.items()):
    rows=[]
    for dcol in drivers:
        for k in [1,2,3,4]:
            lag = df.groupby('pyroCb_id')[dcol].shift(k-1)   # predictor at t-(k-1)
            rows.append((dcol, f'+{(k-1)*6}h', df.assign(_l=lag)[['_l',ycol]].dropna().corr().iloc[0,1]))
    M = pd.DataFrame(rows, columns=['driver','lead','r']).pivot(index='driver', columns='lead', values='r')
    sns.heatmap(M, cmap='RdBu_r', center=0, annot=True, fmt='.2f', ax=ax, cbar_kws={'shrink':0.8}, annot_kws={'size':6.5})
    ax.set_title(f'Driver → {tlab}', fontsize=8.5)
fig.suptitle('F09 — Lead–lag cross-correlation of physical drivers with twin targets', y=1.02)
fig.tight_layout(); save(fig,'F09_leadlag.png')

# F10 phase portrait -------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.6,5))
ph = {0:('growth','#2a9d8f'),1:('mature','#f4a261'),2:('decay','#e63946')}
for p,(lab,col) in ph.items():
    d = df[df.phase==p]
    ax.scatter(d.fire_proxy, d.raw_cloud_bt, s=14, alpha=0.55, c=col, label=lab, edgecolors='none')
for e in EIDS:  # median trajectory arrows
    d = df[df.pyroCb_id==e].dropna(subset=['fire_proxy','raw_cloud_bt'])
    x,y = d.fire_proxy.values, d.raw_cloud_bt.values
    for i in range(0,len(x)-6,6):
        ax.add_patch(FancyArrowPatch((x[i],y[i]),(x[i+5],y[i+5]),arrowstyle='-|>',mutation_scale=8,
                                     color=cmap_ev[e], alpha=0.5, lw=0.9))
ax.set_xlabel('fire proxy (BT07–BT14)'); ax.set_ylabel('cloud-top BT (norm)')
ax.set_title('F10 — Fire–atmosphere phase portrait (arrows = 30-h median drift per event)')
ax.legend(); save(fig,'F10_phase_portrait.png')

# F11 wind roses -----------------------------------------------------------
fig, axes = plt.subplots(1,2, subplot_kw={'projection':'polar'}, figsize=(9,4.2))
for ax,(dircol,spcol,tit) in zip(axes,[('wind_dir_deg','wind_speed10','10-m wind (ERA5)'),
                                       ('wind_dir250','wind250','250-hPa wind (ERA5 pl.)')]):
    th = np.radians(df[dircol].dropna()); sp = df.loc[th.index, spcol]
    nb = 16; bins = np.linspace(0, 2*np.pi, nb+1)
    cnt,_ = np.histogram(th, bins=bins)
    wsp = [sp[(th>=bins[i])&(th<bins[i+1])].mean() for i in range(nb)]
    ax.bar(bins[:-1], cnt, width=2*np.pi/nb, alpha=0.55, color=C['plume'], edgecolor='k', lw=0.4)
    ax.set_theta_zero_location('N'); ax.set_theta_direction(-1); ax.set_title(tit, fontsize=9)
fig.suptitle('F11 — Directional climatology of fire-scale vs steering-level flow', y=1.02)
save(fig,'F11_windroses.png')

# F12 RH vertical profiles -------------------------------------------------
fig, ax = plt.subplots(figsize=(5.6,4.4))
for e in EIDS:
    d = df[df.pyroCb_id==e]
    ax.plot([d.rh_850.mean(), d.rh_750.mean(), d.rh_650.mean()], [850,750,650], '-o', ms=3,
            color=cmap_ev[e], label=LBL[e], lw=1.1)
ax.invert_yaxis(); ax.set_xlabel('Relative humidity (%)'); ax.set_ylabel('Pressure level (hPa)')
ax.set_title('F12 — Event-mean column moisture structure')
ax.legend(fontsize=6.2, ncol=2); save(fig,'F12_rh_profiles.png')

# F13 CAPE-CIN-PII ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(6.6,4.6))
sc = ax.scatter(df.cape, df.cin_filled, c=df.PII, s=10+df.blh/60, cmap='coolwarm', alpha=0.75, edgecolors='k', lw=0.2)
ax.set_xlabel('CAPE (J kg$^{-1}$)'); ax.set_ylabel('CIN filled (J kg$^{-1}$)')
ax.set_title('F13 — Buoyancy phase space (colour = PII, size = BLH)')
fig.colorbar(sc, label='PyroCb Injection Index (PII)'); save(fig,'F13_buoyancy.png')

# F14 heat flux diurnal by regime ------------------------------------------
ev = ev.assign(regime=np.where(ev.lat>55,'boreal', np.where(ev.lat<30,'subtropical','temperate')))
reg = dict(zip(ev.pyroCb_id, ev.regime)); df['regime']=df.pyroCb_id.map(reg)
fig, axes = plt.subplots(1,2, figsize=(9,3.6), sharex=True)
for ax,(c,lab) in zip(axes,[('sshf','sensible heat flux'),('slhf','latent heat flux')]):
    for r,col in [('boreal','#457b9d'),('temperate','#f4a261'),('subtropical','#e63946')]:
        g = df[df.regime==r].groupby('hour_utc')[c].mean()
        ax.plot(g.index, g.values, '-o', ms=3, label=r, color=col)
    ax.set_xlabel('UTC hour'); ax.set_title(lab); ax.legend(fontsize=7)
fig.suptitle('F14 — Surface energy partitioning by fire regime (ECMWF sign: negative = upward)', y=1.03)
fig.tight_layout(); save(fig,'F14_heatflux_regime.png')

# F15 terrain & vegetation -------------------------------------------------
tcat = ev.copy()
fig, axes = plt.subplots(1,4, figsize=(12,3))
axes[0].scatter(tcat.elev, tcat.inj_max, s=40+30*tcat.cape_max, c=[cmap_ev[i] for i in tcat.pyroCb_id], edgecolors='k', lw=0.4)
axes[0].set_xlabel('elevation (m)'); axes[0].set_ylabel('max injection potential'); axes[0].set_title('terrain × injection')
g=df.groupby('pyroCb_id').slope.median(); axes[1].bar(range(10), [g[i] for i in EIDS], color=[cmap_ev[i] for i in EIDS])
axes[1].set_xticks(range(10)); axes[1].set_xticklabels(EIDS, rotation=45, fontsize=6.5); axes[1].set_title('median slope (°)')
veg = df.groupby('pyroCb_id')[['cvh','cvl']].median().loc[EIDS]
axes[2].bar(range(10), veg.cvh, color='#606c38', label='high-veg cover')
axes[2].bar(range(10), veg.cvl, bottom=veg.cvh, color='#dda15e', label='low-veg cover')
axes[2].set_xticks(range(10)); axes[2].set_xticklabels(EIDS, rotation=45, fontsize=6.5); axes[2].legend(fontsize=6.5); axes[2].set_title('vegetation cover structure')
up = df.groupby('pyroCb_id').upslope_idx.mean().loc[EIDS]
axes[3].bar(range(10), up.values, color=[cmap_ev[i] for i in EIDS])
axes[3].axhline(0,color='k',lw=0.7); axes[3].set_xticks(range(10)); axes[3].set_xticklabels(EIDS, rotation=45, fontsize=6.5)
axes[3].set_title('mean upslope-wind index')
fig.suptitle('F15 — Terrain–vegetation controls per event', y=1.05)
fig.tight_layout(); save(fig,'F15_terrain_veg.png')

# F16 missingness ----------------------------------------------------------
raw = pd.read_csv('/home/user/uploads/merged_with_pressure_final.csv')
miss = raw.isna().mean().sort_values(ascending=False)
miss = miss[miss>0]
fig, ax = plt.subplots(figsize=(6.8,3.4))
ax.barh(miss.index, miss.values*100, color=C['warn'])
ax.set_xlabel('% missing'); ax.set_title('F16 — Data-completeness audit (CIN is structurally missing: convectively capped steps)')
save(fig,'F16_missing.png')

# F17 PCA -----------------------------------------------------------------
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
pc = cols[:-1]
X = StandardScaler().fit_transform(df[pc].fillna(df[pc].median()))
p = PCA().fit(X)
fig, axes = plt.subplots(1,2, figsize=(10,3.8))
axes[0].plot(np.cumsum(p.explained_variance_ratio_)*100, '-o', ms=3, color=C['dark'])
axes[0].set_xlabel('n components'); axes[0].set_ylabel('cumulative variance (%)'); axes[0].set_title('PCA scree')
Z = p.transform(X)
for e in EIDS:
    m = (df.pyroCb_id==e).values
    axes[1].scatter(Z[m,0], Z[m,1], s=12, color=cmap_ev[e], label=str(e), alpha=0.8, edgecolors='none')
axes[1].set_xlabel(f'PC1 ({p.explained_variance_ratio_[0]*100:.0f}%)'); axes[1].set_ylabel(f'PC2 ({p.explained_variance_ratio_[1]*100:.0f}%)')
axes[1].legend(fontsize=6.5, ncol=2, title='event'); axes[1].set_title('Twin state space (PC1–PC2)')
fig.suptitle('F17 — Latent structure of the joint fire–atmosphere state', y=1.03)
fig.tight_layout(); save(fig,'F17_pca.png')

# F18 Gantt ----------------------------------------------------------------
fig, ax = plt.subplots(figsize=(9,3.8))
for i,(_,r) in enumerate(ev.sort_values('start').iterrows()):
    ax.barh(r.pyroCb_id, (r.end-r.start).total_seconds()/86400, left=r.start, height=0.6,
            color=cmap_ev[r.pyroCb_id], edgecolor='k', lw=0.4)
ax.set_yticks(sorted(ev.pyroCb_id)); ax.set_ylabel('pyroCb event id'); ax.set_xlabel('date')
ax.set_title('F18 — Observation windows of the 10 tracked PyroCb lifecycles (6-h cadence)')
fig.autofmt_xdate(); save(fig,'F18_gantt.png')

# F19 severity composite ----------------------------------------------------
sevdf = tcat.set_index('pyroCb_id')
rank = (sevdf[['fire_peak','cbt_min']].rank(ascending=True)  # more negative = more intense
        .join(sevdf[['inj_max','pii_max','cape_max']].rank(ascending=False)))
sevdf['severity_score'] = (rank['fire_peak']*0.3 + rank['cbt_min']*0.2 + rank['inj_max']*0.25
                           + rank['pii_max']*0.15 + rank['cape_max']*0.1)
sevdf = sevdf.sort_values('severity_score', ascending=False)
fig, ax = plt.subplots(figsize=(7.4,3.4))
ax.bar([str(i) for i in sevdf.index], sevdf.severity_score, color=[cmap_ev[i] for i in sevdf.index], edgecolor='k', lw=0.4)
ax.set_ylabel('composite severity score'); ax.set_xlabel('event')
ax.set_title('F19 — Event severity composite (fire peak, cloud-top coldness, injection potential, PII, CAPE)')
save(fig,'F19_severity.png')
sevdf.to_csv(R+'tables/T_severity_composite.csv')

# F20 regime embedding ------------------------------------------------------
from sklearn.cluster import KMeans
prof = sevdf[['lat','elev','cape_max','blh_max','w250_max','rhmin','inj_max']].copy()
profS = StandardScaler().fit_transform(prof)
km = KMeans(n_clusters=3, n_init=20, random_state=7).fit(profS)
fig, ax = plt.subplots(figsize=(6,4.2))
Z2 = PCA(n_components=2, random_state=7).fit_transform(profS)
for k in range(3):
    m = km.labels_==k
    ax.scatter(Z2[m,0], Z2[m,1], s=90, label=f'regime cluster {k+1}', edgecolors='k', lw=0.5)
    for i,e in enumerate(sevdf.index[m]):
        ax.annotate(str(e), (Z2[m,0][i], Z2[m,1][i]), fontsize=7, ha='center', va='center', color='w', weight='bold')
ax.set_title('F20 — Fire-regime archetypes in static profile space (k-means, k=3)')
ax.legend(); save(fig,'F20_regimes.png')
pd.DataFrame({'pyroCb_id':sevdf.index,'cluster':km.labels_}).to_csv(R+'tables/T_regime_clusters.csv', index=False)
print("EDA figures complete.")
