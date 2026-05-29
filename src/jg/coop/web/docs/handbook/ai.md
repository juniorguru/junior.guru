---
title: Programování s AI
emoji: ✨
stages: [thinking, trying, learning, creating]
description: TODO
template: main_handbook.html
---

{% from 'macros.html' import lead, note with context %}

# Programování s AI

{% call lead() %}
...
{% endcall %}

{% call note(standout=True) %}
  {{ 'exclamation-circle'|icon }} Kapitola se teprve připravuje.
{% endcall %}


<!-- {#


--- https://discord.com/channels/769966886598737931/769966887055392768/1182391116629286923
Do nedávna byla při programování klíčová schopnost efektivně googlit. Může to vypadat banálně ale umět efektivně googlit se člověk učil roky. Teď bude při programování klíčová schopnost efektivně využívat AI.
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1179302149537140836
<:python:842331892091322389> Mnozí se už přesvědčili, že AI může být extrémně nápomocné, ale zároveň je to občas boj, aby dělalo to, co chceme. Tady je nejen skvěle popsáno, jak toto konkrétní GPTs tvořili, ale hlavně je to zaměřené na pomoc a vysvětlování Pythonu. <:python:842331892091322389>

https://www.linkedin.com/posts/nancyebain_meet-pypilot-a-customgpt-case-study-activity-7134904613622706176-eZ_W
---


--- https://discord.com/channels/769966886598737931/916339896963190785/1192738348998082611
Pokud používáte nějakého AI asistenta při psaní kódu, tak je jistá šance, že bude méně bezpečný a zároveň budete věřit, že je bezpečnější než kdybyste AI nepoužívali https://arxiv.org/abs/2211.03622
---


--- https://discord.com/channels/769966886598737931/1191365076188397591/1192218179880095764
U te diskuze ohledne AI bych vicemene souhlasil se vsemi zucastnenymi.
Ano, jeji podstatou je efektivita. Ta ale v kazde fazi znamena neco jineho.
Kdyz se ucim stavarinu, ochotne mi poradi, jak vypada cihla, proc malta lepi a jak tuhne beton. Odstranim zaseky, kdy nevim jak dal a zvysim efektivitu UCENI. Netroufl bych si ji ale jeste pozadat navrhnout cely dum.
Kdyz uz ale vim, jak se chova cihla, malta a beton, pomuze mi poskladat modulove patrove domy. Odstrani hodiny skladani a pocitani cihel a betonovych konstrukci. Zase to bude efektivita, ale uz efektivita PRACE
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1194549501982163057
Jen tak na okraj kdo je STUDENT? Nebo dokonce i učitel, tak má COPILOT z GITHUBU ZADARMO!!! Šiřte to dál.
https://github.blog/2022-09-08-github-copilot-now-available-for-teachers/
---


https://www.fakturoid.cz/almanach/osobni-rozvoj/jak-pouzivat-chatgpt


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


I regret to say it, but it's true: most of today's programming consists of regurgitating the same things in slightly different forms. High levels of reasoning are not required. LLMs are quite good at doing this, although they remain strongly limited by the maximum size of their context. This should really make programmers think. Is it worth writing programs of this kind? Sure, you get paid, and quite handsomely, but if an LLM can do part of it, maybe it's not the best place to be in five or ten years.
...
Finally, what sense does it make today not to use LLMs for programming? Asking LLMs the right questions is a fundamental skill. The less it is practiced, the less one will be able to improve their work thanks to AI. And then, developing a descriptive ability of problems is also useful when talking to other human beings. LLMs are not the only ones who sometimes don't understand what we want to say. Communicating poorly is a great limitation, and many programmers communicate very poorly despite being very capable in their specific field. And now Google is unusable: using LLMs even just as a compressed form of documentation is a good idea. For my part, I will continue to make extensive use of them. I have never loved learning the details of an obscure communication protocol or the convoluted methods of a library written by someone who wants to show how good they are. It seems like "junk knowledge" to me. LLMs save me from all this more and more every day.
http://antirez.com/news/140


--- https://discord.com/channels/769966886598737931/789087476072710174/1215242926485929994
Návod, jak používat ChatGPT jako svého mentora: https://realpython.com/chatgpt-coding-mentor-python/
---


--- https://discord.com/channels/769966886598737931/1217484087065968684/1219223656895348797
Tak jsem se Devin AI podíval pořádně na zoubek a zatím bych se držel Copilota a ChatGPT. 🙂

Věřím, že průměrný junior tady odsud by podával lepší výsledky než DevinAI!

Tady je o tom příspěvek, lajkujte, sdílejte dle libosti. 🙂
https://www.linkedin.com/posts/bleedingdev_problems-with-devinai-activity-7175429487478603776-5CCS
---



AI: https://www.linkedin.com/posts/marketa-willis_je-opravdu-ai-takov%C3%BD-pomocn%C3%ADk-v-programov%C3%A1n%C3%AD-activity-7215986228007989248-Sh-p?utm_source=share&utm_medium=member_desktop


--- https://discord.com/channels/769966886598737931/1279530837452263435/1279531421178007633
A práve preto si myslím, že tu môžu excelovať aj začínajúci programátori - je to totiž znova viac o premýšľaní a soft skilloch ako o hard skilloch - tie sa začnú do popredia dostávať až za pár rokov, až obor maturuje a bude jasné, čo je potrebné a čo nie - dnes to jasné nie je, môžeme iba hádať.

Pokiaľ by sa do toho teda chcel niekto pustiť, tu je pár tipov čo si pridať do portfólia - a pozor, tu si myslím, že tieto úlohy dokážu pomôcť aj u iných pozícii nielen u AI specialistov. Niektoré firmy dnes na AI proste počujú. Skúsim to popísať čo najviac jazykovo neutrálne ale najfrekventovanejší jazyk v AI svete je asi python a sám z toho sveta pochádzam, preto si dovolím túto skupinu aj tagnúť <@&1085220736957947905> .
- prečítajte si niečo o písaní technických promptov, u všetkých úloh budete model inštruovať, čo má robiť. Nevenujte tomu ale priveľa času. Inšpirujte sa ako to robia iný - existujú napr leaknute system prompty od Applu, oficálne ich publikuje aj spoločnosť Anthropic.
- osahajte si OpenAI API - dnes to už skoro nič nestojí, do začiatku dostanete aj nejaký budget na voľné testovanie
- následne sa pozrite na to, ako sa dnes stavajú konverzácie - aký je rozdiel medzi správou uživateľa a asistenta, čo sú to systémové správy - a následne si nejaké konverzácie sami postavte
- a teraz sa dostávame k prvému veľkému pojmu sveta AI: RAG (Retrieval-augmented generation). Pozrite sa na to, čo to je, ako to funguje.
- naimplementovať RAG bola kedysi zložitá úloha. Vy sa ale pozriete na to, ako využiť OpenAI API pre asistentov - konkrétne funkcionalitu Vector Stores
- keď už budete skúmať API pre asistentov pozrite sa aj na ostatné funkcionality - code interpreter a function calling
---


--- https://discord.com/channels/769966886598737931/1279530837452263435/1279531508931100694
Tieto funkcionality boli ešte rok a pol dozadu celý programátorský tým a tisícky riadkov kódu. Dnes je to jedno API, jeden balíček v Pythone alebo inom jazyku. Postavte si na tomto svoje portfólio projektov a skúste demonštrovať rôzne využitia týchto funkcií v svete, ktorý poznáte. Príklady:
- unstructured to structured - stiahnite si sadu nejakých neštruktúrovaných formátov dát - články z internetu, texty atď - preveďte tieto dáta do štruktúrovanej podoby - nechajte AI určiť titulok, zakategorizovať, vyťiahnuť osoby, miesta, určiť sentiment atď. Tieto úlohy sú veľmi populárne a užitočné
- vymyslite jednoduchú automatizáciu procesu na ktorej demonštrujete svoju komplexitu - na vstupe máte nejaký formát, ten môžete nejako transformovať, niečo z toho programaticky vybrať, nechať to spracovať modelom a následne dostať nejaký pekný výstup - napr. sledujete obľúbené newslattery ale nemáte čas všetko čítať - preto by ste chceli pocníka, ktorý to prečíta za vás a vyberie 5 pre vás najrelevantnejších informácii. Na môžete demonštrovať, že si dokáže scrappnuť stránku, nastaviť prompt a celé to poskladať dokopy.
- postavte si chatbota alebo asistenta - zamerajte ho na niečo, vytvorte si vektorovú databázu - napr. máte vlastné recepty v 50 rôznych PDF. Vytvorte si asistenta, ktorý vám bude navrhovať recepty na základe surovín a vďaka RAGu bude poznať aj tie vaše :).
- nefixujte sa iba na chatbotov - ako sa ukazuje prázdne chatovacie okno je vlastne veľmi špatný frontend pre väčšinu use casov - väčšina ľudí netuší čo tam zadať. Pripravte funkciu, ktorá na vstupe dostane text a na výstupe vráti sumarizáciu. Ako parametre príjma dĺžku sumarizácie (stručná/podrobná), tón (formálna/neformálna), typ (súvislý text, v bodoch) atď. Pokiaľ vás bavia maličké aplikácie vytvorte si jednoduchý frontext napr v dashi alebo streamlite.
---


--- https://discord.com/channels/769966886598737931/788826407412170752/1279530837452263435
Ahojte,
vopred sa ospravedlňujem, tento post bude dlhý. Dúfam ale, že to dá podrobnejší vhľad do AI ako oboru v IT. Mám za sebou 2 mesiace od momentu, keď som svoju kariéru poslal all in do segmentu AI. Mojou prácou sa stalo hľadanie hodnoty rôznych AI riešení pre našu banku a ich privádzanie k životu. Už dlhšie som tu chcel spísať svoje myšlienky a hlavne svoje myšlienky k otázke: **Som ašpirujúci junior v IT, čo pre mňa znamená smerovať svoju kariéru do oboru AI a má to zmysel?**

Hneď na začiatok by som rád poďakoval <@668226181769986078>, vďaka ktorému som objavil Simona Willisona, ktorý o AI veľa píše a veľa hovorí a to čo píše a hovorí je veľmi rozumné :). A okrem toho prednášal aj na PyConUS:
https://youtu.be/P1-KQZZarpc?feature=shared&t=247.
Ak sa chcete dozvedieť, kde sa obor umelej inteligencie nachádzal v květnu 2024 (+- je to stále platné aj pre srpen 2024) dajte si tento talk, je to pre ľudí z IT, ktorý sa ale AI nevenujú, ten najlepší status ktorý som zatiaľ našiel.

Prečo na to odkazujem? Pretože sú to závery veľmi podobné tým, ktoré aktuálne vyvodzujeme aj my v banke. Za prvé je vďaka tomu možné vyvodzovať, čo by sa ašpirujúci junior potreboval naučiť (o tom neskôr) a za druhé, je dôležité uvedomiť si, že pokiaľ sa dostanete do tém, ktoré je možné zhrnúť v 40 minútovom talku, budete patriť medzi 5% najlepších v obore :). Na prvý pohľad odvážne tvrdenie, treba si ale uvedomiť o akom obore sa bavíme.

Keď sa dnes budete baviť s ľuďmi, ktorý o sebe deklarujú, že sa venujú alebo zaujímajú o AI dozviete sa pravdepodobne: Že používajú ChatGPT, že im naplánoval výlet, pripravil recept alebo zhrnul novinový článok. Z pohľadu práce sa možno dozviete o tom, že im zosumarizoval alebo napísal email, preložil text alebo pomohol vybrainstormovať názov udalosti. A tieto odpovede boli u väčšiny ľudí rovnaké mesiac po tom, čo ChatGPT vyšiel a dnes. Existujú ale aj use casy, ktoré prinášajú obrovskú hodnotu a tu môžete aj ako junior excelovať.

A viac vo vlákne 🙂
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1250701548015849492
Mám tady dvě věci na věčné téma AI a programování. Jedna je tenhle krátký příspěvek: https://mamot.fr/@ploum/112591341366625479
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1250701886185672774
Druhá je strašně dlouhý článek, který má argumentovat, že ne, AI fakt programátory nenahradí. Ale ještě jsem ho nestihl celý přečíst. https://stackoverflow.blog/2024/06/10/generative-ai-is-not-going-to-build-your-engineering-team-for-you/
---


--- https://discord.com/channels/769966886598737931/1177266646579163246/1312718422425079810
Odpověď na rebelskou otázku je za mě, že to musíš umět, abys ses mohla správně ptát AI a kontrolovat/vybírat z toho, co ti vytváří. U věcí, kde na tom nezáleží a nerozumím tomu (jednoduchá automatizace v PowerShellu), klidně nechám AI vygenerovat v podstatě všechno, ale když se bavíme o produkčním kódu, tak tomu rozumět dost pomáhá.
A ne, není špatně odpovídat na řečnické otázky. 😉
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1341174664692498553
> We’re trading deep understanding for quick fixes, and while it feels great in the moment, we’re going to pay for this later.
https://nmn.gl/blog/ai-and-learning
---


--- https://discord.com/channels/769966886598737931/806621830383271937/1337160739550527548
Hraju si s AI a mapováním codebase a musím říct, že jsem fakt mile překvapen, jak rychle se jeden může dneska dostat do projektu, když použije AI.

1. Konvertujte repozitář na *AI friendly formát*, např. pomocí Repomix (https://repomix.com/)
2. Použijte Gemini 2.0 Pro na AI Studio (https://aistudio.google.com/)
3. Vložte celý markdown vaší codebase. Limit je **až 2 miliony tokenů**, což je fakt dost (pro srovnání ChatGPT má 10x méně!)
4. Ptejte se.

Kdyby se někdo chtěl podívat na příklad, tak tady je (snad vám půjde načíst konverzace s Gemini - nejspíš musíte být přihlášeni).
https://drive.google.com/file/d/1DgGLqlgjHVbS-tcHYbDYe6yE5Jeddqu-/view?usp=sharing
https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221TIN5E3Tjyd-oDVaUHwu1w0Ks-nAAPTdS%22%5D,%22action%22:%22open%22,%22userId%22:%22116194854355489944248%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1327170061894418452
> While AI-Assisted coding can get you 70% of the way there (great for prototypes or MVPs), the final 30% requires significant human intervention for quality and maintainability.
https://addyo.substack.com/p/the-70-problem-hard-truths-about
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1394319792726605907
Hele hele 🙂 https://medium.com/@kt149/github-ceo-says-the-smartest-companies-will-hire-more-software-engineers-not-less-as-ai-develops-17d157bdd992
---


--- https://discord.com/channels/769966886598737931/788832177135026197/1390795782306660575
Jak promptovat ChatGPT, aby vás učilo 🧑‍🏫 https://gist.github.com/Dowwie/5a66cd8df639e4c98043fc7f507dab9e
---


--- https://discord.com/channels/769966886598737931/789087476072710174/1379089534985310278
Tak za mě supr, ale dokumentace to moc není, ono to projede celý commit, sepíše co se událo, rozepíše všechny stránky, layouty, komponenty, store, objekty a jejich typizace, input validátory,  parsování, použité nástroje jako Eslint atd., dokonce i package.json verze jeho balíčků, dokonce i dotazy na DB, no úplně komplet !   😄  A na všechno vytvoří recenzi = doporučení zlepšení, zabezpečení ( XSS zranitelnosti )  ukázky vylepšení kódů, wow. Vlastně takový validátor celého projektu. Popravdě je toho tuna na co bych se měl podívat a vše vypadá aspoň za zkouknutí, nejsou to úplné blbosti.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1363734255531987084
Čert aby se v tom vyznal 😀 Jeden tvrdí to, druhej něco jiného. Jeden podporuje juniory, druhý je odrazuje kvůli AI, atd. Tak alespoň jeden povzbuzující článek po ránu 🙂 https://www.vzhurudolu.cz/blog/258-ai-programovani-psani
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1361396017810898975
https://www.joshwcomeau.com/blog/the-post-developer-era/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1360212807135789106
Zajímavý článek o AI a potřebě programátorů.
Zaujal mě Jevons Paradox, ten jsem nikdy neslyšel. Je to ekonomické pravidlo, že vyšší efektivita využívání zdroje vede paradoxně k vyšší, spíše než nižší spotřebě.
A tady se mluví o spotřebě vývojářů <:meowthumbsup:842730599906279494>

https://www.infoworld.com/article/3955073/ai-will-require-more-software-developers-not-fewer.html
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1356184716683907092
🎙️ Kdo jste ještě neslyšel <@668226181769986078> na Lupa, tak šup https://www.lupa.cz/clanky/honza-javorek-junior-guru-jenom-clovek-vam-rekne-co-chatgpt-poradil-spatne
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1401950840411132035
Raději sem hodím tohle, co mi poslal <@156884455628341249> jako námět k plánovanému https://discord.com/channels/769966886598737931/1375466381801291918: OpenAI má nově mód na studium https://simonwillison.net/2025/Jul/29/openai-introducing-study-mode/
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1401986878592520344
Teda:
**1. Jak využít AI jako pomocníka při učení se samotnému programování.**
Keď už, prikláňam sa hlavne k chatbotom, vyskúšať si rôzne služby, kde mi ten výklad najviac vyhovuje. Nenechávať chatbota nech za mňa primárne rieši problémy ale robí mi trochu rubber duck pre rôzne dotazy. Ten nový study mode v ChatGPT mi na toto príde veľmi dobrý do chvíle, kým sa naučím postaviť si vlastný prompt.

Na druhej strane mám trochu pocit, že AI sa na začiatku tohto procesu používa až príliš. Chápem, že na začiatku mi ako switcherovi príde každá otázka hlúpa ale od toho takéto komunity existujú. Otázky ako akým smerom sa kariérne vydať, čo študovať, ma čom pracovať, aké projekty zvoliť, feedback na tieto projekty mi prídu ako otázky ktoré si priam žiadajú aby to videl nejaký človek.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1401986922598895757
**2. Jaké znalosti AI asistentů by měli mít juniorní vývojáři, kteří dnes nebo za 6–12 měsíců budou shánět práci?**
Hlavne hands on :). Keď človek s AI nikdy nepracoval (alebo nepracoval "pracovne", iba rekreačne) je podľa mňa jedno kde človek začína, to prvé čo si musím vybudovať je nejaký cit na to, ako sa pýtať, kde sú tie hranice, v čom je AI dobrá v čom nie. A postupne sa posúvať v tom využívaní tak, aby som vždy mal nejaký cit na to, či danej odpovedi verím alebo nie. Príklad: keď si prvý deň otvorím ChatGPT a napíšem, aby mi vytvoril nejakú aplikáciu a vygenerujem si kód, pravdepodone nemám šajn na čo sa práve pozerám. Keď sa učím for cyklus a nechám si vygenerovať príklad na využitie for cyklu alebo sa začnem pýtať na to, či môžem v pythone iterovať cez list, tu už zrejme mám nejaký mentálny model na posúdenie toho, na čo sa pozerám. Týmto systémom by som pristupoval aj k ďalším nástrojom, po pár mesiacoch skúsiť napríklad Github Copilot, nechať si niečo autocompletnuť, nechať si vytvoriť nejaký kód, niekde o niečom pochatovať. V chvíli keď mám pocit, že sa dejú veci ktorým nerozumiem alebo ich nie som schopný posúdiť, pravdepodobne AI preťažujem a mal by som sa niečo doučiť.
---


--- https://discord.com/channels/769966886598737931/1400035170874163272/1400066973206839296
Myslim si, ze pri praci s AI je nutne pouzivat kriticke mysleni a nebrat kazdou odpoved jako automaticky spravnou. Jak pise Wewa, clovek musi rozumet tomu, co dela. A nejsem si jisty, do jake miry je toho schopny zacatecnik, ktery se to teprve uci. Nekomu to pujde, jinemu ne. Uz jsem tu videl pripady, kdy na dotaz pri code review "proc jsi to napsal takhle" padla odpoved "nevim, poradil mi to ChatGPT".

Nejde ale jen o "spravnost" odpovedi – i lidsky mentor muze naucit studenta nesmysly. Rozdil je v tom, ze clovek umi rict "nevim" nebo "nejsem si jisty", zatimco od AI jsem nic podobneho zatim nevidel.

Dalsi vec je, ze proces uceni podle me neni o tom co nejrychleji najit odpoved, ale dojit k ni vlastnimi silami. A prave to LLM dost komplikuji. Jiste, da se napsat prompt tak, aby LLM vedlo uzivatele spravnym smerem, ale zatim je porad mnohem, mnohem jednodussi pouzivat tenhle nastroj spatne.

A nakonec jeste jedna vec, ktere si vsimam – nekteri lide si pochvaluji, jak skvele se uci s pomoci LLM, ale jeste od nich nikdo nevidel ani radek kodu. Nejenze tak nikdo nevi, co se vlastne naucili, ale navic se diky interakci s LLM casto vyhybaji komunikaci a sdileni kodu s ostatnimi programatory – a tomu se v realne praci nevyhnou.
---


--- https://discord.com/channels/769966886598737931/1400035170874163272/1400207237024317500
1) Jak by měl switcher pracovat s AI?
Podle mě by člověk – hlavně na začátku – měl AI využívat jako parťáka k diskuzi. První věc, která mu může opravdu pomoct, je vytvořit si myšlenkovou mapu: co ho baví, kam by chtěl směřovat, jaké má cíle atd. Už jen to, že si to může probrat s AI, mu pomůže zformulovat, co by měl umět a jakým směrem se vydat – jaký jazyk, framework nebo oblast. Úplný nováček totiž často vůbec netuší, co všechno IT obnáší – kolik je technologií, jazyků, frameworků, pozic – a bez mentora v tom snadno tápe.

Další krok je využívat AI jako mentora. A tady je důležitá poznámka: každý by měl znát základní principy práce s AI. Modely jako ChatGPT jsou trénované tak, aby vás vždy podporovaly – bývají málo kritické, často halucinují a neověřují fakta. Takže i když jde „jen“ o konverzaci s AI, je zásadní mu nastavit pravidla. To je kapitola sama o sobě, ale už jednoduché instrukce jako „buď kritický“, „ověřuj fakta“, „používej progresivní myšlení“ dokážou výrazně zlepšit kvalitu odpovědí.

Jako mentor je AI nejpřínosnější právě na začátku, kdy dokáže skvěle vysvětlovat. Ale je potřeba mít na paměti, že AI čerpá pouze z dostupných dat. Jednoduše řečeno – co není na Googlu, AI neví (ber to s nadsázkou). Když řešíš dokumentaci Pythonu, nejspíš ti odpoví správně. Ale pokud se ptáš na něco, co vyšlo minulý týden, je dost možné, že to AI vůbec neví. Čím unikátnější je dotaz, tím víc je potřeba si výstupy ověřovat.

A nakonec – pokud switcher nemá moc času, doporučuju používat voice assistenta. Já ho využívám často na cestách, když nemůžu psát, nebo když se připravuju na pohovor. Úroveň češtiny je už dost dobrá na to, aby šlo simulovat technické kolo podle inzerátu, mých dovedností a profilu lidí, kteří se ho budou účastnit. Nebo si jen procvičuju otázky a odpovědi a dostávám realtime feedback.
---


--- https://discord.com/channels/769966886598737931/1400035170874163272/1400207248747139335
2) Tohle je hodně tenký led – každý by si měl ujasnit pár základních věcí:
1. Všemu, co AI vygeneruje, musím rozumět.
Musím být schopný to napsat z hlavy a chápat, co ten kód dělá. Pokud ne, dostávám se do fáze, kdy sice chápu výstup, ale přicházím o “svalstvo”, které jako junior potřebuju budovat.

2. Nástroje jako CodeRabbit nebo review agenty dokážou hodně pomoct.
Spousta juniorů ani neví, co je to PR nebo code review. AI to sice úplně nenahradí, ale může ukázat chyby a návrhy ještě dřív, než se na to podívá senior. Ještě silnější je propojit AI s kontextem celého projektu. Příklad: začínám s backendem, prošel jsem si pár crash kurzů a začínám psát. Nechávám si zkontrolovat kód, dostávám doporučení podle best practices a vedu diskuzi – proč se to píše takhle, jaká je běžná konvence, co je čisté, co se nedoporučuje atd.

Můj osobní problém jako juniora byl ten, že každý učil jinak a často jsem netušil, co je standard a co už je špatná praxe. AI mi pomáhá tím, že vysvětlí důvody a dodá širší kontext.

3. AI je nástroj na zrychlení a pochopení – ne na obejití učení.
To, že člověk musí napsat 10 000 řádků kódu, aby pochopil základy, prostě nejde obejít. Stejně jako ve sportu nebo vaření – bez opakování, praxe a zpětné vazby se nikam neposuneš. AI ti pomůže cestu zrychlit a zpřehlednit, ale neprojde ji za tebe.

Je tady ale dobrý point od  <@708265650619154521>
AI nám sice pomáhá urychlit řešení problémů, ale zároveň nás může připravit o ten klasický vývojový moment, kdy máš problém, najdeš na internetu podobné řešení a při jeho přizpůsobování se naučíš spoustu věcí kolem.
A teď otázka – je lepší 5 hodin řešit jeden problém a při tom se naučit několik věcí navíc, nebo to s pomocí AI vyřešit za 30 minut a mít 4,5 hodiny na učení něčeho dalšího? Možná záleží na tom, jak efektivně ten čas dokážeš využít.

Těch věcí, které by se k tomu daly říct, je určitě na celé večery. Tohle je jen základ, co mě teď napadl.
---


https://honzajavorek.cz/blog/empowered-by-ai-why-junior-devs-have-the-winning-edge/
https://antirez.com/news/154


--- https://discord.com/channels/769966886598737931/1401948283361955940/1413861490267656324
🤔 https://mikelovesrobots.substack.com/p/wheres-the-shovelware-why-ai-coding
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1409879838650798090
btw, tohle tu proběhlo? (už je to docela staré)
https://www.hrnews.cz/lidske-zdroje/trendy-id-148711/od-unora-plati-povinnost-skolit-zamestnance-na-pouzivani-ai-id-4453113
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1434890300299546674
https://blog.sshh.io/p/how-i-use-every-claude-code-feature
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1431978892201164881
Dobrý video https://youtu.be/-uW5-TaVXu4?si=8mfgjOPj8tS0oncP
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1432688524607619132
mam to tam vsude mozne:

```
...
Your primary mission is to identify and eliminate code duplication, unnecessary abstraction, and over-engineering while ensuring solutions remain maintainable and readable.
...
**Core Analysis Framework:**
1. **Duplication Detection**: Scan for repeated logic, similar functions, or redundant code patterns that violate DRY principles
2. **Abstraction Assessment**: Identify unnecessary layers, over-generalized interfaces, or premature optimization that adds complexity without clear benefit
3. **KISS Evaluation**: Determine if the solution is as simple as possible while still solving the problem effectively
4. **Necessity Audit**: Question every line, function, and component - if it doesn't directly contribute to the core functionality, flag it for removal
...
- For each piece of code, ask: "Is this the simplest way to achieve this goal?"
...
- Recommend removing code rather than adding it when possible
- Ensure any suggested abstractions have clear, immediate benefits
...
```
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1422482844336390184
https://workweave.dev/blog/hiring-only-senior-engineers-is-killing-companies
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1422809502096556072
Tak už vím/umím formulovat, co mě jako starého pardála na AI nejvíc deptá.
> human review, testing, and integration needs will remain. And that is a lot harder when the code has been written without the human thinking about it
AI bleskově vygeneruje kód, já ho musím projít, ale je to obtížné, když přeskočím tu fázi, kdy jsem nad řešením sám přemýšlel.
https://chrisloy.dev/post/2025/09/28/the-ai-coding-trap
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1457232037697290407
teda na konci je promo na další jeho video ale jinak celkem make sence :)) 😄 https://www.youtube.com/watch?v=MjSUCg2NN4g
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1450997661145501798
> I’ve been watching junior developers use AI coding assistants well. Not vibe coding—not accepting whatever the AI spits out. Augmented coding: using AI to accelerate learning while maintaining quality. [...]
> 
> The juniors working this way compress their ramp dramatically. Tasks that used to take days take hours. Not because the AI does the work, but because the AI collapses the search space. Instead of spending three hours figuring out which API to use, they spend twenty minutes evaluating options the AI surfaced. The time freed this way isn’t invested in another unprofitable feature, though, it’s invested in learning. [...]
> 
> If you’re an engineering manager thinking about hiring: The junior bet has gotten better. Not because juniors have changed, but because the genie, used well, accelerates learning.
— [Kent Beck](https://en.wikipedia.org/wiki/Kent_Beck), [The Bet On Juniors Just Got Better](https://tidyfirst.substack.com/p/the-bet-on-juniors-just-got-better)
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1450999030669901865
A tohle mi přijde taky dobrý (stejně jako předchozí i tenhle citát jsem našel na blogu Simona Willisona). Mrk na <@558352510914658335> a <@788486062430355497> 
> If the part of programming you enjoy most is the physical act of writing code, then agents will feel beside the point. You’re already where you want to be, even just with some Copilot or Cursor-style intelligent code auto completion, which makes you faster while still leaving you fully in the driver’s seat about the code that gets written.
> 
> But if the part you care about is the decision-making around the code, agents feel like they clear space. They take care of the mechanical expression and leave you with judgment, tradeoffs, and intent. Because truly, for someone at my experience level, that is my core value offering anyway. When I spend time actually typing code these days with my own fingers, it feels like a waste of my time.
— [Obie Fernandez, What happens when the coding becomes the least interesting part of the work](https://obie.medium.com/what-happens-when-the-coding-becomes-the-least-interesting-part-of-the-work-ab10c213c660)
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1449836454237835389
tohle je zajímavý článek o tom, jak někdo využil agenty a vytvořil s nimi knihovnu, která má bezkonkurenční parametry a lidem by zabralo neskutečné množství času a úsilí ji vytvořit. ale zároveň to nebylo že by si něco „upromptnul“ a bylo by to. navrhnul, jak to má fungovat a jakou to má mít architekturu a dal těm agentům hromady testů, kterými se řídili a díky kterým věděli, jestli je výsledek správně nebo špatně. vytvoření knihovny mu trvalo měsíce a využil u toho hromadu klasických programátorských znalostí https://simonwillison.net/2025/Dec/14/justhtml/
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1472690519166681329
Tohle jsem ještě nečetl, ale podobné téma 🙂 Od Lucie L. https://www.lucielenertova.cz/p/84-vyvojaru-uz-pouziva-ai-ma-smysl
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1472248917017231611
Co si myslíte o tomto? https://engeto.cz/blog/kariera/it-trh-2026-komplexni-pruvodce-pro-juniory/
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1460229003444228254
> Yes, maybe you think that you worked so hard to learn coding, and now machines are doing it for you. But what was the fire inside you, when you coded till night to see your project working? It was building. And now you can build more and better, if you find your way to use AI effectively. The fun is still there, untouched.

https://antirez.com/news/158
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1508781673146351746
Jak s AI psát lepší kód, pomaleji 🙂 https://nolanlawson.com/2026/05/25/using-ai-to-write-better-code-more-slowly/
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1506216459687297094
Claude Code umí přes `/config` nastavit *Preferred output style*, jednou z možností jsou *Explanatory* nebo *Learning*. Není to teda novinka, je to tam už dlouho, ale řekl jsem si, že by se to tu mohlo někomu hodit. Třeba při dělání květnové výzvy 😉 https://discord.com/channels/769966886598737931/789046675247333397/1502010921328050436
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1504830281608204459
Největší slabiny juniorních projektů oproti praxi jsou:

- malá nekomplexní neprodukční codebase
- a nula zkušeností s prací, organizací práce a komunikací v týmu.

Junior ale nemůže udělat víc, než si zajistit nějaké vlastní projekty, takže to firmy berou jako dobrý začátek. Pokud má někdo zkušenost se spoluprací v týmu nebo na větší codebase, třeba na open sourcu nebo nějakém dobrovolnickém projektu, je to velký a významný bonus, ale je tak těžké se kolem něčeho takového vyskytovat, že to po lidech nelze vyžadovat a nastavovat takhle laťku.

A moje pointa: Ani jedno z toho ti AI nedá. Takže podle mě ti to nijak nepomůže obejít komerční praxi. Jasně, můžeš vyrobit vlastní funkční produkt a nahodit ho, ale to je vlastně jiná disciplína, než práce programátora 🙂 To se bavíme o nějakém produktovém nebo podnikatelském myšlení. Pokud to někde ocení, bude to plus, ale pro práci programátora v tradičním slova smyslu to je podle mě bonusová věc do boku, ne něco, u čeho by si při náboru řekli: „jo tak když si dokázal udělat vlastní appku a na app storu ji už používá 10 lidí, tak to asi zvládne pracovat na našem produktu o 400.000 LOC (lines of code) a komunikovat v týmu 10 lidí přes Slack, Jiru, a koordinovat se s kolegama...“, to podle mě nefunguje.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1502274900537380976
https://zdrojak.cz/clanky/ai-rozbila-juniorskou-cestu-k-seniorite-kod-vznika-rychleji-zkusenost-pomaleji/
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1501224147659919402
Zaujímavé čtení 🙂 Jak jsem to tak pročítal napadala mě spousta věci. Skúsim z toho vybrať a zdôrazniť to, čo mi príde, že tu málo rezonuje. Vopred deklarujem, že sa na to pozerám z pohľadu skôr produktovo orientovaného človeka, z bankového prostredia a môj job je spojený s AI a jej využívaním radovými ne-IT zamestnancami.

Podoepisuju, že externé prostredie je overhyped, v rozhodovaní extrémne prevládajú emócie nad nejakým ráciom a dlhodobou víziou. A to sa netýka len nás obyčajných zamestnancov ale aj ľudí (a možno práve ešte viac), ktorý robia rozhodnutia. Povedal by som, že tak ako sa roky riešilo či "na vrch" majú zamestnávatelia alebo zamestnanci, podobná diskusia by sa dnes dala viesť v diskusii agenti vs ľudia. Výrazným prvkom je cenotvorba jednotlivých AI agentov.

Demonštrujem to na príklade (čísla sú vymyslené): ku nám dorazil GH Copilot na konci minulého roku, aktuálne sa rieši Claude Code. Budgeting je téma, ktorá sa vyriešila približne týmto spôsobom: Je to 20 dolárov za licenciu, plánovali sme ich rozdať 100, čo je náklad ktorý nie je treba nijako extra obhajovať. V realite sa ich rozdalo 300, čo je náklad, ktorý je kusnuteľný ale už sa nad ním niekto pozastaví. A prichádzajú otázky: čo nám to prináša? Sú teda tý vývojary efektívnejší alebo nie? O koľko? Jasné, pri 20 dolároch za licenciu tieto otázky toľko nepália. Problém ale je, že pri usage based pricingu sa začneme baviť o reálnych cenovkách ktoré nebudú 2x vyššie ale môžeme sa baviť o stovkách až nižších tisícoch dolárov. A to už sa na dobré slovo v korpráte platiť nebude. 

Je teda pekné, že za stovky až tisíce dolárov dokážete nahradiť juniora, takto sa ale tá matematika mení a možno viac firiem zváži, či tie peniaze radšej neinvestujú do juniora, ktorý má do budúcna potenciál doručiť svojich "10x". A teda spravovať si lokálnu AI je úplne iná komplexita ako zaplatiť licencie, povedal by som, že zatiaľ u väčšiny firiem ďaleko od reality.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1501226776582684803
No a druhá vec je, že charakter samotnej práce sa mení. To je fakt. Treba si ale uvedomiť, že programátori nie sú jednoliatá masa. Sú taký, ktorý milujú kód, hrať sa s ním, hľadať "milisekundy" a optimalizovať. A potom sú ľudia, ktorý majú nápad a chcú ho proste vytvoriť. Trúfol by som si povedať, že v minulosti bolo za svätý grál programátora považované hlavne to prvé. Sám som patril skôr do tej druhej skupiny a vždy som mál pocit, že sa na mňa ostatný pozerajú skôr skrz prsty :). S príchodom AI sa tá hra trochu mení a oveľa viac ľudí z druhej skupiny je schopná "pomocou kódu" tvoriť. Ultimátnym cieľom programovania ale vždy bolo vytvoriť niečo, za čo niekto zaplatí alebo to niekde vygeneruje nejaké peniaze. A to nám zaplatí výplatu :D.

Myslím si, že v tomto sa veľmi líši aj ten pohľad na AI. Ak som v prvej skupine, cítim, že môj prim klesá, keď som v tej druhej skupine, vidím veľkú príležitosť. Z toho čo vidím okolo seba je asi zbytočné predstierať, že niektorých ľudí z prvej skupiny AI skutočne nevyženie, pretože im práce prestane dávať zmysel alebo ich proste prestane baviť. To prostredie sa mení. Tak ako bolo povedané - tak ako sa už zmenilo 1000x.

Súhlasim ale aj s tým, že tá zmena je obrovská. Možno ste niektorý zachytili pojem "Dark Matter Developers" (https://www.hanselman.com/blog/dark-matter-developers-the-unseen-99). To sú taký tý programátory, ktorý pracujú v tých bájnych korporátoch ako je Oracle alebo Banka, šudlia tam niečo v 20 rokov starom systéme v zabudnutom jazyku a všetci im dajú pokoj. Tak AI je tak veľká zmena, že táto nedala pokoj ani im :). A s tým úplne nepočítali. Takže tváriť sa, že AI je zmena ako všetky predtým, podľa mňa tiež nie je úplne pravda. Je to biliardova guľa ktorá rozstrelila všetky ostatné guličky. Tie sú teraz v pohybe a nikto veľmi netuší, kde a ako sa to ustáli.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1499458139626541186
To už je pak efektivní naučit se ty modely střídat, zapojit ty freečkové do méně náročných tasků. Jde to?
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1499344606637330603
Zajímavé srovnání 👍 , ale mám-li být upřímný, souhlasil bych s ním pouze v případě, kdy agent vygeneruje kód, na základě požadavku, který mu někdo zadal, ale na ten kód pak nebude muset koukat, kontrolovat ho, nebude muset mu rozumět, ale spolehne se na to, že je v pořádku a že výsledek dělá to, co dělat má. Jenže pak bychom se už bavili o trochu jiném řemesle, řekl bych a ne o programování, jak ho známe dneska. Možná to k tomu směřuje, ale zatím tam, řekl bych, nejsme. Teď jsme, dle mě, s agentama ve stavu, že si sice pomocí CNC nechám udělat produkt, ale pak ho budu muset vzít, tou frézou doupravit, aby byl výsledek přesně takový, jaký chci. Tudíž bez znalostí práce s frézou by to nešlo, takže ten, kdo by tak chtěl pracovat, by se s tou frézou musel naučít... Takže otázka, která mě napadá, je lepší se naučit nejdříve s frézou a pak s CNC, nebo nejdříve s CNC a pak s frézou?
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1499327836316762223
https://www.youtube.com/watch?v=96jN2OCOfLs
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1499289706284711947
> Ale má pro juniora smysl si ten kód nechávat i generovat? ... Já na to prostor spíš vlastně nevidím.
Ona je to asi otázka spíše na seniorního programátora, který tu zkušenost s agenty má (ve smyslu generování kódu). Mě se v hlavě rojí spousta myšlenek, ale popravdě bych už nenapsal nic nového, než to, co jsem k tomuto tématu už napsal. Chápu, že ve firemním prostředí agenti smysl dávají (jsou tam jiné cíle...) a taky chápu, že zaměstnavatele zajímá, jestli uchazeč s agenty pracovat umí (ve smyslu generování kódu). Stále mi to ale přijde ve vztahu k člověku, který se učí programovat a čeká na svoji první pracovní zkušenost, nekompatibilní. Odpověď na otázku, jestli se má programátor naučit pracovat s agenty (opět ve smyslu generování kódu), je asi ano, protože ten trend tu je a bude, ale pokud se řemeslo programátora nezmění v něco jiného, tak až po tom, co se naučí programovat (nebo získá nějakou jistotu). A tady by si možná někteří senioři, kteří by tuto dovednost po juniorech striktně vyžadovali, mohli zkusit vzpomenout na to, jak se sami učili programovat... Ano i u začínajících programátorů agenti mají svůj smysl, ale řekl bych, že trochu jiný, než jaký je asi ten očekávaný. Ale můžu se samozřejmě plést, nicméně takhle nějak se mi to jeví.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1499069686678163539
co muze dat agent juniorovi je easy - junior si veme nejaky os projekt ktery ho zajima. Ale treba pouziva konstrukce kterym uplne nerozumi a uplne nebere souvislosti. Reknes agentovi aby ti udelal analyzu/zhrnuti etc. presne na tu uroven co potrebujes.

Ultimatni nastroj na uceni se programovani.

Pouzivam to dost casto - na nasi vlastni codebase - kdyz potrebuju resit neco v kodu kam bezne nelezu a nechci neco podelat. Agent dohleda souvislosti asi tak 100x rychleji a 10x lip nez kdyz to budu delat rucne.

Imho se timdle otviraji juniorum neskutecne studnice vedeni a agent jim muze slouzit jako ten seniorni kolega/mentor co jim vysvetli proc to ten kod dela tak jak to dela
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1499070673639702819
ohledne prace s agentem u juniora - rozhodne necekam ze bude clovek drsny agentista co bude provozovat vlastni agent farmu (openclaw neberu, to udelal nekdo jinej :-D) nebo slozitou orchestraci.

Co cekam
- pouzivani chatu na spis nadstandardnim levelu (prece jen by to mel byt technicky junior)
- chapani jaky je rozdil mezi agentem a chatem (trochu tricky protoze aktualni chaty jsou vlastne agenti :-D)
- proaktivni pristup a nikoliv pristup "kdyz me to das tak to teda budu nak pouzivat"
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1499073517071765534
Zajimave mi v tehle diskuzi prijde, ze seniori pouzivaji agenty spis jako juniorni kolegy, zatimco juniori je povazuji za seniory, od kterych se muzou ucit. Asi na tom neni nic prekvapiveho, jen to ukazuje na to, ze ten seniorni pristup (nechat agenta ze sebe udelat praci) je pro juniory tezko nacvicitelny.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1498986207735185530
ano ale to není situace když si se začal učit programovat, nebo někdo dneska - je to problém v pojmech - junior v pracovním procesu určitě může využít AI - ale člověk kterej se učí a ještě nikdy nebyl zrovna vidí kód "poprvý v životě" a ta diskuze všech ten čas než je ze mě "junior" / "medior" má smysl ze začátku nebo vůbec používat AI? Z mého pohledu nějak jo, ale tady ti odepisují lidi a jsou správně na JG kteří mnohdy ještě neprogramovali v práci, nebo se s naží zjistit co se potřebují naučit atp... A řeší se jestli je AI užitečná pro ně jako vstupní nástroj a jestli tak jak, spíš než že kdokoliv kdo už programátor zaměstnaný je ať už junior nebo kdokoliv AI musí umět používat :))
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1498624219469185165
Ja proste neverim, ze clovek, ktery tomu rozumi velmi malo, bude s agentem produkovat neco uzitecneho (production ready, nemluvim o nejakem one shot nastroji). Takze otazka zni, jak muze agent zacatecnikovi pomoct s ucenim. A podle tech reakci tady to vypada, ze moc ne - agenti jsou proste delani na to, aby za nas resili ukoly, a to je pri uceni nezadouci. A vysvetlit agentovi, ze po nem nechci vysledek byva dost frustrujici, clovek pak misto uceni travi cas promptovanim. Dokazu pak pochopit, ze clovek radsi sahne po knizce. Nevim, nakolik byly ty ruzne learning mody v agentech uspesne, je to tam jeste vubec?
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1498376376497999953
Otázka na juniory: Pokud by vám někdo řekl „vyzkoušejte si práci s AI agentem“, co je pro vás největší překážka, abyste to udělali? Nevíte co to je? Kde to sehnat? Jak začít? Je problém, že to stojí peníze? Nevíte z jakého konce na to jít? Co si pod tím představit? Strach, že vás to bude demotivovat a nebude vám dávat smysl se pak dopodrobna učit jak věci fungují?
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1496112110298464408
AI fackupy přehledně: https://crackr.dev/vibe-coding-failures
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1492274379508154600
Poslední dobou se mě mí studenti a taky lidi, co jsou na začátku programovací kariéry, docela často ptají, jestli by se měli začít učit používat AI, místo samotného programování nebo vzdělávání se. Protože jim připadá, že se všechno hýbe kupředu strašně rychle, a že jim ujede vlak, když teď nebudou trávit spoustu času prací s agenty. Říkal jsem si, že tohle téma by mohlo být relevantní pro tento kanál, a že bych tu napsal, co jim na to odpovídám.

Dle mého názoru je to zbytečná obava. Cokoliv, co dneska budete nad agenty dělat navíc, tak se do těch agentů za pár měsíců dostane v základu, a budou to dělat automaticky. Veškeré tipy a triky, které se lidi s agenty učili během minulého roku, tak už dnes agenti mají zabudované v sobě, a nemusíte to víceméně řešit. Zároveň ladění efektivity agentů do posledních pár procent postrádá smysl v momentě, kdy co půl roku vyjde nový model, který ten starý poráží rozdílem třídy.

Z AI mám sice strach ze spousty jiných důvodů, ale zrovna toho ujetí vlaku bych se nebál. V podstatě by definition je to něco, co se dá naučit používat za pár dní, a nepotřebujete k tomu používání nějaké extra znalosti. Rozdíl mezi člověkem, co agenty používá dva roky nebo týden, moc velký nebude. Naopak si myslím, že může mít přidanou hodnotu strávit ten čas učením se věcem opravdu porozumět, a mít pak výhodu oproti lidem, kteří tomu na pozadí nerozumí vůbec, a pouze vibekódují (teda za předpokladu, že v budoucnu bude porozumění věcem stále bráno jako něco potřebného a užitečného, ale to je jiné téma.. 🙂 ).
---


--- https://discord.com/channels/769966886598737931/1421181822389325828/1490545474426507415
Používat nějaký AI/LLM na nějaký security review je fajn nápad, až mě mrzí a stydím se za to, že mě to nenapadlo dřív. Někdy z toho vylezou halucinace ("Claude Code: tohle může být problém když použiješ cURL 7.86 a starší", po chvíli zkoumání co se tam změnilo a když jsem nic nenašel, tak jsem se Clauda zeptal a "aha, sorry, to jsem si vymyslel, žádnej bug jsem nenašel, ale hmm, vypadá to, že tomůže být problém vlastně furt, ale není to jistý, ale když s tím něco uděláš, tak to nebude ničemu vadit"), ale převážně to najde věci, který jsem zapomněl, nebo někdo jiný zapomněl (samozřejmě, že to nenajde věci, na který jsem myslel, jedině, že bych na ně myslel *blbě*), nebo jsem si neuvědomil, třeba proto, že původně to něco mělo jiný scope (což je častý zdroj bezpečnostních chyb: "to nikdo nepoužije jinak a nikdo tam nic nepřidá, to je v cajku").

Většinou to nechci opravit - protože to třeba taky používám na 3rd party code. Tuhle někdo chtěl na každej web nám dávat nějakej chatbot nebo co, tak jsem si stáhl ten JS a "tady je nějakej JS, řekni mi co to dělá a jaký tam jsou bezpečnostní chyby a rizika, ukaž mi ten kód a dej mi čísla řádků". Nějaký věci to našlo, párkrát jsem musel něco dopromptovat, ale vysvětlilo to hezky (nepotřeboval jsem, ale stejně si to nechávám vysvětlit, aby mi třeba něco neuniklo) V tom do určitý míry minifikovaným JS bych to nenašel a když jo, tak za hodně moc času.

Tady je třeba ukázka na nějaký knihovně, kde jsem zkusil jednoduchý "Identify any security vulnerability or even a risk in the codebase that would need fixing before 1.0 happens." a vylezlo z toho něco, na co jsem nemyslel. Zkusil jsem schválně teď napsat ať mi to dovysvětlí 
https://github.com/spaze/security-txt/pull/64#issuecomment-4123888270 Na konci už je to PHP, validuje mi to moje fixy, ale na začátku je to obecný a je vidět, že i kdybych o tom věděl prd, tak bych se z toho něco naučil.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1490689835864817735
Nedávno jsem tady dělal anketu o tom, kdo si pomáhá přes chat a kdo zkoušel někdy nějakého agenta. Vyšlo mi z toho od oka, že junioři prakticky vůbec agenty nevyužívají. Tohle tu možná už dřív bylo, ale rozepsané, tak to tu dávám teď znova, když už je to hotové - návod od Simona Willisona, jak do toho celého proniknout: https://simonwillison.net/guides/agentic-engineering-patterns/
---


--- https://discord.com/channels/769966886598737931/1421181822389325828/1490265161292972073
Lidi ani nenapadne, že po AI můžou security review chtít. Sama od sebe to neudělá. No a když chci pověsit aplikaci na internet, tak ať už se chci učit security, nebo ještě ne, prompt ve stylu toho, který jsem napsal, je to nejmenší, co můžu udělat, a zlepší mi to spaní. Nějaký “správný” způsob učení můžu dělat potom.
---


--- https://discord.com/channels/769966886598737931/1488865008849784944/1489566723211530320
Takhle ať to uvedu přesněji na pravou míru, jsou 3 podstatné faktory. S tím, že pro odpovědi, učení se, vysvětlování, hrají nejvíc roli ty první 2.
Opravy kódu (pokud nejsou brutálně rozsáhlé), tak taky potřebuješ hlavně 1 a 2. Ale jakmile chceš složitější průzkumy, tvorbu celých aplikací a jejich správu, tak už hraje roli i ta 3. Ale třeba MCP téměř nepoužívám.

- Model (LLM, VLM)
-- GPT 5.4, Opus 4.6, Gemini 3.1 Pro
- Harness (to jak ho ovládáš)
-- Claude Code, Codex, Forgecode, Droid, ... 
- Nástroje (a jak je chceš volat)
-- Tohle je vlastně dost zásadní z mnoha důvodů, protože to nejvíc rozbíjí modely. Ty totiž můžeš volat CLI nástroje (v bashi), MCP (a to dvěma způsoby: přes oficiální tool calling nebo uvnitř promptu, a zejména s tím druhým mají modely problém).
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1489339447811248289
Nechtěl bych zpochybňovat přínos vibe codingu. Je to velká demokratizace kódění a jako člověk, který se dekády věnuje tomu, aby si kdokoliv dokázal vytvořit nějaký software, který mu s něčím pomůže, říkám narovinu, že to je super. Objektivně, je to super, že někdo napíše větu do AI asistenta a dostane zpátky pahýl funkční aplikace a je třeba i schopen si ji dál nějak sochat. Hromada lidí, která by musela jít za programátorem a prosit jej na kolenou (nebo zahrnovat penězi), aby jim udělal nějaký custom skript nebo sranda software, je osvobozena a můžou si to vytvořit sami.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1489339905053163601
Problém je, že lidi pak nevidí, kde je čára mezi hraním a doručováním seriózního softwaru. CEOs a novináři společně fetují Dunning-Krugera a dotahují to do extrému, že programování už si každý udělá sám a programátoři nebudou potřeba. To je za mně blbost. Pouze nedohlédnou, co vše ta profese obnáší a co to vůbec znamená vyvíjet, provozovat, opravovat a udržovat software.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1488099386998132777
Ty články hodně píšou o tom, jak je důležité umět si obhájit, že ten člověk v rozumné době dokáže firmě vydělat peníze, které přesáhnou jeho mzdu.

Málokterá firma ale takhle skutečně uvažuje. Pořád je to hodně o nějakém gut feelingu a dojmu z toho, jaký přístup ten člověk má.
Když si vzpomenu na dobu, kdy jsem učil na ČVUT, tak jsem měl největší frustraci z lidí, kteří **zbytečně plýtvali mým časem**.

**Za mě by kvalitní kandidát, byť juniorní, měl:**
- vždy zhodnotit, zda má vše, co potřebuje, a nečekat, až si někdo všimne, že se na něčem zasekl
- pokud řekne "dnes to bude" a ono to nebude, tak mi dá vědět
- dokáže si dohledat základní věci sám a nebude se ptát 10x denně na něco co je jasně vyspecifikované
- dokáže stručně popsat, co zkoušel, co fungovalo a co ne
- dokáže pochopit kontext - proč to děláme a ne jen splnit task
- obecná spolehlivost v malých věcech (dochvilnost, follow-upy, dokončování rozdělaných věcí)

Ne všechny z těchto vlastností se dají odhalit už na pohovoru, ale určitě tomu ten člověk může jít naproti podle toho, jak bude vystupovat a jak bude komunikovat.

A pak je tu celá řada pouček, jak na pohovoru zaujmout - např. že si člověk o té firmě něco nastuduje a to téma ve správný okamžik vytasí... mrkne na sociální sítě lidí, kteří budou na tom meetingu, a prostuduje si, co je baví a co v poslední době postovali. Ale to už je spíše pohovorová psychologie než aspekty, které tomu člověku pomůžou v té firmě dlouhodobě přežít.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1484113362030690344
**Dual-track learning.** Když si naprogramuju nějaké cvičení, malou appku apod. tak potom spustit coding agenta a navést ho, aby stejnou věc vytvořil taky. Potom prozkoumat a pochopit rozdíly mezi mým a jeho řešením, doptat se ho na důvody, proč něco řešil jinak, klidně ho nechat obě řešení srovnat a zhodnotit. Výsledkem je dobré porozumění *a zároveň* schopnost daný problém řešit pomocí agenta.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1484134622433640509
Jasně. Já si to představoval tak, že třeba vytvoříš todo list v Reactu a pak ho necháš vytvořit Codexem. A uvidíš, že to třeba rozdělil do víc komponent, jinak vyřešil loader, ošetřil chybové stavy a tak. A hned jsi o něco chytřejší a příště bys to udělal líp. A zároveň si všimneš, že vůbec nepoužil animace, a tak si zapamatuješ, že tyto detaily nejsou samozřejmé a je třeba je do zadání napsat (a nebo počítat s tím, že ten postup bude iterativní).

Přijde mi, že ta první část je docela blízko tomu, kdybys měl učitele, který by ti tvé výtvory opravoval. Ty chyby pořád uděláš. Ale možná jsi to myslel nějak jinak, nevím.
---


--- https://discord.com/channels/769966886598737931/769966887055392768/1484117751248195614
Jedno hezké motivační video, aby někdo nepodléhal skepsi budoucnosti s AI jako programátor 😄 https://www.youtube.com/watch?v=BAlSzHFmmwU
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1483898899910361208
Junior, který neumí pracovat ani s AI chatem (tak, aby mu pomáhal a aby jej mentoroval, atd.) je na současném trhu úplně ztracený. To je absolutní minimum.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1483899093179957388
Junior, který neumí pracovat s žádným agentem, ani prostě neotevřel Cursor, začíná být na současném trhu taky ztracený. To je nová laťka roku 2026.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1483899675903000738
Víc není třeba. Jasně, dá se šermovat agenty a pokud to někoho láká a chce si s tím hrát a je „product builder” a má peníze na tokeny, tak hurá do toho, klidně surfujte na vlně a uděláte díru do světa – zcela neironicky. Ale pokud jste tady, protože chcete do IT a chcete tvořit webovky v JavaScriptu apod., tak se učte JavaScript, učte se Git, všechno okolo, a naučte se při tom efektivně používat AI v podobě (libovolného) agenta. Tak, aby násobil vaše znalosti, které si neustále prohlubujete, ne tak, aby za vás „podváděl“.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1483777123708567602
Co se nabízí je pomoc při pochopení existujícího projektu. Tam je to za mě někdy gamechanger. Jako úplný junior jsem plaval v pochopení komplexních projektů - co bych za to tehdy dal.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1483778403638317206
To, že je to generativní AI neznamená, že to musí generovat kód. Může to generovat i junior friendly dokumentaci, třeba 😄
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1483780055757881355
1. Rozběhej si claude code nebo něco podobného 
2. Nech si ve svém hobby projektu najít bugy
3. Nech si je opravit
4. Nech si napsat dokumentaci
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1483783462035918878
Možná i kuchařky na nějaké praktické projekty. Typu udělej web, nasaď ho, nastav monitoring…
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1483776551232344104
Já jsem si prostě stáhnul do VS Code Clauda, zaplatil za pětikilo Pro a jedu si. Limity více než dostačující na nějaké domácí žvýkání.
---


--- https://discord.com/channels/769966886598737931/1177266646579163246/1483514733838602252
> tímhle stylem bude na stejnou práci potřeba tak třetina lidí

třeba, ale 

a) i to AI musí někdo „engineerovat“, to se samo neudělá

b) pokud se někde hraničně kopou do zadku a nemají nekonečný backlog, tak možná, ale pokud najednou jde udělat o 30 % víc práce, tak už je to rozhodnutí spíš otázka toho, co má prioritu, není to technologický, ale byznysový: potřebujeme spíš ušetřit za lidi a zhruba jet jako doposud? Chceme za stejný prachy víc kódu? Chceme ještě víc kódu, když je teď takhle levnej?
---


--- https://discord.com/channels/769966886598737931/1177266646579163246/1483515258206289991
Když slyším že jste někde měli desítky padajících testů a takový kód prošel do produkce (WTF OMG) a pak to x lidí měsíce fixovalo, tak teď to může jeden člověk fixnout za měsíc třeba… najednou to je dosažitelný. Přijatelná cena i čas.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1482808665260949696
Správci Rustu – stejně jako správci každého open source projektu – teď řeší, jak se postavit k AI. A protože jsou stejně jako Rust *strukturovaní*, vedou strukturovaně i celou diskuzi 🙂 Jejím výsledkem je zatím dokument shrnující hlavní pohledy, názory a argumenty:

[Diverse perspectives on AI from Rust contributors and maintainers](https://nikomatsakis.github.io/rust-project-perspectives-on-ai/feb27-summary.html)

Nezaznívá v něm nic zas až tak nového, ale je to dobrý přehled různých perspektiv a dává dobrý vhled do toho, s čím se dnes větší open source projekt musí potýkat. Hodně se mi líbí shrnující sekce "Common ground" a "Core tensions" na jeho konci.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1481305876550783018
Podle mě má smysl dávat na GitHub i věci, kde ti pomohla AI, přičemž slovo „pomohla“ může znamenat aji méně, aji více, ale držel bych se toho, že to výrazně označím a napíšu do README, o co jde a co bylo účelem.

Např. „Toto jsem si navibekódila jako experiment, na kód jsem se vůbec nedívala a jen to ručně testovala, co to dělá. Je to appka na zkoušení anglických slovíček pro malou sestřenici.“ Za mně naprosto legit. A říká mi to, že jsi dokázala navibekódit něco funkčního, takže s AI si tykáš, umíš něco vytvořit, a na pohovoru bych se tě i ptal na to, jakým procesem jsi to vytvářela, jak jsi nad tím přemýšlela.

Podobně bych to viděl i s věcmi, kde ti AI pomohlo méně. „Toto jsem napsala v Cursoru, ale veškerý kód jsem viděla, četla, a vím, co dělá.“

Asi bych ale neřešil, pokud jsem s AI pouze něco konzultoval v chatu a nechal si poradit, stejně jako bych si nechal poradit od kámoše nebo od StackOverflow (kdo ještě pamatuje, heh). To už považuju asi za úplně běžnou součást práce nehodnou zmínky.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1481307547527942336
A k tomuto dodám, že bych tam rozepisoval jaký byl proces té tvorby, protože lidi mají ty termíny „vibecoding“ apod. strašně dopletené a i když mají poměrně jasné definice, tak hrozí, že si pod tím za současné překotné situace každý představí něco úplně jiného. Takže bych tam fakt psal „kód jsem viděla/neviděla“ atd.
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1481248790890414082
pridam sa do diskusie, ze suhlasim s obidvoma++ uhlami pohladu v predoslych spravach, ale to s pisanim kodu uz nesuhlasim, ze je "praca" programatora - peniaze dostavame za to, ze riesime business problemy ktore sa daju riesit vyvojom softwaru  - najlepsi sposob vyvoja software bolo pisanie kodu v high level languages pre vela vela problemov.. vacsinou nie assembly a nie english, ale nieco a la Python a TS a C++ a pod., ale samotne pisanie kodu je len hobby ak to neriesi business problemy

ak manazeri prestavaju byt presvedceni/e ze manualne pisanie kodu je stale najlepsi sposob, tak je praca programatora bud presvedcit manazerov o tom ako AI agenti funguju naozaj a co je a nie je najlepsie riesenie naozajstnych business problemov, alebo zmenit pracu kde pisanie kodu nie je len hobby ale stale naozajstna praca, alebo to zacat vnimat ako hobby a najst si pristup k programovaniu tak, ako to potrebuje situacia na trhy - zatial podla mna je to casto o prvej moznosti, ale zaroven nie kazdy business problem je idealne riesit bez pomoci AI coding assistentov aby sme predisli security problemom a tech debt a slopu, ale je to o hladani nejakej cesty z oboch stran (ak budem len AI skeptik, tak nebudem mat argumenty pre manazerov co vieme spolu automatizovat a co je uz riziko... ak budem len AI nadsenec, tak budem zdrojom toho rizika.... ak vsetci manazeri vo firme budu verit AI hype bez realnych skusenosti a intuicie kde to ma hranice, tak to budu velmi unavne diskusie)
---


--- https://discord.com/channels/769966886598737931/1401948283361955940/1480934987363647658
Chce to ale k tomu směřovat. AI funguje v dobrém prostředí dobře, ale samo o sobě nemá snahu to dobré prostředí vytvářet a ani moc udržovat. To musí stále řídit lidi. K tomu práve slouží CLAUDE.md - to není od toho, abych do něj psal obvious věci, které si AI umí zjistit sama, ale je to od toho, že když vidím, že AI dělá něco jinak, než chci, tak přidám “opravu” do CLAUDE.md.
---


#} -->
