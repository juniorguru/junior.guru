---
title: Mentoring
emoji: 💁
stages: [learning, creating, preparing]
description: Kde najít mentory, jak s nimi komunikovat, a proč se toho nebát? Může ti s mentorováním pomoci ChatGPT?
template: main_handbook.html
---

{% from 'macros.html' import note, lead, link_card with context %}

# Mentoring při programování

{% call lead() %}
  Mentorka nebo mentor ti pomůže s věcmi, se kterými si samostatně nevíš rady.
  Kde takové lidi najít, jak s nimi komunikovat, a proč se toho nebát?
  Může ti s mentorováním pomoci AI?
{% endcall %}

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
{% endcall %}

Mentor nemusí být vyloženě mistr v oboru, stačí když bude v programování alespoň o něco zkušenější než ty. A klidně může stačit, když se uvidíte jednu hodinu týdně přes videohovor. Pokud znáš někoho, kdo by mohl být tvým mentorem, ale nemá s tím praktické zkušenosti, projděte spolu [přednášku o mentorování](https://github.com/honzajavorek/become-mentor/blob/master/cs.md#readme) a prostě to zkuste!

<div class="link-cards">
  {{ link_card(
    'Kanál #mentoring v klubu junior.guru',
    pages|docs_url('club.md')|url,
    'Hledej mentory v klubu pro začátečníky.',
    class='highlighted',
  ) }}

  {{ link_card(
    'ReactGirls Mentoring',
    'https://reactgirls.com/mentoring',
    'Mentoringový program pro ženy zajímající se o webový frontend.',
    badge_icon='gender-female',
    badge_text='Pro ženy',
  ) }}

  {{ link_card(
    'Femme Palette',
    'https://www.femmepalette.com/mentoring-for-women-it',
    'Český program placeného mentoringu pro ženy.',
    badge_icon='gender-female',
    badge_text='Pro ženy',
  ) }}

  {{ link_card(
    'Mentoring na robime.it',
    'https://robime.it/mentoring-program-robime-it/',
    'Slovenský mentoringový program.'
  ) }}

  {{ link_card(
    'GISMentors',
    'https://gismentors.cz/',
    'Mentoři, kteří učí využívaní programování v geografii.'
  ) }}

  {{ link_card(
    'Codementor',
    'https://www.codementor.io/tutors',
    'Profesionální, placení mentoři z celého světa.'
  ) }}
</div>


<!-- {#

https://github.com/juniorguru/junior.guru/issues/4

https://github.com/juniorguru/junior.guru/issues/28

Stránka mentoring na webu, kde bude základ o mentoringu obecně, k čemu to je… a pak zvýrazněny odkaz na klub, pak sekce přímo s mentory - jenže jak je propojit, když neexistuje propojovací odkaz přes discord? Sekci přímo s mentory nedělat a kdyžtak dat jen křestní a iniciály.

mít stránku /mentoring/ s představením jak to funguje

včlenit nějak https://github.com/honzajavorek/become-mentor#readme do webu

- školení co je mentorování, jestli to dělají dobře, rozdíl mezi mentoringem a koučingem
- Poznej ... produkt - video nebo lidsky na akci poznat nějaký produkt
- co za tím je, vysvětlit celý proces

dat mentorum tip ze si muzou dat mail na notifikace z discordu

Návod pro mentory musí zahrnovat nastavení notifikaci

- lidi neprijdou na ten mentoring, rezervujou si cas, ale neprijdou
- kdyz uz prijdou, tak je to stack overflow, i ten mentoring channel je stack overflow, neni to mentoring a nema to dlouhodobejsi charakter
- zduraznit ze mentori to delaji dobrovolne a neni slusny neprijit na domluveny cas a predem se neomluvit
- udelat stranku na web, kde bude navod na mentoring a mozna i seznam tech mentoru
- Volat si můžete přímo přes discord nebo přes cokoliv si domluvíte
- webinář a manuál pro mentorky, webinář a manuál pro mentees, kde jsou nastavený očekávání a jak mentorovat nebo SMART cíle mentoringu


 '💡 **Tip:** Ať už jsi junior nebo mentor, pusť si parádní [přednášku o mentoringu](https://www.youtube.com/watch?v=8xeX7wfX_x4) od Anny Ossowski. '
 'Existuje i [přepis](https://github.com/honzajavorek/become-mentor/blob/master/README.md) a [český překlad](https://github.com/honzajavorek/become-mentor/blob/master/cs.md).'

Be a good mentor not dickhead
https://dev.to/mortoray/be-a-good-mentor-not-a-dickhead

jak (ne)najit mentora
https://twitter.com/willjohnsonio/status/1282713655105159170

--- https://discord.com/channels/769966886598737931/864434067968360459/962393354056925234
<@477895566085324801> pokud nevíš zda je koučování pro tebe tak doporučuji mrknout na webinář a poté se zúčastnit základního kurzu https://bytkoucem.cz/zaklady-koucovaciho-pristupu/. Koučovat nebudu, ale hledal jsem další cestu jak zlepšit porady, posouvat lidi dopředu a nakonec to v mnoha ohledech pomohlo mě samotnému. Na zkoušku a pochopení o čem je a není koučování je kurz dostatečný, mé požadavky byly splněny.
---


--- https://discord.com/channels/769966886598737931/931605794040975430/931610600239423488
- líbilo se mi , když mi dokázal vysvětlit mou otázku krok za krokem a zpětně se ujišťoval, že mu rozumím (když jsem váhala, dával další a další příklady k vysvětlení a procvičení)

- naučil mě myslet nad problémem, tj. jak si ho rozložit, jak a kde hledat řešení

- byl lidský, tzn. ujistil mě, že i senioři neví a jsou mnohdy ztracení, že pátrají a stále se učí, že není špatně přiznat si, že mi něco nejde a nestydět se říct si o pomoc, že to děláme všichni
---




--- https://discord.com/channels/769966886598737931/797040163325870092/1121407657258008596
Ahoj! Tady sdilime zaznam z prednasky <@289482229975875584> o tom jak byt dobry mentee a pripravit se na prvni hodinu mentoringu 💪🙂👉 https://www.youtube.com/watch?v=xZJyPeZMl0M
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1148627951630430291
**Tip!** Brzo se budou otvírat podzimní začátečnické kurzy PyLadies. Kdo jste úplně na začátku, pohlídejte si registrace. Kdo už máte něco za sebou (a nemusí to být mnoho!), zvažte koučování. Jak takové koučování vypadá a kolik toho na něj potřebujete umět? Sepsala <@615589948908765206> <:pyladies:842343420420947968> https://ivet1987.wz.cz/2020/03/koucovani-na-pyladies-kurzech/
---


Mentoring guidelines
https://pyvec.slack.com/archives/C1MAJMWTU/p1697534662660139


--- https://discord.com/channels/769966886598737931/769966887055392768/1210520377952829440
> You can ask stupid questions of ChatGPT anytime you like and it can help guide you through to the right answer.
>
> ...
>
> I've had real life teaching assistants who super smart, really great, help you with a bunch of things and on a few things they're stubbornly wrong.
>
> If you want to get good at learning, one of the things you have to do is you have to be able to consult multiple sources and have a sort of sceptical eye.
>
> Be aware that there is no teacher on earth who knows everything and never makes any mistakes.
https://simonwillison.net/2024/Jan/17/oxide-and-friends/#llms-for-learning
---


#} -->
