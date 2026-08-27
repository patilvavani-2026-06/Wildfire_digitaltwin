# PyroCast–MORPHEUS Web Digital Twin — Runbook

## Architecture
```
webapp/
├── backend.py          # FastAPI: data APIs + LIVE trained-model inference (/api/*)
├── twin_engine.py      # shared inference engine: 13 joblib XGB kernels + 8 scenario operators
├── models/             # 13 trained models (fire q10/50/90, Δcbt, yf/yp h1..4, intensifier) + spec.json
├── data/               # 11 JSON packs + pack.js (offline twin dataset, 232 KB)
└── static/             # index.html · app.js (Three.js 4D globe + Plotly) · styles.css · assets/earth.jpg
```

## Run (full-stack, LIVE model backend)
```bash
cd PyroCast/webapp
uvicorn backend:app --host 0.0.0.0 --port 8000
# open http://localhost:8000
```
**LIVE mode** (header pill): every *dream* press re-runs the trained models through selected
do-operator at the current playhead; decision cards served from `/api/decision/{event}`.

## Offline mode (no server)
Open `webapp/static/index.html` directly — the app falls back to `data/pack.js`
(pre-computed futures, nowcasts, EnKF arrays). Everything except live re-inference works.

## What the dashboard shows
- **4D globe**: Earth + 10 PyroCb event markers (click to select) · fire glow ∝ |fire proxy| ·
  smoke column rising with BLH and bending with 250-hPa steering · PyroCb anvil cap ∝ cloud-height/coldness ·
  play/pause 4D timeline over each event's 6-h lifecycle (19–24 frames)
- **Trajectory ⊕ trained nowcast**: observed series + XGB median + quantile 80% band per step
- **EnKF heartbeat**: truth vs free-run vs analysis + divergence pressure D(t) (event 202 demo)
- **Twin console**: Θ trust, D divergence, P(intensify +6h) from the trained classifier
- **Twin state x(t)**: six blocks (fire/plume/atmosphere/land/memory/uncertainty) at playhead
- **Memory card**: top-3 analog donors + distances + α*=0.30 fusion note
- **Counterfactual dreaming**: 9 scenario operators (S0 baseline … S8 pyro-feedback) — baseline vs
  scenario Δ cards + futures fan (+6…+24 h)
- **Decision card**: risk band (CRITICAL/HIGH/ELEVATED/ROUTINE) + posture + top amplifiers
- **Evidence table**: every headline number from results/metrics.json

## API summary
`GET /api/overview · /api/events · /api/series/{id} · /api/nowcast/{id} · /api/enkf · /api/memory/{id}
· /api/coupling · /api/futures/{id} · /api/counterfactual · /api/decision/{id}`
`POST /api/live/nowcast {event,step}` · `POST /api/live/whatif {event,step,scenario}`

## Regenerate everything
`python3 code/p08_serve_models.py && python3 code/p09_export_web.py && python3 code/p10_nowcast_pack.py`
(from `PyroCast/`; re-trains serving kernels + re-exports data packs from the master twin-state table.)
