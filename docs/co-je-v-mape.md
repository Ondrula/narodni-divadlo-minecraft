# Co je v mapě a jak se v ní pohybovat

## Měřítko a souřadnice

- **2 bloky = 1 metr.** Hráč je vysoký necelý metr, divadlo je 100 m dlouhé = 200 bloků, kupole sahá do výšky 39 m = 78 bloků nad ulici.
- **Úroveň Národní třídy je y = 64.** Jeden metr nad ulicí = y 66, jeden metr pod = y 62. Suterény jdou do y 45 (základy v hloubce 9,6 m), kupole končí u y 142, špice v y 158.
- **Osa x míří na východ, osa z na jih** – stejně jako v reálu, sever je −z. Bod 0, 0 leží u hlavního průčelí; divadlo se táhne od z ≈ −75 (lodžie u Národní) po z ≈ 120 (jižní křídlo u Divadelní ulice).
- Souřadnice si zapněte v *Nastavení → Hra → Zobrazit souřadnice*. Hodí se při hlášení chyb.

## Kam se podívat

Příkazy vložíte do chatu (ikona bubliny). Svět je kreativní, takže po `/tp` můžete létat (dvakrát rychle poklepat na skok).

| Místo | Příkaz | Co uvidíte |
|---|---|---|
| Před divadlem (spawn) | `/tp @s -6 69 -96` | Hlavní průčelí s lodžií a trigami, Národní třída |
| Foyer | `/tp @s 0 78 -66` | Foyer v patře nad lodžií, schodiště, lustry |
| Hlediště, přízemí | `/tp @s 0 73 -36` | Stojíte mezi sedadly v parteru, nad vámi lóže a galerie, lustr a strop |
| Jeviště | `/tp @s 10 71 20` | Na jevišti; pod vámi propadla, nad vámi tahy a lávky |
| Zadní jeviště | `/tp @s 10 71 44` | Prostor bývalého Prozatímního divadla |
| Kupole shora | `/tp @s 0 150 -40` | Pohled z výšky na kupoli, korunu a špice (poleťte dolů) |
| Most Legií | `/tp @s -300 71 -100` | Most, Střelecký ostrov, panorama nábřeží |
| Střelecký ostrov | `/tp @s -460 59 -40` | Ostrov s pohledem na divadlo přes řeku |

Doporučená cesta pro první návštěvu: spawn → vejít lodžií dovnitř → foyer → hlediště → jeviště → vyletět kupolí ven.

## Legenda bloků

Každý materiál v původním 3D modelu dostal jeden blok. Když v mapě potkáte blok, tohle znamená:

| Blok | Co představuje |
|---|---|
| pískovec (sandstone) | zdivo fasád |
| tesaný pískovec (chiseled sandstone) | bosáž přízemí |
| hladký pískovec (smooth sandstone) | římsy, pilastry, šambrány, štukové ozdoby v interiéru |
| hladký kámen (smooth stone) | sochy – Múzy, trigy na pylonech jsou z oxidované mědi |
| leštěná břidlice (polished deepslate) | krytina kupole |
| oxidovaná měď (oxidized copper) | měděné střechy jižního křídla, bronzové sochy |
| zlato (gold block) | zlatá koruna kupole, špice, zlacení v hledišti |
| křemen (quartz block) | omítky, mramor, příčky vnitřních místností podle půdorysů 1883 |
| červená vlna (red wool) | sametová sedadla, opona, závěsy |
| červená terakota (red terracotta) | stěny lóží, strop hlediště |
| tmavé dubové desky (dark oak planks) | sedadlové rámy, podlaha jeviště, lampy na Národní |
| dubové desky (oak planks) | parkety |
| glowstone | lustry a lampy – svítí |
| železný blok (iron block) | jevištní mašinerie, krovy, propadla |
| sklo | okna |
| bílá terakota + oranžová terakota | okolní domy (stěny + střechy) z dat IPR |
| světle modré sklo | prosklená fasáda Nové scény |
| kamenné cihly (stone bricks) | nábřežní zdi, most Legií |
| šedý beton (gray concrete) | ulice |
| tráva, hlína, kámen | terén z digitálního modelu IPR |

## Co v mapě chybí nebo je špatně (verze 0.1.0)

Buďte na to připravení – je to první automatický převod, ne ručně stavěná mapa:

- **Sedadla a zábradlí jsou hrubá.** Sedadlo v modelu je 50 cm široké, takže z něj je jeden blok; řady sedadel vypadají jako červené schody. Lóžová zábradlí a sloupky místy visí ve vzduchu, protože jim chybí půlblok podpory.
- **Žádné schody ani půlbloky.** Všechno je z plných bloků. Schodiště ve foyer je terasa z křemenových bloků.
- **Okenní příčky a tramvaje jsme vynechali** – jako bloky vypadaly jako tmavé fleky. Okna jsou souvislé plochy skla.
- **Okolní domy jsou prázdné krabice** s tvarovanými střechami podle dat IPR, bez oken a dveří. Dovnitř se nedostanete jinak než prokopáním.
- **Mostovka mostu Legií je zčásti travnatá** – výškový model terénu nad mostem nesedí přesně na mostovku.
- **Mimo kruh ~330 m je plochá louka.** Dál data nesahají.
- Lampy a lustry svítí (glowstone), ale uvnitř budovy je i tak místy šero. Vezměte si pochodeň nebo zapněte *Nastavení → Video → Jas* naplno.
- Mapa je generovaná pro Bedrock 1.21.90 a ověřená na tabletu (Bedrock Edition, říjen 2026). Na jiných zařízeních by měla fungovat stejně – když ne, napište nám, i to je příspěvek.

Našli jste něco dalšího? Založte [issue](../../../issues) se screenshotem a souřadnicemi.
