from pathlib import Path
from textwrap import dedent

import pytest
from lxml import html
from strictyaml import Enum, Map, Optional, Seq, Str

from juniorguru.jobs.legacy_jobs.pipelines import sections_parser
from juniorguru.jobs.legacy_jobs.pipelines.sections_parser import (ListSection,
                                                           TextFragment)
from testing_utils import (load_yaml, param_startswith_skip,
                           param_xfail_missing, startswith_skip)


schema = Seq(
    Map({
        Optional('heading'): Str(),
        'type': Enum(['paragraph', 'list']),
        'contents': Seq(Str()),
    })
)


def generate_params(fixtures_dirname):
    for html_path in (Path(__file__).parent / fixtures_dirname).rglob('*.html'):
        if startswith_skip(html_path):
            yield param_startswith_skip(html_path)
        else:
            yml_path = html_path.with_suffix('.yml')
            if startswith_skip(yml_path):
                yield param_startswith_skip(yml_path)
            elif yml_path.is_file():
                yield pytest.param(html_path.read_text(),
                                   load_yaml(yml_path.read_text(), schema),
                                   id=html_path.name)  # better readability
            else:
                yield param_xfail_missing(yml_path)


@pytest.mark.parametrize('description_html,expected',
                         generate_params('fixtures_sections_parser'))
def test_sections_parser(item, spider, description_html, expected):
    item['description_html'] = description_html
    item = sections_parser.Pipeline().process_item(item, spider)

    assert item['sections'] == expected


def test_intersperse():
    assert sections_parser.intersperse([1, 2, 3], 42) == [1, 42, 2, 42, 3]


def test_section_to_re():
    section = ListSection(heading='Who are you?', contents=[
        'You are a native German speaker',
        'You love self-management',
    ])

    assert sections_parser.section_to_re(section).pattern == (
        r'\s*'
        r'Who\ are\ you\?'
        r'\s+'
        r'(?:\W{1,2} )?You\ are\ a\ native\ German\ speaker'
        r'\s+'
        r'(?:\W{1,2} )?You\ love\ self\-management'
        r'\s*'
    )


def test_section_to_re_no_heading():
    section = ListSection(heading='', contents=[
        'You are a native German speaker',
        'You love self-management',
    ])

    assert sections_parser.section_to_re(section).pattern == (
        r'\s*'
        r'(?:\W{1,2} )?You\ are\ a\ native\ German\ speaker'
        r'\s+'
        r'(?:\W{1,2} )?You\ love\ self\-management'
        r'\s*'
    )


@pytest.mark.parametrize('section', [
    ListSection(heading='Who are you?', contents=[]),
    ListSection(heading='', contents=[])
])
def test_section_to_re_no_contents(section):
    with pytest.raises(ValueError):
        sections_parser.section_to_re(section)


def test_split_by_section():
    text_fragment = TextFragment(dedent('''
        Text before the list section 💖

        Who are you?

        You are a native German speaker
        You love self-management and can use common sense

        Text after the list section 🛠
    '''))
    section = ListSection(heading='Who are you?', contents=[
        'You are a native German speaker',
        'You love self-management and can use common sense',
    ])

    assert list(sections_parser.split_by_section(text_fragment, section)) == [
        TextFragment('Text before the list section 💖'),
        section,
        TextFragment('Text after the list section 🛠'),
    ]


def test_split_by_section_no_before_text():
    text_fragment = TextFragment(dedent('''
        Who are you?

        You are a native German speaker
        You love self-management and can use common sense

        Text after the list section 🛠
    '''))
    section = ListSection(heading='Who are you?', contents=[
        'You are a native German speaker',
        'You love self-management and can use common sense',
    ])

    assert list(sections_parser.split_by_section(text_fragment, section)) == [
        section,
        TextFragment('Text after the list section 🛠'),
    ]


def test_split_by_section_no_after_text():
    text_fragment = TextFragment(dedent('''
        Text before the list section 💖

        Who are you?

        You are a native German speaker
        You love self-management and can use common sense
    '''))
    section = ListSection(heading='Who are you?', contents=[
        'You are a native German speaker',
        'You love self-management and can use common sense',
    ])

    assert list(sections_parser.split_by_section(text_fragment, section)) == [
        TextFragment('Text before the list section 💖'),
        section,
    ]


def test_split_by_section_multiple_matches():
    text_fragment = TextFragment(dedent('''
        Text before the list section 💖

        Who are you?

        You are a native German speaker
        You love self-management and can use common sense

        Text between the sections 👀

        Who are you?

        You are a native German speaker
        You love self-management and can use common sense

        Text after the list section 🛠
    '''))
    section = ListSection(heading='Who are you?', contents=[
        'You are a native German speaker',
        'You love self-management and can use common sense',
    ])

    assert list(sections_parser.split_by_section(text_fragment, section)) == [
        TextFragment('Text before the list section 💖'),
        section,
        TextFragment('Text between the sections 👀'),
        section,
        TextFragment('Text after the list section 🛠'),
    ]


def test_split_sentences():
    assert sections_parser.split_sentences(
        'Who we are?\n'
        'What do we do? '
        'Our mission is to create Frankenstein! '
        'Really. '
        'Trust us'
    ) == [
        'Who we are?',
        'What do we do?',
        'Our mission is to create Frankenstein!',
        'Really.',
        'Trust us',
    ]


def test_extract_text():
    el = html.fromstring(dedent('''
        Fronted developer JavaScript, HTML – Praha 3 – HPP/IČO<br>Hledáme
        nového frontend developera.<br><br><strong><u>Co Bys u Nás
        Dělal(a)<br></u></strong>
        <ul>
            <li>Vývoj aplikačního SW.</li>
            <li>Dále se rozvíjet a vzdělávat v rámci pozice.<br></li>
        </ul>
        Požadujeme:Co od tebe očekáváme:<br>
    ''').strip())

    assert sections_parser.extract_text(el) == (
        'Fronted developer JavaScript, HTML – Praha 3 – HPP/IČO\n'
        'Hledáme nového frontend developera.\n'
        'Co Bys u Nás Dělal(a)\n'
        'Vývoj aplikačního SW.\n'
        'Dále se rozvíjet a vzdělávat v rámci pozice.\n'
        'Požadujeme:Co od tebe očekáváme:'
    )


def test_fix_orphan_html_list_items():
    el = html.fromstring('''
        <div>Requirements:
        <li><strong>PHP</strong></li>
        <li style="color: red">Java</li>
        <li>Python</li>
        Contact us at company@example.com</div>
    '''.strip())
    el = sections_parser.fix_orphan_html_list_items(el)

    assert html.tostring(el, encoding=str) == '''
        <div>Requirements:
        <ul><li><strong>PHP</strong></li>
        <li style="color: red">Java</li>
        <li>Python</li></ul>
        Contact us at company@example.com</div>
    '''.strip()


def test_fix_orphan_html_list_items_remove_standalone_item():
    el = html.fromstring('''
        <div>Requirements:
        <li><strong>PHP</strong></li>
        Java<br>Python<br>
        Contact us at company@example.com
        <li>Java</li><li>Python</li>
        </div>
    '''.strip())
    el = sections_parser.fix_orphan_html_list_items(el)

    assert html.tostring(el, encoding=str) == '''
        <div>Requirements:
        <span><strong>PHP</strong></span><br>
        Java<br>Python<br>
        Contact us at company@example.com
        <ul><li>Java</li><li>Python</li></ul>
        </div>
    '''.strip()


def test_flatten_nested_html_lists():
    el = html.fromstring('''
        <div>Requirements:
        <ul>
            <li><strong>PHP</strong></li>
            <li style="color: red">
                Java, also:
                <li>Python</li>
                <li>C#</li>!</li>
            <li>HTML</li>
        </ul>
        Contact us at company@example.com</div>
    '''.strip())
    el = sections_parser.flatten_nested_html_lists(el)

    assert html.tostring(el, encoding=str) == '''
        <div>Requirements:
        <ul>
            <li><strong>PHP</strong></li>
            <li style="color: red">
                Java, also:
                </li><li>Python</li>
                <li>C#</li>!
            <li>HTML</li>
        </ul>
        Contact us at company@example.com</div>
    '''.strip()


def test_fix_disconnected_html_lists():
    el = html.fromstring('''
        <div>Requirements:
        <ul><li><strong>PHP</strong></li>
        <li style="color: red">Java</li></ul>
        <ul><li>Python</li></ul>
        <ul><li>C#</li></ul>
        Contact us at company@example.com
        <ul><li>Free food!</li></ul></div>
    '''.strip())
    el = sections_parser.fix_disconnected_html_lists(el)

    assert html.tostring(el, encoding=str) == '''
        <div>Requirements:
        <ul><li><strong>PHP</strong></li>
        <li style="color: red">Java</li><li>Python</li><li>C#</li></ul>
        Contact us at company@example.com
        <ul><li>Free food!</li></ul></div>
    '''.strip()
