---
title: Návod na akce v klubu
description: Honza Javorek si píše tuhle dokumentaci, aby věděl, jak má připravovat akce ve svém klubu.
template: main.html
noindex: true
---

{% from 'macros.html' import note, figure, lead with context %}

# Návod na akce v klubu

{% call lead() %}
  Tuhle dokumentaci si píše [Honza Javorek](#honza), aby věděl, jak má připravovat akce v [klubu](club.md). Je to především seznam úkolů podle toho, jak mají jít za sebou.
{% endcall %}

## Hledání přednášejících

- Najdu speakera, domluvím téma, datum.
- Pošlu přístup do klubu na rok zdarma.
- Pošlu [informace pro speakery](speaker.md) a zodpovím případné dotazy.
- Přidám akci do `events.yml`.

## Týden před akcí

- Mám všechny informace v `events.yml` doladěné.
- Vygenerovaný plakátek dám na sociální sítě.

## Příprava v den akce

- Nabiju si sluchátka a mobil.
- Zajistím, aby počítač byl v době přednášky zásuvce.
- Zajistím, abych měl po ruce mobil.
- Zajistím místnost, kde je co nejméně holých stěn apod. Zkontroluji, co bude za mnou.
- Zkontroluji, jestli od hrudníku nahoru nevypadám jako bezdomovec a případně to napravím. Od hrudníku dolů je to jedno.

## Večer

- Otevřu si **Audio MIDI Setup**. Pokud se nezobrazí [BlackHole](https://github.com/ExistentialAudio/BlackHole), restartuji počítač.
- Nasadím si sluchátka.
- Ověřím, že sluchátka fungují změnou hlasitosti na macOS, musí to ťukat ve sluchátkách.
- V **Discordu** ve _Voice & Video_
    - nastavím BlackHole jako výstup,
    - vypnu _Echo cancellation_,
    - nechám mikrofon na ten sluchátkový,
    - mám _Input mode_ na _Voice Activity_,
    - mám _Blur_ na videu
    - a neřeším _Automatic Gain control_, _Input sensitivity_, _Noise suppression_ a doufám, že se to nerozhodí, protože nevím, jestli to co tam je, jsem nastavil já, nebo to jsou výchozí hodnoty. Také nevím, jestli jsou současné hodnoty lepší nebo horší, ale snad jsou OK, protože si nikdo nestěžuje.
- V **Discordu** si nastavím **DND** kvůli notifikacím.
- Mám aspoň trochu připravený úvod přednášky, představení speakera.

## Akce

- Otevřu **OBS**.
- V **OBS** jdu do _Manage Broadcast_. Z `events.yml` kopíruju informace do políček. Nezapomenu dát před _title_ jméno speakera.
- Dám _Schedule and Select Broadcast_. OBS vytvoří live akci na YouTube.
- Jdu [na YouTube](https://studio.youtube.com/channel/UCp-dlEJLFPaNExzYX079gCA/videos/live) a ověřím, jestli tam akce je. Odkaz mám po ruce.
- 15 minut před akcí se připojím a „rozehřívám“ místnost, pomáhám speakerovi.
- **Otevřu si hovor do okna** a ověřím, že to OBS správně chytá.
- V čas startu přednášky **odpálím Discord event** a ještě chvíli počkám.
- Neudělám chybu a **v OBS zmáčknu Start Streaming**.
- Představím speakera a uvedu přednášku.
- Pokud sdílí obrazovku, kliknu na _Watch Stream_.
- Kontroluji hlasitost lidí, popřípadě ladím šoupátka v OBS.
- V mobilu během akce kontroluji textový chat a další zprávy.
- Pokud potřebuji vypnout sebe, vypnu se jak na Discordu, tak i v OBS.

### Pokud přednáším já

- Vyzkouším si to v den přednášky!
- Mám po ruce odkaz na **YouTube** stream.
- Než začnu, zkontroluju si v **OBS** hlasitost lidí.
- Během přednášení, pokud chci něco ukázat, tak se pak přepínám mezi okny klávesovou zkratkou.
- Během přednášení, pokud chci něco ukázat, zásadně sdílím jen jedno okno a ne celou obrazovku.
- Během přednášení nebýt nikdy na _fullscreen_.

## Po akci

- Poděkuji, pořeším dotazy.
- Vypnu streamování.
- Rozloučím se.
- Zaznamenám odkazy, slajdy (přijdou do popisku na YouTube, v events.yml na to zatím není místo).
- V **Discordu** ve _Voice & Video_
    - můžu odnastavit BlackHole jako výstup,
    - můžu zapnout _Echo cancellation_.
- Odkaz na video hodím do #oznámení, pošlu speakerovi.
- Do `events.yml` přidám odkaz na příspěvek v #oznámení jako odkaz na záznam.
