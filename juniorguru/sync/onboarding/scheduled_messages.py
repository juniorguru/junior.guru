from textwrap import dedent

from juniorguru.lib.club import HONZAJAVOREK


SCHEDULED_MESSAGES = {}

ALLOWED_MENTIONS = [810862212297130005,]  # https://github.com/discord/discord-api-docs/issues/2126


def schedule_message(emoji):
    def decorator(render_content):
        assert emoji not in SCHEDULED_MESSAGES, 'Duplicate emojis!'
        SCHEDULED_MESSAGES[emoji] = render_content
    return decorator


####################################################################
# INTRODUCTION AND BASIC CONCEPTS                                  #
####################################################################


@schedule_message('👋')  # Day 1
def render_hello(context):
    member = context['member']
    text = dedent(f'''
        Vítej v klubu, {member.mention}! Já jsem kuře, zdejší bot. Pomáhám se vším, co by nemusel <@{HONZAJAVOREK}> stíhat sám. Tento privátní kanál jsem vytvořilo jen pro tebe.

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

            Já vím, není to jednoduché. Překonat ostych, vymyslet co napsat a ještě nějak poskládat slova za sebe. Když to však zvládneš, klub ti bude umět posloužit mnohem líp.
        ''')
    return text


@schedule_message('🧭')  # Day 2
def render_orientation(context):
    return dedent('''
        Dnes ti chci pomoci se základní orientací. Kanálů je tady mnoho, ale neboj se toho. Po pár dnech si všimneš, že někde se toho děje víc, jinde je to klidnější a něco tě vůbec nezajímá, tak si to vypneš.

        **Co jsou kanály?** 💬
        Jejich názvy začínají znakem #, ale nejsou to hashtagy. Kanály jsou jako místnosti v bytě nebo pódia na festivalu. Rozdělují diskuzi podle účelu a tématu. Nemusí být jen textové, existují i hlasové a další.

        **Jak se vyznat v kanálech?** 🗺
        Kanály jsou rozděleny do kategorií, např. Rituály, Studium, Shánění práce. To ti může orientaci zjednodušit. Každý kanál má svůj popis, kde zjistíš jeho účel. Na počítači stačí kanál rozkliknout a podívat se do horní lišty. Na mobilu se popis zobrazí, až když zprava vysuneš seznam členů.

        **Stejně nevíš?** 🤔
        Máš téma, které chceš probrat, ale není ti jasné kam s ním? Ujistit se můžeš v kanálu <#806215364379148348>, nebo se soukromě zeptej moderátorů a oni ti poradí. Ale určitě nad tím nedumej moc dlouho. Vždycky to můžeš dát do <#769966887055392768>, který snese cokoliv.

        **Je toho moc!** 🔕
        Pokud nemáš čas sledovat všechny diskuze, mrkni občas aspoň do <#789046675247333397>. Každý týden je tam shrnutí s nejoceňovanějšími příspěvky.

        Kanály, které víš, že tě nebudou zajímat, si můžeš povypínat. Jdi do kanálu a použij zvoneček. Na počítači je v horní liště, na mobilu se lišta zobrazí, až když zprava vysuneš seznam členů.

        Kategorii Archiv (úplně dole) si můžeš schovat kliknutím na její název. Jsou tam staré kanály, které už nepoužíváme, ale chceme, aby jejich historie zůstala ve vyhledávání.
    ''')


@schedule_message('💬')  # Day 3
def render_discord(context):
    return dedent('''
        V tomto tipu ti vysvětlím, jak funguje Discord. Co to vlastně je? Jak tady správně komunikovat? K čemu jsou a jak fungují vlákna?

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
    return dedent(f'''
        Dnes to bude o tom, že na junior.guru není jen klub, ale i spousta motivace a užitečných rad, které by bylo škoda minout.

        **Příručka** 📖
        Na https://junior.guru/handbook/ najdeš příručku pro juniory. Celá je zdarma ke čtení na webu a je v ní hromada užitečných tipů. Jak začít programovat? Jak si sehnat první praxi? Co je u pohovorů důležité? Jak připravit životopis? Tím vším a mnohým dalším tě příručka provede, krok za krokem. <@{HONZAJAVOREK}> stále přidává nové kapitoly, takže i pokud už máš něco přečtené, je dobré se tam po čase vracet.

        **Podcast** 🎙
        Nahoď sluchátka a pusť si do nich příběhy a rady lidí, kteří se motají kolem začátečníků v IT. <@810862212297130005> si zve na rozhovor juniory, lidi z firem, lektory kurzů. V podcastu se snaží přinášet odpovědi, inspiraci, motivaci. Všechny díly najdeš na https://junior.guru/podcast/, ale taky na Spotify, na YouTube a v dalších podcastových aplikacích. Epizody vychází jednou měsíčně a mívají půl hodiny. Máš nápad, koho dalšího pozvat? Napiš nám!
    ''')


@schedule_message('🙋')  # Day 5
def render_roles(context):
    return dedent('''
        Proč je někdo zelený, nebo žlutý? Co znamená medaile vedle jména? A proč se hodí používat emoji reakce na příspěvky?

        **Role** 🏅
        Na Discordu jde lidem dávat role, díky kterým mají barvu, ikonu vedle jména, jsou oddělení v seznamu členů, nebo mají nějaká oprávnění navíc.

        Na každém Discordu je to jinak, zcela podle chuti správců. V klubu se o většinu rolí starám já. Některé dávám jen pro lepší orientaci, jiné za zásluhy. Dvě role ti vysvětlím přímo tady. Popis ostatních najdeš kdykoliv v kanálu <#788822884948770846>.

        **Mám #ahoj a profilovku** 🦸
        Když se představíš v <#788823881024405544> a dáš si profilový obrázek, dostaneš ode mě roli <@&836959652100702248>. V uživatelském nastavení hledej sekci Profily nebo Uživatelský profil (_Profiles_ nebo _User Profile_). Nemusí to být fotka, jde pouze o to, abychom tu neměli deset Honzů, které nerozeznáme od sebe. Chodím do klubu zhruba jednou denně, takže je potřeba počkat, než se role objeví.

        **Hodně pomáhám** 💛
        Když si čteš v klubu a příspěvek tě zaujme, rozdávej emoji reakce, třeba ❤️, 👍, nebo 👀. Někdo si dal práci s odpovědí a je fajn vědět, že to ostatní čtou a že to pomohlo.

        Já reakce počítám a dělám z toho týdenní souhrny v <#789046675247333397>, ale nejen ty. Členové, kteří mají za poslední rok nebo měsíc nejvíc pozitivně hodnocených příspěvků, ode mě dostávají nejprestižnější roli v klubu, <@&836960665578766396>.

        Nehrajeme si na seniory a juniory. Kdokoliv může být nápomocný, ať už dobrou myšlenkou, otázkou, odpovědí, nebo sdílením zajímavých tipů.
    ''')


@schedule_message('💛')  # Day 6
def render_coc(context):
    return dedent(f'''
        Možná tě něco zajímá, ale bojíš se zeptat. Možná máš co napsat k tématu, ale nechceš riskovat nepříjemné reakce. Co když se ti někdo vysměje? Co když tě někdo nepochopí?

        **Neboj!** <:meowsheart:1002448596572061746>
        Smyslem celého klubu je, aby se začátečníci měli kde ptát a po ruce byl někdo, kdo jim poskytne pomoc, podporu nebo vysvětlení. Všichni jsme tu proto, abychom se něco naučili, sdíleli zkušenosti, radili se.

        To se ale může dařit jen pokud k sobě máme respekt a není tu čeho nebo koho se bát. Proto si dáváme záležet, aby tu bylo bezpečné a podporující prostředí.

        **Pravidla** ☑️
        Přečti si zásady, kterými se to tu řídí: https://junior.guru/coc/ Popisují, jak se tady snažíme komunikovat a co tu naopak vítáno není.

        Prohřešky bereme vážně. Na rozdíl od skupin např. na Facebooku, kde můžeš dostat posměšné, jízlivé, sexistické, nebo namachrované odpovědi, tady by byli takoví lidé rychle a rázně vyvedeni.

        **Piš moderátorům** 👮
        Lidi jsou jen lidi a psaný projev má své limity, takže i v klubu samozřejmě dochází k nedorozuměním. I dobře míněná, ale stručná věta může vyznít úsečně, nebo až agresivně.

        Hlídat nevhodné chování je jako dávat pozor, aby zahrádka nezarostla plevelem. Placený zahradník <@{HONZAJAVOREK}> vše vyřeší za tebe, ale nemá oči všude a uvítá pomoc.

        Stačí nechat pár kopřiv a záhonem se už nikdo chtít procházet nebude. Takže pokud se ti něco nepozdává, sdílej svoje pocity s moderátory. Neboj, zůstane to jen mezi vámi.
    ''')


@schedule_message('💡')  # Day 7
def render_asking(context):
    return dedent('''
        Klub je přínosný, i pokud si tady jen čteš. Nejsi však na Wikipedii, tohle je komunita! Když se zapojíš, poslouží ti mnohem lépe. Žádný strach, nic jako hloupá otázka tady neexistuje.

        **Ptej se i na blbosti** 🙋
        Přijde ti, že tvé dotazy jsou moc základní? Čím banálnější problém, tím snáz a rychleji ti může někdo odpovědět! Na obtížný problém je potřeba senior s mnoha lety praxe, ale zapomenutou závorku ti lehce opraví i junioři, kteří na tom jsou jen o něco lépe než ty. Svou otázkou jim dáváš šanci uvědomit si, že už něco umí, a radovat se, že dokázali poradit.

        **Kdo se ptá, ten se dozví** 💭
        Zajímá tě něco? Ptej se. Nejsi ve škole, kde se dotazy a chyby neodpouští. V klubu si myslíme, že je lepší se zeptat, a to klidně i „blbě”, než mlčet a nevědět. Každé nové téma k diskuzi je fajn. To, co vrtá hlavou tobě, často zajímá dalších třicet lidí, akorát nemají odvahu se zeptat.

        **Jak se ptát** 🤔
        Pokud existuje způsob, jak se zeptat lépe, nebo jak lze problém příště řešit i bez nás, tak ti to rádi a bez keců ukážeme. Nikoho neobtěžuješ. Není vůbec snadné položit programátorský dotaz správně a se vším, co k tomu patří. Je to dovednost jako každá jiná. Naučíš se ji jen tím, že se budeš často ptát. A taky přečtením návodu v příručce 😀 https://junior.guru/handbook/help/
    ''')


# ale říct že je to lepší pro klub a třeba "pokud chcete místní komunitu a klub podpořit, prosím napište svůj dotaz do kanálů tomu určených" nebo tak něco
# a potom něco jako : protože je to výhoda i pro ostatní - můžou to vidět, atp atd
#
# asi bych si to klidně i napsal do profilu, že to nestíhám, protože je dotazů hodně, pokud chcete mít "jistotu" že na váš dotaz někdo odpoví, napište ho veřejně :))
#
# @schedule_message('🥷')  # Day 8
# def render_public_over_private(context):
#     return dedent(f'''
#         Kromě citlivých věcí řeš všechno v kanálech, kde si to mohou přečíst i ostatní. Žádání o pomoc nebo názor v soukromých zprávách jde proti komunitní myšlence klubu.

#         **Piš veřejně** 📢
#         Veřejné dotazy jsou užitečné všem. Reakce dostaneš rychleji a budou zahrnovat zkušenosti od více lidí. Ostatní si diskuzi přečtou a poučí se, takže odpovídající vidí větší smysl v psaní propracovanějších mouder. <@{HONZAJAVOREK}> moudra vidí, může je sbírat a postupně dávat do příručky pro všechny. Win-win.

#         **Klub je komunita** 💞
#         Pomáháme si ve veřejných kanálech, všichni se při tom učíme, navzájem se obohacujeme. Díky tomu může být poplatek za klub minimální. Pokrývá jen provoz a rozvoj.

#         Zdejší profesionálové se ti věnují zdarma a z dobré vůle. Většina z nich sem chodí nahodile, když má volnou chvíli a chuť pomáhat. Respektuj to prosím. Klidně relevantní lidi označuj v kanálech a vláknech, aby si všimli. Nech však na nich, zda a kdy odpoví.

#         **Nevýhody soukromých zpráv** ✉️
#         Dotazům v SZ (nebo DM, jako _direct message_) se musí věnovat jen a pouze ten člověk, kterému píšeš. Nemusí mít čas se systematicky věnovat právě tobě, takže můžeš na odpověď dlouze čekat. Napíše ti pouze svůj názor. Nikdo ho neopraví. Nikdo jiný se z toho nepoučí.

#         **Mentoring** 💁
#         Nepředpokládej, že je OK žádat o pomoc přes soukromé zprávy. Nehledej ve veřejných kanálech lidi, kteří by ti „s něčím poradili v DM”. Výjimkami jsou moderátoři, kterým můžeš kdykoliv napsat a poradit se o čemkoliv ohledně klubu.

#         Profíky, kteří si vyhradili čas a energii na to, aby se juniorům věnovali i formou osobních konzultací, najdeš v kanálu <#976054742117658634>. Není to ale vhodné na jednorázové problémy, jedná se o dlouhodobější vztah.
#     ''')


# Dat feedback driv?
# co tu jde delat bude posledni ze serie tech zakladnich, pak uz jen payments


# **CO TU JDE DĚLAT**
# :speech_balloon: Diskutovat. Zkus #kariéra, #zdraví-těla, #kurzy…
# :tv: Chodit na online srazy a přednášky
# :clipboard:  Inzerovat v #práce, #pozvánky… Povolené, vítané!
# :person_tipping_hand: Najít řešení. Vytvoř vlákno v #mentoring, pomůžeme!
# :muscle:  Chlubit se! Umíš něco nového? #til Máš něco hotové? #výrobky
# :people_hugging: Ulevit si v #past-vedle-pasti
# TBD faq - co mam z clenstvi v klubu jako...? co tady jde delat… otevri tema, atd. a dat priklady co se muzou zeptat


####################################################################
# PAYMENTS AND FEEDBACK                                            #
####################################################################


### 🙇‍♂️ FEEDBACK
#
# - odkud prisel
# - co se ti tu libi
# - co se ti tu nelibi, co ti tu chybi


# @schedule_message('💸')  # Day 8
# def render_sth(context):
#     return dedent('''
#           Nazdar!
#     ''')


### 💸 PLACENI
#
#**Za co platíš?** 💸
# Ještě jednou připomenu, že částku neplatíš za službu „někdo mi radí“, ale za „existuje místo, které se snaží být tím místem, kde mi někdo pomůže“, to je zásadní rozdíl.  Něco jako když město postaví za tvoje daně na promenádě pódium pro buskery a pouliční muzikanti tam hrají zadarmo hudbu. Jestli zrovna tu tvoji oblíbenou v době, kdy tam procházíš, to už není na městu, to jen udělalo prostor.
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
# recenze a zkusenosti - jak pouzivat hledani
# kurzy, recenze a zkusenosti, vyhledavani, Co vyplývá z toho, že je členem klubu nějaká vzdělávací agentura?, zkus si vyhledat recenzi na SDA od niny nebo GFA od lukyho, Jak se klub liší od škol, akademií a kurzů? Faq


### 📺 EVENTY
#
# klubove prednasky, ukol pust si neco, discord eventy, jak to probíhá, vlastní akce, iniciativa, role organizuju akce
# :person_raising_hand: Organizovat vlastní akce, vytvářet studijní skupinky, mozna separatni tip na partaky a tak?

### 💁 MENTORING
# jak funguje mentoring, anna prednaska, prostuduj si to, Jak se klub liší od individuálního mentoringu? Faq


### 🧠 ZDRAVÍ MYSLI
# Zatím tam píšou pouze „běžní lidé“. Jediný, kdo tu má vzdělání v psychologii, je Nela. Pokud by tě štvalo i to, co píše ona, bylo by to blbé (ale spis pro Nelu? 😀). Pokud te štve to, co píšou laici, tak to akorát znamená, ze se jim nepovedlo vcitit se do tve situace, nebo ti nesedí způsob, jakým ti chtějí laicky pomoci. To je normální a muže se to stát. Když se diskuze ve zdraví mysli ubírá smerem, který není vhodný (napr. kdyby někdo napsal ze má depresi a někdo jiný mu na to napsal „to bude v pohodě, vždyť svět je krásný“), většinou si toho Nela vsimne a usměrni nás.

# Tedy co napíše Nela bych bral jako nějakou kvalifikovanější radu. Co napíšou ostatní - včetně mě - na tema zdraví mysli, bych bral jako takové to když se sveris kamarádům a oni se ti snaží pomoci, nebo to nějak okomentovat, nebo ti řeknou - já to mám stejně, nejsi v tom sama. Někdy to pomůže, někdy ne. Někdy se to trefí, někdy ne. Někdy pomůže už jen to, ze člověk svou frustraci ventiluje a ty rady lidi vlastně už ani nepotřebuje. Bývá to různé.


### 🏢 JOBS
# :clipboard:  Inzerovat v #práce, #pozvánky… Povolené, vítané!
# pracovní nabídky bot, web jobs, pripomenout mute, k cemu jsou palce
# **Buď vidět** 🦸


### 🚀 CV FEEDBACK
#
# cv feedback, kariera, pohovory, mentoring na pohovory, poh. nanecisto, precti si prirucku na tohle tema - Jak se klub liší od kariérního poradenství? Faq


### ⚽ RITUALY A AKTIVITY
# jak fungujou ritualy (viz pins), parťáci a spolecne aktivity jako adventofcode atd. - zkus vyresit hadanku a projdi partaky, zalozim vam mistnost, roli, atd.


### 🌈 SPOLUPRACE
# Spolupráce s firmami a komunitami - faq
# **Firemní role** ✨
# Firmy, které pomáhají financovat junior.guru, mohou kromě jiného posílat do klubu své lidi. Všichni mají roli <@&837316268142493736> a hvězdičky u jména. Každá firma má pak ještě i svou roli, např. <@&938306918097747968>.


####################################################################
# POWER USER TIPS                                                  #
####################################################################


### 🤓 DALSI TIPY
# 📌 Dej reakci špendlíku ke zprávě, @kuře ti ji uloží
# discord tipy zasobnik - citace, odkazy na zpravy, shift enter
# **Online odkudkoliv** 💌
# Discord jede jen tak v prohlížeči, ale má i svou aplikaci na počítač a na mobil. Mít klub v kapse se hodí, pokud se chceš zabavit nebo pomáhat, když zrovna čekáš ve frontě na poště.


####################################################################
# COLLECTING FEEDBACK                                              #
####################################################################
# TODO
# mozna by to mohla byt i rychla anketa v #pravidla, stejne jako zaklikavani jazyku atd.
