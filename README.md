# Národní divadlo v Minecraftu

**Mapa pro Minecraft (Bedrock Edition – tablet, mobil, Windows), ve které si projdete Národní divadlo v Praze zvenku i zevnitř: hlediště s lóžemi, foyer, jeviště s mašinerií, kupoli se zlatou korunou – a kus Prahy kolem, od Střeleckého ostrova po Národní třídu.**

[🇬🇧 English version](README.en.md)

![Národní divadlo v Minecraftu – náhled](docs/images/nahled-divadlo.png)

<p align="center">
  <a href="https://github.com/Ondrula/narodni-divadlo-minecraft/raw/main/map/Narodni-divadlo.mcworld"><b>⬇️ Stáhnout mapu (Narodni-divadlo.mcworld, 2,4 MB)</b></a><br>
  <sub>verze 0.1.0 · Minecraft Bedrock Edition 1.21.90 a novější · <a href="docs/instalace.md">podrobný návod k instalaci</a></sub>
</p>

---

## Jak mapu spustit (30 sekund)

1. Stáhněte soubor **Narodni-divadlo.mcworld** tlačítkem výše.
2. Soubor otevřete – na iPadu/iPhonu v aplikaci *Soubory*, na Androidu ve *Stažených souborech*, na Windows dvojklikem. Minecraft se sám spustí a mapu naimportuje.
3. V Minecraftu najdete svět **Národní divadlo** v seznamu světů. Spustíte ho a stojíte na Národní třídě přímo před divadlem.

Nefunguje? Podrobný návod pro každé zařízení, včetně toho, co dělat, když se mapa neobjeví, je v [docs/instalace.md](docs/instalace.md). Mapa je **jen pro Bedrock Edition** (verze pro tablety, telefony, Windows 10/11 a konzole). Java Edition pro PC ji neotevře – viz [plán](ROADMAP.md).

## Co v mapě najdete

![Podélný řez divadlem – hlediště, lóže, galerie, kupole](docs/images/nahled-rez.png)

- **Celé Národní divadlo v měřítku 2 bloky = 1 metr**, podle historických plánů z roku 1883. Fasády z pískovce, kupole z břidlice se zlatou korunou a špicemi, trigy na pylonech, sochy v nikách.
- **Interiér:** podkovovité hlediště s červenými sedadly, lóžemi a galeriemi, lustr (svítí), foyer s mramorovým schodištěm, jeviště s propadly a tahy, suterény až k základům.
- **Okolí v kruhu asi 330 metrů:** Vltava, Masarykovo a Smetanovo nábřeží se stromořadím, most Legií, Střelecký a Slovanský ostrov se Žofínem, Nová scéna a přes dvě stě okolních domů (jako hmoty s červenými střechami – bez oken, to je práce pro vás).
- Svět je v **kreativním režimu**, bez nepřátel, stále den. Děti ho můžou rovnou přestavovat.

Užitečné příkazy, souřadnice zajímavých míst, legenda bloků a známé nedostatky: [docs/co-je-v-mape.md](docs/co-je-v-mape.md).

![Okolí divadla – Vltava, most Legií, Střelecký ostrov](docs/images/nahled-okoli.png)

## Jak to vzniklo

Ukazoval jsem dceři [interaktivní 3D model Národního divadla](https://github.com/lukasersil/narodni-divadlo-3d), který vytvořil **Lukáš Eršil** – stavbu divadla po fázích od roku 1868, rentgenový pohled do mašinerie, požár v roce 1881. Koukali jsme na to spolu a napadlo nás: v takovém divadle bychom si chtěli zahrát v Minecraftu. Projít se po jevišti, vylézt na kupoli, sedět v královské lóži.

Lukášův model je otevřený (MIT) a postavený přesně podle dobových plánů, takže šel převést na bloky: jeho model jsme „nakrájeli" na kostky 50 × 50 cm a každé kostce přiřadili blok podle materiálu – pískovec, zlato, červené sametové sedadlo. Terén, řeka a okolní domy pocházejí z otevřených dat pražského IPR. Celý postup je popsaný srozumitelně v [docs/jak-to-vzniklo.md](docs/jak-to-vzniklo.md) a technicky v [pipeline/README.md](pipeline/README.md); mapu si z něj kdokoli může znovu vygenerovat.

Tento projekt by bez Lukášovy práce nevznikl. Je to jeho divadlo, my jsme ho jen přestavěli z kostek.

## Poděkování a zdroje

- **Lukáš Eršil – [narodni-divadlo-3d](https://github.com/lukasersil/narodni-divadlo-3d)** (MIT). Geometrie celé budovy včetně interiéru, jevištní mašinerie a soch, rekonstruovaná podle plánů Josefa Zítka a Josefa Schulze a výkresů J. Fialky z roku 1883. Mapa je odvozené dílo z tohoto modelu.
- **IPR Praha** – digitální model terénu a model budov (CC BY 4.0): terén, nábřeží a okolní domy.
- **ČÚZK, RÚIAN** (CC BY 4.0) – půdorys divadla.
- **OpenStreetMap** (ODbL) – řeka, ulice, most Legií.

Úplný seznam zdrojů, licencí a přesné znění citací: [docs/zdroje-a-licence.md](docs/zdroje-a-licence.md).

## Kam to půjde dál

Nejbližší cíl je dotáhnout interiér (schody místo bloků, jemnější sedadla, okna) a vydat mapu i pro Java Edition. Větší věc na obzoru: **mapa části Prahy** – Staré Město, Malá Strana, Hrad – vygenerovaná ze stejných otevřených dat IPR, do které tohle divadlo zapadne jako detailní vložka. Všechno v [ROADMAP.md](ROADMAP.md).

## Chcete pomoct?

Nejvíc pomůže, když mapu otevřete na svém zařízení a napíšete, jestli funguje – zatím je ověřená na tabletu, ne na každé platformě. Chyby v mapě (díra ve zdi, místo, kam se propadnete) hlaste jako [issue](../../issues) se screenshotem a souřadnicemi. Jak na to a jak přispět i jinak: [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

Repozitář má dvě licence. Kód generátoru (`pipeline/`, `scripts/`) je pod licencí [MIT](LICENSE) – to je licence, kterou GitHub zobrazuje v záhlaví. Samotná mapa (`map/*.mcworld`) a náhledy jsou pod [CC BY 4.0](LICENSE-MAP.md) – můžete ji volně šířit, upravovat i stavět dál, jen uveďte autory: Lukáše Eršila za 3D model, IPR Praha a ČÚZK za data, OpenStreetMap a tento projekt. Podrobnosti v [docs/zdroje-a-licence.md](docs/zdroje-a-licence.md).

*Není to oficiální projekt Národního divadla ani Mojang/Microsoft. Minecraft je ochranná známka Mojang AB.*
