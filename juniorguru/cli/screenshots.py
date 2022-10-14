import io
import re
from datetime import datetime, timedelta
from itertools import chain
from multiprocessing import Pool
from pathlib import Path
from subprocess import PIPE, run

import click
import requests
from lxml import html
from PIL import Image
from playwright.sync_api import (Error as PlaywrightError,
                                 TimeoutError as PlaywrightTimeoutError,
                                 sync_playwright)

from juniorguru.lib import loggers


logger = loggers.get(__name__)


PROJECT_DIR = Path(__file__).parent.parent

PUBLIC_DIR = PROJECT_DIR / 'public'

IMAGES_DIR = PROJECT_DIR / 'juniorguru' / 'web' / 'static' / 'src' / 'images'

SCREENSHOTS_DIR = IMAGES_DIR / 'screenshots'

SCREENSHOTS_OVERRIDES_DIR = IMAGES_DIR / 'screenshots-overrides'

CSS_SELECTORS = [
    ('.link-card', '.link-card-link', '.link-card-image'),
    ('.media-card', '.media-card-link', '.media-card-image'),
]

WIDTH = 640

HEIGHT = 360

MIN_BYTES_THRESHOLD = 10000

YOUTUBE_URL_RE = re.compile(r'(youtube\.com.+watch\?.*v=|youtu\.be/)([\w\-\_]+)')

FACEBOOK_URL_RE = re.compile(r'facebook\.com/')

CACHE_PERIOD = timedelta(days=60)

PLAYWRIGHT_BATCH_SIZE = 3

PLAYWRIGHT_WORKERS = 3

PLAYWRIGHT_RETRIES = 3

HIDDEN_ELEMENTS = [
    # generic annoyances
    '[class*="cookie"]:not(html,body)',
    '[id*="cookie"]:not(html,body)',
    '[class*="rc-anchor"]',
    '[id*="rc-anchor"]',
    '[class*="helpcrunch"]',
    '[id*="helpcrunch"]',
    '[class*="uk-notification"]',
    '[id*="uk-notification"]',
    '[aria-label*="cookie"]',
    '[aria-label*="banner"]',
    '[aria-describedby*="cookie"]',
    '[aria-modal]',
    '[role="dialog"]',
    '[id*="onetrust"]',
    '[class*="onetrust"]',
    '[id*="gdpr-consent"]',
    '[class*="gdpr-consent"]',
    '[id*="consent-banner"]',
    '[class*="consent-banner"]',
    '.alert-dismissible',
    '.intercom-app',
    '[data-cookiebanner]',
    '[data-cookie-path]',
    '.chatbot-wrapper',
    '.adsbygoogle',

    # specific sites
    'body > .announcement',  # junior.guru
    'body > .notice',  # pyvo.cz
    'body > .ch2',  # czechitas.cz
    '[data-before-content*="advertisement"]',  # reddit.com
    '[class*="popupThin"]',  # codecademy.com
    '[id*="kz-modal"]',  # ulekare.cz
    'ir-modal',  # udacity.com
    'ir-cookie-consent',  # udacity.com
    'ir-content .moustache',  # udacity.com
    'ir-moustache',  # udacity.com
    '.butterBar',  # medium.com
    '#banners',  # trello.com
    'body > #selectLanguage',  # code.org
    '[style*="Toaster-indicatorColor"]',  # reddit.com
    '#axeptio_overlay',  # welcometothejungle.com
    '[class*="Modal_modalBackground__"]',  # make.com
    '.hsbeacon-chat__button',  # fakturoid.cz
]

BLOCKED_ROUTES = [
    re.compile(r'go\.eu\.bbelements\.com'),  # ulekare.cz
    re.compile(r'googlesyndication\.com'),  # ulekare.cz
]


@click.command()
def main():
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_OVERRIDES_DIR.mkdir(parents=True, exist_ok=True)

    overriding_paths = set(chain(SCREENSHOTS_OVERRIDES_DIR.glob('*.jpg'),
                                 SCREENSHOTS_OVERRIDES_DIR.glob('*.png')))
    logger.info(f'Found {len(overriding_paths)} manual screenshot overrides')
    Pool().map(edit_screenshot_override, overriding_paths)
    overriding_paths = set(SCREENSHOTS_OVERRIDES_DIR.glob('*.jpg'))

    paths = set(chain(SCREENSHOTS_DIR.glob('*.jpg'),
                      SCREENSHOTS_DIR.glob('*.png')))
    logger.info(f'Found {len(paths)} screenshots')
    expired_paths = set(filter(is_expired_path, paths))
    logger.info(f'Expiring {len(expired_paths)} screenshot images')
    for path in expired_paths:
        logger.warning(f'Expiring {path}')
        path.unlink()

    logger.info('Building HTML')
    run(['npx', 'gulp', 'build'], check=True, stdout=PIPE)
    html_paths = set(Path(PUBLIC_DIR).glob('**/*.html'))
    logger.info(f'Reading {len(html_paths)} HTML files')
    screenshots = set(chain.from_iterable(map(parse_doc, html_paths)))
    logger.info(f'Found {len(screenshots)} links to screenshots')

    existing_screenshots = set(filter(is_existing_screenshot, screenshots))
    logger.info(f'Skipping {len(existing_screenshots)} existing screenshots')
    screenshots = set(screenshots) - existing_screenshots

    overridden_screenshots = set(filter(is_overridden_screenshot, screenshots))
    logger.info(f'Skipping {len(overridden_screenshots)} overridden screenshots')
    screenshots = set(screenshots) - overridden_screenshots

    yt_screenshots = set(filter(is_yt_screenshot, screenshots))
    logger.info(f'Downloading {len(yt_screenshots)} YouTube URLs')
    screenshots = set(screenshots) - yt_screenshots
    Pool().map(download_yt_cover_image, yt_screenshots)

    fb_screenshots = set(filter(is_fb_screenshot, screenshots))
    logger.info(f'Downloading {len(fb_screenshots)} Facebook URLs')
    screenshots = set(screenshots) - fb_screenshots
    Pool(PLAYWRIGHT_WORKERS).map(download_fb_cover_image, fb_screenshots)

    logger.info(f'Downloading {len(screenshots)} regular website URLs')
    screenshots_batches = generate_batches(screenshots, PLAYWRIGHT_BATCH_SIZE)
    Pool(PLAYWRIGHT_WORKERS).map(create_screenshots, screenshots_batches)


def parse_doc(path):
    logger.debug(f'Parsing {path.relative_to(PUBLIC_DIR)}')
    html_tree = html.fromstring(path.read_bytes())
    for select_card, select_link, select_image in CSS_SELECTORS:
        for card in html_tree.cssselect(select_card):
            try:
                link = card.cssselect(select_link)[0]
                image = card.cssselect(select_image)[0]
            except IndexError:
                logger.error(f"Problem parsing {select_card} in {path}")
            else:
                screenshot_url = link.get('href')
                if screenshot_url.startswith('.'):
                    screenshot_url = f'https://junior.guru/{path.parent.relative_to(PUBLIC_DIR) / screenshot_url}'
                screenshot_path = SCREENSHOTS_DIR / Path(image.get('data-src')).name
                yield (screenshot_url, screenshot_path)


def is_expired_path(path):
    return (datetime.now() - datetime.fromtimestamp(path.stat().st_ctime)) > CACHE_PERIOD


def is_overridden_screenshot(screenshot):
    url, path = screenshot
    return (SCREENSHOTS_OVERRIDES_DIR / Path(path).name).exists()


def is_existing_screenshot(screenshot):
    url, path = screenshot
    return Path(path).exists()


def is_yt_screenshot(screenshot):
    url, path = screenshot
    return bool(YOUTUBE_URL_RE.search(url))


def is_fb_screenshot(screenshot):
    url, path = screenshot
    return bool(FACEBOOK_URL_RE.search(url))


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
    iterable = list(iterable)
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
            for blocked_route in BLOCKED_ROUTES:
                page.route(blocked_route, lambda route: route.abort())
            try:
                page.goto(url, wait_until='networkidle')
            except PlaywrightTimeoutError:
                pass
            page.evaluate('''
                selectors => Array.from(document.querySelectorAll(selectors.join(', ')))
                    .forEach(element => element.remove());
            ''', list(HIDDEN_ELEMENTS))
            screenshot_bytes = page.screenshot()
            if len(screenshot_bytes) < MIN_BYTES_THRESHOLD:
                raise PlaywrightError(f'Suspiciously small image: {len(screenshot_bytes)} bytes')
            return screenshot_bytes
        except PlaywrightError as e:
            if attempt_no < PLAYWRIGHT_RETRIES:
                logger.debug(str(e))
            else:
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
