# Pipeline: from the 3D model to a Bedrock world

This folder regenerates `map/Narodni-divadlo.mcworld` from scratch. Everything is deterministic; running it on the pinned commit of the model produces the same world.

```
narodni-divadlo-3d (Lukáš Eršil)  ──export.mjs──▶  out/tris.bin + out/meta.json
                                                        │
                                                   voxelize.py
                                                        ▼
                                                 out/voxels.npz   ──build_world.py──▶  out/Narodni-divadlo.mcworld
                                                        │
                                                    render.py  ──▶  out/*.png (previews)
```

## Requirements

- git, Node.js 20+ (tested on 22), npm
- Python **3.12** (Amulet Core has no wheels for 3.13 yet); `uv` is used if present, otherwise `venv` + `pip`
- Chromium for Playwright (`npx playwright install chromium`; or point `ND_CHROMIUM` at an existing binary)
- ~1 GB RAM for the voxel grid (1200 × 124 × 1200 cells), a few minutes of CPU

## Run

```bash
cd pipeline
./run.sh            # full map, ~5 min
./run.sh theatre    # quick test: theatre only, 540 chunks, ~1 min after export
```

`run.sh` clones the model at the pinned commit into `vendor/`, installs dependencies into `node_modules/` and `.venv/`, and runs the four steps. Outputs land in `out/` (git-ignored).

## Steps

### 1. `export.mjs` — bake the model to triangles

The model has no mesh files: the building is generated procedurally in Three.js at page load. The script serves the repo with its own `serve.py`, opens it in headless Chromium (WebGL 2 fallback – the sandbox has no WebGPU), patches `src/main.js` on the fly to expose the scene, waits for the shader warm-up to finish (the app hides every mesh while compiling shaders), sets the construction clock to the finished state (`R.update(7)`), and walks the scene graph. Every visible `Mesh`/`InstancedMesh` is transformed to world space (instances expanded, collapsed instances skipped) and streamed to `out/tris.bin` as float32 triangles. `out/meta.json` records, per mesh: name, parent path, material key (looked up by identity in the app's `M` material table), base colour, and the registry flags the app uses for X-ray/timeline (`stage`, `modern`, `layer`, `xray`).

The CDN import map (`three@0.186.1` on jsDelivr) is routed to the local `node_modules/three`, so the export works offline and against the exact Three.js version.

World frame of the model (and of the map): metres, x = east, y = up, z = south, origin at the north façade line; street level y = 0 (191.3 m above sea level, Baltic datum).

### 2. `voxelize.py` — triangles to blocks

Pitch 0.5 m (2 blocks per metre). Each triangle is sampled on a barycentric lattice with spacing ≤ 0.225 m (so no 0.5 m voxel is missed), samples are rounded into a dense `uint8` grid. Meshes are written in ascending priority, so e.g. gold overwrites stucco overwrites masonry. `classify()` maps `(material key, colour, name, registry flags)` → `(block id, priority)` or skips the mesh (window bars, trams, section-only "inside" faces, X-ray-only layers).

Post-processing on columns: terrain surface height from the terrain samples; solid fill (stone, 3 layers of dirt, grass top) below it; roads get a concrete top; river columns get 4 blocks of water and a sand bed; where masonry sits just under the surface (quays, the bridge deck) the top is stone bricks. The terrain mesh has a hole around the theatre: columns in it are filled to the nearest terrain height, except columns that contain building structure below ground, which are filled only to the foundation level (−9.6 m) so the basements stay hollow. Everything outside the terrain disc (~330 m) is dropped.

Output: `out/voxels.npz` – the grid, its origin in metres, pitch and the y offset (street level → Minecraft y 64).

### 3. `build_world.py` — write the Bedrock world

Uses Amulet Core 1.9: creates an empty Bedrock world (format version 1.21.90), then for every 16 × 16 chunk builds a `16 × 384 × 16` palette-index array (bedrock at y −64, stone up to the grid base, then the grid) and stores it with `world.put_chunk`. Blocks are given as Java 1.20 names and translated to Bedrock by PyMCTranslate (`grass_block`, `oxidized_copper`, `polished_deepslate`, … all exist in Bedrock ≥ 1.21). A margin of 320 blocks of flat land is pre-generated around the data so the world generator never shows a cliff; `level.dat` is set to the flat generator with matching layers (grass at y 58), creative mode, peaceful, daylight cycle off, spawn at (−6, 69, −96) on Národní street. The world folder is zipped as `.mcworld`.

Arguments: `build_world.py "<world name>" [all|theatre] [output path]`.

### 4. `render.py` — previews

Top-down map (`out/top.png`) and isometric painter's-algorithm renders of exposed voxels (`out/iso_theatre.png`, `out/iso_all.png`). No Minecraft textures – flat colours per block type – but good enough to check the result without launching the game.

## Changing things

- **Block palette / priorities:** `BLOCKS` and `classify()` in `voxelize.py`. Colours of the previews: `COL` in `render.py`.
- **Scale:** `PITCH` in `voxelize.py` (0.5 = 2:1). At 1:1 the interior is unusable; at 3:1 the grid is 27× larger – crop the extent (`X0..Z1`) first.
- **Extent / what is included:** `X0, X1, Z0, Z1` and the 330 m disc in `voxelize.py`; the `trams` / `modern` skips in `classify()`.
- **Different model commit:** `MODEL_COMMIT` in `run.sh`. Check `classify()` afterwards – material keys and colours are matched by name and hex value.
- **Java Edition:** Amulet can convert the generated world (`amulet.load_level` → `world.save_iter` to a Java format wrapper); planned, see `ROADMAP.md`.

## Known limitations of the approach

Surface sampling keeps rooms hollow but makes thin elements (railings, balusters, lamp arms) into floating 1-block fragments. There are no stairs or slabs – everything is full blocks. Windows are solid glass because the bars are skipped. Context buildings are shells from IPR's roof-and-wall model, without openings. See `docs/co-je-v-mape.md` for the user-facing list.
