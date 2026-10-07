# Změny

Formát podle [Keep a Changelog](https://keepachangelog.com/cs/1.1.0/), verze podle [SemVer](https://semver.org/lang/cs/).

## [0.1.0] – 2026-10-07

První veřejná verze.

### Mapa
- Národní divadlo v měřítku 2 bloky = 1 m: fasády, kupole se zlatou korunou, sochy, hlediště s lóžemi a galeriemi, foyer, jeviště s mašinerií, suterény.
- Okolí v kruhu ~330 m: Vltava, obě nábřeží, most Legií, Střelecký a Slovanský ostrov, Nová scéna, ~200 domů z dat IPR.
- Kreativní režim, mír, zastavený den, spawn na Národní před průčelím. Bedrock Edition 1.21.90+.

### Generátor
- Headless export geometrie z modelu *narodni-divadlo-3d* (commit `2d9e2cd`), voxelizace povrchů, zápis světa přes Amulet, náhledy.

### Známé nedostatky
- Plné bloky bez schodů a půlbloků, hrubá sedadla a zábradlí, vynechané okenní příčky a tramvaje, okolní domy bez oken, mostovka mostu Legií zčásti travnatá. Viz `docs/co-je-v-mape.md`.
- Ověřeno na tabletu (Bedrock Edition). Hlášení z dalších zařízení vítána.
