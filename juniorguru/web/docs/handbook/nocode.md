---
title: "Low-code, no-code: Jak programovat bez psaní kódu?"
emoji: 🧱
stages: [thinking]
description: TODO
template: main_handbook.html
---

{% from 'macros.html' import link_card with context %}

# Jde to i „bez kódu“

Na spoustu věcí jsou dnes už hotová řešení, polotovary, služby. Některé dělají vše za tebe („No Code“ služby), jiné můžeš zadarmo stáhnout, nainstalovat, zprovoznit („open source“ řešení). Vytvořit dnes od základů obstojný web je práce pro tým profesionálů. Dělá se to zpravidla pouze v případě, kdy má zadavatel speciální požadavky a tedy se mu vyplatí vytvářet něco zcela nového. S největší pravděpodobností nadstandardní požadavky nemáš a **nemá pro tebe smysl se učit programovat kvůli něčemu, co lze za dvě odpoledne „naklikat“**. Používání polotovarů je v IT zcela běžné a dělají to i lidé, kteří by danou věc naprogramovat dokázali:

-   **Je to ekonomičtější.** Není potřeba vymýšlet znovu kolo. Místo stovek hodin práce programátorů se něco jen pokliká, poladí, nastaví, a je to.

-   **Lze to lépe udržovat.** Ať už řešení v počátku nastaví kdokoliv, jeho standardizovaná povaha umožňuje, aby se v něm posléze zorientoval i někdo jiný. Zároveň tvůrci polotovaru vydávají stále nové verze, které např. ošetřují bezpečnostní a jiné chyby.

-   **Je to kvalitnější.** Neplatí jako u vaření, že polotovar je horší, než vlastní výtvor. V tomto případě šéfkuchaři z celého světa roky ladili a vylepšovali něco, co má lákavou barvu, zdravé přísady a vysoké nutriční hodnoty. Všeho je tam tak akorát, aby to chutnalo většině lidí. Sebelepší jednotlivec by těžko dosáhl stejného výsledku.

-   **Je to bezpečnější.** Tady platí předchozí bod dvojnásobně. V oblasti přihlašování, uchovávání hesel apod. není radno vymýšlet nic na koleně, protože je téměř jistá šance, že jednotlivec nedomyslí všechny hrozby. Polotovary mají toto vyřešené dle oborových standardů a pokud se přece jen najde bezpečnostní díra, tvůrci se ji snaží hned zalepit.

Jestliže se učíš programovat a chceš si to na tvorbě e-shopu jen vyzkoušet, tak v pohodě, klidně si do šuplíku programuj vlastní e-shop. Pokud je ale tvým cílem provozovat použitelný e-shop, neprogramuj si jej, nevynalézej kolo, použij něco hotového. Tento web sice chce lidem ukázat cestu k programování, ale ne za každou cenu, z nesmyslných důvodů.

### Tabulky a dokumenty    <span id="nocode-spreadsheets"></span>

Říká se, že **nejrozšířenějším programovacím jazykem na světě jsou vzorečky v Excelu**. Zní to možná jako vtip, ale není to vtip. Možná je zbytečné učit se programovat v něčem jiném, pokud se tvá práce odehrává v tabulkách a odehrávat se v nich ještě dlouho bude. Nauč se pořádně vzorce, makra, funkce. Excel je velmi silný nástroj a jeho dobrá znalost se ti nikdy neztratí. I pokud budeš chtít později přejít k „opravdovému“ programování, znalost maker apod. ti bude sloužit jako základ, na kterém budeš moci stavět.

Podobně se dá udělat velká paráda i s [Google Apps Script](https://www.google.com/script/start/) a automatizací Google dokumentů, které mají tu výhodu, že jsou online a mohou v sobě snadněji propojovat živá data jinde z internetu (např. aktuální kurzy měn).

### Automatizace    <span id="nocode-automation"></span>

Pokud by se ti hodilo **propojit různé internetové služby tak, aby si podle nějakého scénáře automaticky posílaly informace**, i na to existují hotové nástroje. Můžeš třeba pokaždé, když se objeví platba na tvém bankovním účtu, uložit zůstatek do tabulky a následně si ještě nechat poslat zprávu na mobil. V mluvě velkých firem se tomu říká [RPA](https://cs.wikipedia.org/wiki/Robotick%C3%A1_automatizace_proces%C5%AF) a prý je po tom dnes celkem poptávka. Následující služby umožňují takové scénáře programovat klikáním, přetahováním kurzorem a vyplňováním formulářů, tedy zcela bez psaní kódu v tradičních programovacích jazycích.

<div class="link-cards">
  {{ link_card(
    'Make',
    'https://www.make.com/',
    'Největší platforma, podporuje i české služby jako Fakturoid nebo Fio Banka.'
  ) }}

  {{ link_card(
    'Zapier',
    'https://zapier.com/',
    'Druhá nejznámější platforma pro automatizaci.'
  ) }}

  {{ link_card(
    'IFTTT',
    'https://ifttt.com/',
    'Alternativa pro ty, kterým nesedí Integromat ani Zapier.'
  ) }}
</div>

### Tvorba webu, e-shopu    <span id="nocode-websites"></span>

Jestli chceš psát blog, provozovat e-shop nebo vytvořit webovky pro květinářství kamarádovy tety, **nemusíš se nutně učit programovat**. Najdi vhodnou No Code platformu nebo se nauč pracovat s nějakým open source řešením. Obojího je dnes neskutečné množství, ale tady jsou alespoň tři tipy na ty nejpoužívanější:

<div class="link-cards">
  {{ link_card(
    'WordPress',
    'https://wordpress.com/',
    'Nejpoužívanější hotové řešení na weby. Služba za peníze, ale i open source ke stažení.'
  ) }}

  {{ link_card(
    'Wix',
    'https://www.wix.com/',
    'Služba, kde si web vytvoříš klikáním. Jednodušší, ale ne tak univerzální jako WP.'
  ) }}

  {{ link_card(
    'Shopify',
    'https://www.shopify.com/',
    'Celosvětově nejpoužívanější služba pro vytváření vlastního e-shopu.'
  ) }}
</div>

### Skládat z dílů nebo programovat?    <span id="nocode-vs-code"></span>

K čemu je dobré umět programovat věci od základů, když už polotovary existují na vše podstatné? **Představ si běžné programovací jazyky jako auto a hotová řešení jako MHD.** Auto je drahé, musíš jej řídit, parkovat a pečovat o něj, ale umožní ti jezdit přesně tak, jak chceš. Jezdit autobusem sice vyžaduje rozumět systému jízdenek a přesedat mezi spoji, ale i tak je to levné, jednoduché a dostatečně efektivní pro spoustu lidí. Pokud nevezeš náklad, je neekonomické jezdit autem trasu, která je dobře obsluhovaná MHD.

Stejně tak je nesmysl, aby někdo od základů programoval fotogalerii pro kosmetický salon. Ale pak jsou tady Alza nebo Rohlík, které se s běžným řešením nespokojí. Velký, složitý, nebo jinak unikátní byznys zaměstná i celý tým programátorů, kteří vše vyvíjí na míru. **Úspěšnou kariéru přitom můžeš udělat v obou případech.** Specialista na WordPress, jenž umí skládat weby z velkých dílů, se uživí stejně dobře jako PHP programátorka, která umí ty díly vytvořit.

Tento web je o tom, jak se naučit software vyrábět od základů, takže další tipy už budeš muset najít jinde. Pokud se vidíš spíš mezi polotovary než u psaní kódu, zkus se na další informace poptat třeba na fóru [Webtrh](https://webtrh.cz/).
