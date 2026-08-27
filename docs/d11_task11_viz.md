# PART V (cont.) — TASK 11: The Visualization System (NASA-quality 4D)

*(Concept renders `R01/R02`; 3D globe mock `D51`; animated 4D globe `figures/globe_plume.gif` (rotating terrain–fire–plume–PyroCb); dashboard layout `D52`; render stack `D53`; time system `D54`; counterfactual viewer `D55`.)*

## 11.1 Renderer technology decision

| Engine | Strengths | Weakness | Role chosen |
|---|---|---|---|
| **CesiumJS** | web-scale 3D globe, 3D Tiles, time-dynamic czml, STAC-friendly | volumetric smoke needs custom raymarch | **primary planetary viewport** |
| NASA WorldWind | provenance, KRosetta lineage, GOVStack | aging web stack | heritage/alternate viewport |
| Three.js | custom shaders, volumetric plumes | no native globe tiles | plume/trust-field GPU renderer inside Cesium scene |
| ArcGIS (JS/Pro) | agency-standard 2D, ops dashboards | weak 4D | operations 2D twin view (mutual situation awareness) |
| Unreal/Unity | cinematic volumetrics (fire/smoke), VR briefing | heavyweight deploy | "immersion room" for after-action & public comms |

**Decision:** CesiumJS shell + custom WebGPU/WebGL volumetric smoke pass + ArcGIS 2D ops twin + Unreal cinematic exporter; all fed by the same state-snapshot service (STAC items + COG rasters + Zarr fields — cloud-native, no bespoke formats).

## 11.2 The five composited layer groups (D53)

**I Base Earth** — global imagery (Blue Marble/Sentinel-2), COP-DEM terrain, night-lights context; **II Observations** — GOES ABI RGB + fire-proxy hotspot glyphs + smoke alpha + QC tint; **III Atmosphere** — ERA5/PL fields: BLH translucent volume, CAPE underlay, RH-column curtain, animated 10-m and 250-hPa wind particles (plume tilt becomes *visible*); **IV Twin state** — fire-front polylines, vital-sign extrusion pillars at event anchor, **trust-field tint** Θ(x): regions literally fade as trust decays (uncertainty the eye cannot miss); **V Futures** — counterfactual *ghost plumes* (one translucent volume per ω, colour = risk band), probability isopleths, action pins from Task 9 cards.

## 11.3 Mockup layouts (generated)

1. **`D51`/`globe_plume.gif`** — 4D globe grammar: terrain (gist_earth), fire glow glyph at anchor, bent translucent smoke column drifting with steering wind, flattened white PyroCb cap pulsing at tropopause; camera azimuth sweep demonstrates the rotational inspection; every visual channel mapped to a data channel (Table below).
2. **`D52` — decision dashboard (dark mission console):** live globe (2×2), four vital-sign annular gauges V₁–V₄, futures fan with baseline vs S7/S4 bands, CVaR action ranking bars, 4D timeline scrubber with event markers, twin console line (Θ, D, coverage, memory hits). Grid: 3×8 docking layout, all panels data-bound to the state service.
3. **`D54` — 4D time system:** Hovmöller ribbons (fire proxy / cloud-top BT / PII / Θ), activity stream with event markers (ignition+6h, first PyroCb, NOW, decay onset), hazard-probability strip with NOW playhead; supports click-to-scrub the globe.
4. **`D55` — counterfactual comparison:** split worlds (baseline | S7) with linked cameras and synced playheads + Δ-viewer card (ΔP(PyroCb), Δplume-top, Δσ, confidence; ensemble-member slider k∈[1..48]).

## 11.4 Data→visual grammar (publication rule set)

| Visual channel | Data binding |
|---|---|
| fire glow intensity/size | fire_proxy (t07−t14) |
| smoke column bend/drift | (u10,v10)→(u₂₅₀,v₂₅₀) shear vector |
| plume height/brightness | cloud_height_proxy, raw_cloud_bt |
| anvil cap | t14−t16 positive mask |
| tint overlay | trust field Θ(x,t) |
| ghosts | counterfactual ensemble {ω} |
| gauges | vital signs V₁–V₄ |

## 11.5 Performance & access

3D Tiles/OGC API delivery, LOD plume octrees; 6-h frames interpolated with optical-flow advection for smooth playback (physics-honest interpolation flag in UI); web dashboard for analysts; CGA-quality Unreal exporter for command briefings; WCAG-AA palettes (fire ramps checked for CVD); every frame carries UTC stamp, version, provenance hash.
