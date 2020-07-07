from itertools import chain
from multiprocessing import Pool
from pathlib import Path
from subprocess import DEVNULL, PIPE, CalledProcessError, run

from PIL import Image


PROJECT_DIR = Path(__file__).parent.parent
IMAGES_DIR = PROJECT_DIR / 'juniorguru' / 'web' / 'static' / 'src' / 'images'

URLS_TXT = PROJECT_DIR / 'juniorguru' / 'screenshots-urls.txt'
SCREENSHOTS_DIR = IMAGES_DIR / 'screenshots'
SCREENSHOTS_OVERRIDES_DIR = IMAGES_DIR / 'screenshots-overrides'

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


def parse_url(line):
    url = line.strip().rstrip('/')
    if url.startswith('https://junior.guru/'):
        return url.replace('https://junior.guru/', 'http://localhost:5000/')
    return url


def parse_urls(text):
    urls = (parse_url(line) for line in text.strip().splitlines())
    return list(set(urls))


def generate_batches(iterable, batch_size):
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]


def create_screenshot(urls):
    urls = list(urls)
    pageres = ['npx', 'pageres'] + urls + PAGERES_OPTIONS
    try:
        print(f"[pageres] {len(urls)} URLs")
        run(pageres, check=True, cwd=SCREENSHOTS_DIR, stdout=DEVNULL)
    except CalledProcessError:
        print(f"[pageres] RETRY {len(urls)} URLs")
        run(pageres, check=True, cwd=SCREENSHOTS_DIR, stdout=DEVNULL)


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


if __name__ == '__main__':
    print('[main] screenshots')
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    urls = parse_urls(URLS_TXT.read_text())
    urls_batches = generate_batches(urls, PAGERES_BATCH_SIZE)
    Pool(PAGERES_WORKERS).map(create_screenshot, urls_batches)

    Pool().map(edit_screenshot, SCREENSHOTS_DIR.glob('*.jpg'))

    print('[main] screenshots overrides')
    SCREENSHOTS_OVERRIDES_DIR.mkdir(parents=True, exist_ok=True)
    paths = chain(SCREENSHOTS_OVERRIDES_DIR.glob('*.jpg'),
                  SCREENSHOTS_OVERRIDES_DIR.glob('*.png'))
    Pool().map(edit_screenshot_override, paths)
