#!/usr/bin/env bash
# Rebuilds the map from scratch: model export → voxelization → Bedrock world → previews.
# Requirements: git, Node.js 20+, Python 3.12 (Amulet has no wheels for 3.13 yet), uv or pip.
# Usage: ./run.sh            (full map, ~5 min on a laptop)
#        ./run.sh theatre    (quick test: theatre only, no surroundings)
set -euo pipefail
cd "$(dirname "$0")"

MODEL_REPO="https://github.com/lukasersil/narodni-divadlo-3d.git"
MODEL_COMMIT="2d9e2cd55d9231777eebb3253de8d3e47344b85f"   # pinned: the version the map was built from
CROP="${1:-all}"

echo "== 1/5 model: Lukáš Eršil, narodni-divadlo-3d @ ${MODEL_COMMIT:0:7}"
if [ ! -d vendor/narodni-divadlo-3d/.git ]; then
  git clone --quiet "$MODEL_REPO" vendor/narodni-divadlo-3d
fi
git -C vendor/narodni-divadlo-3d checkout --quiet "$MODEL_COMMIT"

echo "== 2/5 dependencies"
[ -d node_modules ] || npm install --silent
if [ -z "${ND_CHROMIUM:-}" ]; then npx --yes playwright install chromium >/dev/null; fi
if [ ! -x .venv/bin/python ]; then
  PY312="$(command -v python3.12 || true)"
  if command -v uv >/dev/null; then
    uv venv -q -p "${PY312:-3.12}" .venv
    uv pip install -q -p .venv/bin/python -r requirements.txt
  else
    [ -n "$PY312" ] || { echo "Python 3.12 is required (Amulet has no wheels for newer Pythons)"; exit 1; }
    "$PY312" -m venv .venv && .venv/bin/pip install -q -r requirements.txt
  fi
fi
PY=.venv/bin/python

echo "== 3/5 export geometry (headless Chromium, ~1 min)"
node export.mjs

echo "== 4/5 voxelize (2 blocks per metre)"
$PY voxelize.py

echo "== 5/5 write Bedrock world"
$PY build_world.py "Národní divadlo" "$CROP" out/Narodni-divadlo.mcworld
$PY render.py
echo "done: out/Narodni-divadlo.mcworld, previews in out/*.png"
