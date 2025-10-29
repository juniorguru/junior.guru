import pytest

from jg.coop.lib.text import extract_text
from jg.coop.sync.jobs_scraped.pipelines.language_parser import process


@pytest.mark.asyncio
async def test_language_parser_process():
    description_text = """
        <section class="description"><div class="description__text description__text--rich"><ul>
        <li>tworzenie i rozwój aplikacji w oparciu o wymagania biznesowe przy wykorzystaniu najlepszych
        praktyk programowania,</li><li> projektowanie responsywnych i nowoczesnych aplikacji
        front-endowych,</li><li> opracowywanie i obsługa testów jednostkowych oprogramowania,</li>
        <li> dzielenie się wiedzą, przeprowadzanie code review,</li><li> przygotowanie/aktualizacja
        technicznej dokumentacji poprojektowej.</li><li> wykształcenia wyższego (preferowane kierunki
        informatyczne lub pokrewne),</li><li> min. 3-letnie doświadczenie komercyjne w tworzeniu
        aplikacji webowych</li><li> Znajomość i doświadczenie w pracy z technologiami:</li><li> HTML5,
        CSS3, bardzo dobra znajomość JavaScript (ES6/ES7), TypeScript, Bootstrap, ReactJS (Saga, Redux),
        jQuery, TSlint/JSLint, Webpack, Gulp/Grunt, Node.js, NPM, Preprocesor SASS/LESS, wzorców
        projektowych OOP, Webserwisy REST, W3C</li><li> znajomości systemu kontroli wersji Git,</li>
        <li> znajomość zagadnień z optymalizacji i wydajności aplikacji,</li><li> znajomości j. angielskiego
        na poziomie umożliwiającym swobodną pracę z dokumentacją techniczną.<br><br></li><strong>
        <u>Mile Widziane<br><br></u></strong><li> doświadczenie w pracy z Jenkins/Jira Confluence,</li>
        <li> znajomość narzędzi ciągłej integracji CI/CD,</li><li> doświadczenie w pracy w zespole Scrum,</li>
        <li> znajomość techniki TDD.</li><li> umowa o pracę,</li><li> pracę w doświadczonym zespole,
        przy rozwoju jednej z największych platform integracyjnych w kraju,</li><li> atrakcyjny pakiet
        socjalno-motywacyjny, w tym prywatną opiekę zdrowotną i Pracowniczy Program Emerytalny,</li>
        <li> konkurencyjne wynagrodzenie,</li><li> pakiet benefitów,</li><li> profesjonalny system...
    """
    item = dict(
        title="Junior Software Engineer",
        description_text=extract_text(description_text),
    )
    item = await process(item)

    assert item["lang"] == "pl"


@pytest.mark.asyncio
async def test_language_parser_process_missing_body_does_not_raise():
    item = dict(
        title="Junior Software Engineer",
        description_text="-",
    )
    item = await process(item)

    assert len(item["lang"]) == 2
