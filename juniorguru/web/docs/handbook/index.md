---
title: Příručka pro juniory
emoji: 🗺️
thumbnail_badge: zdarma
description: Obsáhlá příručka pro všechny, kdo se chtějí naučit programovat a najít si práci v oboru.
template: main_handbook.html
---

{% from 'macros.html' import lead, img with context %}

# Příručka pro juniory

{% call lead() %}
  Uvažuješ o programování?
  Přemýšlíš nad kariérní změnou do IT, ale nevíš jak na to?
  Láká tě zjistit, jak automatizovat část své práce?
  Studuješ informatiku a zajímá tě, co dál?
  V téhle příručce se postupně hromadí veškerá moudrost, která na toto téma existuje.
{% endcall %}

Celá **cesta juniora** má zhruba {{ stages|length }} fází a připomíná [Člověče, nezlob se](https://cs.wikipedia.org/wiki/%C4%8Clov%C4%9B%C4%8De%2C_nezlob_se!).
Namalované je to hezky jedno za druhým, ale realita je zamotanější.
Je normální, že se zasekneš, nebo něco přeskočíš.
A nemálo lidí se v půlce vrátí zpátky do domečku.

Ne všechna témata se zatím povedlo pokrýt kapitolami v příručce, ale se všemi pomáháme a diskutujeme je ve zdejším [klubu](../club.md).

<div class="stage-cards">
{% for stage_group in stages|slice(3) %}
  {% for stage in stage_group %}
  <div class="stage-card">
    <div class="stage-card-row">
      <div class="stage-card-media">
        <div class="stage-card-icon">{{ stage.icon|icon }}</div>
      </div>
      <div class="stage-card-body">
        <h4 class="stage-card-title">{{ stage.title }}</h4>
        <p class="stage-card-description">
          {{ stage.description }}
        </p>
        <p class="stage-card-pages">
          {% for p in stage.list_pages -%}
            <a href="{{ pages|docs_url(p.src_uri)|url }}">{{ p.nav_name }}</a>
          {%- endfor %}
        </p>
        {% if stage.list_todo_pages|length %}
        <p class="stage-card-todo-pages">
          Plánované kapitoly:
          {% for p in stage.list_todo_pages -%}
            {{ p.title }}
            {%- if not loop.last %}, {% endif -%}
          {%- endfor %}
        </p>
        {% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
  <div class="stage-illustration">
    {{ img('static/chick' + loop.index|string + '.svg', 'Kuře', 50, 50, lazy=False) }}
  </div>
{% endfor %}
</div>

<!-- {#


celkově Hele za mě dobrý, ale asi bych tam ocenil, v rámci přehledu nejen název a popis co se tam dělá, ale i stručně PROČ ta fáze má smysl, co je CÍLem, nějakou větičku.


„Je nor­mál­ní, že se za­sek­neš, nebo něco pře­sko­číš“ Tady říkáš, že to je v pořádku. I když samozřejmě slovo normální neznamená v pořádku, tak si to tak dost lidí vysvětluje. Ale není. Vynecháním něčeho pravděpodobně bude takový člověk dost trpět a možná se mu to nakonec nepovede.


# Příručka pro juniory

Vítej na příručce pro všechny, kteří chtějí začít s programováním. Najdeš tady rozcestník a rady, jež ti pomohou se zorientovat a díky kterým budeš vědět jak začít.

-   **Je to živá stránka**, kde stále probíhají úpravy, ne nějaká hotová kniha. Kdykoliv tady může přibýt něco nového, takže není od věci se sem občas vrátit. O důležitých změnách se můžeš dovědět na [sociálních sítích](#kontakt) junior.guru nebo prostřednictvím [klubu](club.md).

-   **Je zdarma pro každého**, žádná její část není zpoplatněná. Zdrojové kódy příručky jsou [veřejně na GitHubu](https://github.com/honzajavorek/junior.guru/) a veškerý zdejší text může kdokoliv použít, pokud uvede autora a výsledek vystaví pod stejnou [licencí](https://creativecommons.org/licenses/by-sa/4.0/deed.cs).

-   **Příručka je financována

-   **Autorem příručky je [Honza Javorek](#honza)**, stejně jako i celého junior.guru. Psaní příručky je možné jen díky financím získaným z individuálních a firemních členství v [klubu](club.md).

-   **Cílem je zpřístupnit programování komukoliv**, kdo se jej bude chtít naučit. Programovat se můžeš naučit i bez vysoké školy, materiálů a kurzů je k tomu na internetu dost. Ať už to děláš pro zábavu, chceš si usnadnit nějakou činnost, nebo toužíš po kariéře v IT, příručka ti ukáže, jak na to. Ať už jsi z velkého města s širokými možnostmi nebo z odlehlé vesnice, příručka je tu pro tebe.




Na základě reálných zkušeností mnohých začátečníků jsme v [klubu](../club.md) sestavili **osvědčenou cestu juniora**, která má deset fází. Možná existují i jiné cesty, ale tato **úspěšně zafungovala pro spoustu různých lidí**, a proto ji lze obecně doporučit.

**Ujasni si, co už umíš a co je tvým cílem.** Jednak ti to pomůže uvědomit si, co tě ještě čeká a co nesmíš vynechat, jednak zjistíš, které části příručky pro tebe budou nejpřínosnější.

Pokud o IT teprve přemýšlíš (fáze 0), budou pro tebe zajímavé jiné rady, než pokud už máš za sebou nějaký kurz (fáze 2 až 3). A jestli tě programování zajímá proto, že chceš automatizovat zalévání rajčat na zahradě (fáze 3), nemusí tě zajímat kapitoly o shánění práce v oboru (fáze 4 až 10).

## Tempo

neda se smichat intenzivni a pozvolna zmena, mit to jako dve ruzne cesty, nevedi vubec jak dlouho to muze trvat, co je neni normalni, jake jsou tam milniky

## Jak funguje tato příručka

- Kdo ji píše
- Proč ji píše
- message na úvodní stránce příručky - články versus content, dnes už nikdo content nedělá, chtějí to spláchnout clankem, ne udržovat nějaké informace (Czechitas, Engeto)

fáze https://discord.com/channels/769966886598737931/788826407412170752/904981964208087070

nela https://github.com/NelliaS/development-timeline

https://www.freecodecamp.org/news/what-is-web-development-how-to-become-a-web-developer-career-path/

https://twitter.com/jzunigacoayla/status/1380694681911226373

https://blog.lewagon.com/skills/programming-language-to-learn/

https://roadmap.sh/

https://codeburst.io/the-2018-web-developer-roadmap-826b1b806e8d

https://twitter.com/ladybugpodcast/status/1247051343212281856

Front-end Developer Handbook 2019
https://frontendmasters.com/guides/front-end-handbook/2019/

How to Learn to Code & Get a Developer Job [Full Book]
https://www.freecodecamp.org/news/learn-to-code-book/#500-word-executive-summary

https://learntocodewith.me/

https://www.pythondiscord.com/resources/

--- https://discord.com/channels/769966886598737931/788826407412170752/904981964208087070
**Fáze juniora.**

Skoro u každýho kroku je možno se zaseknout a nepřejít dál.
Každej krok má svoje úskalí.

0️⃣ **občas mě něco jako učit se programovat napadne**
úskalí: nezačnu nebo začnu, ale první zkušenost je špatná

1️⃣ **nezávazně zkouším všechno možné nebo začínám s jednou věcí, o které si myslím, že ji chci dělat**
úskalí: nemůžu se rozhodnout mezi technologiemi či oblastmi

2️⃣ **učím se samostatně / v kurzu to, co si myslím, že chci dělat**
úskalí: sám nevím kam až / kurz zas nemusí být dostatečný nebo kvalitní / nedaří se mi najít si dost času se tomu věnovat

3️⃣ **pracuju na projektech**
úskalí: nevím jak začít / nevím jaký projekt / nedám projekt (ani průběžně) ke zhodnocení / špatně odhadnutý rozsah projektu

4️⃣ **připravuju se na hledání práce (CV apod.)**
úskalí: neodvažuju se do téhle fáze přejít, nevím co se v IT očekává nebo dokonce nemám moc zkušeností s prací celkově / neumím sám sebe „prodávat“, mám problém napsat pozitiva do CV

5️⃣ **hledám práci**
úskalí: nemám dostatečnou výdrž / nemám dostatečnou finanční rezervu / odradí mě první neúspěchy / vezmu cokoli i když je to něco jiného, než jsem chtěl dělat (někdy ok, někdy problém)

6️⃣ **mám nalezenou/domluvenou práci a nastupuju v budoucnu**
úskalí: nezačnu se vůbec sám učit technologii, kterou ve firmě používají  nebo to s tím naopak místo odpočinku přeženu

7️⃣ **zkušební doba v první práci**
úskalí: málo se ptám seniora a tím se málo učím / není k dispozici senior / zůstanu ve firmě i když je to tam zjevně špatný

8️⃣ **pracuju (po zkušební době)**
úskalí: přestanu se rozvíjet a učit, nedostávám pokročilejší úkoly

9️⃣ **mám 1-2 roky praxe**
úskalí: to co v 8️⃣ + neřeknu si o větší peníze, přestože mám na trhu o dost vyšší cenu než na začátku

🔟 už nejsem „junior“
---


--- https://discord.com/channels/769966886598737931/788832177135026197/894840146845925427
https://www.codecademy.com/resources/docs

Blog post k tomu https://www.codecademy.com/resources/blog/introducing-docs/

Samozřejmě jsou jiné existující zdroje, ale tady je to hodně stručně, takže to začátečníci asi ocení.
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1061972910488703036
Spíše motivační četba, ale pěkný článek. Něco jako příručka junior.guru ale od freeCodeCamp 🙂
https://www.freecodecamp.org/news/learn-to-code-book/#500-word-executive-summary
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1055146186413187102
Doufal jsem, že sem taky budu moct jednou napsat, že jsem konečně v klubu a našel jsem práci. A stalo se to ! Od února se budu podílet na softwaru v automobilech v Pythonu. 🤩

Od začátku utekly dva roky, kolik jsem oslovil firem přesně nevím, ale mohlo to být kolem dvaceti. Hlavně bych ale chtěl říct, že na začátku není důležité někam spěchat - což se mi také stalo. Pak jsem si uvědomil, že stihnout to za pár měsíců souběžně s prací a rodinou je blbost. A tak jsem v klidnějším tempu pokračoval k cíli.

Pár slov a odkazů k cestě, na začátku za mě nejlepší start na https://www.umimeinformatiku.cz/programovani-v-pythonu , to mi pomohlo nejvíc a je to hlavně zábavnou formou příkladů. Pak jsem si vybral projekt od https://www.techwithtim.net/ , který má super tutorialy na Youtube a zakončil jsem to projektem s Corey Schafer také na Youtube, nicméně ty už jsou pro pokročilejší.

U pohovoru také dost pomohl GitHub, který doporučuji si založit hned první den. Jednak mě motivoval ten kalendář příspěvků udělat něco pokud možno alespoň každý druhý den. A poté je vidět jak dlouho už se člověk tématem zabývá. 🙂

Hodně zdaru, sil a velký dík Honzovi, že to tu založil a spravuje <:dk:842727526736068609> 🥳
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1054800375703683113
Níže založím vlákno s malým shrnutím mého hledání práce, které jsem teď završil přijetím nabídky na pozici Java vývojáře s nástupem v únoru. Přidám pár postřehů o tom, co bych udělal stejně/jinak, kdybych si znovu hledal práci. Taky zmíním jména pár firem, které na mě působily velmi dobře, nebo naopak velmi špatně, a proč. Celé je to založené na mých zkušenostech podpořenými zkušenostmi z práce v IT recruitmentu. Takže všechno můj názor, i když to místy napíšu jako “poučku s absolutní pravdou” nebo tak něco 🙂
---




#} -->
