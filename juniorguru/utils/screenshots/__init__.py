import re
from itertools import chain
from multiprocessing import Pool
from pathlib import Path
from subprocess import DEVNULL, PIPE, CalledProcessError, run

from invoke import task
import requests
from PIL import Image


PROJECT_DIR = Path(__file__).parent.parent
IMAGES_DIR = PROJECT_DIR / 'juniorguru' / 'web' / 'static' / 'src' / 'images'

URLS_TXT = PROJECT_DIR / 'juniorguru' / 'screenshots-urls.txt'
SCREENSHOTS_DIR = IMAGES_DIR / 'screenshots'
SCREENSHOTS_OVERRIDES_DIR = IMAGES_DIR / 'screenshots-overrides'

PAGERES_FB_SCRIPT = PROJECT_DIR / 'tasks' / 'screenshot-facebook.js'

HIDDEN_ELEMENTS = [
    '[data-cookiebanner]',  # facebook.com
    '.fbPageBanner',  # facebook.com
    '[class*="popupThin"]',  # codecademy.com
    '#pageprompt',  # edx.org
    '#page-prompt',  # edx.org
    '[id*="cookie-law"]',  # engeto.cz
    '[data-cookie-path]',  # google.com
    'ir-modal',  # udacity.com
    'ir-cookie-consent',  # udacity.com
    'ir-content .moustache',  # udacity.com
    'ir-moustache',  # udacity.com
    'ytd-popup-container',  # youtube.com
    'iron-overlay-backdrop',  # youtube.com
    '[data-purpose*="smart-bar"]',  # udemy.com
    '[data-before-content*="advertisement"]',  # reddit.com
    '.butterBar',  # medium.com
    '#banners',  # trello.com
    '.intercom-app',
    '[id*="gdpr-consent"]',
    '[id*="consent-banner"]',
    '[class*="cookie-message"]',
    '[class*="cookieBanner"]',
    '[class*="cookiebanner"]',
    '[id*="cookiebanner"]',
    '[aria-label="cookieconsent"]',
    '[aria-describedby="cookieconsent:desc"]',
    '.chatbot-wrapper',  # cocuma.cz
    '.cookies-notification',  # learn2code.cz
    '.js-consent-banner',  # stackoverflow.com
    '[style*="Toaster-indicatorColor"]',  # reddit.com
    '#onetrust-banner-sdk',  # codecademy.com
    '#axeptio_overlay',  # welcometothejungle.com
]

PAGERES_BATCH_SIZE = 3
PAGERES_WORKERS = 3
PAGERES_OPTIONS = [
    '--format=jpg',
    '--verbose',
    '--overwrite',
    '--crop',
    '--filename=<%= url %>',
    '--delay=2',
    '--css=' + ', '.join(HIDDEN_ELEMENTS) + ' { display: none !important; }',
]

WIDTH = 640
HEIGHT = 360

YOUTUBE_URL_RE = re.compile(r'(youtube\.com.+watch\?.*v=|youtu\.be/)([\w\-\_]+)')
FACEBOOK_URL_RE = re.compile(r'facebook\.com/')
ERRONEOUS_DOUBLE_FRAGMENT = re.compile(r'(\#[^\#])\#[^\.]')


@task(name='screenshots')
def main(context):
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    urls = parse_urls(URLS_TXT.read_text())

    print('[main] YouTube cover images')
    yt_urls = filter_yt_urls(urls)
    urls = list(set(urls) - set(yt_urls))
    Pool().map(download_yt_cover_image, yt_urls)

    print('[main] Facebook cover images')
    fb_urls = filter_fb_urls(urls)
    urls = list(set(urls) - set(fb_urls))
    Pool(PAGERES_WORKERS).map(create_fb_screenshot, fb_urls)

    print('[main] web page screenshots')
    urls_batches = generate_batches(urls, PAGERES_BATCH_SIZE)
    Pool(PAGERES_WORKERS).map(create_screenshots, urls_batches)

    Pool().map(edit_screenshot, SCREENSHOTS_DIR.glob('*.jpg'))

    print('[main] screenshots overrides')
    SCREENSHOTS_OVERRIDES_DIR.mkdir(parents=True, exist_ok=True)
    paths = chain(SCREENSHOTS_OVERRIDES_DIR.glob('*.jpg'),
                  SCREENSHOTS_OVERRIDES_DIR.glob('*.png'))
    Pool().map(edit_screenshot_override, paths)


def parse_url(line):
    url = line.strip().rstrip('/')
    if url.startswith('https://junior.guru/'):
        return url.replace('https://junior.guru/', 'http://localhost:5000/')
    return url


def parse_urls(text):
    urls = (parse_url(line) for line in text.strip().splitlines())
    return list(set(urls))


def filter_yt_urls(urls):
    return [url for url in urls if YOUTUBE_URL_RE.search(url)]


def filter_fb_urls(urls):
    return [url for url in urls if FACEBOOK_URL_RE.search(url)]


def parse_yt_id(url):
    match = YOUTUBE_URL_RE.search(url)
    try:
        return match.group(2)
    except AttributeError:
        raise ValueError(f"URL {url} doesn't contain YouTube ID")


def download_yt_cover_image(url):
    resp = requests.get(f"https://img.youtube.com/vi/{parse_yt_id(url)}/maxresdefault.jpg")
    resp.raise_for_status()
    path = SCREENSHOTS_DIR / f"youtube.com!watch!v={parse_yt_id(url)}.jpg"
    path.write_bytes(resp.content)


def generate_batches(iterable, batch_size):
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]


def create_screenshots(urls, options=None):
    urls = list(urls)
    pageres = ['npx', 'pageres'] + urls + PAGERES_OPTIONS + (options or [])
    try:
        print(f"[pageres] {len(urls)} URLs")
        run(pageres, check=True, cwd=SCREENSHOTS_DIR, stdout=DEVNULL)
    except CalledProcessError:
        print(f"[pageres] RETRY {' '.join(urls)}")
        run(pageres, check=True, cwd=SCREENSHOTS_DIR, stdout=DEVNULL)


def create_fb_screenshot(url):
    try:
        print(f"[pageres] {url}")
        run(['node', PAGERES_FB_SCRIPT, url], check=True, cwd=SCREENSHOTS_DIR, stdout=DEVNULL)
    except CalledProcessError:
        print(f"[pageres] RETRY {url}")
        run(['node', PAGERES_FB_SCRIPT, url], check=True, cwd=SCREENSHOTS_DIR, stdout=DEVNULL)


def edit_screenshot(path):
    name = path.name

    image = Image.open(path)
    if image.width > WIDTH or image.height > HEIGHT:
        print(f"[thumbnail] {name} ( → {WIDTH}x{HEIGHT})")
        image.thumbnail((WIDTH, HEIGHT))
        image.save(path, 'JPEG')
    image.close()

    print(f'[imagemin] {name}')
    imagemin = ['npx', 'imagemin', str(path)]
    proc = run(imagemin, check=True, stdout=PIPE)
    path.write_bytes(proc.stdout)

    original_name = name
    if ERRONEOUS_DOUBLE_FRAGMENT.search(name):
        name = ERRONEOUS_DOUBLE_FRAGMENT.sub('\1', name)
    if '#' in name:
        name = name.replace('#', '!')
    if name.startswith('localhost!5000'):
        name = name.replace('localhost!5000', 'junior.guru')
    if original_name != name:
        print(f'[rename] {original_name} ( → {name})')
        path.rename(path.with_name(name))


def edit_screenshot_override(path):
    image = Image.open(path)

    if image.format == 'PNG':
        path_png, path = path, path.with_suffix('.jpg')
        print(f'[png to jpg] {path_png.name} ( → {path.name})')
        image = image.convert('RGB')  # from RGBA
        image.save(path, 'JPEG')
        path_png.unlink()
    elif image.format != 'JPEG':
        raise RuntimeError(f'Unexpected image format: {image.format}')

    if image.width > WIDTH or image.height > HEIGHT:
        # We want to support converting drop-in images made as whole-page
        # manual Firefox screenshots, thus we cannot use 'thumbnail'. Instead,
        # we resize by aspect ratio (ar) and then crop to the desired height.
        print(f"[thumbnail] {path.name} ( → {WIDTH}x{HEIGHT})")
        height_ar = (image.height * WIDTH) // image.width
        image = image.resize((WIDTH, height_ar), Image.BICUBIC)
        image = image.crop((0, 0, WIDTH, HEIGHT))
        image.save(path)

    image.close()
