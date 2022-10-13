---
title: Pro přednášející
description: Máš přednášet v klubu junior.guru? Tady najdeš všechno co potřebuješ
template: main.html
---

{% from 'macros.html' import note, figure, lead with context %}

# Pro přednášející

{% call lead() %}
  Plánuje s tebou Honza [přednášku](/events/) pro členy [klubu](club.md)? Na této stránce najdeš veškeré info. Je fakt supr, že chceš s juniory sdílet svá moudra a zkušenosti. Na přednášku se moc těšíme!
{% endcall %}

## {{ 'person-circle'|icon }} Detaily o přednášce

Aby šlo přednášku oznámit v klubu, v [seznamu na webu](/events/) a na sociálních sítích, potřebuje od tebe Honza pár základních informací. Je nutné je mít **nejpozději týden před datem konání**.

- Název přednášky
- Krátký popis přednášky
- Krátké bio, pár vět o tobě
- Tvoje firma a pozice v ní
- Odkazy na tvoje profily (LinkedIn, GitHub, Twitter…) nebo webovky
- Tvá fotka nebo avatar (ideálně aspoň 500⨯500px)
- Logo tvé firmy (ideálně SVG)

Pokud jde o texty, Honza ti rád pomůže s jejich formulací. Inspirovat se můžeš v [seznamu přednášek, které už proběhly](/events/). Jestli umíš s GitHubem a nebojíš se upravovat YAML soubor, můžeš kouknout i na [events.yml](https://github.com/honzajavorek/junior.guru/blob/main/juniorguru/data/events.yml) nebo přímo poslat i Pull Request, ale nemusíš.

## {{ 'chat-dots'|icon }} Přednášení

Týden před přednáškou ji začne Honza propagovat na sociálních sítích a v klubu. Den před přednáškou a přímo v den přednášky se potom upozornění v klubu stupňují.

Na Discordu se s Honzou sejdeš **půl hodiny předem** a vyzkoušíte spolu, zda správně funguje technika. Následně Honza rozehřívá místnost a čeká, až se připojí lidé. Zhruba pět minut po začátku zapne nahrávání, uvede tě a dá ti slovo.

Lidé mohou pokládat dotazy do chatu v kanálu #klubovna-přednášky, což Honza sleduje a na konci přednášky je čte, případně moderuje diskuzi. Pokud máš k přednášce nějaké odkazy, je dobré je dát do chatu v #klubovna-přednášky. Po přednášce Honza hodí nahrávku na YouTube a odkaz dá do kanálu #oznámení.

### Nainstaluj si aplikaci

Nainstaluj si prosím Discord jako aplikaci. Pro základní používání sice funguje i v prohlížeči, ale přednášení se sdílením obrazovky je náchylné k různým problémům, především pokud máš Linux. S aplikací problémy nebývají.

### Vypni si zvuky

Vypni zvuky v **User Settings**, stránka **Notifications**, sekce **Sounds**. Většina jich souvisí s hovory, takže je potřeba povypínat skoro vše.

Ve výchozím nastavení totiž Discord dělá zvuk při každé aktivitě v hlasovém kanálu, např. při připojení nového účastníka, odpojení, vypnutí zvuku, zapnutí, apod., což by tě rušilo.

### Discord a YouTube

Honza každou akci v klubu nahrává a publikuje na YouTube kanálu [Junior Guru](https://www.youtube.com/channel/UCp-dlEJLFPaNExzYX079gCA). Záznamy jsou pouze pro členy, na neveřejných odkazech. Výjimečně se dá domluvit, že bude video na YouTube veřejně.

Honza nepořizuje záznam, ale dělá neveřejný živý přenos přímo na YouTube. Discord má totiž technické omezení, které limituje videohovor na 25 lidí, pokud si kdokoliv z účastníků zapne kameru. Pokud by se chtělo na akci připojit více jak 25 lidí, pošle Honza do chatu v kanálu #klubovna-přednášky odkaz na tento živý přenos.

## {{ 'info-circle'|icon }} Další info

### Jak Honza vybírá přednášející?

Buď si někoho sám vytipuje, nebo tip od někoho dostane, nebo se přednášející sám přihlásí.

### Kde se přednáší?

[Klub](club.md) je virtuální prostor na platformě [Discord](https://discord.com/). Discord je **něco jako Slack**, skupinový chat, ale kromě textového chatu jsou v něm i kanály (místnosti), kde si mohou lidé na jeden klik i volat, včetně videa nebo sdílení obrazovky. Přesně tímto způsobem probíhají i večerní přednášky.

Budeš tedy pro účely přednášení potřebovat **účet na Discordu**. Ideálně si nainstaluj i **Discord aplikaci**, funguje to s ní lépe.

### Kdo má do klubu přístup?

Honza tě v předstihu do klubu pozve, ať se můžeš rozkoukávat. Klub je placený, ale **přednášející mají roční vstup zdarma** jako poděkování.

Kdokoliv může klub **zdarma vyzkoušet na dva týdny**. Pokud se tedy přidá těsně před přednáškou, může na ni jít, ačkoliv si klub neplatí. Má tedy smysl na přednášku zvát i veřejnost mimo klub.

### Bude se přednáška nahrávat?

Honza **dělá záznam z každé přednášky** a ten poté okamžitě nahrává na YouTube jako _unlisted_, tedy neveřejné video. Odkaz na toto video mají členové klubu k dispozici a mohou jej sdílet i dalším lidem mimo klub, pokud chtějí.

### Kolik přijde lidí?

Návštěvnost je různá a lze těžko předvídat. **Někdy se živě připojí 20 lidí, někdy jen 5.** Neříká to nic o popularitě přednášky. Mnoho členů počítá s tím, že si pustí záznam, protože v době živého vysílání nemají čas. **Záznamy mívají 50 až 100 zhlédnutí.**

### Kdo je v publiku?

Publikum jsou **především junioři**, začátečníci v programování. Občas studenti, častěji ale **lidé všeho věku a z různých koutů republiky, kteří se rekvalifikují do IT**. Členy klubu jsou i senioři a na přednášky mohou přijít. Projdi si na Discordu kanál #ahoj pro lepší obrázek.

Cílem je podat úvod do problematiky a přiblížit ji začátečníkům. Používej slova, kterým porozumí téměř laik. Zkratky vysvětluj.

### Mám si připravit slajdy?

Pokud chceš, můžeš. Povinnost to není. Např. pokud spolu plánujeme Q&A, tak to ani nedává smysl. Formát slajdů je na tobě, **ukázat můžeš cokoliv ze své obrazovky**.

### Mohu promovat svoji firmu?

Určitě! Pokud máte otevřené pozice pro juniory, nebo děláte něco, co by mohlo juniory zajímat, je to vyloženě žádoucí. I bez toho je ale vhodné říct něco o sobě, o svých úspěších, o firmě pro kterou dělám a co ta firma dělá.

### Kdy to bývá?

Přednášky jsou zpravidla v **úterky v 18:00**, ale pokud by ti to vyhovovalo jinak, není problém se domluvit. Mezi přednáškami bývá dvoutýdenní mezera.

### Kolik mám času?

Jsi **jediná hvězda večera**. Je na tobě, jestli ti dává smysl mluvit 20, 30, nebo 40 minut. V ideálním případě by ale přednáška neměla s následnými dotazy překročit hodinu času.

### Co je Q&A, dříve AMA?

Q&A znamená _questions and answers_. Pozveme si odborníka na určité téma a lidé z klubu mohou pokládat libovolné dotazy. Většinou je pokládají v předstihu a písemně do chatu v kanálu #klubovna-přednášky, takže se na ně lze i připravit. Mohou ale přibývat i v průběhu.

Když akce začne, Honza pomáhá číst dotazy a ty odpovídáš, jak nejlépe umíš. Je úplně v pohodě říct, že nevíš. To je celé, nevyžaduje to žádnou speciální přípravu.

Dříve jsme tomu říkali AMA, což znamená _ask me anything_, ale tuto zkratku moc lidí nezná, tak teď používáme Q&A.
