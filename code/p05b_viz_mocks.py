"""PyroCast Step 5b — NASA-quality visualization concept mockups D51-D55 + animated 4D globe GIF."""
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt, matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle
from mpl_toolkits.mplot3d import Axes3D  # noqa
import matplotlib.animation as animation
R='/home/user/PyroCast/'; FIG=R+'figures/'
plt.rcParams.update({'figure.dpi':140,'savefig.dpi':140,'font.size':8})
rng=np.random.default_rng(3)

# ---- synthetic high-relief terrain (event-179-like) ----------------------
def terrain(n=90):
    x=np.linspace(-3,3,n); y=np.linspace(-3,3,n); X,Y=np.meshgrid(x,y)
    Z=( np.exp(-(X**2+Y**2)/2.2)*2600 + 0.4*np.exp(-((X-1.4)**2+(Y+0.8)**2)/0.7)*1700
        + 0.25*np.exp(-((X+1.5)**2+(Y-1.1)**2)/0.5)*1500 + rng.normal(0,16,(n,n)) )
    from scipy.ndimage import gaussian_filter
    return X,Y,gaussian_filter(Z,1.2)

def plume_points(cx,cy,cz,ntheta=22,nz=34,h=5200,bend=(0.35,0.12)):
    """bent smoke column: radius grows, center drifts with wind"""
    th=np.linspace(0,2*np.pi,ntheta); zs=np.linspace(0,1,nz)
    P=[]
    for z in zs:
        r=70+340*z**1.7
        xo,yo=bend[0]*z*h/40, bend[1]*z*h/40
        for t in th:
            P.append((cx+xo+r*np.cos(t)*(1+0.25*np.sin(3*t+z*9)),
                      cy+yo+r*np.sin(t)*(1+0.25*np.sin(3*t+z*9)), cz+z*h))
    return np.array(P)

def cloud_cap(cx,cy,cz,z0,rx=1050,rz=210,n=26):
    th,ph=np.meshgrid(np.linspace(0,2*np.pi,n),np.linspace(0,np.pi/2,n))
    x=cx+rx*np.cos(th)*np.sin(ph)+0.35*z0/40
    y=cy+rx*np.sin(th)*np.sin(ph)+0.12*z0/40
    z=cz+z0+rz*np.cos(ph)
    return x,y,z

def draw_globe(ax, azim=35, t=0.0):
    ax.clear()
    X,Y,Z=terrain()
    ax.plot_surface(X,Y,Z,cmap='gist_earth',alpha=0.96,lw=0,antialiased=True,zorder=1)
    fx,fy=0.2,-0.4; fz=float(np.exp(-(fx**2+fy**2)/2.2)*2600+300)
    # fire glow
    for rr,a in [(60,0.9),(130,0.55),(230,0.28)]:
        ax.scatter([fx],[fy],[fz+15],s=rr,color='#ff3300',alpha=a,edgecolors='none',zorder=5)
    ax.scatter([fx],[fy],[fz+15],s=26,color='#ffd27f',edgecolors='none',zorder=6)
    # plume
    P=plume_points(fx,fy,fz+30)
    age=np.linspace(0.15,0.85,len(P))
    ax.scatter(P[:,0],P[:,1],P[:,2],s=9,c=np.full(len(P),0.45),alpha=0.10,edgecolors='none',zorder=4)
    # pyroCb cap
    x,y,z=cloud_cap(P[:,0].mean(),P[:,1].mean(),fz+30,4800*(1+0.06*np.sin(t)))
    ax.plot_surface(x,y,z,color='white',alpha=0.88,lw=0,zorder=7)
    ax.view_init(elev=22,azim=azim)
    ax.set_box_aspect((1,1,0.55)); ax.axis('off')
    ax.set_title('PyroCast 4D Twin — terrain ⊗ fire ⊗ plume ⊗ PyroCb (concept render)',fontsize=9)

# D51 static 3D concept
fig=plt.figure(figsize=(8,5.6)); ax=fig.add_subplot(111,projection='3d')
draw_globe(ax,azim=42)
fig.text(0.02,0.02,'GOES overlay: fire-proxy hotspot (amber) • ERA5 BLH volume (grey) • twin plume trajectory • Cesium/WorldWind port: layer groups I–V',
         fontsize=6.8)
fig.savefig(FIG+'D51_globe_3d.png',bbox_inches='tight',facecolor='#0b0f14'); plt.close(fig); print('saved D51')

# animated GIF (rotating, pulsing cap)
fig=plt.figure(figsize=(5.4,3.8)); ax=fig.add_subplot(111,projection='3d')
def upd(i):
    draw_globe(ax, azim=(i*12)%360, t=i/6.0)
    return []
ani=animation.FuncAnimation(fig,upd,frames=30)
ani.save(FIG+'globe_plume.gif',writer='pillow',fps=6,dpi=90)
plt.close(fig); print('saved GIF')

# ---- D52 dashboard mock ---------------------------------------------------
fig=plt.figure(figsize=(11.4,7.0),facecolor='#0d1117')
gs=gridspec.GridSpec(3,8,figure=fig,hspace=0.55,wspace=0.6)
def panel(ax,title):
    ax.set_facecolor('#161b22'); ax.tick_params(colors='#8b949e',labelsize=6)
    for s in ax.spines.values(): s.set_color('#30363d')
    ax.set_title(title,color='#c9d1d9',fontsize=7.4,loc='left',pad=3)
# map panel
ax=fig.add_subplot(gs[0:2,0:4]); panel(ax,'LIVE 4D GLOBE — Cesium viewport (twin state, GOES overlay, plume ensemble)')
ax.imshow(plt.imread(FIG+'D51_globe_3d.png')); ax.set_xticks([]); ax.set_yticks([])
# gauges V1-V4
for i,(v,lab,c) in enumerate([(0.82,'V1 fire intensity','#e63946'),(0.66,'V2 convective energy','#f4a261'),
                              (0.41,'V3 ventilation/RH','#457b9d'),(0.73,'V4 coupling','#2a9d8f')]):
    ax=fig.add_subplot(gs[0,4+i]); panel(ax,lab)
    ax.pie([v,1-v],colors=[c,'#21262d'],startangle=90,counterclock=False,wedgeprops=dict(width=0.32))
    ax.text(0,0,f'{v:.2f}',ha='center',va='center',color='white',fontsize=10,weight='bold')
# futures fan
ax=fig.add_subplot(gs[1,4:6]); panel(ax,'FUTURES FAN — fire proxy +24h')
h=np.arange(1,5); ax.plot(h*6,[ -92,-95,-99,-104],'o-',color='#e63946',ms=3)
ax.fill_between(h*6,[-80,-78,-75,-72],[-104,-112,-121,-131],color='#e63946',alpha=0.25)
ax.plot(h*6,[-92,-90,-87,-83],'--',color='#2a9d8f'); ax.text(6,-83,'S4 rain-out',color='#2a9d8f',fontsize=5.6)
ax.text(20,-128,'S7 extreme',color='#e63946',fontsize=5.6); ax.set_xlabel('lead (h)',color='#8b949e')
# risk ranking
ax=fig.add_subplot(gs[1,6:8]); panel(ax,'ACTION RANKING — CVaR₀.₉')
acts=['task GOES mesoscale','pre-position crews','heighten alert L3','Rx-burn hold']
vals=[0.12,0.31,0.55,0.78]
ax.barh(range(len(acts)),vals,color='#606c38'); ax.set_yticks(range(len(acts)))
ax.set_yticklabels(acts,fontsize=5.8,color='#c9d1d9'); ax.invert_yaxis()
# timeline scrubber
ax=fig.add_subplot(gs[2,0:6]); panel(ax,'4D TIMELINE — event 202 lifecycle (6-h frames; playhead 18:00 UTC Jun 12)')
t=np.arange(24); sig=np.sin(t/3.4)*0.5+0.5
ax.fill_between(t,0,sig,color='#457b9d',alpha=0.6); ax.axvline(17,color='#ffd27f',lw=2)
ax.text(17.2,0.8,'NOW',color='#ffd27f',fontsize=7)
ax.set_xlabel('cycles since ignition',color='#8b949e')
# console
ax=fig.add_subplot(gs[2,6:8]); panel(ax,'TWIN CONSOLE — trust & divergence')
ax.text(0.03,0.85,'Θ trust field      0.87',color='#2a9d8f',fontsize=7,transform=ax.transAxes)
ax.text(0.03,0.60,'D divergence        3.4 σ',color='#f4a261',fontsize=7,transform=ax.transAxes)
ax.text(0.03,0.35,'coverage 80% PI     0.78',color='#2a9d8f',fontsize=7,transform=ax.transAxes)
ax.text(0.03,0.10,'memory hits         258, 216',color='#c9d1d9',fontsize=7,transform=ax.transAxes)
fig.suptitle('D52 — PyroCast Decision Dashboard (layout specification; dark mission-console theme)',color='white',fontsize=10,y=0.99)
fig.savefig(FIG+'D52_dashboard.png',bbox_inches='tight',facecolor='#0d1117'); plt.close(fig); print('saved D52')

# ---- D53 layer stack -------------------------------------------------------
fig,ax=plt.subplots(figsize=(8.6,5.4)); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
ax.set_title('D53 — Rendering stack (CesiumJS/WorldWind/Unreal): five composited layer groups',fontsize=9.5,weight='bold')
layers=[('I   BASE EARTH','Blue Marble / Sentinel-2 imagery • COP-DEM terrain • bathymetry','#3d405b'),
        ('II  OBSERVATIONS','GOES ABI RGB + fire-proxy hotspots • smoke classification alpha','#457b9d'),
        ('III ATMOSPHERE','ERA5 BLH/CAPE/RH isosurfaces • wind vector particles (10 m & 250 hPa)','#2a9d8f'),
        ('IV TWIN STATE','fire front polylines • plume volumes LOD • trust-field tinting Θ(x)','#e63946'),
        ('V   FUTURES','counterfactual plume ghosts • probability isopleths • action pins','#f4a261')]
for i,(a,b,c) in enumerate(layers):
    y=0.86-i*0.17
    ax.add_patch(FancyBboxPatch((0.06+i*0.02,y-0.11),0.74,0.13,boxstyle='round,pad=0.01',fc=c,ec='k',lw=0.5,alpha=0.93))
    ax.text(0.09+i*0.02,y-0.015,a,fontsize=8.2,color='white',weight='bold')
    ax.text(0.09+i*0.02,y-0.070,b,fontsize=6.6,color='white')
    if i<4:
        ax.annotate('',xy=(0.43+(i+1)*0.02,y-0.19),xytext=(0.43+i*0.02,y-0.11),
                    arrowprops=dict(arrowstyle='-|>',color='#333',lw=1.2))
ax.text(0.5,0.02,'compositing: order-independent transparency for volumes; GPU raymarching for smoke; temporal interpolation 6-h → smooth playback',
        ha='center',fontsize=6.4)
fig.savefig(FIG+'D53_layer_stack.png',bbox_inches='tight'); plt.close(fig); print('saved D53')

# ---- D54 4D timeline concept ----------------------------------------------
fig,axes=plt.subplots(3,1,figsize=(9.4,5.6),gridspec_kw={'height_ratios':[2.2,1,1]})
t=np.arange(24)
rib=np.vstack([np.sin(t/6)*0.5+0.5+np.random.rand(24)*0.08, np.cos(t/5)*0.5+0.5+np.random.rand(24)*0.08,
               1/(1+np.exp(-(t-11)))+np.random.rand(24)*0.05, 0.9-0.02*t+np.random.rand(24)*0.05])
im=axes[0].imshow(rib,aspect='auto',cmap='magma')
axes[0].set_yticks(range(4)); axes[0].set_yticklabels(['fire proxy','cloud-top BT','PII','trust Θ'],fontsize=7)
axes[0].set_title('D54 — 4D time system: Hovmöller ribbons + playhead + event markers',fontsize=9.5,weight='bold')
axes[0].axvline(13,color='w',lw=1.6)
axes[1].fill_between(t,0,np.sin(t/3.4)*0.5+0.5,color='#457b9d',alpha=0.55)
axes[1].axvline(13,color='#ffd27f',lw=2); axes[1].set_yticks([]); axes[1].set_ylabel('activity',fontsize=7)
marks=[(3,'ignition+6h'),(9,'first PyroCb'),(13,'NOW'),(19,'decay onset')]
for x,lab in marks: axes[1].annotate(lab,xy=(x,1.0),fontsize=6,rotation=0,xytext=(x,1.25),ha='center',
                                     arrowprops=dict(arrowstyle='-|>',lw=0.7))
axes[1].set_ylim(0,2.1)
ax=axes[2]; ax.plot(t,1/(1+np.exp(-(t-11))),'#e63946')
ax.set_ylabel('P(PyroCb)',fontsize=7); ax.set_xlabel('6-h cycles'); ax.axvline(13,color='#ffd27f',lw=2)
fig.tight_layout(); fig.savefig(FIG+'D54_timeline.png',bbox_inches='tight'); plt.close(fig); print('saved D54')

# ---- D55 counterfactual comparison ----------------------------------------
fig,axes=plt.subplots(1,3,figsize=(11,4.0),facecolor='white')
for ax,(lab,c) in zip(axes[:2],[('BASELINE future','#457b9d'),('S7 COMPOUND EXTREME','#e63946')]):
    X,Y,Z=terrain(50)
    ax.contourf(X,Y,Z,levels=16,cmap='gist_earth'); 
    for k in range(14):
        th=np.linspace(0,2*np.pi,40); w=(60+40*k)* (2.2 if c=='#e63946' else 1.2)
        ax.fill(0.2+0.05*k+w/900*np.cos(th), -0.4+0.03*k+w/900*np.sin(th), color='0.4', alpha=0.08)
    ax.scatter([0.2],[-0.4],s=90,c='#ff3300',marker='^',edgecolors='k',lw=0.5)
    ax.set_title(lab,fontsize=8.5); ax.set_xticks([]); ax.set_yticks([])
axes[2].axis('off')
axes[2].set_title('Δ DELTA VIEWER',fontsize=8.5)
boxt=('ΔP(PyroCb) +0.4 pp\nΔplume top +1.8 km\nΔspread (σ) ×1.9\nconfidence: MEDIUM\n\ninteractions: linked cameras,\nsynced playheads, swipe-blend,\nensemble-members slider k∈[1..48]')
axes[2].add_patch(FancyBboxPatch((0.06,0.25),0.88,0.62,boxstyle='round,pad=0.02',fc='#f6f8fa',ec='k',lw=0.6))
axes[2].text(0.10,0.80,boxt,fontsize=7.4,va='top',family='monospace')
fig.suptitle('D55 — Counterfactual comparison viewport (split world + delta panel)',fontsize=10,weight='bold')
fig.savefig(FIG+'D55_cf_compare.png',bbox_inches='tight'); plt.close(fig); print('saved D55')
print('viz mocks done')
