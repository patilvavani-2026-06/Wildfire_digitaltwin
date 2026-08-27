# PART I — TASK 1: Forensic Study of the Uploaded Datasets

## 1.1 What the real-world system *is*

The seven uploaded files collapse to a single coherent object (proven in `code/p01_profile.py`: every `merged_*` file is a strict column-superset of its predecessor — row values identical, new sensor/derived blocks appended):

> **A six-hourly multi-sensor trajectory archive of ten pyrocumulonimbus (PyroCb) lifecycles**, each row being a synchronized snapshot of (a) the GOES-observed fire/cloud system at the PyroCb pixel, (b) the ERA5 atmosphere over that pixel, (c) the underlying terrain–vegetation substrate, and (d) pressure-level moisture and steering flow.

The cohort (`tables/T_event_catalog.csv`, figure `F01`, `F18`):

| ID | Window (UTC) | Lat/Lon | Duration tracked | Plausible 2021–22 identification* | Regime |
|---|---|---|---|---|---|
| 179 | 27 May–2 Jun 2021 | 33.29°N −108.59°W | 138 h | **Johnson Fire**, Gila NF, New Mexico (lightning-caused; confirmed coordinates 33.24°N −108.47°W) | high-elevation subtropical continental |
| 180 | 12–17 Jun 2021 | 33.20°N −111.08°W | 132 h | Telegraph-complex-consistent, Arizona | arid continental |
| 181 | 16–21 Jun 2021 | 37.71°N −113.79°W | 132 h | SW-Utah-consistent (Flatt Fire vicinity) | plateau |
| 189 | 28 Jun–3 Jul 2021 | 41.47°N −122.33°W | 132 h | **Lava Fire**-consistent, Mt Shasta, CA (explosive pyroCb, late Jun 2021) | Cascade |
| 190 | 28 Jun–3 Jul 2021 | 57.52°N −123.00°W | 132 h | British-Columbia **heat-dome** fires (CAPE max 1578 J/kg — extreme for that latitude; wind250 max 46 m/s) | boreal cordillera |
| 202 | 8–13 Jul 2021 | 50.80°N −95.03°W | 138 h | Manitoba Interlake fires (cohort's most intense fire proxy, −143) | boreal lowland |
| 216 | 17–21 Jul 2021 | 64.12°N −133.02°W | 108 h | Yukon/NT fires | subarctic |
| 253 | 29 Mar–3 Apr 2022 | 25.60°N −80.43°W | 138 h | south-Florida (Big Cypress/Everglades) spring fire; cohort's **CAPE peak 2687 J/kg** and highest injection potential | subtropical wetland |
| 258 | 9–14 Jun 2022 | 63.79°N −153.40°W | 132 h | interior-Alaska event A | boreal |
| 260 | 8–14 Jun 2022 | 63.33°N −155.60°W | 138 h | interior-Alaska event B (258's regional sibling) | boreal |

\*Identification by date/location cross-match against public fire records (e.g., the Johnson Fire match is confirmed; the rest are stated as *consistent with* named 2021–2022 events, hedged deliberately). Each event shows 19–24 steps at ~6-hour cadence (some 12-h gaps — QC flags in §1.6).

**This is not a generic wildfire dataset. It is a PyroCb lifecycle dataset** — the atmosphere's violent response to extreme fire — which is precisely the regime where fire–atmosphere coupling becomes a feedback loop rather than a one-way forcing.

## 1.2 Feature families: physical meaning (audit in `tables/T02_…T05_*`)

**(a) GOES ABI block (Table T02).** The README confirms the proxies derive from ABI window/absorption bands: B07 3.9 µm (sub-pixel hotspot sensitivity — the classic Matson–Dozier fire channel; confirmed by the NOAA FDC ATBD lineage), B14 11.2 µm (cloud-top window), B16 13.3 µm (CO₂ absorption; `t14 − t16 > 0` indicates cold *high* cloud because channel 16 cannot see through to the warmer surface), B01–B03 (visible pseudo-green for smoke texture). The file therefore encodes **fire radiative activity** (`fire_proxy = t07 − t14`), **plume verticality** (`cloud_height_proxy = t14 − t16`), and **cloud-top thermodynamic state** (`raw_cloud_bt`) — the three observables by which a PyroCb announces itself to geostationary orbit.

**(b) ERA5 single-levels (Table T03).** `t2m, sp, u10, v10, z, blh, cape, cin, tp, slhf, sshf, fg10` — the surface-energy, boundary-layer, and buoyancy triad. ECMWF sign conventions verified: heat fluxes are accumulated **J m⁻² per 6 h, positive downward** (so the strongly negative `sshf/slhf` daytime peaks are *upward* fluxes feeding the plume). `cin` is structurally missing in 201/227 rows because no buoyant parcel exists on capped steps — an informative missingness that the upstream team correctly `cin_filled` and `capped_flag`-ged.

**(c) Pressure-level block (Table T05).** `rh_850/750/650` gives the *vertical moisture structure* needed to reason about entrainment and evaporative downdrafts; `u_250/v_250` samples anvil-level steering. These two blocks are what elevate the file above ordinary fire-weather datasets: they permit genuine diagnosis of **plume–jet interaction**.

**(d) Terrain/vegetation (Table T04).** DEM-derived `elevation, slope, aspect, tpi, tri` (static) and ERA5 land parameters `cvh/cvl, tvh/tvl` (fuel structure). Event 179 sits at 3040 m with 29° slopes — an orographic chimney; 253 at 8 m — a wetland floor. The cohort deliberately spans the terrain-contrast axis.

**(e) Pre-derived indices.** `injection_potential` and `PII` (PyroCb Injection Index) are prior-work composites; we retain them as *features and labels* but audit them (Fig `F06`, `F13`) rather than trust them.

## 1.3 What the cohort can and cannot represent (Tasks 1a–1f, answered in evidence)

| Phenomenon | Represented? | Evidence in the corpus |
|---|---|---|
| **Fire behaviour (intensity)** | ✔ proxy-level | `fire_proxy` spans −33…−143; `raw_fire_bt` saturates 320 K-scale daytime spikes; diurnal amplitude clear in `F08` |
| **Atmospheric evolution** | ✔ | Diurnal BLH pump (12→5200 m), flux sign flips, RH-column evolution, CAPE/CIN intermittency (`F07`, `F08`, `F12`) |
| **PyroCb formation/lifecycle** | ✔ | Cold cloud-top invigoration tracked via `raw_cloud_bt` minima to 0.03; growth/mature/decay phase portrait separable (`F10`); PII/injection labels |
| **Fire intensity ↔ convection coupling** | ✔ | Learned coupling matrix `F31` (next-section result); `F09`: BLH/CAPE/fluxes lead 6-h Δcloud-top BT; `F13` buoyancy phase space |
| **Smoke transport (dynamics)** | ◐ partial | 250-hPa steering + BLH ventilation + directional shear (`F11`) permit plume-drift reasoning; *no smoke concentration/aerosol field* — flagged as data gap G3 |
| **Fuel moisture** | ◐ proxy only | no d2m/fuel model; we synthesize `dry_spell` memory (§IX method) and use RH-column + flux partition as surrogates — data gap G1 |
| **Ignition location counterfactuals** | ◐ static | terrain supports relocation operators (used in S6) but within-event spread is unresolved |

## 1.4 The physical grammar recovered from the signals (key EDA findings)

1. **The afternoon invigoration cycle dominates short-horizon dynamics.** Next-cycle cloud-top cooling correlates −0.65 with diurnal phase (`F09`→`y_cbt_chg_p1` row; `F08` BLH/SSHF/CAPE composites) — convection and fire beat to the same solar drum.
2. **Regimes separate.** Boreal events run moist columns (`rh_colmean` median 33–44% vs 5–8% in the desert Southwest, `F12`), and regime archetypes emerge cleanly in profile space (`F20`).
3. **The cohort's state space is low-dimensional.** PCA on 28 variables: PC1 (fire intensity + geography) and PC2 (buoyancy/moisture) carry the dominant variance; events form elongated lifecycle ribbons, not clouds (`F17`) — license for a *latent* twin state (§IV).
4. **Cross-event level shift is large.** `pixel_longitude` alone correlates |0.64| with next-cycle fire proxy — geography is a confounder that any honest validation must block (LOEO; §IX).
5. **Severity is multi-dimensional**, not ordered by any single index: intensity peak (202), energy (253), injection (253/190), cold-core depth (216/258) — motivating the *vital-signs* representation (`F39`).

## 1.5 Unit/scale audit (a data-engineering finding that becomes a Task-18 issue)

The GOES block mixes raw physical units with per-file normalization: `raw_cloud_bt`∈[0.03, 2.10] and `raw_fire_bt`∈[0, 320] are clearly *scaled* brightness temperatures (event 179 shows `raw_fire_bt`=0.082 ≪ physical BT), while `simulated_green` carries DN-like magnitudes (~72–98). `fire_proxy` values (−143…−33 for cloud-shielded PyroCb pixels) are consistent with B07−B14 over cold anvils at night (solar reflectance absent; B07 sees less of the warm sub-layer), but a strict unit provenance is absent from the README. **Actions taken:** (i) all learning pipelines standardize per training fold; (ii) the twin's fusion layer includes a mandatory *unit-audit gate* (T06, D50); (iii) interpretation is sign/magnitude-relative, never absolute-kelvin. This is not cosmetic: unit drift between GOES-16 and GOES-17 processing is a real hazard in production twins.

## 1.6 Data quality ledger

- 3 rows carry NaN GOES blocks (cloud-contaminated QC drops) — imputed within-fold (T06, T14).
- ~12-h cadence irregularities on 4 events (steps 5.8–12.2 h) — the synchronizer treats Δt explicitly (§V).
- `tp` ≈ 0 almost everywhere — PyroCb boreal/dry bias; the rain-out counterfactual (S4) therefore probes a *rare* corner (handled cautiously, Task 18).

**Verdict:** the corpus can fire, breathe, and storm in silico — exactly the minimal viable *living* substrate a wildfire digital twin requires, provided the twin (i) assimilates rather than free-runs and (ii) remembers rather than re-learns. Both provisions become architectural law in Part II.
