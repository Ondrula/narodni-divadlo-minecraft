"""Step 3 – write the voxel grid into a new Bedrock world with Amulet and pack it as .mcworld.

Usage: python build_world.py "<world name>" [all|theatre] [output file]
"""
import sys, os, json, shutil, time, zipfile
import numpy as np
import amulet
from amulet.api.block import Block
from amulet.api.chunk import Chunk
from amulet.api.selection import SelectionGroup, SelectionBox
from amulet.level.formats.leveldb_world import LevelDBFormat
from amulet.api.level import World
import amulet_nbt as nbt
from voxelize import BLOCKS

BEDROCK_VERSION = (1, 21, 90)
NAME = sys.argv[1] if len(sys.argv) > 1 else 'Národní divadlo'
OUTDIR = 'out/world'
CROP = sys.argv[2] if len(sys.argv) > 2 else 'all'   # 'theatre' for a quick test

d = np.load('out/voxels.npz')
grid = d['grid']; X0, Y0, Z0 = d['origin']; PITCH = float(d['pitch']); YOFF = int(d['yoff'])
nx, ny, nz = grid.shape
# minecraft coordinates of grid index 0
MX0 = int(round(X0 / PITCH)); MZ0 = int(round(Z0 / PITCH)); MY0 = int(round(Y0 / PITCH)) + YOFF
print('grid', grid.shape, 'mc origin', MX0, MY0, MZ0)

if CROP == 'theatre':
    gx0, gx1 = int((-80 - X0) / PITCH), int((80 - X0) / PITCH)
    gz0, gz1 = int((-100 - Z0) / PITCH), int((110 - Z0) / PITCH)
else:
    gx0, gx1, gz0, gz1 = 0, nx, 0, nz

# ---- ground outside the data: flat profile matching the generator settings
FLAT_TOP = 58          # grass at y=58 (bedrock -64, stone, 2 dirt, grass)
occupied_cols = (grid > 0).any(axis=1)

shutil.rmtree(OUTDIR, ignore_errors=True)
os.makedirs(OUTDIR, exist_ok=True)
fmt = LevelDBFormat(OUTDIR)
fmt.create_and_open('bedrock', BEDROCK_VERSION, bounds=SelectionGroup(SelectionBox((-30000000, -64, -30000000), (30000000, 320, 30000000))), overwrite=True)
fmt.close()
open(os.path.join(OUTDIR, 'levelname.txt'), 'w').write(NAME)
world = amulet.load_level(OUTDIR)
fmt = world.level_wrapper
dim = 'minecraft:overworld'
tm = world.translation_manager
java = tm.get_version('java', (1, 20, 0))

def ublock(name):
    ns, base = name.split(':')
    b = Block(ns, base)
    ub, _, _ = java.block.to_universal(b)
    return ub

UB = {i: ublock(n) for i, n in BLOCKS.items()}
UB_BEDROCK = ublock('minecraft:bedrock')
UB_AIR = ublock('minecraft:air')

t0 = time.time()
MARGIN = 0 if CROP == 'theatre' else 320   # flat chunks written around the data so the generator never shows a cliff
cx0, cx1 = (MX0 + gx0 - MARGIN) // 16, (MX0 + gx1 - 1 + MARGIN) // 16
cz0, cz1 = (MZ0 + gz0 - MARGIN) // 16, (MZ0 + gz1 - 1 + MARGIN) // 16
total = (cx1 - cx0 + 1) * (cz1 - cz0 + 1); done = 0
H_STONE_TOP = FLAT_TOP - 3
for cx in range(cx0, cx1 + 1):
    for cz in range(cz0, cz1 + 1):
        done += 1
        # grid index window for this chunk
        ax0, az0 = cx * 16 - MX0, cz * 16 - MZ0
        sx0, sx1 = max(ax0, gx0), min(ax0 + 16, gx1)
        sz0, sz1 = max(az0, gz0), min(az0 + 16, gz1)
        chunk = Chunk(cx, cz)
        if sx1 <= sx0 or sz1 <= sz0:
            # flat filler chunk
            air = chunk.block_palette.get_add_block(UB_AIR); bed = chunk.block_palette.get_add_block(UB_BEDROCK)
            stone = chunk.block_palette.get_add_block(UB[1]); dirt = chunk.block_palette.get_add_block(UB[2]); grass = chunk.block_palette.get_add_block(UB[3])
            arr = np.full((16, 384, 16), air, dtype=np.uint32)
            arr[:, 0, :] = bed; arr[:, 1:H_STONE_TOP + 64, :] = stone; arr[:, H_STONE_TOP + 64:FLAT_TOP + 64, :] = dirt; arr[:, FLAT_TOP + 64, :] = grass
            chunk.blocks[:, -64:320, :] = arr; chunk.changed = True; world.put_chunk(chunk, dim)
            if done % 500 == 0: world.save(); world.unload()
            continue
        sub = grid[sx0:sx1, :, sz0:sz1]
        pal = {}
        def pidx(i):
            if i not in pal: pal[i] = chunk.block_palette.get_add_block(UB[i])
            return pal[i]
        air = chunk.block_palette.get_add_block(UB_AIR)
        bed = chunk.block_palette.get_add_block(UB_BEDROCK)
        stone = pidx(1); dirt = pidx(2); grass = pidx(3)
        # full chunk array: 16 x (320+64) x 16, indexed from y=-64
        arr = np.full((16, 384, 16), air, dtype=np.uint32)
        arr[:, 0, :] = bed
        ox, oz = sx0 - ax0, sz0 - az0
        w, l = sx1 - sx0, sz1 - sz0
        cols = occupied_cols[sx0:sx1, sz0:sz1]
        # columns with data: solid stone from bedrock up to the grid base
        base = MY0 + 64  # array index of grid y=0
        a = arr[ox:ox + w, :, oz:oz + l]
        a[:, 1:base, :] = np.where(cols[:, None, :], stone, air)
        # columns without data: flat ground
        flat = ~cols
        a[:, 1:H_STONE_TOP + 64, :][flat[:, None, :].repeat(H_STONE_TOP + 63, axis=1)] = stone
        a[:, H_STONE_TOP + 64:FLAT_TOP + 64, :][flat[:, None, :].repeat(3, axis=1)] = dirt
        a[:, FLAT_TOP + 64, :][flat] = grass
        # the voxel data
        ids = np.unique(sub); ids = ids[ids > 0]
        lut = np.zeros(256, dtype=np.uint32)
        for i in ids: lut[i] = pidx(int(i))
        a[:, base:base + ny, :] = np.where(sub > 0, lut[sub], a[:, base:base + ny, :])
        chunk.blocks[:, -64:320, :] = arr
        chunk.changed = True
        world.put_chunk(chunk, dim)
        if done % 500 == 0:
            print(f'{done}/{total} chunks, {time.time() - t0:.0f}s', flush=True)
            world.save(); world.unload()

# ---- level.dat: name, flat generator, spawn, creative
root = fmt.root_tag
if hasattr(root, 'compound'): root = root.compound
root['LevelName'] = nbt.StringTag(NAME)
root['Generator'] = nbt.IntTag(2)
root['FlatWorldLayers'] = nbt.StringTag(json.dumps({"biome_id": 1, "block_layers": [
    {"block_name": "minecraft:bedrock", "count": 1}, {"block_name": "minecraft:stone", "count": H_STONE_TOP + 63},
    {"block_name": "minecraft:dirt", "count": 3}, {"block_name": "minecraft:grass_block", "count": 1}],
    "encoding_version": 6, "structure_options": None, "world_version": "version.post_1_18"}))
# spawn in front of the north facade on Narodni
sx, sz = int(round(-3 / PITCH)), int(round(-48 / PITCH))
col = grid[int((-3 - X0) / PITCH), :, int((-48 - Z0) / PITCH)]
top = int(np.nonzero(col)[0].max()) + MY0 if col.any() else FLAT_TOP
root['SpawnX'] = nbt.IntTag(sx); root['SpawnY'] = nbt.IntTag(top + 2); root['SpawnZ'] = nbt.IntTag(sz)
root['GameType'] = nbt.IntTag(1)
root['RandomSeed'] = nbt.LongTag(1883)
root['SpawnV1'] = nbt.IntTag(1)
root['Time'] = nbt.LongTag(6000)
root['currentTick'] = nbt.LongTag(6000)
root['InventoryVersion'] = nbt.StringTag('1.21.90')
root['MinimumCompatibleClientVersion'] = nbt.ListTag([nbt.IntTag(i) for i in (1, 21, 90, 0, 0)])
root['NetworkVersion'] = nbt.IntTag(818)
root['Platform'] = nbt.IntTag(2)
root['hasBeenLoadedInCreative'] = nbt.ByteTag(1)
root['bonusChestEnabled'] = nbt.ByteTag(0)
root['spawnMobs'] = nbt.ByteTag(0)
root['keepinventory'] = nbt.ByteTag(1)
root['dodaylightcycle'] = nbt.ByteTag(0)
root['doweathercycle'] = nbt.ByteTag(0)
root['mobgriefing'] = nbt.ByteTag(0)
root['LANBroadcast'] = nbt.ByteTag(1)
root['isFromWorldTemplate'] = nbt.ByteTag(0)
root['worldStartCount'] = nbt.LongTag(0)
root['commandsEnabled'] = nbt.ByteTag(1)
root['dodaylightcycle'] = nbt.ByteTag(0)
root['Difficulty'] = nbt.IntTag(0)
world.save()
world.close()
print('spawn', sx, top + 2, sz, 'elapsed', time.time() - t0)

# ---- pack .mcworld
mc = sys.argv[3] if len(sys.argv) > 3 else 'out/Narodni-divadlo.mcworld'
with zipfile.ZipFile(mc, 'w', zipfile.ZIP_DEFLATED) as z:
    for rootdir, _, files in os.walk(OUTDIR):
        for f in files:
            p = os.path.join(rootdir, f)
            z.write(p, os.path.relpath(p, OUTDIR))
print('wrote', mc, os.path.getsize(mc) / 1e6, 'MB')
