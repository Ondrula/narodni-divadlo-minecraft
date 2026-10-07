"""Step 2 – voxelize the exported triangle soup into a dense block grid (2 blocks per metre).

Every mesh is sampled on its surface (so rooms stay hollow), each sample marks a block; the block type and its
priority come from classify(). Afterwards the terrain is filled solid below its surface, roads get a concrete top,
the Vltava gets water, and the pit under the theatre is filled to the foundation level.
"""
import json, sys, numpy as np
from scipy import ndimage

PITCH = 0.5                      # metres per block  (2:1)
YOFF = 64                        # street level 0 m -> Minecraft y = 64
# world extent (metres): x east, z south
X0, X1 = -300, 300
Z0, Z1 = -310, 290
Y0, Y1 = -12, 50                 # metres

BLOCKS = {
    1: 'minecraft:stone', 2: 'minecraft:dirt', 3: 'minecraft:grass_block', 4: 'minecraft:gray_concrete',
    5: 'minecraft:water', 6: 'minecraft:stone_bricks', 7: 'minecraft:white_terracotta', 8: 'minecraft:orange_terracotta',
    9: 'minecraft:light_blue_stained_glass', 10: 'minecraft:oak_log', 11: 'minecraft:oak_leaves',
    12: 'minecraft:sandstone', 13: 'minecraft:chiseled_sandstone', 14: 'minecraft:smooth_sandstone',
    15: 'minecraft:polished_granite', 16: 'minecraft:oxidized_copper', 17: 'minecraft:polished_deepslate',
    18: 'minecraft:gold_block', 19: 'minecraft:smooth_stone', 20: 'minecraft:glass', 21: 'minecraft:quartz_block',
    22: 'minecraft:red_wool', 23: 'minecraft:red_terracotta', 24: 'minecraft:dark_oak_planks', 25: 'minecraft:oak_planks',
    26: 'minecraft:glowstone', 27: 'minecraft:iron_block', 28: 'minecraft:sand', 29: 'minecraft:bricks',
    30: 'minecraft:polished_andesite', 31: 'minecraft:spruce_planks', 32: 'minecraft:light_gray_concrete',
}

def classify(it):
    """-> (block id, priority) or None to skip. Higher priority overwrites lower."""
    k, c, name, path = it['matKey'], it['color'], it['name'], it['path']
    r = it.get('reg') or {}
    if path.startswith('trams'): return None
    if ':inside' in name or name == 'wall:inside': return None
    if r.get('modern') and r.get('layer') == 'lighting': return None    # modern stage lanterns
    if path.startswith('site'):
        if name == 'terrain': return (3, 0)
        if name == 'vltava': return (5, 1)
        if name == 'ulice': return (4, 2)
        if name == 'okoli_wall': return (7, 3)
        if name == 'okoli_roof': return (8, 4)
        if name in ('okoli_glass', 'okoli_glassroof'): return (9, 4)
        if k == 'siteStone': return (6, 5)
        if k == 'grass': return (3, 1)
        if k == 'woodDark': return (10, 6)
        if c == '56703f': return (11, 6)
        return (6, 5)
    # theatre
    if k == 'frame': return None                 # thin window bars: ugly as blocks
    if k == 'rubble': return None
    if name.startswith('partitions-'): return (21, 20)
    if k == 'stone': return (12, 10)
    if k == 'rustic': return (13, 11)
    if k == 'trim': return (14, 12)
    if k == 'granite': return (15, 12)
    if k == 'copper': return (16, 14)
    if k == 'slate': return (17, 14)
    if k == 'bronze': return (16, 15)
    if k == 'statue': return (19, 15)
    if k == 'gold' or c == 'e2bd62': return (18, 30)
    if k == 'glass': return (20, 13)
    if k in ('plaster', 'ivory', 'foyerWall', 'inlay', 'inlayBorder'): return (21, 21)
    if k == 'stucco': return (14, 22)
    if k == 'velvet' or k == 'drape': return (22, 24)
    if k == 'boxWall': return (23, 23)
    if k == 'parquet': return (25, 22)
    if k == 'stageFloor': return (24, 22)
    if k in ('lamp',) or c in ('fffaf0', 'fff2d8', 'f6c9bc', 'f4ede0'): return (26, 31)
    if k in ('steel', 'iron', 'ironNew'): return (27, 16)
    if k in ('paving', 'concrete'): return (30, 10)
    if k == 'woodDark': return (24, 22)
    if c in ('4a2a1a', '3b2f25', '1b1511', '141210', '2a2622', '2f3530'): return (24, 23)
    if c in ('6a2a28', '5e1c22', '7a0e24'): return (23, 23)
    if c in ('e9dcc3', 'e8dcc2', 'e7dfcf', 'efe9de', 'c9cdd2', 'ffffff', 'e3d2b4', 'c6a29f', '9aa1a8', 'c8c1b5'):
        if r.get('xray') == 'struct': return (29, 9)
        return (21, 21)
    if c == '2d4a3d': return (16, 15)
    return (21, 21)

def main():
    meta = json.load(open('out/meta.json'))
    T = np.fromfile('out/tris.bin', dtype=np.float32)
    nx = int((X1 - X0) / PITCH); nz = int((Z1 - Z0) / PITCH); ny = int((Y1 - Y0) / PITCH)
    grid = np.zeros((nx, ny, nz), dtype=np.uint8)
    prio = np.zeros((nx, ny, nz), dtype=np.uint8)
    origin = np.array([X0, Y0, Z0], dtype=np.float32)
    print('grid', grid.shape, grid.nbytes / 1e6, 'MB')

    colH = {3: np.full((nx, nz), -1, np.int64), 5: np.full((nx, nz), -1, np.int64), 4: np.full((nx, nz), -1, np.int64)}

    def stamp(P, bid, pr):
        idx = np.floor((P - origin) / PITCH).astype(np.int64)
        if bid in colH and pr <= 2:
            ok0 = (idx[:, 0] >= 0) & (idx[:, 0] < nx) & (idx[:, 2] >= 0) & (idx[:, 2] < nz)
            np.maximum.at(colH[bid], (idx[ok0, 0], idx[ok0, 2]), idx[ok0, 1])
        ok = (idx[:, 0] >= 0) & (idx[:, 0] < nx) & (idx[:, 1] >= 0) & (idx[:, 1] < ny) & (idx[:, 2] >= 0) & (idx[:, 2] < nz)
        idx = idx[ok]
        if len(idx) == 0: return
        lin = np.unique(np.ravel_multi_index((idx[:, 0], idx[:, 1], idx[:, 2]), grid.shape))
        g = grid.reshape(-1); p = prio.reshape(-1)
        sel = lin[p[lin] <= pr]
        g[sel] = bid; p[sel] = pr

    items = [(classify(it), it) for it in meta['items']]
    items = [(cl, it) for cl, it in items if cl and it['type'] == 'mesh']
    items.sort(key=lambda x: x[0][1])
    spacing = PITCH * 0.45
    for (bid, pr), it in items:
        V = T[it['start']:it['start'] + it['floats']].reshape(-1, 3, 3)
        A, B, C = V[:, 0], V[:, 1], V[:, 2]
        e = np.maximum.reduce([np.linalg.norm(B - A, axis=1), np.linalg.norm(C - B, axis=1), np.linalg.norm(A - C, axis=1)])
        n = np.clip(np.ceil(e / spacing).astype(np.int64), 1, 10000)
        for nsub in np.unique(n):
            sel = n == nsub
            a, b, c = A[sel], B[sel], C[sel]
            ii, jj = np.meshgrid(np.arange(nsub + 1), np.arange(nsub + 1), indexing='ij')
            m = (ii + jj) <= nsub
            u = (ii[m] / nsub).astype(np.float32); v = (jj[m] / nsub).astype(np.float32)
            # batch to keep memory bounded
            per = max(1, int(2_000_000 / len(u)))
            for s in range(0, len(a), per):
                aa, bb, cc = a[s:s + per], b[s:s + per], c[s:s + per]
                P = aa[:, None, :] + (bb - aa)[:, None, :] * u[None, :, None] + (cc - aa)[:, None, :] * v[None, :, None]
                stamp(P.reshape(-1, 3), bid, pr)
        print(f'{it["name"][:30]:30s} {it["matKey"]:10s} {it["color"]} -> {BLOCKS[bid]:35s} tris={len(V)}', flush=True)

    # ---------------- terrain: column fill
    h = colH[3]
    cover = h >= 0
    print('terrain columns', cover.sum())
    filled = ndimage.binary_fill_holes(cover)
    hole = filled & ~cover
    # nearest terrain height for the hole (under/around the theatre)
    dist, (ix, iz) = ndimage.distance_transform_edt(~cover, return_indices=True)
    hfill = h[ix, iz]
    # water: columns of the river surface
    wh = colH[5]
    road = colH[4] >= 0
    yy = np.arange(ny)[None, :, None]
    # any theatre/site structure in the column below ground (foundation walls, basement floors)
    struct = (grid >= 6) & (grid != 11) & (grid != 10)
    below = struct[:, : int((0 - Y0) / PITCH), :].any(axis=1)
    found_y = int((-9.6 - Y0) / PITCH)
    H = np.where(cover, h, np.where(hole, hfill, -1))
    # hole columns that contain building structure: fill only up to the foundation underside
    H = np.where(hole & below, np.minimum(H, found_y), H)
    colmask = H >= 0
    fill = (yy < H[:, None, :]) & colmask[:, None, :]
    empty = grid == 0
    grid[fill & empty] = 1
    top = (yy == H[:, None, :]) & colmask[:, None, :] & (grid == 0)
    grid[top] = 3
    # under the building the fill is bare stone, not grass
    grid[top & (hole & below)[:, None, :]] = 1
    # dirt just below the surface
    dirt = (yy < H[:, None, :]) & (yy >= (H - 3)[:, None, :]) & colmask[:, None, :] & (grid == 1)
    grid[dirt] = 2
    # roads: top block -> concrete
    rtop = (yy == H[:, None, :]) & (road & colmask)[:, None, :]
    grid[rtop & (grid == 3)] = 4
    # bridge deck and quays: where masonry sits just under the surface, the top is paved stone, not grass
    masonry = ((grid == 6) & (yy >= (H - 3)[:, None, :]) & (yy <= H[:, None, :])).any(axis=1)
    grid[(yy == H[:, None, :]) & (masonry & colmask)[:, None, :] & (grid == 3)] = 6
    # river: water from 3 blocks under the surface up to the water level, sand bed
    wcol = wh >= 0
    wat = (yy <= wh[:, None, :]) & (yy >= (wh - 4)[:, None, :]) & wcol[:, None, :]
    grid[wat & ((grid == 1) | (grid == 2) | (grid == 3) | (grid == 0))] = 5
    bed = (yy == (wh - 5)[:, None, :]) & wcol[:, None, :]
    grid[bed & ((grid == 1) | (grid == 2) | (grid == 3))] = 28
    # drop anything outside the terrain coverage (context buildings beyond the terrain disc would float)
    xs = (np.arange(nx) * PITCH + X0)[:, None]; zs = (np.arange(nz) * PITCH + Z0)[None, :]
    outside = ~(cover | hole | (wh >= 0)) | (np.hypot(xs, zs) > 330)
    grid[outside[:, None, :] & np.ones((1, ny, 1), bool)] = 0

    np.savez_compressed('out/voxels.npz', grid=grid, origin=np.array([X0, Y0, Z0]), pitch=PITCH, yoff=YOFF)
    ids, cnt = np.unique(grid, return_counts=True)
    for i, c in zip(ids, cnt):
        print(i, BLOCKS.get(int(i), 'air'), c)

if __name__ == '__main__':
    main()
