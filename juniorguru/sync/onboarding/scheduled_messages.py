from textwrap import dedent


SCHEDULED_MESSAGES = {}


def schedule_message(emoji):
    def decorator(render_text):
        SCHEDULED_MESSAGES[emoji] = render_text
    return decorator


####################################################################
# INTRODUCTION AND BASIC CONCEPTS                                  #
####################################################################


@schedule_message('👋')  # Day 1
def render_hello(context):
    member = context['member']
    text = dedent(f'''
        Vítám tě v klubu, {member.mention}! Jsme rádi, že jsi tady s námi. Klub je místo, kde můžeš spolu s ostatními posunout svůj rozvoj v oblasti programování, nebo s tím pomoci ostatním.

        Já jsem kuře, zdejší bot. Pomáhám se vším, co by nemusel <@!668226181769986078> stíhat sám. Tento privátní kanál jsem vytvořilo jen pro tebe.

        **Jak funguje tento kanál?** 💬
        V klubu se toho děje hodně, tak ti sem budu posílat tipy, jak se orientovat. Ptej se tady na cokoliv ohledně fungování klubu, klidně reaguj na jednotlivé tipy, posílej zpětnou vazbu. Já odpovídat neumím, ale vidí sem i moderátoři a se vším ti rádi pomůžou.

        **Jak funguju já?** 🤖
        Jsem většinou ranní ptáče – vstanu, udělám všechnu svou práci a zbytek dne se do klubu už nekoukám. Tipy ti tedy budou chodit zhruba jednou denně.

        **Neboj se chyb** 💁
        Různých rad a pravidel ti sem postupně dám dost, takže si je určitě všechny nezapamatuješ a rozhodně uděláš něco jinak. To vůbec nevadí! Moderátoři tě rádi opraví, nebo nasměrují. Neboj se jich a ber je spíš jako pomocníky, ne policajty.
    ''')
    if member.intro:
        text += dedent('''
            **Představení ostatním** 👋
            Koukám, že už máš svoje představení v kanálu <#788823881024405544>. To je super! Pod tvou zprávou je teď vlákno (_thread_), kam mohou ostatní reagovat a kde můžeš případně něco doplnit. Krátké uvítání tam máš i ode mně.
        ''')
    else:
        text += dedent('''
            **Představ se ostatním** 👋
            První, co se hodí v klubu udělat, je představit se v kanálu <#788823881024405544>. Ostatní členové klubu se tak doví, co už máš za sebou a co je tvým cílem. Zajímá nás všechno, díky čemu tě poznáme, ale piš jen to, co chceš, abychom o tobě věděli. Povinné není nic, ale těžko ti dobře poradíme s kariérou nebo kurzem, pokud nebudeme znát tvou situaci.

            Co tě přivedlo do klubu? Jaké máš vzdělání a čím se teď živíš? Máš za sebou nějaké IT školy nebo kurzy? Jaké věci už umíš? Jak dlouho se zajímáš o programování? Co tě láká: weby, hry, datová analýza, mobilní appky…? Máš nějaký svůj projekt? Plánuješ si hledat práci v oboru? Kolik na to máš času?

            Já vím, není to jednoduché. Překonat ostych, vymyslet co o sobě napíšeš a ještě poskládat slova za sebe tak, aby to mělo hlavu a patu. Když to však zvládneš, klub ti bude moci posloužit fakt mnohem víc a líp.
        ''')
    if not member.has_avatar:
        text += dedent('''
            Když si navíc dáš i profilový obrázek, dostaneš ode mě roli <@&836959652100702248>. Udělat to můžeš v sekci Profily nebo Uživatelský profil (_Profiles_ nebo _User Profile_) ve svém nastavení na Discordu. Nemusí to být přímo fotka, jde pouze o to, abychom tu neměli deset Honzů, které nerozeznáme od sebe.
        ''')
    text += dedent('''
        **P. S.** Všichni si tu tykáme!
    ''')
    return text.strip()


@schedule_message('🧭')  # Day 2
def render_orientation(context):
    return dedent('''
        Krásný den přeju, dnes bych ti chtělo pomoci se základní orientací v klubu. Jak najít ten správný kanál a jak se tím vším nenechat zahltit?

        **Jak se vyznat v kanálech?** 🗺
        Je tady mnoho kanálů, ale neboj se toho. Po pár dnech si všimneš, že někde se toho děje víc, jinde je to klidnější a něco tě vůbec nezajímá, tak si to vypneš.

        Kanály jsou rozděleny do kategorií, např. Rituály, Studium, Shánění práce. To ti může orientaci zjednodušit.

        Každý kanál má svůj popis, kde zjistíš jeho účel. Na počítači stačí kanál rozkliknout a podívat se do horní lišty. Na mobilu se popis zobrazí, až když zprava vysuneš seznam členů.

        Nelam si s tím ale moc hlavu. Potřebuješ na něco zeptat? Máš téma, které chceš probrat, ale nevíš kam s tím? Vždy se můžeš ujistit tady! Moderátoři ti poradí. Nebo to prostě dej do <#769966887055392768>, ten snese cokoliv.

        **Je toho moc!** 🔕
        Pokud nemáš moc času sledovat všechny diskuze, sleduj aspoň <#789046675247333397>. Každý týden je tam shrnutí s nejoceňovanějšími příspěvky.

        Kanály, které víš, že tě nebudou zajímat, si můžeš povypínat. Jdi do kanálu a použij zvoneček. Na počítači je v horní liště, na mobilu se lišta zobrazí, až když zprava vysuneš seznam členů.

        Kategorii Archiv (úplně dole) si můžeš schovat kliknutím na její název. Jsou tam staré kanály, které už nepoužíváme, ale chceme, aby jejich historie zůstala ve vyhledávání.
    ''')


@schedule_message('💬')  # Day 3
def render_discord(context):
    return dedent('''
        Píp píp! V tomto tipu ti vysvětlím, jak funguje Discord. Co to vlastně je? Jak tady správně komunikovat? K čemu jsou a jakfungují vlákna?

        **Co je Discord?** 👾
        Něco mezi sociální sítí a chatovací aplikací. Původně to začalo jako služba pro hráče, ale dnes už je tu všechno možné. Kdokoliv si tady může založit skupinu a pozvat do ní lidi, podobně jako na Facebooku. Skupiny jsou ale soukromé a jen na pozvánky, spíš jako na WhatsApp. Každá skupina (_Discord server_) se dělí na diskuzní kanály, podobně jako to má Slack. A navíc jsou tady hlasové kanály, kde se lidi mohou na jeden klik spojit přes (video)hovor.

        Jestli něco takového vidíš poprvé, asi ti z toho jde hlava kolem. Dej tomu čas a neboj se ptát moderátorů. Může se hodit i nápověda, která je tady https://support.discord.com/hc/en-us/categories/200404398

        **Odpovídání** ↩️
        Je to tady chat, takže zprávy se sypou jedna za druhou. Aby šlo snadněji sledovat prolínající se diskuze nebo reagovat i na příspěvky z hlubin historie, jde na předchozí zprávy navazovat použitím funkce Odpovědět (_Reply_). Má ikonu zatočené šipky.

        **Vlákna** 🧵
        Když chceš řešit něco konkrétního, třeba životopis, projekt nebo dotaz, hodí se založit vlákno (_thread_). Díky němu se diskuze rozvětví a zprávy k tématu se schovají na jedno místo, které má vlastní název. Neplevelí to hlavní diskuzi v kanálu a lépe se to čte.

        Do většiny kanálů můžeš psát zcela volně a nemusíš nad tím moc přemýšlet, ale některé mají speciální režim. Jsou to Rituály (<#788823881024405544>, <#806621830383271937>, <#815906954534191117>) a <#878937534464417822>. Aby zůstaly přehledné, odpovídá se v nich pouze pomocí vláken.

        Vlákno zmizí ze seznamu kanálů po týdnu bez aktivity. Můžeš ho ale kdykoliv oživit novým příspěvkem.
    ''')


@schedule_message('🐣')  # Day 4
def render_juniorguru(context):
    return dedent('''
        Čau! Dnes to bude o tom, že na junior.guru není jen klub, ale i spousta motivace a užitečných rad, které by bylo škoda minout.

        **Příručka** 📖
        Na https://junior.guru/handbook/ najdeš příručku pro juniory. Celá je zdarma ke čtení na webu a je v ní hromada užitečných tipů. Jak začít programovat? Jak si sehnat první praxi? Co je u pohovorů důležité? Jak připravit životopis? Tím vším a mnohým dalším tě příručka provede, krok za krokem. <@668226181769986078> stále přidává nové kapitoly, takže i pokud už máš něco přečtené, je dobré se tam po čase vracet.

        **Podcast** 🎙
        Nahoď sluchátka a pusť si do nich příběhy a rady lidí, kteří se motají kolem začátečníků v IT. <@810862212297130005> si zve na rozhovor juniory, lidi z firem, lektory kurzů. V podcastu se snaží přinášet odpovědi, inspiraci, motivaci. Všechny díly najdeš na https://junior.guru/podcast/, ale taky na Spotify, na YouTube a v dalších podcastových aplikacích. Epizody vychází jednou měsíčně a mívají půl hodiny. Máš nápad, koho dalšího pozvat? Napiš nám!
    ''')


# @schedule_message('🙋')  # Day 5
# def render_roles(context):
#     member = context['member']
#     text = dedent('''
#         Ahoj! Víš proč je někdo zelený a jiný žlutý? Co znamená medaile nebo hvězdička vedle jména? A k čemu je dobré reagovat na příspěvky pomocí emoji?

#         **Role** 🏅
#         Na Discordu jde lidem dávat role, díky kterým mají barvu, ikonu vedle jména, jsou oddělení v seznamu členů, nebo mají oprávnění navíc, např. přístup do jinak skrytých kanálů.

#         Na každém Discordu je to jinak, zcela podle chuti jeho správců. Tady v klubu se o většinu rolí starám já. Některé dávám jen pro lepší orientaci, jiné za zásluhy.
#     ''')
#     if not member.intro or not member.has_avatar:
#         text += dedent('''
#             **Mám #ahoj a profilovku** 🦸
#             Když se představíš v <#788823881024405544> a dáš si profilový obrázek, dostaneš ode mě roli <@&836959652100702248>. Obrázek si můžeš nastavit v sekci Profily nebo Uživatelský profil (_Profiles_ nebo _User Profile_) na Discordu. Nemusí to být přímo fotka, jde pouze o to, abychom tu neměli deset Honzů, které nerozeznáme od sebe. Chodím do klubu zhruba jednou denně, takže je potřeba počkat, než se role objeví.
#         ''')
#     text += dedent('''
#         **Hodně pomáhám** 💛
#         Když si čteš v klubu a zaujme tě něčí příspěvek, rozdávej emoji reakce, třeba ❤️, 👍, nebo 👀. Někdo si dal práci s odpovědí a je fajn vědět, že to ostatní čtou a že to třeba pomohlo.

#         Já pak tyto reakce počítám a dělám z toho týdenní souhrny v <#789046675247333397>, ale nejen to. Členové, kteří mají od začátku existence klubu nebo za poslední měsíc nejvíc pozitivně hodnocených příspěvků, ode mě dostávají nejprestižnější roli v klubu, <@&836960665578766396>.

#         Všimni si, že si nehrajeme na seniory a juniory. Kdokoliv může být nápomocný, ať už dobrou myšlenkou, otázkou, odpovědí, nebo sdílením zajímavých tipů.

#         **Firemní role** ✨
#         Firmy, které pomáhají financovat junior.guru, mohou kromě jiného posílat do klubu své lidi. Všichni mají roli <@&837316268142493736> a hvězdičky u jména. Každá firma má pak ještě i svou roli, např. <@&938306918097747968>.

#         **Další role** 👑
#         Následující role jsou docela vidět a je dobré je znát:

#         ⭐️ <@&795609174385098762>
#         🧠 <@&915967369661251624> (aby bylo ve <#864434067968360459> poznat, kdo je a není laik)
#         <@&898289895624302653> (dobrovolníci, kteří pravidelně pořádají nějaké klubové akce)
#         <@&974297387935866910> (kdo nabízí svou pomoc v <#976054742117658634>)
#         <@&836928169092710441> (přednášející z oficiálních klubových akcí)
#         🎄 Advent of Code (řešitelé <#819935312272424982>, používá se v prosinci)
#         🏅 Rok v klubu, Zakládající člen
#         <@&836930259982352435> (prvních 15 dní v klubu)

#         Pak je tu ještě hodně dalších, které nemají velký význam a slouží především <@668226181769986078>, aby tu v tom měl pořádek.
#     ''')
#     return text


# @schedule_message('💡')  # Day 6
# def render_sth(context):
#     return dedent('''
#          To jsem zase já!
#     ''')


### 💡 CO TADY DELAT
#
# NASE SLA
#
# Dnes to bude o tom, jak to tady chodí a co všechno tady vlastně můžeš dělat.
# Ten týpek, kterýho jsme hledali v klubu mi říkal, že se tolik neptal, protože nechtěl obtěžovat, přišlo mu, že jsou to blbosti a tak
#
# **CO TU JDE DĚLAT**
# :speech_balloon: Diskutovat. Zkus #kariéra, #zdraví-těla, #kurzy…
# :tv: Chodit na online srazy a přednášky
# :person_tipping_hand: Najít řešení. Vytvoř vlákno v #mentoring, pomůžeme!
# :person_raising_hand: Organizovat vlastní akce, vytvářet studijní skupinky
# :clipboard:  Inzerovat v #práce, #pozvánky… Povolené, vítané!
# :muscle:  Chlubit se! Umíš něco nového? #til Máš něco hotové? #výrobky
# :people_hugging: Ulevit si v #past-vedle-pasti
#
# Veřejné a soukromé
# TBD faq - co mam z clenstvi v klubu jako...? co tady jde delat… otevri tema, atd. a dat priklady co se muzou zeptat - verejne psani versus soukroma zprava, rady primo od honzy tady v kanalu, ptat se na vse kdyz nevis jak to funguje, poradime, jsme recepce, tajemstvi nepoustim bokem a kdyz dojde na lamani chleba, zastavam se junioru…
#
# Proč vůbec něco psát?
# TBD, dat priklady co se muzou zeptat, co mam z clenstvi v klubu jako… faq, verejne psani versus soukroma zprava, rady primo od honzy tady v kanalu, ptat se na vse kdyz nevis jak to funguje, poradime, jsme recepce, tajemstvi nepoustim bokem a kdyz dojde na lamani chleba, zastavam se junioru…


# @schedule_message('💛')  # Day 7
# def render_sth(context):
#     return dedent('''
#           Nazdar!
#     ''')


### 💛 COC
#
# coc a jak se to lisi od skupin na FB, attitude a hodnoty - Jak se klub liší od skupin na Facebooku? Faq
# Čau! Dnes to bude o tom, jak se klub liší od většiny jiných skupin na internetu, ať už jsou na Facebooku, na Discordu, nebo jinde.
#
# Bezpečný prostor
#
# Zahradník


# @schedule_message('💸')  # Day 8
# def render_sth(context):
#     return dedent('''
#           Nazdar!
#     ''')


### 💸 PLACENI
#
# placení za klub, vykopnutí, musí být kartou, kde najdes nastaveni a jak se prihlasis - budu rad za dosavadni feedback, napis jak se ti tu zatim libi, Existuje způsob, jak být v klubu zdarma? faq... celkově odkaz na sekci jak platit ve faq
# na konci doplnit, že pokud 14 dní nestačilo na vyzkoušení, lze ti napsat a prodloužíš - nebo dát do „zadej kartu“ emailu, stejně tak sbírat feedback
#
# Discord je samostatná firma, která vydělává na tom, že si jednotlivci kupují tzv. Nitro, prémiové členství. To umožňuje používat víc emoji, posílat větší obrázky, apod.
#
# **Jiné Discordy** 👋
# Na Discordu není pouze klub, můžeš se přidat i do dalších skupin a komunit. Svůj Discord mají i čeští Pythonisti https://discord.gg/wUfGAQ7jVv nebo Frontendisti https://discord.gg/XMc85GPHQg. Ty jsou na rozdíl od klubu zdarma.
#
# Klub je zdarma jen na první dva týdny, a proto máš kromě Discordu účet i na https://juniorguru.memberful.com/, kde se pak řeší všechno kolem placení.


####################################################################
# MAIN CLUB FEATURES EXPLAINED                                     #
####################################################################


### 🤔 PORADNA
#jak funguje poradna, jak se spravne ptat, psani kodu barevně (na mobilu nefunguje), dej lidem aspon DK, ukol zkus zalozit dotaz a kdyz ti to nepujde dej vedet, nemusis to dokoncit
# vysvetlit markdown
# **Formátování zpráv a kód**
# Text zpráv může být **tučně** `**tučně**`, __kurzívou__ `__kurzívou__`, nebo může vypadat jako `kód`, když kolem něj napíšeš tenhle divný znak, kterému se říká __backtick__: \` Kód na víc řádků se hodí dát do trojice takových backticků na začátku a na konci: \`\`\`


### 🔎 KURZY A VYHLEDAVANI
# kurzy, recenze a zkusenosti, vyhledavani, Co vyplývá z toho, že je členem klubu nějaká vzdělávací agentura?, zkus si vyhledat recenzi na SDA od niny nebo GFA od lukyho, Jak se klub liší od škol, akademií a kurzů? Faq


### 📺 EVENTY
#
# klubove prednasky, ukol pust si neco, discord eventy, jak to probíhá, vlastní akce, iniciativa, role organizuju akce


### 💁 MENTORING
# jak funguje mentoring, anna prednaska, prostuduj si to, Jak se klub liší od individuálního mentoringu? Faq


### 🏢 JOBS
# pracovní nabídky bot, web jobs, pripomenout mute, k cemu jsou palce


### 🚀 CV FEEDBACK
#
# cv feedback, kariera, pohovory, mentoring na pohovory, poh. nanecisto, precti si prirucku na tohle tema - Jak se klub liší od kariérního poradenství? Faq


### ⚽ RITUALY A AKTIVITY
# jak fungujou ritualy (viz pins), parťáci a spolecne aktivity jako adventofcode atd. - zkus vyresit hadanku a projdi partaky, zalozim vam mistnost, roli, atd.


### 🌈 SPOLUPRACE
# Spolupráce s firmami a komunitami - faq


####################################################################
# POWER USER TIPS                                                  #
####################################################################


### 🤓 DALSI TIPY
# discord tipy zasobnik - citace, odkazy na zpravy, shift enter
# **Online odkudkoliv** 💌
# Discord jede jen tak v prohlížeči, ale má i svou aplikaci na počítač a na mobil. Mít klub v kapse se hodí, pokud se chceš zabavit nebo pomáhat, když zrovna čekáš ve frontě na poště.


####################################################################
# COLLECTING FEEDBACK                                              #
####################################################################
# TODO
# mozna by to mohla byt i rychla anketa v #pravidla, stejne jako zaklikavani jazyku atd.
