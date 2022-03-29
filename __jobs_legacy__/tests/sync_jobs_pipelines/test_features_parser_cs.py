import pytest

from juniorguru.jobs.legacy_jobs.pipelines.features_parser import parse_from_sentence


def get_rule_ids(parse_results):
    return {rule_id for rule_id, match, pattern in parse_results}


@pytest.mark.parametrize('sentence', [
    'AJ minimálně na úrovni technické specifikace',
    'Angličtinu minimálně na úrovni technické specifikace',
    'AJ alespoň na úrovni porozumění',
    'Znalost anglického jazyka minimálně na úrovni aktivního písemného projevu a porozumění odbornému textu',
    'komunikativní znalost AJ',
    'jazykové znalosti: CZ, EN',
    'komunikativní znalost anglického nebo německého jazyka',
    'výborná znalost ČJ/SJ, pokročilá AJ',
    'domluvíš se anglicky',
    'komunikativní znalost anglického jazyka a český / slovenský jazyk podmínkou',
    'Umíte anglicky dostatečně dobře abyste se domluvili.',
    'technická AJ',
])
def test_parse_from_sentence_cs_english_required(sentence):
    assert 'ENGLISH_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'máš k dispozici plně hrazenou výuku angličtiny a němčiny',
    'Jazykové kurzy (angličtina, španělština, čínština..)',
    'PHP programátor - GPS sledování, bez AJ (35-55.000 Kč)',
    'C++ Developer | Nekorporát bez EN',
])
def test_parse_from_sentence_cs_english_required_not(sentence):
    assert 'ENGLISH_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Ve vývoji ve frontendu/backendu už nejsi úplný zelenáč',
    'pár projektů máš za sebou',
    'Dobrá znalost Android SDK.',
    'Zkušenost s vývojem rozsáhlejších webových aplikací',
    'zkušenosti s návrhem a vývojem aplikací na platformě Java EE',
    'týmový hráč s širokým rozhledem v oblasti technologií používaných pro vývoj Java aplikací',
    'pokročilá znalost jazyka Java, OOP a návrhových vzorů',
    'Dobrá znalost jazyka C# a zkušenost s vývojem na .NET platformě',
    'Pokročilá znalost GIT flow a code review.',
    'výborné znalosti s REST API a přehled o síťových protokolech a knihovnách (Alamofire, Firebase, atp.)',
    'Alespoň minimální komerční zkušenosti s Javou',
    'Zkušenosti s vývojem aplikací na platformě AWS v Java, případně Python',
    'relevantní praxi v daném oboru',
    'Nebo již máš řadu projektů za sebou a rád se zapojíš do nového týmu, popř.',
    'máš ambice v blízké době postoupit do role architekta?',
    'máš za sebou již slušnou řádku zářezů ve vývoji v JavaScriptu a Reactu',
    'máš schopnost architektonicky strukturovat části aplikace',
    'výborné znalosti XHTML a CSS2',
    'praxe s provozováním databází a práce s SQL',
    'Skvělé algoritmické a technické myšlení',
    'praxi z vývoje komplexních aplikací v týmech',
    'Praxi ve vývoji webových aplikací',
    'Perfektní znalost OOP a PHP7, SQL',
    'Velmi dobrá znalost HTML5/CSS/JavaScript pro Front-End Development',
    'spolehlivost a samostatnost při řešení problémů',
    'dobrá znalost OS Linux včetně konfigurace',
    'spolupracovat s juniorními kolegy a kvalitně je nasměrovat',
    'Máš solidní background s vývojem škálovatelného produktu a praktickou zkušenost s ukládáním do cache.',
    'přehled o databázích a dalších úložištích (PostgreSQL, MySQL nebo Redis, Elasticsearch)',
    'zodpovědnost za projekt od plánování, vývoje, realizace až po jeho testování',
])
def test_parse_from_sentence_cs_advanced_required(sentence):
    assert 'ADVANCED_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Školní nebo komerční praxe v .NET',
    'Samostatnost, zodpovědnost, čitelný kód',
    'Praktické zkušenosti s GIT, Maven',
    'schopnost převzít zodpovědnost',
    'Mít předchozí zkušenosti s programováním ve Swiftu (mohou být i ze školy).',
    'Praxi v IT oblasti v největší české bance',
    'Pozice je vhodná jak pro uchazeče s praxí, tak umíme poskytnout podporu i absolventům.',
    'Vítána zkušenost ve vývoji databázových aplikací pro ERP systémy.',
    'vítány zkušenosti ve vývoji databázových aplikací',
    'praxe',
    'bez komunikativní znalosti angličtiny se neobejdeš, stejně jako s perfektní znalostí češtiny nebo slovenštiny',
    'ČJ/SJ ovládáš na výborné úrovni, neobejdeš se bez znalosti alespoň technické angličtiny',
    'Nemusíš mít za sebou dlouholetou praxi',
    'Pošli nám zprávu a připoj životopis, svůj profil na LinkedInu nebo cokoliv jiného, z čeho poznáme, co máš za sebou',
    'výborná znalost ČJ/SJ, pokročilá AJ',
    'ČJ/SJ na výborné úrovni, znalost technické angličtiny nebo němčiny',
    'Chceš získávat zkušenosti z vývoje aplikací napříč odvětvími',
    'protože budeš pracovat se Zdeňkem naším architektem',
    'Není nutné znát programovací jazyky nebo mít přehled v IT',
    'U nás jsme všichni zodpovědní za to, jak firma funguje',
    'Práci v malém týmu zodpovědném za návrh',
    'Získáte přehled o IT trhu',
    'Podílejte se společně s námi na návrhu architektury a vyzkoušejte si nové technologie.',
    'Nezáleží nám na zkušenostech a dosavadní praxi, zejména hledáme nadšence, kterého bude práce bavit a bude plnohodnotným členem v týmu.',
    'Možnost získat praxi v oboru',
])
def test_parse_from_sentence_cs_advanced_required_not(sentence):
    assert 'ADVANCED_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'SŠ/VŠ vzdělání technického zaměření',
    'Absolvent/ka SŠ nebo VŠ (IT nebo technický obor)',
    'studium informatiky nebo příbuzného oboru',
    'VŠ technického směru (ideálně zaměření na tvorbu SW)',
    'VŠ/SŠ v oboru informačních technologií (příležitost i pro absolventy)',
    'Je určitě plus, pokud už máš vysokoškolský titul (ideálně s IT zaměřením) nebo jej brzy získáš.',
])
def test_parse_from_sentence_cs_tech_degree_required(sentence):
    assert 'TECH_DEGREE_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Vzdělání:vyšší odborné, SŠ s maturitou, bakalářské, vysokoškolské',
    'VŠ/SŠ vzdělání v oblasti elektrotechniky/IT či relevantní praxi v daném oboru',
    'SŠ, VŠ vzdělání',
    'SŠ/VŠ vzdělání - obor nerozhoduje, vítáno IT,',
    'Pozice je vhodná i pro studenty či absolventy střední či vysoké školy.',
    'Vzdělání: SŠ/VŠ',
    'Uvítáme i šikovné absolventy, ale rádi bychom v tobě viděli chuť se učit, zapáleností pro technologie.',
])
def test_parse_from_sentence_cs_tech_degree_required_not(sentence):
    assert 'TECH_DEGREE_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Znalost problematiky programování webových aplikací (min. 3 roky)',
    'je potřeba mít min rok praktickou zkušenost s Docker',
    'praxe v oboru 2 roky nebo přesvědčivý projekt',
    'máš za sebou cca 2 roční zkušenosti a projekty v Javě',
])
def test_parse_from_sentence_cs_years_experience_required(sentence):
    assert 'YEARS_EXPERIENCE_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Jsme stabilní rodinná firma s více než 20 let zkušeností a dlouhodobými projekty',
    'Máš zájem zapojit se do mladého kolektivu s věkovým průměrem okolo 23 let na pozici programátora?',
    'Už 10 let pomáháme lidem podnikat',
])
def test_parse_from_sentence_cs_years_experience_required_not(sentence):
    assert 'YEARS_EXPERIENCE_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'komunikativní znalost anglického nebo německého jazyka',
])
def test_parse_from_sentence_cs_german_required(sentence):
    assert 'GERMAN_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'máš k dispozici plně hrazenou výuku angličtiny a němčiny',
])
def test_parse_from_sentence_cs_german_required_not(sentence):
    assert 'GERMAN_REQUIRED' not in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Samostatnost, zodpovědnost, čitelný kód',
    'Aktivní a samostatný přístup k práci',
    'Schopnost pracovat samostatně, přesto mít týmového ducha.',
    'schopnost pracovat samostatně, ale zároveň týmový duch',
    'Jsi samostatný/á – vítáš self-management.',
    'zajímá tě nejenom práce v týmu, ale zvládáš i samostatnou práci',
    'jsi zodpovědný, samostatný a je na tebe spolehnutí',
    'Musíte ale umět pracovat do značné míry i samostatně.',
    'spolehlivost a samostatnost při řešení problémů',
    'Schopnost sebeřízení, týmové i individuální práce',
])
def test_parse_from_sentence_cs_independence_preferred(sentence):
    assert 'INDEPENDENCE_PREFERRED' in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Smluvní mzdu - individuální ujednání v návaznosti na pracovní zkušenosti a ...',
    'nezáleží, zda u nás chceš pracovat na HPP nebo třeba na živnost – individuálně hledáme řešení',
    'Mnoho funkcionalit již máme implementováno, ale stále přidáváme nové a nové, které většinou poběží jako samostatné mikroservisy.',
])
def test_parse_from_sentence_cs_independence_preferred_not(sentence):
    assert 'INDEPENDENCE_PREFERRED' not in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Zvýšíme výrazně tvojí hodnotu na trhu, naučíme tě pracovat s mnoho DevOps a Cloud technologiemi',
    'Jsi čerstvý absolvent/ka a rád/a by ses věnoval/a programování?',
    'Alespoň základní znalost programování v C++ (vše ostatní tě naučíme)',
    'nastartujte svou kariéru',
    'Nabízíme fulltime-job, vhodný i pro absolventy s dostatečnou znalostí.',
    'Co neumíš, to se naučíš – nehledáme supermana.',
    'Budeš mít spoustu prostoru se učit.',
    'Pokud ještě studuješ, umožníme ti skloubit školu s prací',
    'třeba nemají léta zkušeností, ale chtějí se učit',
    'máš za sebou již nějaké zkušenosti a projekty v Javě (třeba i ze školy)',
    'Nemusíš umět nazpaměť odříkat celou iOS dokumentaci',
    'Nemusíš být zkušeným vývojářem.',
    'Rádi tě vše naučíme.',
    'Pozice je vhodná i pro studenty či absolventy střední či vysoké školy.',
    'Mít předchozí zkušenosti s programováním ve Swiftu (mohou být i ze školy).',
    'Příležitost pro absolventy, kteří se chtějí hodně naučit',
    'Znalost programovacího jazyka (předně Java, Javascript, C++, C také C#, Python)',
    'Ze začátku budeš dostávat menší úkoly, kterými se naučíš nové věci a zároveň nám pomůžeš.',
    'Vhodné i pro studenty',
    'Nemusíš mít za sebou dlouholetou praxi',
    'alespoň jeden hotový projekt',
    'Pokud máte zkušenosti s jinými jazyky např. C++, C#, Java, podpoříme přeškolení',
    'Projekťák na zácvik!',
    'společně se seniorním developerem se budeš podílet na analýze',
    'vždy k sobě budeš mít někoho, kdo ti pomůže',
    'Znalost Golang (naučíme pokud neumíš)',
    'Zlepšování znalostí PHP, Git, HTML, JavaScript a MySQL',
    'Rozšiřování znalostí práce s Dockerem, Symfony frameworkem',
    'Pokud některé technologie neznáte, velmi rádi vám pomůžeme se toho co nejvíce naučit.',
    'máš zkušenosti s React.js (nebo se to dokážeš rychle doučit)',
    'Nezáleží nám na zkušenostech a dosavadní praxi, zejména hledáme nadšence, kterého bude práce bavit a bude plnohodnotným členem v týmu.',
    'Vezme si tě na starost jeden z našich zkušených programátorů a bude ti pomáhat.',
    'Alespoň 2x týdně práce z kanceláře (Praha 8 - Karlín) (nebráníme se ani spolupráci se studenty)',
    'umí (nebo má chuť se naučit) programovat v Symfony',
    'Možnost získat praxi v oboru',
    'Pomůžeme ti, aby jsi se rychle začlenil do týmu a mohl mít pocit z dobře vykonané práce.',
    'po tvém nástupu dostaneš přiděleného mentora, který tě zasvětí do fungování vývojové infrastruktury, tvorby aplikací',
    'V zádech budeš mít vždycky tým zkušenějších administrátorů, kterým budeš moct případné složitější problémy předat.',
    'Od nich je také možné naučit se spoustu nového a postupně přejímat zajímavější oblasti problémů k řešení',
    'Mentoring ze strany seniornějších kolegů je samozřejmostí.',
])
def test_parse_from_sentence_cs_junior_friendly(sentence):
    assert 'JUNIOR_FRIENDLY' in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Angličtinu alespoň na základní úrovni',
    'Stravenky, Sickdays, možnost HomeOffice (po zaučení)',
    'práce odkudkoliv – jedná se o práci na dálku, po zaučení můžeš mít tedy 100% „home office“ (ze začátku ideální pracovat z ARTINu Praha)',
])
def test_parse_from_sentence_cs_junior_friendly_not(sentence):
    assert 'JUNIOR_FRIENDLY' not in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Hledáme juniorního vývojáře, který rozšíří řady našich backenďáků',
    'Junior Linux Admin (part-time)',
    'A ačkoli k nám přijdeš jako junior, během chvíle můžeš raketově vyrůst vzhůru',
    'Na pozici Graduate/Junior Software Developer budete pracovat na vývoji',
    'A ačkoli k nám přijdeš jako junior, během chvíle můžeš raketově vyrůst vzhůru',
    'Padawan pro QA Team – tester',
    'PHP programátor - Vývojářův učeň (25-45.000 Kč)',
    'Internship: JAVA DEVELOPER ',
])
def test_parse_from_sentence_cs_explicitly_junior(sentence):
    assert 'EXPLICITLY_JUNIOR' in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Pokud hledáte spíše juniornější pozici, podívejte se na naše další inzeráty nebo na web níže.',
])
def test_parse_from_sentence_cs_explicitly_junior_not(sentence):
    assert 'EXPLICITLY_JUNIOR' not in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'As a senior developer your will focus',  # mixed language jobs posting
    'má seniorní zkušenost s frontendem.',
])
def test_parse_from_sentence_cs_explicitly_senior(sentence):
    assert 'EXPLICITLY_SENIOR' in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Uděláme z tebe seniora😁',
    'společně se seniorním developerem se budeš podílet na analýze',
    'Budete TÝM se senior technikem',
    'Pracovat v tandemu se Senior technikem',
    'Mentoring ze strany seniornějších kolegů je samozřejmostí.',
])
def test_parse_from_sentence_cs_explicitly_senior_not(sentence):
    assert 'EXPLICITLY_SENIOR' not in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'Předchozí zkušenost s vedením týmu',
])
def test_parse_from_sentence_cs_leadership_required(sentence):
    assert 'LEADERSHIP_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'cs'))


@pytest.mark.parametrize('sentence', [
    'chuť učit se novým věcem',
    'ochota a schopnost učit se novým technologiím',
    'chuť inovovat a stále se učit nové věci',
    'analytické myšlení, schopnost rychle se učit novým věcem',
    'Schopnost učit se a získané znalosti dál rozvíjet.',
    'Chuť se stále učit a pracovat na sobě',
    'máš zapálení pro práci a chuť na sobě pracovat',
    'Chuť se učit novým věcem.',
    'ochotu učit se nové věci',
    'chuť učit se a pracovat v týmu',
    'Ochotu učit se novým věcem',
    'Nejvíc nás ale zajímá tvoje otevřenost a chuť se rozvíjet.',
    'třeba nemají léta zkušeností, ale chtějí se učit',
    'učit se a neustále aktivně posouvat svoje znalosti potřebné během vývoje',
    'Učení a rozvoj sebe samého.',
    'který se bude chtít postupně rozvíjet',
    'Rozvíjet se v programovacích jazycích.',
])
def test_parse_from_sentence_cs_learning_required(sentence):
    assert 'LEARNING_REQUIRED' in get_rule_ids(parse_from_sentence(sentence, 'cs'))
