---
title: Jak na Git a GitHub
description: Co je Git a k čemu se používá? Jaký je rozdíl mezi Gitem a GitHubem? Jak začít s Gitem?
template: main_handbook.html
---

{% from 'macros.html' import lead, note, link_card, blockquote_avatar with context %}

# Git a GitHub

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Tuto stránku Honza právě přepisuje. Je velmi pravděpodobné, že za pár dní tady bude jiný text, lepší, voňavější, nápomocnější.
{% endcall %}

<!-- {% call lead() %}
  Bla bla
{% endcall %} -->

Git je **nástroj, který ti umožňuje sledovat historii změn v kódu, ale kromě toho jej také sdílet s dalšími lidmi**. Je to program, který nainstaluješ do svého počítače a pracuješ s ním v příkazové řádce, nebo jej ovládáš např. prostřednictvím svého editoru. Git se dnes používá skoro v každé firmě. I když jeho výhody nejvíc oceníš při práci ve dvou a více lidech, může ti pomoci i jako jednotlivci: Zálohovat kód svých projektů jinam, synchronizovat jej mezi vlastním počítačem a internetem, na dálku jej někomu ukázat.

## GitHub

[GitHub](https://github.com/) je **úložiště kódu a sociální síť pro programátory**. Kód tam lze poslat pomocí Gitu. GitHub není jediným takovým úložištěm, další jsou např. GitLab nebo BitBucket, ale je nejoblíbenějším pro [open source](../practice.md#zkus-open-source), takže tam najdeš nejvíce projektů a lidí.

## Neboj se ukázat kód!    <span id="showoff"></span>

U začátečníků rozhodně platí, že **nemají co schovávat a měli by světu ukázat co nejvíce toho, co dokázali vytvořit, nebo co zkoušeli řešit**. Můžeš tím jenom získat. GitHub je příhodné místo, kam všechny své projekty a pokusy nahrávat. Zároveň je to místo, kde mají své projekty i všichni ostatní a kde lze spolupracovat s lidmi z celého světa.

Nenech se omezovat strachem, že někdo uvidí tvůj kód a pomyslí si, že nic neumíš. Neboj se mít svůj kód veřejně a ukazovat ho druhým! Tato obava je zbytečnou překážkou ve tvém rozjezdu. Programování je o spolupráci a **GitHub je hřiště pro programátory, kde si každý experimentuje na čem chce.** Čím více tam toho máš, tím lépe. Nejen že se naučíš lépe ovládat Git, ale hlavně budeš moci svůj kód ukázat, když budeš potřebovat [pomoc na dálku](../learn.md#kde-najdes-pomoc). Pokud tě někdo straší, že si tvůj GitHub budou procházet náboráři, [nenech se tím zmást, je to trochu jinak](../candidate-handbook.md#projekty).

## Jak se naučit Git a GitHub    <span id="howto-git-github"></span>

<div class="link-cards">
  {{ link_card(
    'Git a GitHub od základov',
    'youtube.com!watch!v=0v5K4GvK4Gs.jpg',
    'https://www.youtube.com/watch?v=0v5K4GvK4Gs',
    'YouTube kurz Gitu a GitHubu od <a href="http://robweb.sk">yablka</a>.'
  ) }}

  {{ link_card(
    'Nauč se Python',
    'naucse.python.cz!course!pyladies!git!basics.jpg',
    'https://naucse.python.cz/course/pyladies/git/basics/',
    'Nauč se Git z nejznámějších českých materiálů pro Python.'
  ) }}

  {{ link_card(
    'The Missing Semester',
    'missing.csail.mit.edu!2020!version-control.jpg',
    'https://missing.csail.mit.edu/2020/version-control/',
    'Git podle materiálů z americké univerzity MIT.'
  ) }}
</div>

## Projekty

Na inzerát bytu k pronájmu, u kterého nejsou fotky, nikdo odpovídat nebude. Stejně je to i s kandidáty. **Potřebuješ ukázat, že umíš něco vyrobit, dotáhnout do konce, že máš na něčem otestované základní zkušenosti z kurzů a knížek.** K tomu slouží [projekty](../practice.md#najdi-si-projekt). Pokud nemáš vysokou školu s IT zaměřením, kompenzuješ svými projekty i chybějící vzdělání. Snažíš se jimi říct: „Sice nemám školu, ale koukejte, když dokážu vytvořit toto, tak je to asi jedno, ne?“

Říká se, že [kód na GitHubu](../practice.md#github) je u programátorů stejně důležitý, ne-li důležitější, než životopis. Není to tak úplně pravda. U zkušených profesionálů je to ve skutečnosti [velmi špatné měřítko dovedností](https://www.benfrederickson.com/github-wont-help-with-hiring/). Náboráři se na GitHub nedívají, maximálně jej přepošlou programátorům ve firmě. Přijímací procesy mají většinou i jiný způsob, jak si ověřit tvé znalosti, např. domácí úkol nebo test. **Zajímavý projekt s veřejným kódem ti ale může pomoci přijímací proces doplnit nebo přeskočit.** Dokazuje totiž, že umíš něco vytvořit, že umíš s Gitem, a tví budoucí kolegové si mohou rovnou omrknout tvůj kód. Člověk s projekty skoro jistě dostane přednost před někým, kdo nemá co ukázat, zvlášť pokud ani jeden nebudou mít formální vzdělání v oboru.

Konkrétně GitHub s tím ale nesouvisí. Stejný efekt má, pokud kód vystavíš na BitBucket nebo pošleš jako přílohu v e-mailu. Když někdo říká, že „máš mít GitHub“, myslí tím hlavně to, že máš mít [prokazatelnou praxi na projektech](../practice.md#najdi-si-projekt). GitHub je akorát příhodné místo, kam všechny své projekty a pokusy nahrávat. **Nahrávej tam vše a nestyď se za to,** ať už jsou to jen řešení [úloh z Codewars](../practice.md#procvicuj) nebo něco většího, třeba [tvůj osobní web](../candidate-handbook.md#osobni-web-a-blog). Nikdo od tebe neočekává skládání symfonií, potřebují ale mít aspoň trochu realistickou představu, jak zvládáš základní akordy. Budou díky tomu vědět, co tě mají naučit.

Pokud se za nějaký starý kód vyloženě stydíš, můžeš repozitář s ním [archivovat](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/archiving-repositories). Jestliže se chceš nějakými repozitáři pochlubit na svém profilu, můžeš si je tam [přišpendlit](https://github.blog/2016-06-16-pin-repositories-to-your-github-profile/). Výhodou je, že přišpendlit jde i cizí repozitáře, do kterých pouze přispíváš.

{% call blockquote_avatar(
  'Na pohovoru mě nezajímá, co kdo vystudoval, ale jak přemýšlí a jaké má vlastní projekty. Nemusí být nijak světoborné, je to však praxe, kterou ani čerstvý inženýr často nemá.',
  'josef-skladanka.jpg',
  'Josef Skládanka'
) %}
  Josef Skládanka, profesionální programátor
{% endcall %}

Máš-li za sebou nějakou vysokou školu z oboru, ukaž svou bakalářku nebo diplomku. Je to něco, co je výsledkem tvé dlouhodobé, intenzivní práce. Pochlub se s tím!
