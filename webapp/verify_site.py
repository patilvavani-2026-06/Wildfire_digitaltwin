"""Headless verification of the deployed PyroCast twin (v2)."""
import json
from playwright.sync_api import sync_playwright

URL = 'https://pyrocast-morpheus-twin.netlify.app/'
with sync_playwright() as pw:
    b = pw.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader'])
    pg = b.new_page(viewport={'width':1500,'height':2200})
    errors=[]
    pg.on('pageerror', lambda e: errors.append(f'PAGEERROR: {e}'))
    pg.on('console', lambda m: errors.append(f'CONSOLE-{m.type}: {m.text}') if m.type in ('error','warning') else None)
    pg.goto(URL, wait_until='networkidle', timeout=120000)
    pg.wait_for_timeout(6000)
    checks={}
    checks['data_pack']=pg.evaluate('()=> typeof window.PYROCAST_DATA!=="undefined"')
    checks['three']=pg.evaluate('()=> typeof THREE!=="undefined"')
    checks['plotly']=pg.evaluate('()=> typeof Plotly!=="undefined"')
    checks['eventSel_options']=pg.evaluate('()=> document.getElementById("eventSel").options.length')
    checks['modePill']=pg.evaluate('()=> document.getElementById("modePill").textContent')
    for cid in ['trajChart','enkfChart','couplingChart','vitalsChart','futuresChart','envChart']:
        checks[cid+'_svg']=pg.evaluate(f'()=> document.querySelectorAll("#{cid} svg").length')
    checks['stateTable_rows']=pg.evaluate('()=> document.querySelectorAll("#stateTable tr").length')
    checks['memory_rows']=pg.evaluate('()=> document.querySelectorAll("#memoryCard tr").length')
    checks['decision_band']=pg.evaluate('()=> (document.querySelector("#decisionCard .riskband")||{}).textContent||"none"')
    checks['monitor_tiles']=pg.evaluate('()=> document.querySelectorAll(".mtile").length')
    # local 4D view
    pg.evaluate('()=> document.getElementById("viewBtn").click()')
    pg.wait_for_timeout(1500)
    checks['view_local_label']=pg.evaluate('()=> document.getElementById("viewBtn").textContent')
    pg.locator('#globe-wrap').screenshot(path='/home/user/PyroCast/webapp/verify_local.png')
    pg.evaluate('()=> document.getElementById("viewBtn").click()')
    # live ops mode
    pg.evaluate('()=> document.getElementById("playBtn").click()')
    pg.wait_for_timeout(5200)
    checks['livelog_lines']=pg.evaluate('()=> document.querySelectorAll("#liveLog .ll").length')
    checks['playbtn_live']=pg.evaluate('()=> document.getElementById("playBtn").textContent')
    checks['step_after_live']=pg.evaluate('()=> document.getElementById("stepLbl").textContent')
    pg.evaluate('()=> document.getElementById("playBtn").click()')
    # ghost plume + what-if S7
    pg.evaluate('()=> document.getElementById("ghostBtn").click()')
    pg.evaluate('()=>{document.getElementById("scenSel").value="S7 compound extreme";document.getElementById("runWhatIf").click();}')
    pg.wait_for_timeout(900)
    checks['ghost_label']=pg.evaluate('()=> document.getElementById("ghostBtn").textContent')
    checks['whatif_s7_rows']=pg.evaluate('()=> document.querySelectorAll("#whatifOut tr").length')
    pg.screenshot(path='/home/user/PyroCast/webapp/verify_full.png', full_page=False)
    pg.evaluate('()=>{const s=document.getElementById("stepSlider");s.value=10;s.dispatchEvent(new Event("input"));}')
    pg.wait_for_timeout(1200)
    pg.locator('#globe-wrap').screenshot(path='/home/user/PyroCast/webapp/verify_globe.png')
    print(json.dumps(checks, indent=1))
    print('ERRORS:', json.dumps(errors[:12], indent=1) if errors else 'none')
    b.close()
print('VERIFICATION DONE')
