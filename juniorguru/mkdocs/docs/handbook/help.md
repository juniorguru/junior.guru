---
title: Kde a jak hledat pomoc během programování? Jak se ptát? Jak debugovat?
emoji: 🙋
thumbnail_title: Řešení problémů během programování
description: Při programování tě i drobný zádrhel může zaseknout na týdny a úplně ti zkazit radost z učení. Kde můžeš své problémy konzultovat a jak se ptát tak, aby se ti dostalo odpovědi?
template: main_handbook.html
---

{% from 'macros.html' import lead, link_card, note with context %}


# Kde najdeš pomoc

{#
  spravne se ptat je dost narocna samostatna disciplina, je potreba se to naucit jako kazdy jiny skill, googlit je skill, cist odpovedi je skill. zkus vyhledavac, ale pokud vysledkum nerozumis, ptej se, ptej se, kdo se pta, ten se dozvi
#}

{% call lead() %}
  Je velmi těžké se učit zcela bez cizí pomoci. I drobný zádrhel tě může zaseknout na týdny a úplně ti zkazit radost z učení. Neboj se ptát online, radit se s lidmi na [akcích](practice.md#najdi-inspiraci-poznej-lidi), nebo si najít [mentora](practice.md#najdi-si-mentora).
{% endcall %}

## Kde a jak se ptát

Neboj se ptát, ale zároveň se nauč formulovat dotazy správně. **Žádná otázka není hloupá, může však být hloupě položená.** Než se někde začneš ptát, přečti si [nejslavnější návod na internetu o psaní dotazů](https://www.root.cz/texty/jak-se-spravne-ptat/), nebo alespoň [tento krátký návod od Stack Overflow](https://stackoverflow.com/help/how-to-ask).

<div class="link-cards">
  {{ link_card(
    'Klub junior.guru',
    pages|docs_url('club.md')|url,
    'Ptej se v klubu pro začátečníky, kde najdeš nejen pomoc, ale i motivaci, kamarády, práci.',
    badge_icon='discord',
    badge_text='Discord',
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
  {{ 'exclamation-circle'|icon }} Tuto stránku Honza právě přepisuje. Brzy tady bude jiný text, lepší, voňavější, nápomocnější.
{% endcall %}


<!-- {#

https://jvns.ca/blog/good-questions/

https://www.hash.cz/inferno/otazky.html

Zajímavý článek o tom, jak se správně ptát https://hamatti.org/posts/how-to-ask-help-for-technical-problems/

https://github.com/honzajavorek/junior.guru/issues/30

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

#} -->
