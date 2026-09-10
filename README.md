# Wildfire_digitaltwin
# PyroCast–MORPHEUS — Living Wildfire Digital Twin (research artifact)

A complete framework invention + **fully trained reference implementation** on the uploaded
10-event GOES/ERA5 PyroCb cohort (227 six-hourly twin-state vectors, 2021–2022).


## Reproduce (≈3.5 min CPU)
```bash
python3 code/p01_profile.py            # inventory
python3 code/p02_master.py             # twin-state table data/master.csv (227×82)
python3 code/p03_figs_eda.py           # 21 cohort-science figures
python3 code/p04a_train_core.py        # LOEO nowcasts, ablations, quantiles, classifier
python3 code/p04a2_delta_conformal.py  # delta-skill, conformal audit, within-event
python3 code/p04b_twin_engines.py      # memory engine, coupling kernel, EnKF sync
python3 code/p04c_counterfactual.py    # 46,224 counterfactual futures
python3 code/p04d_finalize_metrics.py  # results/metrics.json consolidation
python3 code/p05a_diagrams.py          # architecture diagrams D40–D50
python3 code/p05b_viz_mocks.py         # 4D globe GIF + viz mockups D51–D55
python3 code/p06_tables.py             # table registry
```

## Layout
`data/` twin-state table · `results/` metrics, predictions, futures, models ·
`figures/` 59 PNGs + animated GIF · `tables/` 33 machine-readable tables ·
`docs/` thesis parts · `code/` pipeline.

## Web Digital Twin (full-stack)
`webapp/` — FastAPI backend (live trained-model inference: `/api/live/whatif`, `/api/decision`) +
Three.js 3D/4D frontend (globe, plume physics, 4D timeline, twin-state console, counterfactual dreaming,
decision cards). Run: `cd webapp && uvicorn backend:app --port 8000` → open http://localhost:8000.
Offline: open `webapp/static/index.html` directly (pack.js fallback). See `webapp/README_RUN.md`.

## Live deployment
Public twin (static-pack mode): **https://pyrocast-morpheus-twin.netlify.app**
(deploy bundle: `webapp/site/`; redeploy with any change via Netlify API
POST /sites/ef3d9534-1108-477c-9595-0ef4c523bc2e/deploys).
Full LIVE-model mode requires the FastAPI backend (`webapp/backend.py`) on a Python host.

## F35 erratum (2026-08)
`figures/F35_uncertainty_growth.png` and `F35_uncertainty_audit_FINAL.png` implement the honest
uncertainty decomposition (verification RMSE vs persistence, seed-jitter floor, inter-scenario
spread) that supersedes the earlier "trust decay" panel. See `docs/d08_task8_counter.md`,
`code/p11_f35_fix.py`, and `results/f35_audit.json`.

## Quick start
```bash
pip install -r requirements.txt
python3 code/p02_master.py   # then follow the pipeline order above
```

## Citation
If you use this framework, please cite it — see `CITATION.cff` (GitHub renders a "Cite this repository" button).
License: MIT (`LICENSE`).
