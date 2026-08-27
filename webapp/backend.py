"""PyroCast–MORPHEUS Digital Twin Web Backend (FastAPI).
Serves the 3D/4D twin frontend + live trained-model inference APIs.
Run:  uvicorn backend:app --host 0.0.0.0 --port 8000   (from webapp/)
"""
import json, os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import twin_engine as TE

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
STATIC = os.path.join(HERE, "static")

def load(name):
    return json.load(open(os.path.join(DATA, name + ".json")))

app = FastAPI(title="PyroCast–MORPHEUS Digital Twin API", version="1.0.0")

# ---------------- data endpoints ----------------
@app.get("/api/overview")
def overview():
    m = load("metrics")
    return {"cohort": m["cohort"], "enkf_mean_reduction_pct": m["enkf_sync"]["mean_RMSE_reduction_pct"],
            "n_futures": m["counterfactual_engine"]["n_futures"],
            "memory_finding": m["memory_engine"]["finding"],
            "mode": "LIVE-MODEL"}

@app.get("/api/events")
def events(): return load("events")

@app.get("/api/series/{eid}")
def series(eid: int):
    s = load("series").get(str(eid))
    if s is None: raise HTTPException(404, "event not found")
    return s

@app.get("/api/nowcast/{eid}")
def nowcast(eid: int):
    n = load("nowcast").get(str(eid))
    if n is None: raise HTTPException(404, "event not found")
    return n

@app.get("/api/enkf")
def enkf(): return load("enkf")

@app.get("/api/memory/{eid}")
def memory(eid: int):
    recs = load("memory")["retrieval"]
    r = [x for x in recs if x["query_event"] == eid]
    if not r: raise HTTPException(404, "event not found")
    return {"retrieval": r[0], "fusion": load("memory")["fusion"]}

@app.get("/api/coupling")
def coupling(): return load("coupling")

@app.get("/api/futures/{eid}")
def futures(eid: int):
    f = load("futures")
    ev = f["by_event"].get(str(eid))
    if ev is None: raise HTTPException(404, "event not found")
    return {"scenarios": f["scenarios"], "by_scenario": ev}

@app.get("/api/counterfactual")
def counterfactual(): return load("counterfactual")

# ---------------- live trained-model inference ----------------
ROWS = load("rows")

class NowcastReq(BaseModel):
    event: int
    step: int

class WhatIfReq(BaseModel):
    event: int
    step: int
    scenario: str

@app.post("/api/live/nowcast")
def live_nowcast(req: NowcastReq):
    try:
        row = ROWS[str(req.event)][req.step]
    except Exception:
        raise HTTPException(404, "event/step not found")
    return TE.predict_row(row, "S0 baseline")

@app.post("/api/live/whatif")
def live_whatif(req: WhatIfReq):
    try:
        row = ROWS[str(req.event)][req.step]
    except Exception:
        raise HTTPException(404, "event/step not found")
    valid = ["S0 baseline","S1 wind +20%","S2 heatwave +5K","S3 drying RH -30%","S4 rain-out",
             "S5 deep drought","S6 relocate: high-relief","S7 compound extreme","S8 pyro-feedback ON"]
    if req.scenario not in valid: raise HTTPException(400, "unknown scenario")
    base = TE.predict_row(row, "S0 baseline")
    scen = TE.predict_row(row, req.scenario)
    return {"baseline": base, "scenario": scen,
            "delta": {"fire_nowcast_q50": scen["fire_nowcast"]["q50"] - base["fire_nowcast"]["q50"],
                      "p_intensify": scen["p_intensify"] - base["p_intensify"],
                      "p_pyrocb_24h": scen["p_pyrocb_24h"] - base["p_pyrocb_24h"],
                      "pii_24h": scen["pii_h"][3] - base["pii_h"][3]}}

@app.get("/api/decision/{eid}")
def decision(eid: int):
    f = load("futures"); ev = f["by_event"].get(str(eid))
    if ev is None: raise HTTPException(404)
    import math
    cards = []
    for scen, rec in ev.items():
        mu, sd = rec["pii_p4"]
        p = 1 - 0.5*(1+math.erf((0.5-mu)/((sd+0.05)*math.sqrt(2))))
        cards.append({"scenario": scen, "pii_24h_mean": mu, "sd": sd, "p_pyrocb": p,
                      "fire_24h_mean": rec["fire_p4"][0]})
    p0 = [c for c in cards if c["scenario"] == "S0 baseline"][0]
    band = ("CRITICAL" if p0["p_pyrocb"] >= 0.5 else "HIGH" if p0["p_pyrocb"] >= 0.25
            else "ELEVATED" if p0["p_pyrocb"] >= 0.10 else "ROUTINE")
    posture = {"CRITICAL":"Immediate escalation; task mesoscale sector; aviation SIGMET prep",
               "HIGH":"Pre-position crews; restrict Rx-burn windows",
               "ELEVATED":"Increase observation cadence; brief IMT",
               "ROUTINE":"Nominal 6-h cycle"}[band]
    amp = sorted([c for c in cards if c["scenario"] != "S0 baseline"], key=lambda c: -c["p_pyrocb"])[:3]
    return {"event": eid, "baseline": p0, "risk_band": band, "posture": posture,
            "top_amplifiers": amp, "n_scenarios": len(cards)}

# ---------------- static frontend ----------------
@app.get("/")
def index(): return FileResponse(os.path.join(STATIC, "index.html"))
app.mount("/data", StaticFiles(directory=DATA), name="data")
app.mount("/", StaticFiles(directory=STATIC), name="static")
