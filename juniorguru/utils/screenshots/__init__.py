import io
import re
from itertools import chain
from datetime import datetime, timedelta
from pathlib import Path
from multiprocessing import Pool
from subprocess import PIPE, run

import requests
import playwright
from playwright.sync_api import sync_playwright
from invoke import task
from PIL import Image

from juniorguru.lib import loggers


logger = loggers.get(__name__)


PROJECT_DIR = Path(__file__).parent.parent.parent.parent

DOCS_DIR = PROJECT_DIR / 'juniorguru' / 'mkdocs'

IMAGES_DIR = PROJECT_DIR / 'juniorguru' / 'web' / 'static' / 'src' / 'images'

SCREENSHOTS_DIR = IMAGES_DIR / 'screenshots'

SCREENSHOTS_OVERRIDES_DIR = IMAGES_DIR / 'screenshots-overrides'

LINK_CARD_RE = re.compile(r'''
    (link_card|video_card|video_card_engeto)
    \(\s*
    ('[^']+',\s*)+
    '(?P<path>[^']+\.jpg)'
    ,\s*
    '(?P<url>http[^']+)'
''', re.VERBOSE | re.IGNORECASE)

WIDTH = 640

HEIGHT = 360

YOUTUBE_URL_RE = re.compile(r'(youtube\.com.+watch\?.*v=|youtu\.be/)([\w\-\_]+)')

FACEBOOK_URL_RE = re.compile(r'facebook\.com/')

CACHE_PERIOD = timedelta(days=60)

PLAYWRIGHT_BATCH_SIZE = 3

PLAYWRIGHT_WORKERS = 3

PLAYWRIGHT_RETRIES = 3

HIDDEN_ELEMENTS = [
    '[class*="ookie"]',
    '[id*="ookie"]',
    '[aria-label*="ookie"]',
    '[aria-describedby*="ookie"]',
    '[aria-modal]',
    '[role="dialog"]',
    '[id*="onetrust"]',
    '[data-cookiebanner]',  # facebook.com
    '[class*="popupThin"]',  # codecademy.com
    '#pageprompt',  # edx.org
    '#page-prompt',  # edx.org
    '[data-cookie-path]',  # google.com
    'ir-modal',  # udacity.com
    'ir-cookie-consent',  # udacity.com
    'ir-content .moustache',  # udacity.com
    'ir-moustache',  # udacity.com
    '[data-purpose*="smart-bar"]',  # udemy.com
    '[data-before-content*="advertisement"]',  # reddit.com
    '.butterBar',  # medium.com
    '#banners',  # trello.com
    '#selectLanguage',  # code.org
    '.intercom-app',
    '[id*="gdpr-consent"]',
    '[id*="consent-banner"]',
    '.chatbot-wrapper',  # cocuma.cz
    '.js-consent-banner',  # stackoverflow.com
    '[style*="Toaster-indicatorColor"]',  # reddit.com
    '#axeptio_overlay',  # welcometothejungle.com
    '.alert-dismissible',
    '#rc-anchor-alert',
    '.notice',  # pyvo.cz
    '[class*="Modal_modalBackground__"]',  # integromat.com
    '.hsbeacon-chat__button',  # fakturoid.cz
    '.ch2',  # czechitas.cz
]


@task(name='screenshots')
def main(context):
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_OVERRIDES_DIR.mkdir(parents=True, exist_ok=True)

    expired_paths = [path for path
                     in chain(SCREENSHOTS_DIR.glob('*.jpg'), SCREENSHOTS_DIR.glob('*.png'))
                     if (datetime.now() - datetime.fromtimestamp(path.stat().st_ctime)) > CACHE_PERIOD]
    logger.info(f'Expiring {len(expired_paths)} screenshots')
    for path in expired_paths:
        logger.warning(f'Expiring {path}')
        path.unlink()

    paths_docs = list(Path(DOCS_DIR).glob('**/*.md'))
    logger.info(f'Reading {len(paths_docs)} documents')
    screenshots = list(chain.from_iterable(parse_doc(doc_path) for doc_path in paths_docs))
    logger.info(f'Found {len(screenshots)} screenshots')

    existing_screenshots = filter_existing_screenshots(screenshots)
    logger.info(f'Found {len(existing_screenshots)} existing screenshots')
    screenshots = list(set(screenshots) - set(existing_screenshots))

    yt_screenshots = filter_yt_screenshots(screenshots)
    logger.info(f'Downloading {len(yt_screenshots)} YouTube URLs')
    screenshots = list(set(screenshots) - set(yt_screenshots))
    Pool().map(download_yt_cover_image, yt_screenshots)

    fb_screenshots = filter_fb_screenshots(screenshots)
    logger.info(f'Downloading {len(fb_screenshots)} Facebook URLs')
    screenshots = list(set(screenshots) - set(fb_screenshots))
    Pool(PLAYWRIGHT_WORKERS).map(download_fb_cover_image, fb_screenshots)

    logger.info(f'Downloading {len(screenshots)} regular website URLs')
    screenshots_batches = generate_batches(screenshots, PLAYWRIGHT_BATCH_SIZE)
    Pool(PLAYWRIGHT_WORKERS).map(create_screenshots, screenshots_batches)

    paths = list(chain(SCREENSHOTS_OVERRIDES_DIR.glob('*.jpg'),
                       SCREENSHOTS_OVERRIDES_DIR.glob('*.png')))
    logger.info(f'Editing {len(paths)} manual screenshot overrides')
    Pool().map(edit_screenshot_override, paths)


def parse_doc(doc_path):
    doc_text = Path(doc_path).read_text()
    for match in LINK_CARD_RE.finditer(doc_text):
        groups = match.groupdict()
        yield (groups['url'], SCREENSHOTS_DIR / groups['path'])


def filter_existing_screenshots(screenshots):
    return [(url, path) for url, path in screenshots
            if Path(path).exists()]


def filter_yt_screenshots(screenshots):
    return [(url, path) for url, path in screenshots
            if YOUTUBE_URL_RE.search(url)]


def filter_fb_screenshots(screenshots):
    return [(url, path) for url, path in screenshots
            if FACEBOOK_URL_RE.search(url)]


def parse_yt_id(url):
    match = YOUTUBE_URL_RE.search(url)
    try:
        return match.group(2)
    except AttributeError:
        raise ValueError(f"URL {url} doesn't contain YouTube ID")


def download_yt_cover_image(screenshot):
    url, path = screenshot
    logger.info(f"Shooting {url}")
    resp = requests.get(f"https://img.youtube.com/vi/{parse_yt_id(url)}/maxresdefault.jpg")
    resp.raise_for_status()
    image_bytes = edit_image(resp.content)
    logger.info(f"Writing {path}")
    Path(path).write_bytes(image_bytes)


def download_fb_cover_image(screenshot):
    url, path = screenshot
    logger.info(f"Shooting {url}")
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        image_url = page.evaluate('''
            () => document.querySelector('img[data-imgperflogname="profileCoverPhoto"]').src
        ''')
        browser.close()
    resp = requests.get(image_url)
    resp.raise_for_status()
    image_bytes = edit_image(resp.content)
    logger.info(f"Writing {path}")
    Path(path).write_bytes(image_bytes)


def generate_batches(iterable, batch_size):
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]


def create_screenshots(screenshots):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        for url, path in screenshots:
            logger.info(f"Shooting {url}")
            image_bytes = create_screenshot(page, url)
            image_bytes = edit_image(image_bytes)
            logger.info(f"Writing {path}")
            Path(path).write_bytes(image_bytes)
        browser.close()


def create_screenshot(page, url):
    for attempt_no in range(1, PLAYWRIGHT_RETRIES + 1):
        try:
            logger.debug(f"Shooting {url} (attempt #{attempt_no})")
            try:
                page.goto(url, wait_until='networkidle')
            except playwright.TimeoutError:
                pass
            page.evaluate('''
                selectors => selectors
                    .map(selector => document.querySelector(selector))
                    .filter(element => element)
                    .forEach(element => element.remove());
            ''', list(HIDDEN_ELEMENTS))
            screenshot_bytes = page.screenshot()
            if not screenshot_bytes:
                raise playwright.Error('No bytes')
            return screenshot_bytes
        except playwright.Error as e:
            logger.debug(str(e))
            if attempt_no == PLAYWRIGHT_RETRIES:
                raise


def edit_image(image_bytes):
    with Image.open(io.BytesIO(image_bytes)) as image:
        if image.format == 'PNG':
            image = image.convert('RGB')  # from RGBA
        elif image.format != 'JPEG':
            raise RuntimeError(f'Unexpected image format: {image.format}')

        if image.width > WIDTH or image.height > HEIGHT:
            image.thumbnail((WIDTH, HEIGHT))

        input_bytes = io.BytesIO()
        image.save(input_bytes, 'JPEG')
    input_bytes.seek(0)
    proc = run(['npx', 'imagemin'], input=input_bytes.getvalue(), stdout=PIPE, check=True)
    return proc.stdout


def edit_screenshot_override(path):
    path = Path(path)
    logger.info(f'Editing {path.name}')

    with Image.open(path) as image:
        if image.format == 'PNG':
            path_png, path = path, path.with_suffix('.jpg')
            image = image.convert('RGB')  # from RGBA
            image.save(path, 'JPEG')
            path_png.unlink()
        elif image.format != 'JPEG':
            raise RuntimeError(f'Unexpected image format: {image.format}')

        if image.width > WIDTH or image.height > HEIGHT:
            # We want to support converting drop-in images made as whole-page
            # manual Firefox screenshots, thus we cannot use 'thumbnail'. Instead,
            # we resize by aspect ratio (ar) and then crop to the desired height.
            height_ar = (image.height * WIDTH) // image.width
            image = image.resize((WIDTH, height_ar), Image.BICUBIC)
            image = image.crop((0, 0, WIDTH, HEIGHT))
            image.save(path, 'JPEG')

    proc = run(['npx', 'imagemin', path], stdout=PIPE, check=True)
    path.write_bytes(proc.stdout)
