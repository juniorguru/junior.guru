import re
import itertools
from pathlib import Path

import pytest


SCSS_VARIABLE_RE = re.compile(r'(\$[^:]+):\s+([^;]+);')
CSS_VARIABLE_RE = re.compile(r'(\-\-[^:]+):\s+([^;]+);')
SVG_FILL_RE = re.compile(r"fill='(\#[^']+)'" + r'|fill="(\#[^"]+)"|fill:\s*(\#[^;]+);')
PACKAGE_DIR = Path(__file__).parent.parent / 'juniorguru'


def parse(css_text, match_re):
    for line in css_text.splitlines():
        match = match_re.search(line)
        if match:
            yield match


def find_fill(svg_text):
    try:
        return next(filter(None, SVG_FILL_RE.search(svg_text).groups()))
    except (AttributeError, StopIteration):
        raise ValueError('Could not find the fill declaration in given SVG')


@pytest.fixture
def source_of_truth():
    path = PACKAGE_DIR / 'web' / 'static' / 'src' / 'css-mkdocs' / '_defaults.scss'
    return {match.group(1): match.group(2) for match
            in parse(path.read_text(), SCSS_VARIABLE_RE)
            if match.group(1).startswith('$jg-')}


def test_source_of_truth_variables_exist(source_of_truth):
    assert source_of_truth


VARS_LEGACY_WEB = [
    (match.group(1), match.group(2))
    for match in
    parse((PACKAGE_DIR / 'web' / 'static' / 'src' / 'css' / 'spaghetti' / 'variables.scss').read_text(), SCSS_VARIABLE_RE)
    if match.group(1).startswith('$jg-')
]


def test_legacy_web_variables_exist():
    assert VARS_LEGACY_WEB


@pytest.mark.parametrize('name, value', VARS_LEGACY_WEB)
def test_legacy_web(name, value, source_of_truth):
    assert source_of_truth[name] == value


VARS_LEGACY_WEB_DOTS = [
    (match.group(1), match.group(2))
    for match in
    parse((PACKAGE_DIR / 'web' / 'static' / 'src' / 'css' / 'spaghetti' / 'variables.scss').read_text(), SCSS_VARIABLE_RE)
    if match.group(1).startswith('$dots-')
]


def test_legacy_web_dots_variables_exist():
    assert VARS_LEGACY_WEB_DOTS


@pytest.mark.parametrize('name, value', VARS_LEGACY_WEB_DOTS)
def test_legacy_web_dots(name, value, source_of_truth):
    color = source_of_truth[name.replace('$dots-', '$jg-')].replace('#', '%23')

    assert f"fill='{color}'" in value


VARS_IMAGE_TEMPLATES = [
    (match.group(1), match.group(2))
    for match in
    parse((PACKAGE_DIR / 'image_templates' / 'variables.css').read_text(), CSS_VARIABLE_RE)
    if match.group(1).startswith('--color-')
]


def test_image_templates_variables_exist():
    assert VARS_IMAGE_TEMPLATES


@pytest.mark.parametrize('name, value', VARS_IMAGE_TEMPLATES)
def test_image_templates(name, value, source_of_truth):
    assert source_of_truth[name.replace('--color-', '$jg-')] == value


SVG_IMAGES_WEB = list(itertools.chain(
    (PACKAGE_DIR / 'web' / 'static' / 'src' / 'images').glob('*.svg'),
    (PACKAGE_DIR / 'web' / 'static' / 'src' / 'images' / 'donate').glob('*.svg'),
    (PACKAGE_DIR / 'images').glob('*.svg'),
))


def test_svg_images_exist():
    assert SVG_IMAGES_WEB


@pytest.mark.parametrize('path', [
    pytest.param(path, id=str(path)) for path in SVG_IMAGES_WEB
    if path.stem.endswith('-i')
])
def test_white_svg_images(path, source_of_truth):
    color = source_of_truth['$jg-white']

    assert find_fill(path.read_text()) == color


@pytest.mark.parametrize('path', [
    pytest.param(path, id=str(path)) for path in SVG_IMAGES_WEB
    if path.stem.endswith('-blue')
])
def test_blue_svg_images(path, source_of_truth):
    color = source_of_truth['$jg-blue']

    assert find_fill(path.read_text()) == color


@pytest.mark.parametrize('path', [
    pytest.param(path, id=str(path)) for path in SVG_IMAGES_WEB
    if not (path.stem.endswith('-i') or path.stem.endswith('-blue'))
])
def test_dark_svg_images(path, source_of_truth):
    color = source_of_truth['$jg-dark']

    assert find_fill(path.read_text()) == color


def test_annotations(source_of_truth):
    js_text = (PACKAGE_DIR / 'web' / 'static' / 'src' / 'js' / 'annotations.js').read_text()

    assert source_of_truth['$jg-blue'] in js_text
