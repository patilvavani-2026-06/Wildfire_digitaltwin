"""PyroCast digital-twin inference engine (shared: backend API + offline parity)."""
import numpy as np, joblib, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = json.load(open(os.path.join(HERE, "models", "spec.json")))
FEATS, FILL = SPEC["feature_list"], SPEC["median_fill"]
MODELS = {f.replace(".joblib", ""): joblib.load(os.path.join(HERE, "models", f))
          for f in os.listdir(os.path.join(HERE, "models")) if f.endswith(".joblib")}

def _recompute(r):
    r = dict(r)
    ws = max(r.get("wind_speed10") or 1e-3, 1e-3)
    r["ventilation"] = r["blh"] * ws
    r["gust_factor"] = r["fg10"] / ws
    r["speed_shear"] = r["wind250"] - ws
    r["buoy_forcing"] = r["cape"] - abs(r["cin_filled"])
    r["net_hflux"] = r["sshf"] + r["slhf"]
    r["rh_colmean"] = float(np.nanmean([r["rh_850"], r["rh_750"], r["rh_650"]]))
    r["rh_lapse"] = r["rh_850"] - r["rh_650"]
    r["dry_air_entrain"] = 100 - r["rh_650"]
    return r

def apply_scenario(row, scen):
    r = {k: (row.get(k) if row.get(k) is not None else FILL.get(k, 0.0)) for k in set(FEATS) | {"wind_speed10"}}
    S = scen
    if S == "S0 baseline": pass
    elif S == "S1 wind +20%":
        for k in ["u10","v10","fg10","wind250","wind_speed10"]: r[k] = r.get(k,0.0)*1.2
    elif S == "S2 heatwave +5K":
        r["t2m"] += 5
        for k in ["rh_850","rh_750","rh_650"]: r[k] *= 0.75
    elif S == "S3 drying RH -30%":
        for k in ["rh_850","rh_750","rh_650"]: r[k] *= 0.70
    elif S == "S4 rain-out":
        r.update(tp=0.005); r["cape"]*=0.3; r["blh"]*=0.6; r["sshf"]*=0.4; r["t2m"]-=3
    elif S == "S5 deep drought":
        r["dry_spell"] = r.get("dry_spell",0)+4
        for k in ["rh_850","rh_750","rh_650"]: r[k]*=0.85
        r["slhf"]*=0.6; r["sshf"]*=1.2
    elif S == "S6 relocate: high-relief":
        r.update(elevation=3040.0, slope=29.0, tpi=4.57, tri=1.0, cvh=0.889, cvl=0.094, upslope_idx=0.8)
    elif S == "S7 compound extreme":
        r["t2m"] += 8
        for k in ["rh_850","rh_750","rh_650"]: r[k] *= 0.5
        r["wind250"]*=1.5; r["fg10"]*=1.4; r["cape"]=max(r["cape"],1500.0)
        r["wind_speed10"]*=1.4; r["u10"]*=1.4; r["v10"]*=1.4
    elif S == "S8 pyro-feedback ON":
        if r["fire_proxy"] < -90: r["blh"]*=1.3; r["cape"]*=1.2
    return _recompute(r)

def _x(r):
    return np.array([[r.get(c, FILL[c]) if r.get(c) is not None else FILL[c] for c in FEATS]])

def predict_row(row, scenario="S0 baseline"):
    r = apply_scenario(row, scenario)
    xx = _x(r)
    out = {
      "scenario": scenario,
      "fire_nowcast": {"q10": float(MODELS["fire_p1_q10"].predict(xx)[0]),
                       "q50": float(MODELS["fire_p1_q50"].predict(xx)[0]),
                       "q90": float(MODELS["fire_p1_q90"].predict(xx)[0])},
      "cbt_change_p1": float(MODELS["cbt_chg_p1"].predict(xx)[0]),
      "p_intensify": float(MODELS["intensify_clf"].predict_proba(xx)[0,1]),
      "fire_h": [float(MODELS[f"yf_p{h}"].predict(xx)[0]) for h in [1,2,3,4]],
      "pii_h":  [float(MODELS[f"yp_p{h}"].predict(xx)[0]) for h in [1,2,3,4]],
    }
    import math
    # Gaussian risk: P(PII>0.5) at +24h using model-seed sd floor 0.05
    mu = out["pii_h"][3]; sd = 0.08
    out["p_pyrocb_24h"] = float(1 - 0.5*(1+math.erf((0.5-mu)/(sd*math.sqrt(2)))))
    return out
