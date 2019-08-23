import shutil
from pathlib import Path
from itertools import islice
from subprocess import run, PIPE, CalledProcessError


PROJECT_DIR = Path(__file__).parent.parent
LINKS_TXT = PROJECT_DIR / 'juniorguru' / 'links.txt'

IMAGES_DIR = PROJECT_DIR / 'juniorguru' / 'images'
SCREENSHOTS_DIR = IMAGES_DIR / 'screenshots'
SCREENSHOTS_OVERRIDES_DIR = IMAGES_DIR / 'screenshots-overrides'

BATCH_SIZE = 5

HIDDEN_ELEMENTS = [
    '[data-cookiebanner]',  # facebook.com
    '.fbPageBanner',  # facebook.com
    '[class*="popupThin"]',  # codecademy.com
    '#pageprompt',  # edx.org
    '[id*="cookie-law"]',  # engeto.cz
    '[data-cookie-path]',  # google.com
    'ir-modal',  # udacity.com
    'ir-cookie-consent',  # udacity.com
    'ir-content .moustache',  # udacity.com
    'ir-moustache',  # udacity.com
    'ytd-popup-container',  # youtube.com
    '[data-purpose*="smart-bar"]',  # udemy.com
    '[data-before-content*="advertisement"]',  # reddit.com
    '.intercom-app',
    '[id*="gdpr-consent"]',
    '[id*="consent-banner"]',
    '[class*="cookie-message"]',
    '[class*="cookieBanner"]',
    '[class*="cookiebanner"]',
    '[id*="cookiebanner"]',
    '[aria-label="cookieconsent"]',
    '[aria-describedby="cookieconsent:desc"]',
]


options = [
    '--verbose',
    '--overwrite',
    '--crop',
    '--filename=<%= url %>',
    '--delay=2',
    '--css=' + ', '.join(HIDDEN_ELEMENTS) + ' { display: none !important; }',
]
links = (
    link for link in (
        line.strip().rstrip('/') for line
        in LINKS_TXT.read_text().splitlines()
    )
    if link
)


screenshots_dirs = [SCREENSHOTS_DIR, SCREENSHOTS_OVERRIDES_DIR]

for screenshots_dir in screenshots_dirs:
    screenshots_dirs.mkdir(parents=True, exist_ok=True)

for links_batch in iter(lambda: list(islice(links, BATCH_SIZE)), []):
    pageres = ['npx', 'pageres'] + links_batch + options
    try:
        run(pageres, check=True, cwd=SCREENSHOTS_DIR)
    except CalledProcessError:
        run(pageres, check=True, cwd=SCREENSHOTS_DIR)  # dummy retry

for screenshots_dir in screenshots_dirs:
    run(['mogrify', '-resize', '640x480', '*.png'], check=True, cwd=screenshots_dir)

    for image_path in screenshots_dir.glob('*.png'):
        proc = run(['npx', 'imagemin', str(image_path)], check=True, stdout=PIPE)
        image_path.write_bytes(proc.stdout)
