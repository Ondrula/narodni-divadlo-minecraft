# Zdroje, licence a jak citovat

Mapa je odvozené dílo. Všechno, z čeho vznikla, má otevřenou licenci, a každá z nich vyžaduje uvedení autora. Tady je to pohromadě – pokud mapu šíříte, upravujete nebo z ní něco stavíte, převezměte prosím tento seznam.

## 1. 3D model Národního divadla – Lukáš Ersil

- **Dílo:** *narodni-divadlo-3d* – interaktivní 3D model Národního divadla v Praze (Three.js, WebGPU): stavba 1868–1883, rentgen, řez, noc, požár 1881
- **Autor:** Lukáš Ersil
- **Odkaz:** https://github.com/lukasersil/narodni-divadlo-3d
- **Licence:** MIT (kód a geometrie modelu)
- **Použitá verze:** commit `2d9e2cd55d9231777eebb3253de8d3e47344b85f` (5. 10. 2026)
- **Co jsme použili:** kompletní geometrii dokončené budovy (fáze 7 jeho časové osy) – vnější plášť, fasády, kupoli, sochy, interiér hlediště, foyer, jevištní mašinerii, vnitřní příčky vektorizované z půdorysů 1883 – a jeho předzpracovaná data okolí (terén, budovy, řeka, ulice), která sám odvodil ze zdrojů níže.
- **Co jsme nepoužili:** textury (fotografie z Wikimedia Commons pod CC BY-SA), historické ilustrace a dobové plány v `assets/`. Mapa tedy nenese žádný obsah pod CC BY-SA.

Doporučená citace:

> Ersil, Lukáš. *narodni-divadlo-3d: Interaktivní 3D model Národního divadla v Praze.* GitHub, 2026. https://github.com/lukasersil/narodni-divadlo-3d. Licence MIT.

Lukáš svůj model postavil podle plánů Josefa Zítka a Josefa Schulze, výkresů J. Fialky (1883) a krovu (1876), které jsou volným dílem, a podle dat uvedených níže. Tento projekt vznikl jako jeho inspirace a bez něj by neexistoval.

## 2. IPR Praha – 3D data Prahy

- **Vydavatel:** Institut plánování a rozvoje hlavního města Prahy (IPR Praha)
- **Datové sady:** Digitální model povrchu a terénu (1m rastr), Model budov a mostů (Budovy 3D)
- **Odkaz:** https://geoportalpraha.cz/data-a-sluzby/clanky-a-projekty/3D-model
- **Licence:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.cs)
- **Co jsme použili:** terén a výšky okolí (nábřeží, ostrovy, dno řeky), hmoty okolních budov včetně tvarů střech, výšku kupole a střech divadla. V podobě, kterou z nich odvodil L. Ersil (`src/data/site.js` jeho repozitáře).

Uvedení zdroje: *© IPR Praha, CC BY 4.0*

## 3. ČÚZK – RÚIAN

- **Vydavatel:** Český úřad zeměměřický a katastrální
- **Datová sada:** Registr územní identifikace, adres a nemovitostí (RÚIAN) – stavební objekt č. p. 223, Praha 1
- **Licence:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.cs)
- **Co jsme použili:** půdorys divadla, na který je model registrován.

Uvedení zdroje: *© ČÚZK, RÚIAN, CC BY 4.0*

## 4. OpenStreetMap

- **Autoři:** přispěvatelé OpenStreetMap
- **Licence:** [ODbL 1.0](https://www.openstreetmap.org/copyright)
- **Co jsme použili:** linii Vltavy a ostrovů, ulice a jejich šířky, most Legií, části budovy divadla (OSM building parts).

Uvedení zdroje: *© přispěvatelé OpenStreetMap, ODbL*

## 5. Nástroje

- [Three.js](https://threejs.org/) 0.186 (MIT) – běh modelu při exportu
- [Playwright](https://playwright.dev/) (Apache 2.0) – neviditelný prohlížeč
- [NumPy](https://numpy.org/), [SciPy](https://scipy.org/) (BSD) – voxelizace
- [Amulet Core](https://github.com/Amulet-Team/Amulet-Core) (MIT, PyMCTranslate) – zápis světa Bedrock

## Licence tohoto projektu

- **Kód** ve složce `pipeline/` a skripty: [MIT](../LICENSE), © 2026 Ondřej Skřehota.
- **Mapa** (`map/*.mcworld`), náhledy a dokumentace: [CC BY 4.0](../LICENSE-MAP.md), © 2026 Ondřej Skřehota – odvozeno z díla Lukáše Ersila a dat IPR Praha, ČÚZK a OpenStreetMap.

## Jak citovat tento projekt

Pokud mapu použijete, šíříte ji dál nebo z ní stavíte, uveďte prosím:

> *Národní divadlo v Minecraftu* (Ondřej Skřehota, 2026, CC BY 4.0, https://github.com/Ondrula/narodni-divadlo-minecraft), podle 3D modelu *narodni-divadlo-3d* Lukáše Ersila (MIT); data © IPR Praha a © ČÚZK (CC BY 4.0), © přispěvatelé OpenStreetMap (ODbL).

Strojově čitelná citace je v souboru [CITATION.cff](../CITATION.cff).

## Ochranné známky

Minecraft je ochranná známka Mojang AB / Microsoft. Tento projekt není s Mojangem, Microsoftem ani s Národním divadlem nijak spojen a není jimi schválen. Název a podoba Národního divadla jsou kulturní dědictví; projekt je nekomerční a vzdělávací.
