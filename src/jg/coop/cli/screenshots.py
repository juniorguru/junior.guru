import re
from datetime import datetime, timedelta
from io import BytesIO
from itertools import chain
from multiprocessing import Pool
from pathlib import Path

import click
import requests
from lxml import html
from PIL import Image
from playwright.sync_api import (
    Error as PlaywrightError,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)

from jg.coop.cli.web import build
from jg.coop.lib import loggers
from jg.coop.lib.youtube import parse_youtube_id


logger = loggers.from_path(__file__)


PUBLIC_DIR = Path("public")

IMAGES_DIR = Path("jg/coop/images")

SCREENSHOTS_DIR = IMAGES_DIR / "screenshots"

SCREENSHOTS_OVERRIDES_DIR = IMAGES_DIR / "screenshots-overrides"

WIDTH = 640

HEIGHT = 360

MIN_BYTES_THRESHOLD = 10000

FACEBOOK_URL_RE = re.compile(r"facebook\.com/")

CACHE_PERIOD = timedelta(days=60)

PLAYWRIGHT_BATCH_SIZE = 3

PLAYWRIGHT_WORKERS = 3

PLAYWRIGHT_RETRIES = 3

HIDDEN_ELEMENTS = [
    '[class*="cookie"]:not(html,body)',
    '[id*="cookie"]:not(html,body)',
    '[class*="rc-anchor"]',
    '[id*="rc-anchor"]',
    '[class*="helpcrunch"]',
    '[id*="helpcrunch"]',
    '[class*="uk-notification"]',
    '[id*="uk-notification"]',
    '[aria-label*="cookie"]',
    '[aria-label*="Cookie"]',
    '[aria-label*="banner"]',
    '[aria-describedby*="cookie"]',
    "[aria-modal]",
    '[role="dialog"]',
    '[id*="onetrust"]',
    '[class*="onetrust"]',
    '[id*="transcend"]',
    '[class*="transcend"]',
    '[id*="onesignal"]',
    '[class*="onesignal"]',
    '[id*="gdpr-consent"]',
    '[class*="gdpr-consent"]',
    '[id*="cookie-banner"]',
    '[class*="cookie-banner"]',
    '[id*="consent-banner"]',
    '[class*="consent-banner"]',
    '[id*="consent-manager"]',
    '[class*="consent-manager"]',
    '[id*="cky-consent"]',
    '[class*="cky-consent"]',
    '[data-section-name*="cookie"]',
    '[data-component-name*="cookie"]',
    '[class*="termsfeed-com---"]',
    ".alert-dismissible",
    ".intercom-app",
    "[data-cookiebanner]",
    "[data-cookie-path]",
    ".chatbot-wrapper",
    ".adsbygoogle",
    "#credential_picker_container",
    ".tawk-min-container",
    ".fb_iframe_widget",
    ".fb_dialog",
    '[id*="cookiebanner-container"]',
    "#cc--main",  # seduo.cz
    "#cc_div",  # seduo.cz
    '[class*="frb-"]',  # wikipedia.org
    '[id="siteNotice"]',  # wikipedia.org
    '[id*="drift-"]',  # pluralsight.com
    "body > .announcement",  # junior.guru
    "body > .notice",  # pyvo.cz
    "body > .ch2",  # czechitas.cz
    "#voucher-stripe",  # czechitas.cz
    '[data-before-content*="advertisement"]',  # reddit.com
    '[class*="popupThin"]',  # codecademy.com
    '[id*="kz-modal"]',  # ulekare.cz
    "ir-modal",  # udacity.com
    "ir-cookie-consent",  # udacity.com
    "ir-content .moustache",  # udacity.com
    "ir-moustache",  # udacity.com
    ".butterBar",  # medium.com
    "#banners",  # trello.com
    "body.modal-open > #selectLanguage",  # code.org
    "body.modal-open > .modal.fade",  # code.org
    '[style*="Toaster-indicatorColor"]',  # reddit.com
    "reddit-cookie-banner",  # reddit.com
    "#axeptio_overlay",  # welcometothejungle.com
    '[class*="Modal_modalBackground__"]',  # make.com
    ".hsbeacon-chat__button",  # fakturoid.cz
    ".n-ads-branding-spacer",  # heroine.cz
    ".n-paywall-notification",  # heroine.cz
    "#didomi-notice",  # heroine.cz
    ".cm-wrapper",  #
    '[id*="CybotCookiebotDialog"]',  # shoptet.cz
    ".toast-container",  # coderslab.cz
    '[class*="dc-ps-banner"]',  # datacamp.com
    ".oj-page-content .homebanner",  # onlinejazyky.cz
    "#awsccc-cb-c",  # aws.amazon.com
    '[class^="truste-"]',  # redhat.com
    '[id^="truste-"]',  # redhat.com
    ".cc_banner",  # it-academy.sk
    "cc_container",  # it-academy.sk
    "#IMS_box1",  # it-academy.sk
    "#IMS_iframe1",  # it-academy.sk
    ".IMS_iframeBox",  # it-academy.sk
]

BLOCKED_ROUTES = [
    re.compile(r"go\.eu\.bbelements\.com"),  # ulekare.cz
    re.compile(r"googlesyndication\.com"),  # ulekare.cz
]


@click.command()
@click.pass_context
def main(context):
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_OVERRIDES_DIR.mkdir(parents=True, exist_ok=True)

    overriding_paths = set(
        chain(
            SCREENSHOTS_OVERRIDES_DIR.glob("*.jpg"),
            SCREENSHOTS_OVERRIDES_DIR.glob("*.png"),
            SCREENSHOTS_OVERRIDES_DIR.glob("*.webp"),
        )
    )
    logger.info(f"Found {len(overriding_paths)} manual screenshot overrides")
    Pool().map(edit_screenshot_override, overriding_paths)
    overriding_paths = set(SCREENSHOTS_OVERRIDES_DIR.glob("*.webp"))

    paths = set(chain(SCREENSHOTS_DIR.glob("*.webp")))
    logger.info(f"Found {len(paths)} screenshots")
    expired_paths = set(filter(is_expired_path, paths))
    logger.info(f"Expiring {len(expired_paths)} screenshot images")
    for path in expired_paths:
        logger.warning(f"Expiring {path}")
        path.unlink()

    logger.info("Building HTML")
    context.invoke(build)
    html_paths = set(Path(PUBLIC_DIR).glob("**/*.html"))
    logger.info(f"Reading {len(html_paths)} HTML files")
    screenshots = set(chain.from_iterable(map(parse_doc, html_paths)))
    logger.info(f"Found {len(screenshots)} links to screenshots")

    existing_screenshots = set(filter(is_existing_screenshot, screenshots))
    logger.info(f"Skipping {len(existing_screenshots)} existing screenshots")
    screenshots = set(screenshots) - existing_screenshots

    overridden_screenshots = set(filter(is_overridden_screenshot, screenshots))
    logger.info(f"Skipping {len(overridden_screenshots)} overridden screenshots")
    screenshots = set(screenshots) - overridden_screenshots

    yt_screenshots = set(filter(is_yt_screenshot, screenshots))
    logger.info(f"Downloading {len(yt_screenshots)} YouTube URLs")
    screenshots = set(screenshots) - yt_screenshots
    Pool().map(download_yt_cover_image, yt_screenshots)

    fb_screenshots = set(filter(is_fb_screenshot, screenshots))
    logger.info(f"Downloading {len(fb_screenshots)} Facebook URLs")
    screenshots = set(screenshots) - fb_screenshots
    Pool(PLAYWRIGHT_WORKERS).map(download_fb_cover_image, fb_screenshots)

    logger.info(f"Downloading {len(screenshots)} regular website URLs")
    screenshots_batches = generate_batches(screenshots, PLAYWRIGHT_BATCH_SIZE)
    Pool(PLAYWRIGHT_WORKERS).map(create_screenshots, screenshots_batches)


def parse_doc(path):
    logger.debug(f"Parsing {path.relative_to(PUBLIC_DIR)}")
    html_tree = html.fromstring(path.read_bytes())
    for card in html_tree.cssselect(
        "*[data-screenshot-source-url][data-screenshot-image-url]"
    ):
        screenshot_source_url = card.get("data-screenshot-source-url")
        if screenshot_source_url.startswith("."):
            screenshot_source_url = f"https://junior.guru/{path.parent.relative_to(PUBLIC_DIR) / screenshot_source_url}"
        screenshot_path = (
            SCREENSHOTS_DIR / Path(card.get("data-screenshot-image-url")).name
        )
        yield (screenshot_source_url, screenshot_path)


def is_expired_path(path):
    return (
        datetime.now() - datetime.fromtimestamp(path.stat().st_ctime)
    ) > CACHE_PERIOD


def is_overridden_screenshot(screenshot):
    url, path = screenshot
    return (SCREENSHOTS_OVERRIDES_DIR / Path(path).name).exists()


def is_existing_screenshot(screenshot):
    url, path = screenshot
    return Path(path).exists()


def is_yt_screenshot(screenshot):
    url, path = screenshot
    try:
        return bool(parse_youtube_id(url))
    except ValueError:
        return False


def is_fb_screenshot(screenshot):
    url, path = screenshot
    return bool(FACEBOOK_URL_RE.search(url))


def download_yt_cover_image(screenshot):
    url, path = screenshot
    logger.info(f"Shooting {url}")
    resp = requests.get(
        f"https://img.youtube.com/vi/{parse_youtube_id(url)}/maxresdefault.jpg"
    )
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        resp = requests.get(
            f"https://img.youtube.com/vi/{parse_youtube_id(url)}/hqdefault.jpg"
        )
        resp.raise_for_status()
    image_bytes = edit_image(resp.content)
    logger.info(f"Writing {path}")
    Path(path).write_bytes(image_bytes)


def download_fb_cover_image(screenshot):
    url, path = screenshot
    logger.info(f"Shooting {url}")
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        image_url = page.evaluate(
            """
                () => document.querySelector('img[data-imgperflogname="profileCoverPhoto"]').src
            """
        )
        browser.close()
    resp = requests.get(image_url)
    resp.raise_for_status()
    image_bytes = edit_image(resp.content)
    logger.info(f"Writing {path}")
    Path(path).write_bytes(image_bytes)


def generate_batches(iterable, batch_size):
    iterable = list(iterable)
    for i in range(0, len(iterable), batch_size):
        yield iterable[i : i + batch_size]


def create_screenshots(screenshots):
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch()
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
                page.goto(url, wait_until="networkidle")
            except PlaywrightTimeoutError:
                pass
            page.evaluate(
                """
                    selectors => Array.from(document.querySelectorAll(selectors.join(', ')))
                        .forEach(element => element.remove());
                """,
                list(HIDDEN_ELEMENTS),
            )
            screenshot_bytes = page.screenshot()
            if len(screenshot_bytes) < MIN_BYTES_THRESHOLD:
                raise PlaywrightError(
                    f"Suspiciously small image: {len(screenshot_bytes)} bytes"
                )
            return screenshot_bytes
        except PlaywrightError as e:
            if attempt_no < PLAYWRIGHT_RETRIES:
                logger.debug(str(e))
            else:
                raise


def edit_image(image_bytes):
    with Image.open(BytesIO(image_bytes)) as image:
        if image.format in ("PNG", "JPEG"):
            image = image.convert("RGB")  # from RGBA
        elif image.format != "WEBP":
            raise RuntimeError(f"Unexpected image format: {image.format}")

        if image.width > WIDTH or image.height > HEIGHT:
            image.thumbnail((WIDTH, HEIGHT))

        stream = BytesIO()
        image.save(stream, "WEBP", quality=80, method=6, lossless=False)
    return stream.getvalue()


def edit_screenshot_override(path):
    path = Path(path)
    logger.info(f"Editing {path.name}")

    with Image.open(path) as image:
        if image.format in ("PNG", "JPEG"):
            path_original, path = path, path.with_suffix(".webp")
            image = image.convert("RGB")  # from RGBA
            image.save(path, "WEBP", quality=80, method=6, lossless=False)
            path_original.unlink()
        elif image.format != "WEBP":
            raise RuntimeError(f"Unexpected image format: {image.format}")

        if image.width > WIDTH or image.height > HEIGHT:
            # We want to support converting drop-in images made as whole-page
            # manual Firefox screenshots, thus we cannot use 'thumbnail'. Instead,
            # we resize by aspect ratio (ar) and then crop to the desired height.
            height_ar = (image.height * WIDTH) // image.width
            image = image.resize((WIDTH, height_ar), Image.Resampling.BICUBIC)
            image = image.crop((0, 0, WIDTH, HEIGHT))
            image.save(path, "WEBP", quality=80, method=6, lossless=False)
