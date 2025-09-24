---
title: Google vám dá odpovědi, někdy ale potřebujete spíš dobrou otázku, říká rekvalifikovaný Pythonista Dvořák
date: 2023-10-12
interviewee: Roman Viktor Dvořák
interviewee_avatar_path: avatars-participants/roman-viktor-dvorak.jpg
author: Adéla Pavlun
author_avatar_path: avatars-participants/adela-pavlun.jpg
author_url: https://www.linkedin.com/in/adelapavlun/
thumbnail_subheading: Roman Viktor Dvořák
thumbnail_image_path: avatars-participants/roman-viktor-dvorak.jpg
thumbnail_button_heading: Čti na
thumbnail_button_link: junior.guru/stories
template: main_stories.html
---

{% from 'macros.html' import img, lead with context %}

# {{ page.meta.title }}

<ul class="article-details">
  <li class="article-details-item">
    <a class="article-details-author" href="{{ page.meta.author_url }}" target="_blank" rel="noopener">
      {{ img('static/' + page.meta.author_avatar_path, page.meta.author + ', profilovka', 50, 50, lazy=False, class='article-details-avatar') }}
      <strong>{{ page.meta.author }}</strong>
    </a>
  </li>
  <li class="article-details-item">{{ '{:%-d.%-m.%Y}'.format(page.meta.date) }}</li>
</ul>

<div class="article-lead">
{{ img('static/' + page.meta.interviewee_avatar_path, page.title + ', foto', 100, 100, lazy=False, class='article-image') }}
{% call lead() %}
Nebyl prominentem v matematice, ani nemá vysokou školu. Právě to sedmatřicetiletého Romana Viktora Dvořáka drželo zpět od IT oboru, kterým se dnes úspěšně živí. Pro rekvalifikaci z elektrikáře na programátora se rozhodl až v momentě, kdy vyhlásil osobní bankrot. Za pět let samostudia IT posbíral Roman nespočet střípků do své mozaiky. Ten poslední zacvakl díky Junior Guru a dnes se Roman živí jako Python vývojář.
{% endcall %}
</div>

**Tento rozhovor bude hodně o profesních věcech, tak pojďme začít něčím jiným. Kdo je Roman, když zrovna nepracuje?**

Pracovní a nepracovní život se nesnažím oddělovat, ale spíš sjednotit. Nechci žít dvojí život. Programování má pro mě hluboký osobní, symbolický význam. Vedle toho tím nicméně vydělávám peníze, což je stejně důležité. Definovat bych se mohl třeba jako šachová figurka v procesu sebepoznání.

**Na jaké pozici teď pracuješ?**

Živím se především jako externí Tech Lead pro [Keyguru](https://keyguru.cz/). S touto firmou jsem začal spolupracovat na jaře 2022, do té doby jsem pracoval mimo IT. Moje první úkoly se týkaly úpravy frontendu jejich rezervačního systému a postupně jsem pronikl do backendu. Na konci roku 2022 z firmy odešel projektový manažer, po kterém v týmu zůstala díra. Navrhl jsem, že část jeho kompetencí převezmu, a tak se ze mě na začátku roku 2023 stal vedoucí vývoje. Dávalo to smysl, protože Keyguru nevyvíjí jen SW, ale taky vlastní HW a mechanický design, a já jsem původní profesí mechanik-elektronik.

**Takže jsi v sobě objevil ještě i vůdcovského ducha. Jak se tvoje role proměnila?**

Jsem programátor a projektový manažer, ale nemám žádné podřízené, jen dodavatele. V organizačních záležitostech jsem si prostě věřil a ukázalo se, že právem. Na jaře 2023 mi k vedení vývoje navíc přibyla ještě reorganizace výroby. V podstatě jsem během tří měsíců rozjel úplně nový výrobní provoz. V červenci už nová výroba nějakým způsobem fungovala a já jsem tehdy řekl, že s manažerováním končím, protože to pro mě bylo za daných podmínek dlouhodobě neúnosné. O prázdninách jsem si odpočinul, a nakonec jsme se dohodli, že budu vedle programování i nadále koordinovat technický vývoj jako celek. Tentokrát už ale bez výroby a logistiky.

**Dřív jsi vůbec nepovažoval za reálné se IT živit. Kde se v tobě vzalo odhodlání překonat bariéry?**

Vyrůstal jsem v paradigmatu, ve kterém na takovou práci člověk musí mít vysokou školu a být hodně dobrý v matematice. Trvalo mi dlouho, než jsem si uvědomil, že to není pravda.

**Kdy sis začal hrát s myšlenkou, že se začneš učit programovat?**

Začal jsem o tom uvažovat v roce 2014.

**Než ses přidal do klubu Junior Guru, strávil jsi hodně času samostudiem. Co jsi dělal, když ses na něčem zasekl?**

Googlil (smích).

**Dnes samostudium příliš nedoporučuješ, byť sám ses k němu často vracel. Co je podle tebe nejeefektivnější cestou, jak se něco nového naučit?**

Jedna věc je něco umět a druhá věc je živit se tím. Když chcete změnit profesi, tak musíte být v kontaktu s lidmi, kteří v tom oboru pracují, jinak do toho světa těžko proniknete. Programování se zase reálně naučíte jedině tak, že budete programovat.

**Umím si představit, že nějaké propady motivace sem-tam přišly. Kde se v tobě brala síla pokračovat, když část tebe by raději třeba dělala jednoduchou práci a měla klid?**

Míra motivace byla samozřejmě proměnlivá. Rekvalifikaci jsem zahájil vyhlášením insolvence, abych měl pokoj od exekutorů. Mohl jsem pracovat ve výrobě nebo na montážích, ale věděl jsem, že by mi nezbyla energie na učení, tak jsem vzal místo v bezpečnostní agentuře. První čtyři měsíce byly jako v kriminále. Potom jsem si ale v té firmě vyjednal lepší pozici, na které jsem už měl víc času pro sebe. Bylo to za cenu toho, že jsem další čtyři roky dělal prakticky pouze noční směny, takže jsem měl trvale převrácený režim. Je dobré si uvědomit, že jednou zemřeme a že svoboda nikdy není bez boje.

**Postoji „pamatovat na smrt a bojovat za svobodu“ se určitě nedá nic vytknout. Jak se to však vztahuje k tomu, že jsi dělal čtyři roky noční a měl převrácený režim?**

Věděl jsem, že nikde jinde nebudu mít lepší perspektivu, než v IT. Cokoliv jiného by byl zase jenom kompromis, podobně jako bezpečnostní agentura. Motivace někdy pramení z pochopení vlastní vyjednávací pozice. Na nočních směnách jsem se mohl věnovat učení, aniž by to bylo na úkor pracovních povinností. Na denních směnách by to nešlo.

**V Junior Guru se ti dostalo mentoringu, přitom jde spíš o diskusní fórum. Pokaždé ti radil někdo jiný, nebo sis tam našel opravdového guru?**

[Klub Junior Guru](../club.md) pro mě byl tak trochu chybějící střípek do mozaiky, věci potom nabraly rychlý spád. Taky by se dalo říct, že mě to odbrzdilo. Když jsem poprvé narazil na [příručku Junior Guru](../handbook/index.md), tak na mě působila nedůvěryhodně. Připadalo mi to přehnaně pozitivní, sluníčkářské. Pak jsem jednou narazil na nabídku placeného členství v diskusní skupině a to mi dávalo smysl. Právě proto, že to nebylo zadarmo.

**V čem ti skupina pomohla?**

Během prvního chatu s Danem Srbem jsem vybředl z rozhodovací paralýzy, ve které jsem nevěděl, jakou technologii si vybrat, abych neudělal chybu. Google vám dá odpovědi, jenže někdy naopak potřebujete dostat správnou otázku. To se Danovi povedlo mistrovsky. Základní strategii jsem si tehdy ujasnil díky Danovi a s technologiemi mi pak už většinou radili ostatní.

**Co by ti profesní tranzici usnadnilo ještě víc?**

Předpokládám, že placený osobní koučing a mentoring. Na to jsem ale v insolvenci neměl rozpočet.

**Po jaké době se ti podařilo získat první práci v IT?**

První firma mě oslovila na LinkedIn dřív, než jsem začal aktivně hledat. Dokonce jsem tam nastoupil, ale nesedlo mi prostředí a tak jsem za 14 dní odešel. Díky tomu jsem aspoň věděl, že open space je pro mě no-go zóna. O týden později jsem se dohodl na full-remote spolupráci s Keyguru.

**Tvůj vzkaz juniorům po prvních pohovorech zněl: „Dotáhněte do konce svůj ukázkový projekt a dejte si na něm záležet. Máš nějakou radu jako dnes již zkušený programátor?“**

„Zkušený programátor“ mi zní trochu přehnaně. Vlastní ukázkový projekt je absolutní základ. Všechny důvody, proč ho nedělat, jsou výmluvy. Nikoho nezajímá, jaké jste dělali tutoriály. Musíte dokázat, že jste schopni řešit problémy a učit se nové věci za pochodu. Díky chatbotům a kopilotům to nikdy nebylo pohodlnější než dnes.
