import pytest

from juniorguru.jobs.legacy_jobs.pipelines.short_description_filter import (
    Pipeline, ShortDescription)


def test_short_description_filter(item, spider):
    item['description_html'] = '''
        <div class="description__text description__text--rich">Požadavky<br>
        <br>Zkušenosti s programováním v Pythonu<br>Python 2x, Python 3x<br>
        PostgreSQL/SQL server<br><br>Preferujeme<br>Django framework<br>
        Vue.js<br>HTML5<br><br>Náplň práce<br><br>Do týmu "srdcařů" hledáme
        Python developery do OLOMOUCE<br><br>Možnost spolupráce jak HPP tak
        i DPP či freelance.<br><br>Jedná se o práci na dlouhodobých českých
        i zahraničních projektech, vývoj sw na zakázku. Bližší informace
        o našich projektech Vám rádi představíme osobně :-)<br><br>Nabízíme<br>
        <br><strong><u>Nadstandardní Benefity<br><br></u></strong>cvičení s
        fyzioterapeutem v pracovní době /abyste si protáhli záda od sezení
        u PC/<br>stravenky 100 Kč<br>každých 6 měsíců přehodnocení platu<br>
        příspěvek na nákup techniky<br>příspěvek na penzijní či jiné
        připojištění<br>firemní telefonní číslo i pro blízkou rodinu s výhodným
        tarifem<br>nadstandardní příplatky navíc za support na telefonu pro
        zákazníky<br>systém kafeteria<br>a v neposlední řadě výborný pohodový
        tým, férové jednání</div>
    '''

    assert len(item['description_html']) > Pipeline.min_chars_count
    Pipeline().process_item(item, spider)


def test_short_description_filter_drops(item, spider):
    item['description_html'] = '''
        <div class="description__text description__text--rich">
        Nabízíme možnost vybrat si z variace projektů, na kterých využijete
        nejmodernější technologie pro vývoj aplikací v oblasti zdravotnictví
        a státních institucí (zdravotní pojišťovny, nemocnice, státní a veřejná
        správa, finanční a kapitálové trhy). Pracovat můžete v distribuovaných
        týmech zkušených i méně zkušených programátorů pod vedením zběhlých
        ředitelů vývoje.* 5 týdnů dovolené* firemní notebook a telefon*
        vzdělávací kurzy (odborné i...
        </div>
    '''

    assert len(item['description_html']) < Pipeline.min_chars_count
    with pytest.raises(ShortDescription):
        Pipeline().process_item(item, spider)



def test_short_description_filter_drops_regardless_html(item, spider):
    item['description_html'] = '''
        <div class="description__text description__text--rich">
        <strong>Nabízíme možnost vybrat</strong> si z variace projektů,
        na kterých <a href="https://www.example.com/example?q=1">využijete</a>
        nejmodernější technologie pro vývoj aplikací v oblasti zdravotnictví
        a státních institucí (zdravotní pojišťovny, nemocnice, státní a veřejná
        správa, finanční a kapitálové trhy). Pracovat můžete v distribuovaných
        týmech zkušených i méně zkušených programátorů pod vedením zběhlých
        ředitelů vývoje.* 5 týdnů dovolené* firemní notebook a telefon*
        vzdělávací kurzy (odborné i...
        </div>
    '''

    assert len(item['description_html']) > Pipeline.min_chars_count
    with pytest.raises(ShortDescription):
        Pipeline().process_item(item, spider)
