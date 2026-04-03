---
title: Kde a jak hledat pomoc během programování
emoji: 🙋
stages: [learning, creating]
description: Jak se ptát? Jak debugovat? Při programování tě i drobný zádrhel může zaseknout na týdny a úplně ti zkazit radost z učení. Kde můžeš své problémy konzultovat a jak se ptát tak, aby se ti dostalo odpovědi?
template: main_handbook.html
---

{% from 'macros.html' import lead, link_card, illustration, note with context %}


# Řešení problémů během programování

{#
  spravne se ptat je dost narocna samostatna disciplina, je potreba se to naucit jako kazdy jiny skill, googlit je skill, cist odpovedi je skill. zkus vyhledavac, ale pokud vysledkum nerozumis, ptej se, ptej se, kdo se pta, ten se dozvi
#}

{% call lead() %}
  Je velmi těžké se učit zcela bez cizí pomoci. I drobný zádrhel tě může zaseknout na týdny a úplně ti zkazit radost z učení. Neboj se ptát online, radit se s lidmi na [akcích](community.md), nebo si najít [mentora](mentoring.md).
{% endcall %}

{{ illustration('static/illustrations/help.webp') }}

## Kde a jak se ptát

Neboj se ptát, ale zároveň se nauč formulovat dotazy správně. **Žádná otázka není hloupá, může však být hloupě položená.** Než se někde začneš ptát, přečti si [nejslavnější návod na internetu o psaní dotazů](https://www.root.cz/texty/jak-se-spravne-ptat/), nebo alespoň [tento krátký návod od Stack Overflow](https://stackoverflow.com/help/how-to-ask).

<div class="link-cards">
  {{ link_card(
    'Klub junior.guru',
    pages|docs_url('club.md')|url,
    'Ptej se v klubu pro začátečníky, kde najdeš nejen pomoc, ale i motivaci, kamarády, práci.',
    badge_icon='discord',
    badge_text='Discord',
    class='highlighted',
  ) }}

  {{ link_card(
    'Stack Overflow',
    'https://stackoverflow.com',
    'Ptej se na celosvětově největším webu s otázkami a odpovědmi ohledně programování.'
  ) }}

  {{ link_card(
    'Pyonýři',
    'https://www.facebook.com/groups/pyonieri/',
    'Ptej na se české a slovenské Python komunity na Facebooku.',
    badge_icon='facebook',
    badge_text='Facebook',
  ) }}

  {{ link_card(
    'Programátoři začátečníci',
    'https://www.facebook.com/groups/144621756262987/',
    'Ptej se ve Facebookové skupině pro začátečníky v programování.',
    badge_icon='facebook',
    badge_text='Facebook',
  ) }}

  {{ link_card(
    'Python CZ/SK',
    'https://discord.gg/yUbgArVAyF',
    'Ptej na Discordu české a slovenské Python komunity.',
    badge_icon='discord',
    badge_text='Discord',
  ) }}

  {{ link_card(
    'r/learnpython',
    'https://www.reddit.com/r/learnpython/',
    'Pokládej dotazy komunitě pro začátečníky s Pythonem.',
    badge_icon='reddit',
    badge_text='Reddit',
  ) }}

  {{ link_card(
    'r/learnprogramming',
    'https://www.reddit.com/r/learnprogramming/',
    'Pokládej dotazy komunitě pro začátečníky v programování.',
    badge_icon='reddit',
    badge_text='Reddit',
  ) }}
</div>

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
{% endcall %}


<!-- {#

vylepsit stranku kde hledat pomoc - a v tom mit i AI


Nechceš o tom napsat článek? Rozepsat tyhle body (nebo tak něco, viděls asi hodinu, kdy sem šel spát…) 1) rady je těžké dávat 2) neraď to, co fungovalo tobě, každý je jiný a zbytek kontextu je taky jiný, říkej mě fungovalo toto 3) neraď, dokud nevíš, co někdo potřebuje Krátkej, že bychom to dali do pravidel nebo doporučení.

https://jvns.ca/blog/good-questions/

https://www.hash.cz/inferno/otazky.html

Zajímavý článek o tom, jak se správně ptát https://hamatti.org/posts/how-to-ask-help-for-technical-problems/

https://github.com/juniorguru/junior.guru/issues/30

Zdravím Honzo, z těch tutoriálů by se klidně ještě hodilo nějaké uvedení do Stack Overflow :smile: . Já se v něm už snad tak nějak "orientuji", ale potřeboval bych asi ujasnit, jak v tom lépe (čti přesněji) vyhledávat a ideálně nevytvářet duplikátní posty k již zodpovězeným issues :thumbsup:

ja mam pocit, ze kym naformulujeme dobru otazku, napr. podla https://hamatti.org/posts/how-to-ask-help-for-technical-problems/ tak je vacsia sanca ze sami najdeme odpoved na danu otazku a tak ju nikde nenapiseme ... a potom tie otazky co vidime napisane od inych ludi nemusia byt reprezentativne najlepsie otazky ¯\_(ツ)_/¯

https://honzajavorek.cz/blog/empowered-by-ai-why-junior-devs-have-the-winning-edge/

- kdy se zeptat, rule of thumb
- jak se zeptat - navod podle lukyho
- kde se ptat
- jak se vyporadat s odpovedmi - zastaraly python, sexismus, debilni odpovedi, 50 ruznych odpovedi, kazdy to svoje s cim ma zkusenost, fanouskovstvi...
- TODO dobře položená otázka je skill, dobře položená otázka pomáhá ostatním ti dát užitečnou odpověď
- Poznej ... produkt - video nebo lidsky na akci poznat nějaký produkt
- jak funguje poradna? text od lukase, jak se ptat. neexistuje hloupa otazka, ale muze byt spatne polozena.
- Lukáš Kubec překlad jak se ptát otázky
- HOW TO DEBUG? :thinking:
- https://www.codeac.io/blog/upgrade-your-debugging-skills-and-code-like-pro.html
- https://www.codeac.io/blog/3-5-best-practices-on-how-to-prevent-debugging.html
- https://www.codeac.io/blog/how-to-save-time-while-debugging.html
- Co se týče contentu, bavíme se o nové kapitole do https://junior.guru/handbook/ a to mi může trvat, ale až k tomu dojde, tak se ozvu. Určitě to pak můžete sdílet, překládat do angličtiny, vydávat u sebe, atd. Ostatně licence příručky je https://creativecommons.org/licenses/by-sa/4.0/deed.cs
- https://www.instagram.com/p/CgcCjV8DkCj/
- https://en.wikipedia.org/wiki/Rubber_duck_debugging
- do pravidel v poradně dát nějaký tip jak se ptát správně
- dobře položená otázka je skill, dobře položená otázka pomáhá ostatním ti dát užitečnou odpověď https://stackoverflow.com/help/how-to-ask, https://jvns.ca/blog/good-questions/
- jak dávat kód na discord - drag and drop, fenced code blocks, screenshot...
- jak si pomoci s AI https://www.youtube.com/watch?v=DPg4EVufkfs
- https://meta.stackoverflow.com/questions/421831/temporary-policy-chatgpt-is-banned
- Jak se postavit k AI https://www.joshwcomeau.com/blog/the-end-of-frontend-development/
- These are incredibly powerful tools. They are far harder to use effectively than they first appear. Invest the effort, but approach with caution: we accidentally invented computers that can lie to us and we can't figure out how to make them stop. https://simonwillison.net/2023/Apr/7/chatgpt-lies/
- Ahoj, napadá mě, že do Příručky by se do Řešení problémů dalo přidat něco o chatgpt. Nebo teď to tam aspoň nevidím.


jak se ptat a proc juniori neumi pokladat dotazy
On je problém, že aby člověk mohl udělat ten dotaz, tak:

- musí aspoň zhruba tušit, na co se ptát (co je nám zřejmé, na to někdo v začátcích prostě hledí jak puk)
- musí umět dostatečně anglicky, aby dotaz položil (např. vědět, že podtržítko je "underscore", že když se něco sekne, říká se tomu "hangs", apod.)
- musí umět rozšifrovat dotaz/odpověď na Stack Overflow, kde je často jen podobný problém a tři nejednoznačné odpovědi, ze kterých dvě jsou na Python 2 nebo nebudou dotyčnému fungovat z jiných důvodů

Prostě je to složitější. Ono ani pokládat správně dotazy a rozšifrovat odpověď z různých stránek není tak primitivní, jak se pokročilejším zdá. Je to skill a přichází až časem. Vyloženě lenost nebo blbost tady vidím málokdy.


Jak se vůbec učit? V tomhle threadu je pěkně ilustrované, že někteří lidé se učí způsobem, který je pro naučení se programovat dost neefektivní: https://discord.com/channels/769966886598737931/1032224640392769576
Kdyby třeba v budoucnu do příručky přibyla kapitola "Jak se učit" něbo tak něco 🙂

Dev tip: Add "after:2018" to the end of every Google search for solutions to technical issues. It filters the results with fewer clicks. 💁🏾‍♀️— Taylor Poindexter (@engineering_bae) January 8, 2020
https://twitter.com/engineering_bae/status/1214956636730744833

Codebytes
http://links.iterable.com/e/evib?_t=13e4e7efd5b34d1d982e9fb34505f006&_m=94b78d4c11ee40998424e05884535f1f&_e=NtkvZFbtt5kmcjizGz3G6WJ1gv2GVvqrn_TOCqaxZNrvhrVZ_y7XsNa3TxV3WOMoq3uEhQfCmnasml1yGerDFC1MOjGSQmqJ5mwWGAlW0gDdJiO_YOczThgwbd4_2nWouzE7JLsfAAB5FsTjzvYdgg%3D%3D

Jak si nechat radit od druhých
The more universal a solution someone claims to have to whatever software engineering problem exists, and the more confident they are that it is a fully generalized solution, the more you should question them. The more specific and contingent the advice - the more someone says ‘it depends’ or ‘YourSQL works well in a read-heavy context with the following constraints’ the more likely they are to be leading you in the right direction. At least that’s what I have found.
https://earthly.dev/blog/thought-leaders/


Nevzdávej to. Většina lidí, kteří se začnou učit, odpadne v prvním měsíci. Zkus tento kritický čas překonat.
Nejúspěšnější jsou ti, kteří se učí pravidelně. Radši se uč každý den deset minut než dvakrát do měsíce čtyři hodiny.
Zkus na to přijít bez pomoci ostatních. Píšeš nějaký kód a nevíš si s ním rady? Nedívej se hned na správné řešení. Nehledej hned pomoc lektora. Udělej pár variací tvého kódu. Když na to přijdeš sám, posuneš se o veliký kus dál a rozvineš své problem solving skills. A navíc ze sebe máš dobrý pocit.
Používej Google. Když si nevíš rady a hledáš správnou odpověď, napiš to do Google. Určitě najdeš spoustu správných odpovědí, protože problém, který řešíš, už před tebou řešilo spoustu lidí. Stoprocentně.
Teorie nestačí. Určitě je dobré mít teoretické základy, ale ty musíš vyzkoušet na praktických úlohách.
Dej si pozor na stránky, které tvrdí, že tě naučí programovat za 4 dny nebo dokonce za pár hodin. Snaží se tě nalákat na své výukové materiály, které často nejsou příliš kvalitní. Naučit se programovat je záležitost několika měsíců až let.
Investice do vzdělání se vyplatí. Sice jsme v Česku a na Slovensku zvyklí, že za vysoké školy neplatíme, ale u kurzů je to trochu jinak. Když máš kurzy zpoplatněné, často dostaneš komplexnější a propracovanější materiály a doplňkové služby.
https://player.vimeo.com/video/302030589?badge=0&autopause=0&player_id=0&app_id=109608

tldr pages (man pages) https://tldr.sh/

jak se ptat kdy se ptat
https://trello.com/c/0kzSVb96/5606-jak-se-ptat-kdy-se-ptat

--- https://discord.com/channels/769966886598737931/788832177135026197/872541661706748026
<:python:842331892091322389>  Motivace k pokročilejšímu debuggování:
https://youtu.be/5AYIe-3cD-s
---


--- https://discord.com/channels/769966886598737931/806621830383271937/872033850581188658
[WebDev/JS] Naucil jsem se nedavat vsude `console.log` na debuggovani a misto toho pouzivat logpointy: https://developer.chrome.com/blog/new-in-devtools-73/#logpoints
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1049637818273632328
Tak, jestli ještě někdo nezaregistroval https://chat.openai.com tak ho vřele doporučuji, takový stackoverflow už u mě nemá šanci... odpověď je okamžitá, nabízí víc možností i s ukázkou kódu, komplet v češtině, výklad krásně srozumitelný...  začínajícím programátorům vřele doporučuji! Je nutné se nejdřív registrovat, ale pak už je to nepopsatelný luxus.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/959408332395937814
Ona taky existuje nějaká poučka, že když něco řešíš a neposouváš se víc než (doplň si časovou jednotku), tak je lepší se zeptat.

Pokud je časová jednotka nula, tak je to hodně ptaní a může jít o otravování. Fakt je dobrý na to nejdřív zkusit přijít. Ale když je jednotka zase moc velká, tak ten člověk zase zbytečně bloudí, třeba mu chybí nějaký kontext, který nemůže vědět, nebo stačí postrčit správným směrem, název algoritmu… prostě je zase zbytečný, aby vymýšlel tři dny kolo, když mu někdo dokáže za 10 minut pomoct a posunout úplně jinam.

Ideální časová jednotka asi neexistuje, každý to bude mít trochu jinde, ale podle mě by to měly být nižší jednotky hodin. Třeba 1-3h, kdy se na to snažíš přijít sama a pak se jdeš zeptat.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/959408485051826196
<:ducky:843773644945489941>  https://en.wikipedia.org/wiki/Rubber_duck_debugging
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1091322623943786577
Co si myslíte o používání Copilota (apod.) někým, kdo se učí programovat? Je větší výhoda, že to třeba dává člověku nápady jak ten kód napsat, který by ho normálně nenapadly a on se tím něco naučí nebo je to horší tím, že si pak člověk nenabíjí tolik držku, na spoustu věcí si nepřijde sám a třeba mu uniknou i nějaký důležitý vlastnosti jazyka?
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1080894646424703046
Velmi mě zaujalo video https://www.youtube.com/watch?v=DPg4EVufkfs - vypadá to, že autorka Lucie Lénertová je velmi dobrá v tom, co dělá. 🙂
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1080049938173542411
Krátký článek o feedbacku, jak ho dávat, přijímat... https://brightinventions.pl/blog/5-feedback-models-you-should-know Užitečné nejen v IT 🙂
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1060527570539532368
Zajímavý jak se to schází... O debuggingu vydala nedávno zine i Julia Evans: https://wizardzines.com/zines/debugging-guide/
---


--- https://discord.com/channels/769966886598737931/938529943023915069/938923222156595230
Ahoj,
draft překladu: https://docs.google.com/document/d/1apa_4Mw9CwCTO_z3tYVYRGmfw0-s_iJJ/edit?usp=sharing&ouid=112039692281202535262&rtpof=true&sd=true

je tam jedna červená část, kterou ještě musím přeložit, je to jeden odstavec, který se odkazuje na jiný anglický text hodně.

Klasicky mám problém s gramatikou, na to pozor a je to draft, takže jakýkoliv zásah, učesání, oprava či změna prkennosti vítána, jen mezi napsáním tohoto komentáře a jeho odesláním jsem tam pár věcí upravil, znovu si to přečtu až zítra.

Suggest edit či comment je pro všechny otevřené, <@!652142810291765248>  a <@!668226181769986078> když mi napíšete mail, dám vám tam přístup i pro přímé úpravy, není dobré, když do toho může takhle naplno lézt mnoho lidí, ať to má nějaký řád - ale jestli chcete, klidně to otevřu pro všechny.

Dík,
L.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1108854332331397231
Zkoušeli jste někdo? Používáte? https://www.phind.com/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1117365521696948336
**a debugging manifesto ** 🐛
zdroj: https://twitter.com/b0rk/status/1570060516839641092
---


--- https://discord.com/channels/769966886598737931/1144270855375958016/1144281111594291330
Přidávám volný překlad [klasického článku](https://solhsa.com/dontask.html), kde je vysvětleno, proč není nejlepší se ptát tak, jak se ptáš.
—————
https://hackmd.io/@benabraham/ptej-se-rovnou
---


--- https://discord.com/channels/769966886598737931/1141758341408894996/1158419236952215613
V tehle situaci (pocit, ze uz neco resim moc dlouho a nikam to nevede) mi vetsinou pomohla jedna nebo vice z techo tri veci:
- jit se projit,
- popsat nekomu dany problem (rubberducking),
- odlozit a chvili resit neco jineho.
Tohle je moje zkusenost, ymmv.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1157406282786033717
Jedna kamarádka mi říkala (pracuje v kanclu ajťáků, sama zatím na nevýv. pozici): *Já jsem tak nějak předpokládala, že když se na něco zeptám programátora, tak si vyslechne otázku, otevře pusu a vysloví odpověď. Ale ne. Otočí se a jde to googlit.*

Podle mě jediný rozdíl je v efektivitě googlení a kvalitě interpretace výsledků (ke které přispívá dřívější znalost a pochopení oblasti), jinak je googlení základní lopatička. I proto, že ty dokumentace občas nejsou nic moc. A otázka pro mě je, jak vypadá kvalitní dokumentace a pro koho je (a pro koho ne). Ale to je asi deformace tím, že jsem byla líznutá vzděláváním, vstřebatelností dokumentů atd.

V jiných oblastech je seniorní ten, kdo odpovědi má, tady ten, kdo je umí rychle nacházet. Pro lidi, co jsou odjinud, to je podle mě dost změna paradigmatu (pro mě určitě).
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1157365315185946725
Viděno na LI.
---


https://dontasktoask.com/
https://xyproblem.info/
https://nohello.net/


--- https://discord.com/channels/769966886598737931/916339896963190785/1192738348998082611
Pokud používáte nějakého AI asistenta při psaní kódu, tak je jistá šance, že bude méně bezpečný a zároveň budete věřit, že je bezpečnější než kdybyste AI nepoužívali https://arxiv.org/abs/2211.03622
---


--- https://discord.com/channels/769966886598737931/1191365076188397591/1192218179880095764
U te diskuze ohledne AI bych vicemene souhlasil se vsemi zucastnenymi.
Ano, jeji podstatou je efektivita. Ta ale v kazde fazi znamena neco jineho.
Kdyz se ucim stavarinu, ochotne mi poradi, jak vypada cihla, proc malta lepi a jak tuhne beton. Odstranim zaseky, kdy nevim jak dal a zvysim efektivitu UCENI. Netroufl bych si ji ale jeste pozadat navrhnout cely dum.
Kdyz uz ale vim, jak se chova cihla, malta a beton, pomuze mi poskladat modulove patrove domy. Odstrani hodiny skladani a pocitani cihel a betonovych konstrukci. Zase to bude efektivita, ale uz efektivita PRACE
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1192241831518412891
Jak se správně ptát, když chcete poradit s kódem - narazil jsem na nový článek na toto téma https://angelika.me/2024/01/03/how-to-ask-for-help-with-your-code-online/
---


--- https://discord.com/channels/769966886598737931/797040163325870092/1207487079743758416
<:exactly:1100463303190396968> https://dontasktoask.com/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1210182361816498226
(Další) návod jak se dobře ptát https://www.pythondiscord.com/pages/guides/pydis-guides/asking-good-questions/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1220986911401705572
Zrovna čtu https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/ a jen se mi potvrzuje, že AI je hodně užitečné, ale (zatím?) není snadné umět si tím správně pomoct. Přijde mi skvělé, co vše to umí, ale necítím se nahrazen, ani ohrožen 🙂 Prostě toho jen stihneme víc.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1372863264756596756
Je pravda, že v poslední době když tam jdu něco hledat, tak jsou tam otázky i odpovědi zpravidla 3, 5, nebo dokonce 10 let staré, ale aktuálnějšího často nic nenajdu 🫤 https://blog.pragmaticengineer.com/stack-overflow-is-almost-dead/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1368339153309405307
Proč na tomhle Discordu najdete lepší rady, než u svého kámoše, který už v oboru programuje 15 roků https://jacobian.org/2025/mar/13/beware-advice-from-old-heads/
---


--- https://discord.com/channels/769966886598737931/1356815451442778256/1359809991372181605
A pokud je nějaký příspěvěk, kde je toho moc, prostě ho vykopíruj a nech si ty pojmy od ChatGPT klidně vysvětlit <:meowthumbsup:842730599906279494> I já to tak někdy dělám a je to překvapivě nápomocné.
---

https://blog.pragmaticengineer.com/stack-overflow-is-almost-dead/


--- https://discord.com/channels/769966886598737931/769966887055392768/1434810985289351189
toto je pekne https://overreacted.io/how-to-fix-any-bug/ .. tolko trpezlivosti by som v sebe asi nenasiel, vyslovene umelecke dielo ako Dan pretvoril debugovaciu session na prilezitost nieco vysvetlit a ucit principy ako vytvorit minimal repro steps napriek vsetkym tendenciam na sabotaz

> At this point, it’s worth trying to change the code a few times in either direction (comment it in, comment it out) to verify that each edit predicts the new repro result. (It’s also worth doing other edits to rule out that every second edit works.)
uff, kiezby toto bola len prehnana paranoja <:lemon_sweat:754441881718620281>
---


#} -->
