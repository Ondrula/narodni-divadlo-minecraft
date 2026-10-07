#!/usr/bin/env bash
# Publishes map/Narodni-divadlo.mcworld as a GitHub release (needs the `gh` CLI, logged in).
# Usage: scripts/release.sh 0.1.0
set -euo pipefail
VERSION="${1:?version, e.g. 0.1.0}"
cd "$(dirname "$0")/.."
gh release create "v$VERSION" "map/Narodni-divadlo.mcworld#Narodni-divadlo.mcworld (Minecraft Bedrock)" \
  --title "Národní divadlo v Minecraftu $VERSION" \
  --notes "Mapa pro Minecraft Bedrock Edition. Návod k instalaci: https://github.com/${GITHUB_REPOSITORY:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}/blob/main/docs/instalace.md

Změny: viz CHANGELOG.md. Podle 3D modelu *narodni-divadlo-3d* Lukáše Eršila (MIT); data © IPR Praha, © ČÚZK (CC BY 4.0), © přispěvatelé OpenStreetMap (ODbL)."
