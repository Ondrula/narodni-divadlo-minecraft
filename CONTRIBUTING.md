# Jak přispět

Nemusíte být programátor. Většina práce, která mapě chybí, se dělá v Minecraftu nebo prostě tím, že ji vyzkoušíte.

## 1. Vyzkoušejte mapu a napište, jak dopadla

Nejcennější příspěvek právě teď. Mapa je generovaná a ověřená nástroji, ne každou verzí hry. Založte [issue](../../issues/new?template=hlaseni.md) (nebo napište do [diskuzí](../../discussions)) s tím:

- jaké zařízení a verzi Minecraftu máte (*Nastavení → Profil*, úplně dole),
- jestli se import povedl,
- co vás potkalo – i „funguje, jen se to seká na starém iPadu" je užitečná informace.

## 2. Hlaste chyby v mapě

Díra ve zdi, propadnete se podlahou, sedadla v lóži visí ve vzduchu, kde by neměla být. Do issue dejte:

- **screenshot**,
- **souřadnice** (zapněte *Nastavení → Hra → Zobrazit souřadnice*),
- jednu větu, co je špatně a jak by to mělo být (pokud víte – třeba z Lukášova [modelu](https://github.com/lukasersil/narodni-divadlo-3d), kde se dá podívat na totéž místo).

Chyby, které vyplývají z principu převodu (všechno jsou plné bloky, sedadla jsou hrubá), jsou sepsané v [docs/co-je-v-mape.md](docs/co-je-v-mape.md) – ty hlásit nemusíte, pracujeme na nich v [plánu](ROADMAP.md).

## 3. Stavte

Ručně postavené části (foyer se schody, lóže, Nová scéna s okny, Žofín, později Hrad a Karlův most) jsou přesně to, co automatika neumí. Pokud něco postavíte:

1. Stavte přímo v této mapě, ať sedí souřadnice a měřítko (2 bloky = 1 m v divadle).
2. Vyexportujte stavbu jako **strukturu**: v chatu `/give @s structure_block`, položte ho, nastavte rozsah, *Export* – vznikne soubor `.mcstructure`. Nebo pošlete celý `.mcworld` (*Nastavení světa → Exportovat svět*).
3. Založte issue nebo pull request se souborem, screenshotem a souřadnicemi, kam patří.

Dohoda o stylu: držíme se [legendy bloků](docs/co-je-v-mape.md#legenda-bloků), aby mapa vypadala jednotně, a nepoužíváme mody ani placené doplňky.

## 4. Vylepšujte generátor

Pokud umíte Python nebo JavaScript, generátor je ve složce [`pipeline/`](pipeline/README.md) a je napsaný tak, aby se dal číst. Dobré první úkoly:

- nahradit terasy schodovými bloky tam, kde model má schodiště (`voxelize.py`),
- tenké prvky (zábradlí) rozpoznat a dát jim minimální tloušťku,
- Java Edition export přes Amulet,
- načítání mapových listů IPR pro [mapu Prahy](ROADMAP.md).

Před větší změnou založte issue, ať se nepotkáme na stejné věci. Pull request prosím s krátkým popisem a náhledem (`render.py`).

## 5. Překlady a texty

Dokumentace je česky s anglickým README. Oprava překlepu nebo lepší formulace je vítaná jako pull request přímo v souboru.

---

Pravidla jsou jednoduchá: buďte slušní, uvádějte zdroje (všechno, co do mapy přijde, musí mít licenci slučitelnou s CC BY 4.0 – viz [docs/zdroje-a-licence.md](docs/zdroje-a-licence.md)), a berte to jako to, co to je: hračka postavená s dětmi na ramenou pořádné práce Lukáše Ersila.
