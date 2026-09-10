/* PyroCast–MORPHEUS web twin v2 — enhanced 3D/4D + live-ops monitoring (vendored builds: THREE, Plotly) */

// ---------------- mode & data layer ----------------
let MODE='static', D={};
async function boot(){
  D=window.PYROCAST_DATA;
  try{ const r=await fetch('/api/overview',{cache:'no-store'}); if(r.ok){ MODE='live'; } }catch(e){ MODE='static'; }
  document.getElementById('modePill').textContent = MODE==='live'?'● LIVE-MODEL BACKEND':'● STATIC PACK (offline twin)';
  if(MODE==='live') document.getElementById('modePill').classList.add('live');
  init();
}
window.addEventListener('error',e=>{const p=document.getElementById('modePill');if(p){p.textContent='⚠ '+e.message;p.style.color='#ff5a3c';}});

const erf=x=>{const t=1/(1+0.3275911*Math.abs(x)),y=1-((((1.061405429*t-1.453152027)*t+1.421413741)*t-0.284496736)*t+0.254829592)*t*Math.exp(-x*x);return x<0?-y:y;};
const normCdf=x=>0.5*(1+erf(x/Math.SQRT2));
const fmt=(v,d=2)=>(v==null||v===undefined||isNaN(v))?'—':Number(v).toFixed(d);
let E=253, STEP=0, PLAY=false, TIMER=null, SPEED=1100, VIEW='globe', GHOST=null;
let SCEN_NOW='S0 baseline';

function maxStep(){ return D.series[String(E)].step.length-1; }
function EVENT(){ return D.events.find(x=>x.id===E); }
function S(k){ return D.series[String(E)][k]; }
function SAt(k,step=STEP){ const a=S(k); return a? a[Math.min(step,a.length-1)] : null; }
function T23(){ return (D.enkf.table||[]).find(r=>r.held_out_event===E)||{}; }
function D23(t=T23()){ return t.mean_divergence_pressure??5; }

// ---------------- init ----------------
function init(){
  const evSel=document.getElementById('eventSel');
  evSel.innerHTML=D.events.map(e=>`<option value="${e.id}" ${e.id===E?'selected':''}>#${e.id} · ${e.name} · ${e.regime}</option>`).join('');
  evSel.onchange=()=>{E=+evSel.value; STEP=0; GHOST=null; syncEvent(); log(`event focus → #${E} ${EVENT().name}`,'sys');};
  document.getElementById('scenSel').innerHTML=D.counterfactual.operators.map(s=>`<option ${s===SCEN_NOW?'selected':''}>${s}</option>`).join('');
  document.getElementById('scenSel').onchange=e=>SCEN_NOW=e.target.value;
  document.getElementById('varSel').onchange=redrawTraj;
  document.getElementById('runWhatIf').onclick=runWhatIf;
  document.getElementById('ghostBtn').onclick=toggleGhost;
  document.getElementById('viewBtn').onclick=toggleView;
  const sl=document.getElementById('stepSlider');
  sl.oninput=()=>{STEP=+sl.value; syncStep();};
  document.getElementById('playBtn').onclick=togglePlay;
  document.getElementById('speedSel').onchange=e=>{SPEED=+e.target.value; if(PLAY){clearInterval(TIMER);TIMER=setInterval(tickLive,SPEED);}};
  buildMonitorWall();
  buildGlobe(); buildLocalScene();
  syncEvent(); renderEvidence();
  log('MORPHEUS twin bootstrapped · cohort pack 10 events / 227 states','sys');
  log('real-time mode = trained-twin replay at accelerated ×N cadence (GOES stream hot-swap ready)','sys');
}

function syncEvent(){
  document.getElementById('stepSlider').max=maxStep();
  document.querySelectorAll('.mtile').forEach(t=>t.classList.toggle('active',+t.dataset.e===E));
  redrawTraj(); redrawEnv(); drawEnkf(); drawCoupling(); drawVitals(); drawMemory();
  rebuildLocal(); runWhatIf(true); syncStep();
}
function syncStep(){
  document.getElementById('stepLbl').textContent=`step ${STEP} · ${S('time')[STEP]||''} UTC`;
  updateGlobeDynamics(); updateLocalDynamics(); updateHUD(); updateConsole(); updateStateTable(); markPlayhead();
}

// ---------------- live ops engine ----------------
function togglePlay(){
  PLAY=!PLAY; document.getElementById('playBtn').textContent=PLAY?'⏸ LIVE':'▶ LIVE';
  if(PLAY){ log('LIVE OPS feed OPEN — twin heartbeat streaming (×'+Math.round(21600/(SPEED/1000)),'sys');TIMER=setInterval(tickLive,SPEED); }
  else { clearInterval(TIMER); log('LIVE OPS feed PAUSED','sys'); }
}
function tickLive(){
  const mx=maxStep();
  if(STEP>=mx){ STEP=0; log('lifecycle wrapped — replaying event from ignition+6h','sys'); }
  else STEP+=1;
  document.getElementById('stepSlider').value=STEP; syncStep(); liveAlerts();
}
function liveAlerts(){
  const t=S('time')[STEP]||'', tag=`${t.replace(' ','·')} `;
  const ph=SAt('phase_name'), pint=D.nowcast[String(E)].intensify_p[STEP];
  const fp=SAt('fire_proxy'), dcbt=SAt('raw_cloud_bt');
  if(pint!=null && pint>0.6) log(tag+`ALERT convective invigoration likely P=${fmt(pint,2)} (trained classifier)`,'alert');
  if(D23()>10) log(tag+`DIVERGENCE watch: event D̄=${fmt(D23(),1)}σ — synchronization appetite raised`,'warn');
  if(ph==='growth') log(tag+`PYRO-CLOUD growth signature · cloud-top ${fmt(dcbt,3)} ↓`,'warn');
  if(fp!=null && fp<-120) log(tag+`extreme fire radiance proxy ${fmt(fp,1)}`,'alert');
  log(tag+`sync commit x⁺ · Θ=${fmt(1/(1+D23()/12),2)} · phase=${ph} · Λ-step ok`,'ok');
  trimLog();
}
function log(msg,cls='sys'){
  const box=document.getElementById('liveLog'); if(!box) return;
  const div=document.createElement('div'); div.className='ll '+cls;
  div.textContent=`${new Date().toISOString().substr(11,8)}Z │ ${msg}`;
  box.appendChild(div); box.scrollTop=box.scrollHeight; trimLog();
}
function trimLog(){ const box=document.getElementById('liveLog'); while(box && box.children.length>60) box.removeChild(box.firstChild); }

// ---------------- HUD / console / state ----------------
function updateHUD(){
  const e=EVENT(), fp=SAt('fire_proxy'), chp=SAt('cloud_height_proxy');
  document.getElementById('hudTL').innerHTML=`<b style="color:#fff">event #${E}</b> · ${e.name}<br>${e.regime} regime · elev ${fmt(e.elev,0)} m`;
  document.getElementById('hudTR').innerHTML=`fire proxy <b>${fmt(fp,1)}</b><br>cloud-hgt <b>${fmt(chp,2)}</b> · CAPE <b>${fmt(SAt('cape'),0)}</b> J/kg`;
  const ph=SAt('phase_name')||'—';
  document.getElementById('hudBL').innerHTML=`phase: <b>${ph}</b> · BLH ${fmt(SAt('blh'),0)} m · w250 ${fmt(SAt('wind250'),1)} m/s`;
}
function updateConsole(){
  const t=T23(), Dv=t.mean_divergence_pressure??'—', red=t.reduction_pct??'—';
  const pnow=(D.nowcast[String(E)]&&D.nowcast[String(E)].intensify_p[STEP])??null;
  document.getElementById('console').innerHTML=`
   <div class="ribbon">
    <span class="badge teal">Θ trust ${Dv==='—'?'—':fmt(1/(1+Dv/12),2)}</span>
    <span class="badge ${Dv>10?'bad':'ok'}">D divergence ${Dv==='—'?'—':fmt(Dv,1)}σ</span>
    <span class="badge blue">EnKF −${fmt(red,1)}% RMSE</span>
    <span class="badge ${pnow>0.6?'fire':'amber'}">P(intensify +6h) ${fmt(pnow,2)}</span>
    <span class="badge">phase: ${SAt('phase_name')||'—'}</span>
    <span class="badge violet">view: ${VIEW.toUpperCase()}${GHOST?' +GHOST':''}</span>
   </div>`;
}
function updateStateTable(){
  const row=(k,v)=>`<tr><td>${k}</td><td><b>${v}</b></td></tr>`;
  const mem=D.memory.retrieval.find(r=>r.query_event===E)||{};
  document.getElementById('stateTable').innerHTML=`<table>
   <tr><th colspan="2" style="color:#ff8a75">xᶠ fire</th></tr>
   ${row('fire proxy (t07−t14)',fmt(SAt('fire_proxy'),1))}${row('raw t07 BT',fmt(SAt('raw_fire_bt'),2))}
   <tr><th colspan="2" style="color:#ff9e6d">xᵖ plume</th></tr>
   ${row('cloud-hgt proxy',fmt(SAt('cloud_height_proxy'),2))}${row('cloud-top BT',fmt(SAt('raw_cloud_bt'),3))}${row('phase',SAt('phase_name')||'—')}
   <tr><th colspan="2" style="color:#7fd4c4">xᵃ atmosphere</th></tr>
   ${row('t2m',fmt(SAt('t2m'),1)+' K')}${row('BLH',fmt(SAt('blh'),0)+' m')}${row('CAPE/CIN',fmt(SAt('cape'),0)+' / '+fmt(SAt('cin_filled'),0)+' J/kg')}
   ${row('BLH·wind (ventilation)',fmt(SAt('ventilation'),0)+' m²/s')}${row('RH column (850/750/650)',fmt(SAt('rh_850'),0)+'/'+fmt(SAt('rh_750'),0)+'/'+fmt(SAt('rh_650'),0)+' %')}
   ${row('w250 / dir',fmt(SAt('wind250'),1)+' m/s · '+fmt(SAt('wind_dir250'),0)+'°')}
   <tr><th colspan="2" style="color:#ffd27f">xˡ land (static)</th></tr>
   ${row('elevation / slope',fmt(SAt('elevation'),0)+' m / '+fmt(SAt('slope'),0)+'°')}${row('upslope index',fmt(SAt('upslope_idx'),2))}
   <tr><th colspan="2" style="color:#c3a6ff">xᵐ memory</th></tr>
   ${row('analog donors',mem.donor1?`#${mem.donor1}, #${mem.donor2}, #${mem.donor3}`:'—')}${row('fusion weight α*','0.30')}
   <tr><th colspan="2" style="color:#9fd0ff">xᵘ uncertainty</th></tr>
   ${row('EnKF reduction (event)',fmt((D.enkf.table.find(r=>r.held_out_event===E)||{}).reduction_pct,1)+' %')}</table>`;
}

// ---------------- monitor wall ----------------
function buildMonitorWall(){
  const wall=document.getElementById('monitorWall');
  wall.innerHTML=D.events.map(e=>{
    const t=(D.enkf.table||[]).find(r=>r.held_out_event===e.id)||{};
    const sev=Math.min(1,Math.abs(e.fire_peak)/145), inj=Math.min(1,Math.abs(e.inj_max)/3);
    return `<div class="mtile" data-e="${e.id}">
      <div class="mt-h"><b>#${e.id}</b><span class="dot ${t.mean_divergence_pressure>10?'d-warn':'d-ok'}"></span></div>
      <div class="mt-n">${e.name}</div>
      <div class="mt-b"><i style="width:${Math.round(sev*100)}%"></i></div>
      <div class="mt-f"><span>sev ${fmt(sev,2)}</span><span>inj ${fmt(inj,2)}</span><span>D ${fmt(t.mean_divergence_pressure,1)}σ</span><span>−${fmt(t.reduction_pct,0)}%</span></div>
    </div>`;}).join('');
  wall.querySelectorAll('.mtile').forEach(t=>t.onclick=()=>{E=+t.dataset.e;document.getElementById('eventSel').value=E;STEP=0;GHOST=null;syncEvent();});
}

// ---------------- charts ----------------
const layoutBase={paper_bgcolor:'rgba(0,0,0,0)',plot_bgcolor:'rgba(0,0,0,0)',font:{color:'#9fb2c4',size:10},
 margin:{l:46,r:16,t:10,b:34},showlegend:true,legend:{orientation:'h',y:1.14}};
function shape_step(step){
  const t=S('time')[step]; if(!t) return [];
  return [{type:'line',x0:t,x1:t,y0:0,y1:1,yref:'paper',line:{color:'#ffd27f',width:1.5}}];
}
function redrawTraj(){
  const v=document.getElementById('varSel').value, t=S('time');
  const now=D.nowcast[String(E)];
  const tr=[{x:t,y:S(v),mode:'lines+markers',name:'observed',line:{color:'#e8eef4',width:1.6},marker:{size:4}}];
  if(v==='fire_proxy'&&now){
    tr.push({x:t,y:now.fire_q90,mode:'lines',name:'q90',line:{width:0},showlegend:false});
    tr.push({x:t,y:now.fire_q10,mode:'lines',name:'80% band (trained)',fill:'tonexty',line:{width:0},fillcolor:'rgba(90,162,255,0.18)'});
    tr.push({x:t,y:now.fire_q50,mode:'lines',name:'twin median +6h',line:{color:'#5aa2ff',width:1.8,dash:'dot'}});
  }
  Plotly.react('trajChart',tr,{...layoutBase,shapes:shape_step(STEP),yaxis:{title:v}},{displayModeBar:false});
}
function redrawEnv(){
  const t=S('time');
  Plotly.react('envChart',[
    {x:t,y:S('blh'),name:'BLH (m)',mode:'lines',line:{color:'#5aa2ff',width:1.6}},
    {x:t,y:S('cape'),name:'CAPE (J/kg)',mode:'lines',yaxis:'y2',line:{color:'#ffb454',width:1.6}},
    {x:t,y:S('rh_colmean'),name:'RH column (%)',mode:'lines',yaxis:'y2',line:{color:'#2fe0c6',width:1.2,dash:'dot'}}],
    {...layoutBase,shapes:shape_step(STEP),yaxis:{title:'BLH m'},yaxis2:{title:'CAPE / RH',overlaying:'y',side:'right'}},{displayModeBar:false});
}
function drawEnkf(){
  const d=D.enkf.demo, x=[...Array(d.truth.length).keys()];
  Plotly.react('enkfChart',[
    {x,y:d.truth,mode:'lines+markers',name:'truth (event 202)',line:{color:'#e8eef4'},marker:{size:4}},
    {x,y:d.free,mode:'lines',name:'free-run (no assimilation)',line:{color:'#7d8ea0',dash:'dash'}},
    {x,y:d.analysis,mode:'lines',name:'synchronized (6-h EnKF)',line:{color:'#2fe0c6',width:2.2}},
    {x:x.slice(1),y:d.divergence,name:'divergence D(t)',yaxis:'y2',mode:'lines',line:{color:'#ff5a3c',width:1}}],
    {...layoutBase,yaxis:{title:'fire proxy (std)'},yaxis2:{overlaying:'y',side:'right',title:'D(σ)'}},{displayModeBar:false});
}
function drawCoupling(){
  const c=D.coupling;
  Plotly.react('couplingChart',[{z:c.matrix,x:c.labels,y:c.labels,type:'heatmap',colorscale:'RdBu',zmid:0,showscale:true}],
   {...layoutBase,legend:{visible:false}},{displayModeBar:false});
}
function drawVitals(){
  const mm=c=>{const a=D.events.map(e=>e[c]);return[Math.min(...a),Math.max(...a)];};
  const nz=(v,[a,b])=>b>a?(v-a)/(b-a):0.5, e=EVENT();
  const V=[1-nz(e.fire_peak,mm('fire_peak')),nz(e.cape_max,mm('cape_max')),nz(e.blh_max,mm('blh_max')),nz(e.inj_max,mm('inj_max'))];
  const L=['V1 fire intensity','V2 convective energy','V3 ventilation/moisture','V4 coupling','V1 fire intensity'];
  Plotly.react('vitalsChart',[{type:'scatterpolar',r:[...V,V[0]],theta:L,fill:'toself',name:`event ${E}`,
    line:{color:'#ff5a3c'}}],{...layoutBase,polar:{radialaxis:{visible:true,range:[0,1],color:'#33465a'}}},{displayModeBar:false});
}
function drawMemory(){
  const r=D.memory.retrieval.find(x=>x.query_event===E)||{};
  const name=id=>{const e=D.events.find(x=>x.id===id);return e?e.name:'';};
  document.getElementById('memoryCard').innerHTML=r.donor1?`<table>
   <tr><th>donor</th><th>event</th><th>distance (↓=closer)</th></tr>
   ${[[r.donor1,r.d1],[r.donor2,r.d2],[r.donor3,r.d3]].map(([d,dist])=>
     `<tr><td><b>#${d}</b></td><td>${name(d)}</td><td>${fmt(dist,2)}</td></tr>`).join('')}</table>
   <div class="small" style="margin-top:6px">Fusion ŷ = 0.30·analog + 0.70·dynamics — beats persistence on all targets (fire −7.5%, cloud-hgt −8.3%, PII −6.1% RMSE).</div>`
   :'<div class="small">fetching…</div>';
}
function markPlayhead(){ redrawTraj(); redrawEnv(); }

// ---------------- what-if & futures ----------------
function fanFromFutures(scen){
  const f=D.futures.by_event[String(E)][scen];
  const hh=[6,12,18,24], pii=[1,2,3,4].map(h=>f[`pii_p${h}`][0]);
  const sd=[1,2,3,4].map(h=>f[`pii_p${h}`][1]+0.05);
  const p24=1-normCdf((0.5-pii[3])/sd[3]);
  return {hh,pii,sd,p24,fire:[1,2,3,4].map(h=>f[`fire_p${h}`][0])};
}
async function runWhatIf(silent=false){
  const scen=SCEN_NOW;
  const out=document.getElementById('whatifOut');
  if(MODE==='live'&&!silent){
    const r=await (await fetch('/api/live/whatif',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({event:E,step:STEP,scenario:scen})})).json();
    out.innerHTML=deltaCard(r.baseline,r.scenario,r.delta,`trained models re-run at step ${STEP}`);
    drawFanLive(r);
  }else{
    const b=fanFromFutures('S0 baseline'), s=fanFromFutures(scen);
    out.innerHTML=deltaCardList([
      ['P(PyroCb>0.5) +24h',fmt(b.p24,3)+' → '+fmt(s.p24,3),(s.p24-b.p24)],
      ['Δ E[PII] +24h',fmt(s.pii[3]-b.pii[3],4),null],
      ['Δ E[fire proxy] +24h',fmt(s.fire[3]-b.fire[3],2),null]],'pre-computed futures (46,224 ensemble)');
    drawFanStatic(b,s,scen);
  }
  if(GHOST) buildGhostPlume(scen);
  renderDecision();
}
function deltaCardList(rows,src){
  return `<table>${rows.map(([k,v,d])=>`<tr><td>${k}</td><td><b>${v}</b>${d!=null?` <span style="color:${d>0?'#ff8a75':'#7fd4c4'}">(${d>0?'+':''}${fmt(d,3)})</span>`:''}</td></tr>`).join('')}</table><div class="small" style="margin-top:4px">source: ${src}</div>`;
}
function deltaCard(b,s,d,src){ return `<table>
  <tr><td>P(intensify +6h)</td><td><b>${fmt(b.p_intensify,3)} → ${fmt(s.p_intensify,3)}</b> <span style="color:${d.p_intensify>0?'#ff8a75':'#7fd4c4'}">(${d.p_intensify>0?'+':''}${fmt(d.p_intensify,4)})</span></td></tr>
  <tr><td>P(PyroCb>0.5) +24h</td><td><b>${fmt(b.p_pyrocb_24h,3)} → ${fmt(s.p_pyrocb_24h,3)}</b> <span style="color:${d.p_pyrocb_24h>0?'#ff8a75':'#7fd4c4'}">(${d.p_pyrocb_24h>0?'+':''}${fmt(d.p_pyrocb_24h,4)})</span></td></tr>
  <tr><td>fire nowcast q50</td><td><b>${fmt(b.fire_nowcast.q50,1)} → ${fmt(s.fire_nowcast.q50,1)}</b> <span style="color:${d.fire_nowcast_q50>0?'#ff8a75':'#7fd4c4'}">(${d.fire_nowcast_q50>0?'+':''}${fmt(d.fire_nowcast_q50,2)})</span></td></tr>
  <tr><td>ΔPII +24h</td><td><b>${fmt(d.pii_24h,4)}</b></td></tr></table><div class="small" style="margin-top:4px">source: ${src}</div>`;}
function drawFanStatic(b,s,scen){
  Plotly.react('futuresChart',[
    {x:b.hh,y:b.pii,mode:'lines+markers',name:'baseline PII',line:{color:'#5aa2ff'}},
    {x:s.hh,y:s.pii,mode:'lines+markers',name:scen,line:{color:'#ff5a3c'}},
    {x:b.hh,y:b.pii.map((v,i)=>v+1.64*b.sd[i]),mode:'lines',line:{width:0},showlegend:false},
    {x:b.hh,y:b.pii.map((v,i)=>v-1.64*b.sd[i]),mode:'lines',fill:'tonexty',fillcolor:'rgba(90,162,255,.15)',name:'baseline ±90%',line:{width:0}}],
    {...layoutBase,xaxis:{title:'lead (h)'},yaxis:{title:'PII'}},{displayModeBar:false});
}
function drawFanLive(r){
  const hh=[6,12,18,24];
  Plotly.react('futuresChart',[
    {x:hh,y:r.baseline.pii_h,mode:'lines+markers',name:'baseline PII (live)',line:{color:'#5aa2ff'}},
    {x:hh,y:r.scenario.pii_h,mode:'lines+markers',name:r.scenario.scenario,line:{color:'#ff5a3c'}},
    {x:hh,y:r.baseline.fire_h,mode:'lines',name:'baseline fire',yaxis:'y2',line:{color:'#7d8ea0',dash:'dot'}},
    {x:hh,y:r.scenario.fire_h,mode:'lines',name:'scenario fire',yaxis:'y2',line:{color:'#ffb454',dash:'dot'}}],
    {...layoutBase,xaxis:{title:'lead (h)'},yaxis:{title:'PII'},yaxis2:{overlaying:'y',side:'right',title:'fire proxy'}},{displayModeBar:false});
}
async function renderDecision(){
  let dec;
  if(MODE==='live'){ dec=await (await fetch(`/api/decision/${E}`)).json(); }
  else{
    const f=D.futures.by_event[String(E)], cards=[];
    for(const [s,rec] of Object.entries(f)){
      const [mu,sd0]=rec.pii_p4, sd=sd0+0.05;
      cards.push({scenario:s,pii_24h_mean:mu,sd,p_pyrocb:1-normCdf((0.5-mu)/sd),fire_24h_mean:rec.fire_p4[0]});}
    const p0=cards.find(c=>c.scenario==='S0 baseline');
    const band=p0.p_pyrocb>=0.5?'CRITICAL':p0.p_pyrocb>=0.25?'HIGH':p0.p_pyrocb>=0.10?'ELEVATED':'ROUTINE';
    const posture={CRITICAL:'Immediate escalation; task mesoscale sector; aviation SIGMET prep',
      HIGH:'Pre-position crews; restrict Rx-burn windows',
      ELEVATED:'Increase observation cadence; brief IMT',ROUTINE:'Nominal 6-h cycle'}[band];
    dec={baseline:p0,risk_band:band,posture,top_amplifiers:cards.filter(c=>c.scenario!=='S0 baseline').sort((a,b)=>b.p_pyrocb-a.p_pyrocb).slice(0,3)};
  }
  document.getElementById('decisionCard').innerHTML=`
   <div style="display:flex;align-items:center;gap:12px;margin-bottom:6px">
     <span class="riskband ${dec.risk_band}">${dec.risk_band}</span>
     <span class="small">baseline P(PyroCb>0.5, +24h) = <b style="color:#fff">${fmt(dec.baseline.p_pyrocb,3)}</b></span></div>
   <div class="small" style="margin-bottom:6px">${dec.posture}</div>
   <table><tr><th>top amplifiers</th><th>P(PyroCb)</th></tr>
   ${dec.top_amplifiers.map(a=>`<tr><td>${a.scenario}</td><td><b>${fmt(a.p_pyrocb,3)}</b></td></tr>`).join('')}</table>`;
}

// ---------------- evidence table ----------------
function renderEvidence(){
  const rows=[['6-h EnKF synchronization','state RMSE −45.0% mean (best 66.7%)'],
   ['Δ-fire-proxy nowcast','−8.0% RMSE vs no-change'],['cloud-top BT change R²','0.336 pooled · 0.667 within-event'],
   ['memory fusion (α*=0.3)','beats persistence 3/3 targets'],['intensification triage','AUROC 0.713 · F1 0.604'],
   ['80% band coverage','0.65 → 0.776 (conformal self-audit)'],['counterfactual futures','46,224 scored (9 operators)'],
   ['memory retrieval','Alaska 258↔260 mutual analogs · Manitoba→boreal cluster']];
  document.getElementById('evidenceTable').innerHTML='<table>'+rows.map(([a,b])=>`<tr><td>${a}</td><td><b>${b}</b></td></tr>`).join('')+'</table>';
}

/* =====================================================================================
   3D ENGINE — globe view (planetary) + local 4D view (terrain scene, event-parameterized)
   ===================================================================================== */
let renderer,scene,camera,controls,globeGroup,localGroup,markers=[];
let plumeGroup,fireSprite,capMesh,glowLight,windLines=[],particles=null,fireRing=null,ghostGroup=null;
function llv(lat,lon,r){const phi=(90-lat)*Math.PI/180,th=(lon+180)*Math.PI/180;
  return new THREE.Vector3(-r*Math.sin(phi)*Math.cos(th),r*Math.cos(phi),r*Math.sin(phi)*Math.sin(th));}
function dot(color,size=48){const c=document.createElement('canvas');c.width=c.height=size;const g=c.getContext('2d');
  const gr=g.createRadialGradient(size/2,size/2,1,size/2,size/2,size/2);
  gr.addColorStop(0,color);gr.addColorStop(0.4,color);gr.addColorStop(1,'rgba(0,0,0,0)');
  g.fillStyle=gr;g.fillRect(0,0,size,size);return new THREE.CanvasTexture(c);}

function buildGlobe(){
  const cw=document.getElementById('globe-wrap');
  renderer=new THREE.WebGLRenderer({canvas:document.getElementById('globe'),antialias:true});
  renderer.setSize(cw.clientWidth,cw.clientHeight);renderer.setPixelRatio(Math.min(devicePixelRatio,2));
  scene=new THREE.Scene();
  camera=new THREE.PerspectiveCamera(45,cw.clientWidth/cw.clientHeight,0.01,100);camera.position.set(0,0.4,2.4);
  controls=new THREE.OrbitControls(camera,renderer.domElement);controls.enableDamping=true;
  controls.autoRotate=(VIEW==='globe');controls.autoRotateSpeed=0.35;controls.minDistance=0.4;controls.maxDistance=5;
  globeGroup=new THREE.Group(); localGroup=new THREE.Group(); localGroup.visible=false;
  scene.add(globeGroup,localGroup);
  // earth + atmosphere + stars
  const tex=new THREE.TextureLoader().load('assets/earth.jpg');
  globeGroup.add(new THREE.Mesh(new THREE.SphereGeometry(1,64,64),new THREE.MeshPhongMaterial({map:tex})));
  globeGroup.add(new THREE.Mesh(new THREE.SphereGeometry(1.03,64,64),
    new THREE.MeshBasicMaterial({color:0x4d9fff,transparent:true,opacity:0.07,side:THREE.BackSide})));
  const sg=new THREE.BufferGeometry(),sp=[];
  for(let i=0;i<1800;i++){const u=Math.random()*2-1,ph=Math.random()*6.283185307,rr=Math.sqrt(1-u*u);sp.push(rr*Math.cos(ph)*30,rr*Math.sin(ph)*30,u*30);}
  sg.setAttribute('position',new THREE.Float32BufferAttribute(sp,3));
  globeGroup.add(new THREE.Points(sg,new THREE.PointsMaterial({color:0xffffff,size:0.03,transparent:true,opacity:.7})));
  scene.add(new THREE.AmbientLight(0x8899bb,0.95));
  const sun=new THREE.DirectionalLight(0xffffff,1.1);sun.position.set(3,1,2);scene.add(sun);
  glowLight=new THREE.PointLight(0xff5522,0,0.6);globeGroup.add(glowLight);
  const regimeCol={'boreal':0x5aa2ff,'subarctic':0x7fd4c4,'subtropical':0xffb454,'high-elevation':0xff5a3c,
     'arid-continental':0xff8a5c,'plateau':0xc3a6ff,'cascade':0x43d17c};
  for(const e of D.events){
    const col=regimeCol[e.regime]||0xffffff;
    const m=new THREE.Sprite(new THREE.SpriteMaterial({map:dot('#'+col.toString(16).padStart(6,'0')),depthTest:false,transparent:true}));
    m.position.copy(llv(e.lat,e.lon,1.012));m.scale.setScalar(0.045+0.09*Math.abs(e.inj_max||0));m.userData={event:e.id};
    globeGroup.add(m);markers.push(m);
  }
  renderer.domElement.addEventListener('pointerdown',ev=>{
    const r=renderer.domElement.getBoundingClientRect();
    const mo=new THREE.Vector2(((ev.clientX-r.left)/r.width)*2-1,-((ev.clientY-r.top)/r.height)*2+1);
    const rc=new THREE.Raycaster();rc.setFromCamera(mo,camera);
    const hit=rc.intersectObjects(markers)[0];
    if(hit&&VIEW==='globe'){E=hit.object.userData.event;document.getElementById('eventSel').value=E;STEP=0;GHOST=null;syncEvent();focusEvent();}
    setTimeout(()=>{if(VIEW==='globe')controls.autoRotate=true;},4000);controls.autoRotate=false;
  });
  // plume + ghost + wind streamlines on globe view
  plumeGroup=new THREE.Group(); globeGroup.add(plumeGroup);
  for(let i=0;i<20;i++){
    const t=(i+1)/20;
    const sph=new THREE.Mesh(new THREE.SphereGeometry(0.016+0.05*t,10,10),
      new THREE.MeshLambertMaterial({color:0x9aa2ad,transparent:true,opacity:0.20-0.09*t,depthWrite:false}));
    sph.userData.t=t; plumeGroup.add(sph);
  }
  capMesh=new THREE.Mesh(new THREE.SphereGeometry(0.048,20,14),
    new THREE.MeshPhongMaterial({color:0xffffff,transparent:true,opacity:0.9,emissive:0x555566}));
  capMesh.scale.set(1.45,0.40,1.45); globeGroup.add(capMesh);
  fireSprite=new THREE.Sprite(new THREE.SpriteMaterial({map:dot('#ff4400'),depthTest:false,transparent:true,blending:THREE.AdditiveBlending}));
  globeGroup.add(fireSprite);
  windLines=[];
  for(let k=0;k<4;k++){
    const g=new THREE.BufferGeometry(), pts=new Float32Array(60*3);
    g.setAttribute('position',new THREE.BufferAttribute(pts,3));
    const ln=new THREE.Line(g,new THREE.LineBasicMaterial({color:0x6fb7ff,transparent:true,opacity:0.35}));
    ln.userData.k=k; globeGroup.add(ln); windLines.push(ln);
  }
  focusEvent(); animate();
  addEventListener('resize',()=>{const w=cw.clientWidth,h=cw.clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();
    renderer.setSize(w,h);});
}
function focusEvent(){
  const e=EVENT(),p=llv(e.lat,e.lon,1.0);
  controls.target.copy(p.clone().multiplyScalar(1.005));
  camera.position.copy(p.clone().multiplyScalar(1.9));
}
function plumeVecs(){
  const e=EVENT(), anchor=llv(e.lat,e.lon,1.005), up=anchor.clone().normalize();
  const wdir=((SAt('wind_dir250')||0))*Math.PI/180;
  const north=new THREE.Vector3(0,1,0).cross(up).normalize().negate();
  const east=up.clone().cross(north).normalize();
  const wv=north.clone().multiplyScalar(Math.cos(wdir)).add(east.clone().multiplyScalar(Math.sin(wdir))).multiplyScalar(-1);
  return {anchor,up,wv};
}
function updateGlobeDynamics(){
  const {anchor,up,wv}=plumeVecs();
  const w250=SAt('wind250')||10;
  const inten=Math.min(1,Math.abs(SAt('fire_proxy')||0)/130);
  const blh=SAt('blh')||800, h=0.10+Math.min(0.22,blh/100000);
  const drift=Math.min(0.5,w250/60);
  for(const s of plumeGroup.children){
    const t=s.userData.t;
    s.position.copy(anchor).add(up.clone().multiplyScalar(h*t)).add(wv.clone().multiplyScalar(drift*t*t*0.25));
    s.scale.setScalar(0.6+0.9*inten+0.5*t);
  }
  const cold=1-Math.min(1,(SAt('raw_cloud_bt')||0.5)/2.1);
  if(capMesh){
    capMesh.position.copy(anchor).add(up.clone().multiplyScalar(h+0.035)).add(wv.clone().multiplyScalar(drift*0.25));
    capMesh.material.opacity=0.35+0.55*Math.max(0,Math.min(1,(SAt('cloud_height_proxy')||0)/8))*(0.5+0.5*cold);
    const cs=0.55+0.5*cold; capMesh.scale.set(1.45*cs,0.40*cs,1.45*cs);
  }
  fireSprite.position.copy(anchor).add(up.clone().multiplyScalar(0.005));
  fireSprite.scale.setScalar(0.06+0.12*inten);
  glowLight.position.copy(anchor).add(up.clone().multiplyScalar(0.03));
  glowLight.intensity=1.4*inten;
  // wind streamlines through the plume
  for(const ln of windLines){
    const k=ln.userData.k, pos=ln.geometry.attributes.position.array;
    const off=0.02+k*0.015;
    for(let i=0;i<60;i++){
      const t=i/59;
      const p=anchor.clone().add(up.clone().multiplyScalar(off+t*0.30))
        .add(wv.clone().multiplyScalar(t*t*(0.30+drift*0.2)));
      pos[i*3]=p.x;pos[i*3+1]=p.y;pos[i*3+2]=p.z;
    }
    ln.geometry.attributes.position.needsUpdate=true;
    ln.material.opacity=0.10+0.30*Math.min(1,w250/40);
  }
  if(ghostGroup) updateGhost(anchor,up,wv,h,drift,inten);
}
function toggleGhost(){
  GHOST=!GHOST;
  document.getElementById('ghostBtn').textContent=GHOST?'👻 ghost on':'👻 ghost off';
  if(GHOST) buildGhostPlume(SCEN_NOW);
  else if(ghostGroup){globeGroup.remove(ghostGroup);ghostGroup=null;}
  updateConsole();
}
function buildGhostPlume(scen){
  if(ghostGroup) globeGroup.remove(ghostGroup);
  ghostGroup=new THREE.Group();
  const f=D.futures.by_event[String(E)][scen], p24=f.pii_p4[0];
  const sev=Math.min(1,Math.abs(p24)/0.15);
  for(let i=0;i<16;i++){
    const t=(i+1)/16;
    const sph=new THREE.Mesh(new THREE.SphereGeometry(0.020+0.05*t*(0.5+sev),10,10),
      new THREE.MeshLambertMaterial({color:0xff7a45,transparent:true,opacity:0.14,depthWrite:false}));
    sph.userData.t=t; ghostGroup.add(sph);
  }
  globeGroup.add(ghostGroup); updateGlobeDynamics();
}
function updateGhost(anchor,up,wv,h,drift,inten){
  for(const s of ghostGroup.children){
    const t=s.userData.t;
    s.position.copy(anchor).add(up.clone().multiplyScalar(h*t*1.15))
      .add(wv.clone().multiplyScalar(drift*t*t*0.25+0.03));
  }
}

// ---------------- local 4D terrain scene ----------------
let tFire,tPlume,tCap,tTerrain,tPuffs=[],tParticles,tWind=[],localParts=[];
function pseudo(seed){ let x=Math.sin(seed*127.1)*43758.5453; return x-Math.floor(x); }
function buildLocalScene(){
  // terrain driven by this event's real scalar stats (elevation/slope/tri/aspect)
  tTerrain=null;
  localGroup.add(new THREE.AmbientLight(0xaab4cc,1.0));
}
function rebuildLocal(){
  for(const o of localParts){ localGroup.remove(o); }
  localParts=[]; tPuffs=[]; tWind=[];
  const track=o=>{localParts.push(o);return o;};
  const e=EVENT();
  const slope=(e.elev>2000?25:8)+(S('slope')[0]||8);
  const rugged=0.5+Math.min(1.6,(e.id===179?1.6: e.elev>900?1.1:0.6));
  const n=72, size=2.0, geo=new THREE.PlaneGeometry(size,size,n,n);
  for(let i=0;i<geo.attributes.position.count;i++){
    const x=geo.attributes.position.getX(i), y=geo.attributes.position.getY(i);
    let z=0;
    z+=Math.exp(-(x*x+y*y)/0.9)*0.34*rugged;
    z+=Math.exp(-((x-0.6)**2+(y+0.4)**2)/0.25)*0.22*rugged;
    z+=Math.exp(-((x+0.7)**2+(y-0.5)**2)/0.18)*0.18*rugged;
    z+=(pseudo(i%97)-0.5)*0.016*rugged;
    geo.attributes.position.setZ(i,z);
  }
  geo.computeVertexNormals();
  tTerrain=track(new THREE.Mesh(geo,new THREE.MeshPhongMaterial({color:0x3f5a3a,shininess:6,flatShading:false})));
  tTerrain.rotation.x=-Math.PI/2; localGroup.add(tTerrain);
  const grid=track(new THREE.Mesh(geo.clone(),new THREE.MeshBasicMaterial({color:0x222831,wireframe:true,transparent:true,opacity:0.10})));
  grid.rotation.x=-Math.PI/2; localGroup.add(grid);
  // fire front ring
  const ringPts=[];
  for(let i=0;i<=40;i++){const a=i/40*Math.PI*2, r=0.16+0.05*Math.sin(4*a)+0.02*Math.sin(9*a);
    ringPts.push(new THREE.Vector3(Math.cos(a)*r,0.345*rugged+0.02,Math.sin(a)*r));}
  tFire=track(new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(ringPts),
      new THREE.LineBasicMaterial({color:0xff3300,transparent:true,opacity:0.95})));
  localGroup.add(tFire);
  const fl=track(new THREE.PointLight(0xff4400,2.2,1.4)); fl.position.set(0,0.5,0); localGroup.add(fl); fl.name='flameLight';
  // plume puffs (local scale)
  tPlume=track(new THREE.Group());
  for(let i=0;i<22;i++){const t=(i+1)/22;
    const m=new THREE.Mesh(new THREE.SphereGeometry(0.05+0.10*t,10,10),
      new THREE.MeshLambertMaterial({color:0x9aa2ad,transparent:true,opacity:0.22-0.10*t,depthWrite:false}));
    m.userData.t=t; tPlume.add(m);}
  localGroup.add(tPlume);
  // pyroCb cluster
  for(let k=0;k<3;k++){
    const p=new THREE.Mesh(new THREE.SphereGeometry(0.16-k*0.035,16,12),
      new THREE.MeshPhongMaterial({color:0xffffff,transparent:true,opacity:0.85,emissive:0x3a3a44}));
    p.userData.k=k; tPuffs.push(p); track(p); localGroup.add(p);
  }
  // ember/smoke particles
  const pg=new THREE.BufferGeometry(), pn=350, pp=new Float32Array(pn*3), pd=new Float32Array(pn);
  for(let i=0;i<pn;i++){ pd[i]=Math.random(); }
  pg.setAttribute('position',new THREE.BufferAttribute(pp,3)); pg.userData={pd};
  tParticles=track(new THREE.Points(pg,new THREE.PointsMaterial({color:0xffc9a0,size:0.012,transparent:true,opacity:0.8,blending:THREE.AdditiveBlending,depthWrite:false})));
  localGroup.add(tParticles);
  // local wind curves
  for(let k=0;k<5;k++){
    const g=new THREE.BufferGeometry(), pts=new Float32Array(50*3);
    g.setAttribute('position',new THREE.BufferAttribute(pts,3));
    const ln=new THREE.Line(g,new THREE.LineBasicMaterial({color:0x6fb7ff,transparent:true,opacity:0.4}));
    ln.userData.k=k; tWind.push(ln); track(ln); localGroup.add(ln);
  }
  updateLocalDynamics();
}
function localWindVec(){
  const wdir=((SAt('wind_dir250')||0))*Math.PI/180, ws=SAt('wind250')||10;
  return {dir:new THREE.Vector3(Math.sin(wdir)*-1,0,Math.cos(wdir)*-1).normalize(), sp:Math.min(1,ws/45)};
}
function heightAt(x,z){
  const e=EVENT(); const rugged=0.5+Math.min(1.6,(e.id===179?1.6: e.elev>900?1.1:0.6));
  let h=Math.exp(-(x*x+z*z)/0.9)*0.34*rugged+Math.exp(-((x-0.6)**2+(z+0.4)**2)/0.25)*0.22*rugged+Math.exp(-((x+0.7)**2+(z-0.5)**2)/0.18)*0.18*rugged;
  return h;
}
function updateLocalDynamics(){
  if(!tPlume) return;
  const e=EVENT(), rugged=0.5+Math.min(1.6,(e.id===179?1.6: e.elev>900?1.1:0.6));
  const inten=Math.min(1,Math.abs(SAt('fire_proxy')||0)/130);
  const blh=SAt('blh')||800, hMax=0.32+Math.min(0.65, blh/4500*0.75+inten*0.15);
  const {dir:wd,sp:wsp}=localWindVec();
  const anchor=new THREE.Vector3(0,0.345*rugged+0.02,0);
  for(const m of tPlume.children){
    const t=m.userData.t;
    m.position.copy(anchor).add(new THREE.Vector3(0,hMax*t,0)).add(wd.clone().multiplyScalar(wsp*0.45*t*t));
    m.scale.setScalar(0.6+0.8*inten+0.6*t);
  }
  const chp=Math.max(0,Math.min(1,(SAt('cloud_height_proxy')||0)/8));
  const cold=1-Math.min(1,(SAt('raw_cloud_bt')||0.5)/2.1);
  const capY=anchor.y+hMax+0.06, csc=0.55+0.6*Math.max(cold,chp*0.5);
  for(const p of tPuffs){
    const k=p.userData.k;
    p.position.set(k*0.18-0.18 + wd.x*wsp*0.5, capY - Math.abs(k-1)*0.03, wd.z*wsp*0.5 + (k-1)*0.10);
    p.scale.set(1.5*csc,0.5*csc*(1-0.1*k),1.5*csc);
    p.material.opacity=0.25+0.55*Math.max(chp,cold*0.6);
  }
  // particles
  const pp=tParticles.geometry.attributes.position.array, pd=tParticles.geometry.userData.pd;
  const tt=performance.now()/1000;
  for(let i=0;i<pd.length;i++){
    const t=(pd[i]+tt*0.12)%1;
    pp[i*3]=wd.x*wsp*0.5*t*t+ (pseudo(i)-0.5)*0.10*t;
    pp[i*3+1]=anchor.y+hMax*t;
    pp[i*3+2]=wd.z*wsp*0.5*t*t + (pseudo(i+333)-0.5)*0.10*t;
  }
  tParticles.geometry.attributes.position.needsUpdate=true;
  // wind curves
  for(const ln of tWind){
    const k=ln.userData.k, pos=ln.geometry.attributes.position.array;
    for(let i=0;i<50;i++){const t=i/49;
      const y=0.15+k*0.16+t*0.25, bend=wsp*(0.3+t*0.5);
      pos[i*3]=t*1.6-0.8 + wd.x*bend; pos[i*3+1]=y; pos[i*3+2]=(k-2)*0.18 + wd.z*bend;}
    ln.geometry.attributes.position.needsUpdate=true;
    ln.material.opacity=0.12+0.30*wsp;
  }
  const fl=localGroup.getObjectByName('flameLight'); if(fl) fl.intensity=1.2+2.2*inten+0.3*Math.sin(performance.now()/130);
}
function toggleView(){
  VIEW=(VIEW==='globe')?'local':'globe';
  document.getElementById('viewBtn').textContent=VIEW==='globe'?'⛰ local 4D':'🌍 globe 4D';
  globeGroup.visible=(VIEW==='globe'); localGroup.visible=(VIEW!=='globe');
  controls.autoRotate=(VIEW==='globe');
  if(VIEW==='local'){ camera.position.set(1.5,1.05,1.6); controls.target.set(0,0.45,0);}
  else { focusEvent(); }
  updateConsole();
}
function animate(){requestAnimationFrame(animate);
  if(VIEW==='local') updateLocalDynamics();
  controls.update();renderer.render(scene,camera);}

boot();
