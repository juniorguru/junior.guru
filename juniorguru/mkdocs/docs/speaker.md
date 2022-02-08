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

Pokud jde o texty, rád ti pomůže s jejich formulací. Inspirovat se můžeš v [seznamu přednášek, které už proběhly](/events/). Jestli umíš s GitHubem a nebojíš se upravovat YAML soubor, můžeš kouknout i na [events.yml](https://github.com/honzajavorek/junior.guru/blob/main/juniorguru/data/events.yml) nebo přímo poslat i Pull Request, ale nemusíš.

## {{ 'chat-dots'|icon }} Přednášení

V den přednášky se na Discordu sejdeš s Honzou **půl hodiny předem** a vyzkoušíte spolu, zda správně funguje technika.

### Nainstaluj si aplikaci

Nainstaluj si prosím Discord jako aplikaci. Pro základní používání sice funguje i v prohlížeči, ale přednášení se sdílením obrazovky je náchylné k různým problémům, především pokud máš Linux. S aplikací problémy nebývají.

### Vypni si zvuky

Vypni zvuky v **User Settings**, stránka **Notifications**, sekce **Sounds**. Většina jich souvisí s hovory, takže je potřeba povypínat skoro vše.

Ve výchozím nastavení totiž Discord dělá zvuk při každé aktivitě v hlasovém kanálu, např. při připojení nového účastníka, odpojení, vypnutí zvuku, zapnutí, apod., což by tě rušilo.

### Videohovor na Discordu

Discord má technické omezení, které **limituje videohovor na 25 lidí, pokud si kdokoliv z účastníků zapne kameru**. Toto omezení neplatí, když se pouze sdílí obrazovka.

Všichni v publiku mají zakázáno video používat. Ty sice budeš mít tlačítko na sdílení kamery funkční, ale **prosím, neklikej na něj**. Způsobilo by to omezení hovoru na 25 lidí až do jeho konce (i pokud kameru hned zase vypneš).

{{ figure('discord-controls.png', 'Ovládání videohovoru') }}

Jako přednášející máš funkční i tlačítko _Share Your Screen_. Pomocí něj můžeš nasdílet cokoliv ze svého počítače, např. slajdy.

**Díky triku se „zrcadlem“ tě publikum uvidí i přesto, že nesmíš zapnout kameru.** Tlačítkem níže otevři zrcadlo. Když lidem nasdílíš svůj prohlížeč, půjdeš vidět jako na kameře, ale bez limitu na počet účastníků.

Pokud máš slajdy, počítá se s tím, že zrcadlo využiješ hlavně na začátku a na konci přednášky. Ovládáš si to dle libosti. Buďto sdílíš slajdy, nebo se přepneš na stránku se zrcadlem a půjde vidět hlava.

<div class="mirror">
  <noscript>
    {%- call note(standout=True) -%}
      {{ 'exclamation-circle'|icon }} Kameru se nedaří spustit. Buď nemáš kameru povolenou pro tento prohlížeč, nebo to nepodporuje, nebo se něco pokazilo. Zkontroluj prosím nastavení, nebo zkus jiný prohlížeč.
    {%- endcall -%}
  </noscript>
  <div class="standout text-center">
    <button type="button" class="mirror-run">Spustit zrcadlo</button>
    <button type="button" class="mirror-expand">Roztáhnout zrcadlo</button>
  </div>
</div>

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

Honza **dělá záznam z každé přednášky** a ten poté okamžitě nahrává na YouTube jako _unlisted_, tedy neveřejné video.

Odkaz na toto video mají členové klubu k dispozici a mohou jej sdílet i dalším lidem mimo klub, pokud chtějí.

### Kolik přijde lidí?

Návštěvnost je různá a lze těžko předvídat. Aktuálně se na přednášky připojuje **přes 20 lidí živě**. Mnoho členů ale počítá s tím, že si pustí záznam, protože v době živého vysílání němají čas. **Záznamy mívají 50 až 100 zhlédnutí.**

### Kdo je v publiku?

Publikum jsou především junioři, začátečníci v programování, studenti, lidé všeho věku rekvalifikující se do IT. Členy klubu jsou ale i senioři nebo mentoři a mohou přijít také, pokud je bude téma zajímat. Jestli si chceš udělat konkrétnější obrázek, projdi si místnost #ahoj.

### Mám si připravit slajdy?

### Kdy to bývá a kolik mám času?

Přednášky jsou zpravidla v úterky v 18:00, ale pokud by ti to vyhovovalo jinak, není problém se domluvit.

Jsi jediná hvězda večera. Na přednášku není časový limit, ale předpoklad je, že se běžně vejde i s následnými dotazy do hodiny času. Je na tobě, jestli ti dává smysl mluvit 20, 30, nebo 40 minut.

### Jak přednáška probíhá?
