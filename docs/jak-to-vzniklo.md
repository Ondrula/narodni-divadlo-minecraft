# Jak mapa vznikla

Tahle stránka vysvětluje, jak se z 3D modelu na webu stane svět v Minecraftu, bez programátorského žargonu. Technický popis se vším, co je potřeba k opakování, je v [pipeline/README.md](../pipeline/README.md).

## Výchozí bod: model Lukáše Ersila

Lukáš Ersil vytvořil [interaktivní 3D model Národního divadla](https://github.com/lukasersil/narodni-divadlo-3d), který běží v prohlížeči. Není to „naskenovaná" budova – je to **rekonstrukce podle historických plánů**: půdorysů a řezů Josefa Zítka a J. Fialky z roku 1883, výkresů krovu z roku 1876, dobových fotografií. Rozměry sedí na decimetry: proscénium je 36,6 m od severního průčelí, jeviště je 14 m široké, kupole končí 39 m nad ulicí.

Pro nás je důležité, že model zahrnuje i to, co zvenku nevidíte: hlediště s lóžemi, foyer, jevištní mašinerii (propadla, točnu, tahy), suterény. A že má otevřenou licenci (MIT), takže ho smíme použít a přetvořit.

Model má jednu zvláštnost, která převod zkomplikovala: **neexistuje jako soubor**. Budova se počítá z čísel přímo v prohlížeči – program říká „od této římsy po tuhle vytáhni profil pilastru". Takže první krok byl model spustit v neviditelném prohlížeči, nechat ho postavit dokončené divadlo (fáze 7 z jeho časové osy) a z paměti prohlížeče vyčíst všechny trojúhelníky, ze kterých se skládá. Je jich 1,3 milionu.

## Krok 2: nakrájet na kostky

Minecraft nezná plochy, jen kostky. Zvolili jsme **měřítko 2 bloky na metr** – kostka má 50 cm. Při měřítku 1 : 1 by lóže široká dva metry měla dva bloky a hráč by se jí nevešel; při 3 : 1 by naopak okolí bylo obří a svět by měl stovky megabajtů.

Každý trojúhelník modelu jsme posypali hustou sítí bodů (po 22 cm) a každý bod zapsal kostku, do které spadl. Důležité je, že se takto vyplní jen **povrchy** – stěna je tlustá tak, jak byla v modelu, místnosti zůstávají duté a dá se do nich vejít. Pod budovou se nic nedosypává, takže suterény jsou skutečně pod zemí.

Když se v jedné kostce sejde víc materiálů (třeba zlacení na štuku), vyhrává ten „důležitější": zlato přebije štuk, štuk přebije zdivo. To je jediné ruční rozhodnutí v celém procesu – tabulka, který materiál modelu je jaký blok a kdo koho přebíjí. Je v souboru `pipeline/voxelize.py` a v [legendě bloků](co-je-v-mape.md#legenda-bloků).

## Krok 3: terén, řeka, domy

Okolí nepochází z Lukášova modelu přímo, ale z toho, co i on použil: **otevřená data pražského Institutu plánování a rozvoje (IPR)**. Výškový model terénu v metrové mřížce dal tvar nábřeží a ostrovů, model budov dal hmoty okolních domů i s tvary střech, OpenStreetMap dala řeku, ulice a most Legií. Lukáš tato data upravil do podoby, kterou jeho model umí zobrazit; my jsme ji převzali.

Terén je v Minecraftu plný: pod povrchem je hlína a kámen až k podloží, Vltava má vodu a písčité dno, na ulicích je beton. Kolem divadla je v terénu vybraná jáma pro suterény a zasypaná jen po úroveň základů.

## Krok 4: zapsat svět

Minecraft Bedrock ukládá svět do databáze po „chuncích" 16 × 16 bloků. Pomocí knihovny [Amulet](https://www.amuletmc.com/) (nástroj, kterým komunita Minecraftu světy upravuje) jsme vytvořili prázdný svět a vložili do něj 13 456 chunků. Nastavili jsme kreativní režim, mír, zastavený den a spawn na Národní třídě. Mimo kruh, kam sahají data, generátor pokračuje plochou loukou ve stejné výšce.

Výsledek je soubor `.mcworld`, což je obyčejný zip se světem, který Minecraft umí naimportovat.

## Co zbývá udělat ručně

Automatika zvládne hmotu a materiály, ale ne detail: sedadlo z jednoho bloku nevypadá jako sedadlo, zábradlí z kostek visí ve vzduchu, schodiště je terasa. To je přesně ta část, která se dá dělat v Minecraftu rukama – a je to ta zábavná. Stavíte-li něco, co by stálo za zařazení do mapy, dejte vědět ([CONTRIBUTING.md](../CONTRIBUTING.md)).

## Čísla

| | |
|---|---|
| trojúhelníků v modelu | 1 286 837 (705 objektů) |
| bloků divadla (včetně vnitřních příček a mašinerie) | asi 740 000 |
| bloků celkem bez výplně terénu (z toho 2,1 milionu vody) | asi 5 milionů |
| chunků | 13 456 |
| velikost `.mcworld` | 2,4 MB |
| doba generování | 5 minut na běžném notebooku |
