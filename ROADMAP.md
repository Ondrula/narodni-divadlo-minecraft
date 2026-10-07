# Plán

Co je hotové, co přijde a co by bylo hezké. Pořadí odpovídá tomu, co dává pro hraní největší smysl, ne tomu, co je technicky nejzajímavější. Návrhy a hlasování: [issues](../../issues).

> **Upřímné varování:** tohle je projekt táty a dcery. Napadá nás spousta věcí a může se stát, že se k němu už nevrátíme. Všechno je proto zveřejněné tak, aby se u toho mohli bavit i ostatní bez nás – mapa jde hrát, generátor jde spustit, postup je popsaný. Pokud něco z plánu níže zůstane ležet a chcete to udělat, udělejte to; forky i pull requesty jsou vítané.

## 🎯 Hned teď – prozkoumat divadlo

Projít Národní divadlo celé, od suterénů po kupoli, a zapsat, co ruší: kde se nedá projít, co visí ve vzduchu, co nevypadá jako to, co to má být. Z toho vznikne seznam pro 0.2. Tohle je ta část, kterou děláme kvůli sobě.

## ✅ 0.1 – První mapa (říjen 2026)

- Celé divadlo včetně interiéru v měřítku 2 : 1, okolí v kruhu 330 m, Bedrock Edition.
- Automatický převod z modelu Lukáše Eršila, reprodukovatelný z tohoto repozitáře.

## 🔜 0.2 – Hratelnější interiér

Cíl: aby se dalo divadlem projít jako skutečný návštěvník, bez létání a kopání.

- Dveře a průchody tam, kde jsou v půdorysech 1883 (vstup lodžií, foyer → hlediště, zákulisí). Dnes se dovnitř nejsnáz létá.
- Schodiště ze schodových bloků místo teras (foyer, galerie).
- Lóže: sloupky a zábradlí, které nevisí ve vzduchu – plot nebo zdi místo rozpadlých bloků.
- Sedadla jako schody s červenou vlnou, uličky v parteru průchozí.
- Okna z tabulového skla (panes) místo plného skla; tenké prvky modelu přes práh tloušťky, aby se netrhaly.
- Ověření na reálných zařízeních (iPad, Android, Windows) a seznam verzí, kde to funguje.

## 🔜 0.3 – Java Edition

- Export stejného světa i pro Java Edition (Amulet umí převod, chybí jen otestovat palety bloků).
- Jedno vydání = dva soubory: `.mcworld` a zip se složkou světa pro Javu.

## 🗺️ 1.0 – Kusy Prahy, které známe, z dat IPR

Větší projekt, pro který tento repozitář vzniká: ne „Praha", ale **místa, kde bydlíme a kudy chodíme** – vlastní ulice, cesta do školy, okolí divadla – generovaná ze stejných otevřených dat. Každý si může vygenerovat svůj kousek.

- **Zdroj:** [Model budov a mostů](https://geoportalpraha.cz/data-a-sluzby/clanky-a-projekty/3D-model/3d-model-budovy-mosty) a [digitální model terénu](https://geoportalpraha.cz/data-a-sluzby/clanky-a-projekty/3D-model) IPR Praha – otevřená data CC BY 4.0, pokrývají celé město, střechy modelované do detailu (komíny, věže, vikýře), přesnost 0,5 m. Stahují se po mapových listech (DWG / 3D shapefile / DGN).
- **Výřez:** parametr generátoru – zadáte střed a velikost (třeba 1 × 1 km kolem vaší ulice) a dostanete svět. My začneme okolím divadla a vlastní čtvrtí. Celá Praha (496 km²) nemá smysl: svět by měl desítky gigabajtů.
- **Měřítko:** 1 : 1 pro město, divadlo zůstane jako „detailní vložka" ve 2 : 1 (musí se vyřešit přechod, nejspíš sokl kolem divadla).
- **Co bude automaticky:** terén, řeka, mosty, hmoty všech domů se střechami, ulice z OpenStreetMap. Panorama by mělo sedět na metr.
- **Co bude ručně:** dominanty – Hrad, Týn, Karlův most, Rudolfinum – jako komunitní stavby, viz [CONTRIBUTING.md](CONTRIBUTING.md).
- **Pipeline:** nový krok, který načte mapové listy IPR přímo (bez průchodu Three.js) a voxelizuje je stejným kódem jako divadlo. Nejdřív se musí vyřešit souřadnice (S-JTSK → metry od divadla) a formát (3D shapefile je nejsnazší).
- **Barvy fasád:** z fotorealistického meshe IPR (2023, zatím na vyžádání) by šlo odečíst převládající barvu každého domu a dát mu odpovídající terakotu. Bonus, ne podmínka.

## 💡 Nápady bez termínu

- **Fáze stavby a požár 1881** jako varianty světa nebo přepínatelné struktury: Lukášův model má sedm fází stavby 1868–1883 a epizodu požáru – v mapě by to byly „místnosti času".
- **Rentgen:** verze mapy jen s nosnou konstrukcí, krovem a mašinerií, podle rentgenových vrstev modelu.
- **Naučná stezka:** cedule (sign blocks) s texty z Lukášova modelu (má popisky v češtině i angličtině) na místech, kterých se týkají.
- **Resource pack** s pískovcem v barvě hořického kamene a sametem místo vlny.
- **Marketplace / Realms** – aby se mapa dala sdílet bez souboru.

## Co dělat nebudeme

- Textury a fotografie z Wikimedia Commons (CC BY-SA) – aby mapa mohla zůstat pod CC BY.
- Celou Prahu v jednom světě.
- Cokoli, co vyžaduje mody nebo placené doplňky. Mapa musí jít otevřít na holém Minecraftu z obchodu.
