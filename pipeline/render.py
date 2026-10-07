"""Step 4 (optional) – previews of the voxel grid: a top-down map and isometric views (painter's algorithm)."""
import numpy as np, sys
from PIL import Image

COL = {0: (0, 0, 0), 1: (120, 120, 120), 2: (134, 96, 67), 3: (95, 159, 53), 4: (76, 76, 76), 5: (49, 92, 180),
       6: (122, 121, 121), 7: (210, 178, 161), 8: (161, 83, 37), 9: (102, 165, 216), 10: (109, 85, 50), 11: (60, 120, 40),
       12: (216, 203, 155), 13: (205, 190, 140), 14: (226, 214, 171), 15: (154, 106, 89), 16: (83, 163, 132), 17: (62, 62, 68),
       18: (249, 236, 79), 19: (160, 160, 160), 20: (190, 230, 240), 21: (236, 233, 226), 22: (160, 39, 34), 23: (143, 61, 46),
       24: (66, 43, 20), 25: (162, 130, 78), 26: (240, 200, 110), 27: (220, 220, 220), 28: (219, 207, 163), 29: (150, 97, 83),
       30: (132, 134, 133), 31: (114, 84, 48), 32: (125, 125, 115)}

def topdown(grid, path, step=1):
    nx, ny, nz = grid.shape
    occ = grid > 0
    top = np.where(occ.any(axis=1), ny - 1 - np.argmax(occ[:, ::-1, :], axis=1), -1)
    ids = np.zeros((nx, nz), np.uint8)
    xi, zi = np.nonzero(top >= 0)
    ids[xi, zi] = grid[xi, top[xi, zi], zi]
    lut = np.zeros((256, 3), np.uint8)
    for k, v in COL.items(): lut[k] = v
    img = lut[ids].astype(np.float32)
    # simple height shading
    sh = np.clip((top - np.roll(top, 1, axis=0)) * 0.12 + 1.0, 0.6, 1.3)
    img = np.clip(img * sh[..., None], 0, 255).astype(np.uint8)
    Image.fromarray(img.transpose(1, 0, 2)[::step, ::step]).save(path)  # rows = z (south down), cols = x (east right)

def iso(grid, path, x0, x1, z0, z1, scale=2):
    sub = grid[x0:x1, :, z0:z1]
    occ = sub > 0
    # exposed voxels only
    pad = np.pad(occ, 1)
    exposed = occ & ~(pad[2:, 1:-1, 1:-1] & pad[:-2, 1:-1, 1:-1] & pad[1:-1, 2:, 1:-1] & pad[1:-1, :-2, 1:-1] & pad[1:-1, 1:-1, 2:] & pad[1:-1, 1:-1, :-2])
    xs, ys, zs = np.nonzero(exposed)
    ids = sub[xs, ys, zs]
    # view from the north-west (camera at -x, -z, above): screen u = (x - z), v = (x + z)/2 - y
    u = (xs - zs).astype(np.float32); v = ((xs + zs) * 0.5 - ys).astype(np.float32)
    depth = xs + zs + ys * 0.0  # farther = larger (x+z); draw far first
    order = np.argsort(xs + zs + ys * 1e-3)
    W = int((u.max() - u.min()) * scale) + 4; H = int((v.max() - v.min()) * scale) + 2 * scale + 4
    img = np.zeros((H, W, 3), np.uint8)
    lut = np.zeros((256, 3), np.float32)
    for k, c in COL.items(): lut[k] = c
    px = ((u - u.min()) * scale).astype(np.int64)[order]; py = ((v - v.min()) * scale).astype(np.int64)[order]
    c = lut[ids[order]]
    for dy in range(2 * scale):
        for dx in range(scale):
            shade = 1.0 if dy < scale else 0.72
            img[py + dy, px + dx] = (c * shade).astype(np.uint8)
    Image.fromarray(img).save(path)

if __name__ == '__main__':
    d = np.load('out/voxels.npz'); grid = d['grid']
    topdown(grid, 'out/top.png', 1)
    # theatre crop: world x -60..60, z -80..90  -> indices
    def ix(x): return int((x - (-300)) / 0.5)
    def iz(z): return int((z - (-310)) / 0.5)
    iso(grid, 'out/iso_theatre.png', ix(-70), ix(60), iz(-90), iz(90), 3)
    iso(grid[:, :, :], 'out/iso_all.png', ix(-300), ix(300), iz(-310), iz(290), 1)
    print('ok')
