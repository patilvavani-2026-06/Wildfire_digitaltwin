# PART XI — References, Data Notes, and Closing

## Selected references & technical sources

1. NOAA NCEI, *GOES-R Series ABI Level 2 Fire/Hot Spot Characterization (FDC)* — product lineage and the B07/B14 (3.9/11.2 µm) sub-pixel fire contrast heritage (Matson–Dozier; WF_ABBA/FDCA). ncei.noaa.gov (accessed 2026-08).
2. NOAA/NESDIS/STAR, *ATBD: GOES-R ABI Fire Detection and Characterization* v2.6 — multispectral thresholding lineage for band 7/14 fire logic.
3. CIMSS/SSEC, *ABI Quick Guide: Band 7 (3.9 µm)*; CIMSS Satellite Blog (2020), *When is an ABI hot spot not a fire?* — interpretation caveats for t07−t14 under clouds/solar contamination.
4. DestinE Earth Data Hub, *ERA5 hourly data on single levels* — variable definitions/units (blh m; cape/cin J kg⁻¹; tp m; cvh/cvl fractions; accumulated fluxes J m⁻²), accessed 2026-08.
5. ECMWF Confluence KB, *ERA5-Land data documentation* — accumulation convention; ECMWF vertical-flux sign convention (positive downward), corroborated by NOAA ARL `era52arl` notes (HYSPLIT forum).
6. Copernicus/CDS (ERA5) parameter listing via `ecmwf_models` docs (u10/v10, fg10, z, t2m etc.).
7. Wikipedia/Wikidata, *Johnson Fire (2021, Gila NF)* — ignition date/coordinates used for the event-179 identification cross-check.
8. Peterson, D. et al. — pyrocumulonimbus climatology and conceptual model (BAMS 2017; subsequent catalogs); U. Manitoba PyroCb tracking blog — event-numbering convention consistent with uploaded `pyroCb_id`s.
9. Evensen, G. — *Data Assimilation: The Ensemble Kalman Filter* (Springer) — stochastic EnKF form used for the heartbeat.
10. Pearl, J. — *Causality* — do-operator semantics for the counterfactual engine.
11. Rockafellar & Uryasev (2000) — CVaR optimization form used in decision intelligence.
12. Kirkpatrick et al. (2017) — EWC anti-forgetting penalty (memory consolidation).
13. Chen, R.T.Q. et al. (2018) — Neural ODEs (designated kernel upgrade).
14. Vaswani et al. (2017); Gu & Dao (2023, Mamba) — deferred sequence backbones (positioning in §7.1).
15. Vovk, V. — conformal prediction foundations (self-audit module).
16. Rothermel (1972); Van Wagner (1987, FWI) — fire-spread/physics priors referenced for graph-edge constraints and fuel-moisture extension design.
17. Fromm, M. et al. — PyroCb outburst dynamics and stratospheric injection case literature (mechanism priors in KG).
18. Tao et al.; Bauer, Stevens & Hazeleger (DestinE) — digital-twin-Earth strategic context (positioning in §2.1).

*(Web-grounded lookups during this build: GOES ABI band/fire-product lineage, ERA5 units & sign conventions by ECMWF/D2E documentation; event identity cross-check for Johnson Fire.)*

## Data-stewardship notes

- `data/master.csv` is derived from the uploads and preserves row-level provenance ordering; schema T30.
- Known limitations: single-pixel anchors; proxy-level fire intensity (no FRP); no smoke concentration field; fuel moisture proxied; CIN structural missingness; 12-h cadence irregularities on 4 events.
- Recommended enrichment order: FRP/active-fire products → d2m & fuel models → GLM lightning → AOD/MAIAC → multi-cell grids (E1–E6).

## Closing statement

We were asked to invent, not to explain. PyroCast–MORPHEUS is therefore delivered as three things at once: a **definition** (a new twin species with nine coined, operational concepts), a **machine** (an 11-stratum architecture with complete mathematics and algorithms), and — because invention untested is speculation — a **living reference instance** that synchronizes (heartbeat: 45% error annihilation), remembers (Alaska finds Alaska; α\*=0.3 fusion wins everywhere), dreams (46,224 futures, decisions ranked by their tails), and audits itself (coverage 0.65→0.776). Its flaws have been hunted in the open (Part X). The wildfire community does not need another predictor; it needs an infrastructure that learns every fire season and is honest about what it does not know. That infrastructure now has a name, a state, a heartbeat, a memory, an imagination — and a repository.

*— End of thesis body. Appendices: artifact registries (Part VIII), machine artifacts (`results/`), and the condensed IEEE-TGRS paper (`PyroCast_TGRS_paper.md`).*
