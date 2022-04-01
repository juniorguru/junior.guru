import hashlib
from pathlib import Path
from multiprocessing import Pool
from io import BytesIO

import requests
import favicon
from PIL import Image, ImageChops, ImageOps

from juniorguru.lib.tasks import sync_task
from juniorguru.models import db, ListedJob
from juniorguru.lib import loggers
from juniorguru.sync.jobs_listing import main as jobs_listing_task


MAX_SIZE_PX = 1000

SIZE_PX = 100

ROOT_DIR = Path(__file__).parent.parent

LOGOS_DIR = ROOT_DIR / 'images' / 'logos-jobs'

WORKERS = 4

# https://docs.python-requests.org/en/master/user/advanced/#timeouts
REQUEST_TIMEOUT = (3.05, 15)

# Just copy-paste of raw headers Firefox sends to a web page. None of it is
# intentionally set to a specific value with a specific meaning.
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:93.0) Gecko/20100101 Firefox/93.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.8,cs;q=0.6,sk;q=0.4,es;q=0.2',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Cache-Control': 'max-age=0',
}


logger = loggers.get(__name__)


@sync_task(jobs_listing_task)
@db.connection_context()
def main():
    Path(LOGOS_DIR).mkdir(exist_ok=True, parents=True)

    with Pool(WORKERS) as pool:
        jobs = ListedJob.listing()
        urls = {}

        logger.info('Registering company logo URLs')
        for job in jobs:
            for logo_url in job.company_logo_urls:
                urls.setdefault(logo_url, dict(type='logo', jobs=[]))
                urls[logo_url]['jobs'].append(job.id)

        logger.info('Fetching and registering company icon URLs')
        inputs = ((job.id, job.company_url) for job in jobs if job.company_url)
        results = pool.imap_unordered(fetch_icon_urls, inputs)
        for job_id, icon_urls in results:
            for icon_url in icon_urls:
                urls.setdefault(icon_url, dict(type='icon', jobs=[]))
                urls[icon_url]['jobs'].append(job_id)

        logger.info('Downloading images from both logo and icon URLs')
        results = pool.imap_unordered(download_image, urls.keys())
        for image_url, image_path, orig_width, orig_height in results:
            urls[image_url]['image_path'] = image_path
            urls[image_url]['orig_width'] = orig_width
            urls[image_url]['orig_height'] = orig_height

        logger.info('Deciding which images to use')
        logo_paths = {}
        for logo in sorted(urls.values(), key=sort_key):
            for job_id in logo['jobs']:
                logo_paths.setdefault(job_id, logo['image_path'])
        for job in jobs:
            logo_path = logo_paths.get(job.id)
            if logo_path:
                job.company_logo_path = Path(logo_path).relative_to(ROOT_DIR)
                logger.debug(f'Logo for {job!r}: {job.company_logo_path}')
            job.save()


def sort_key(logo):
    # Such image didn't download, put it to the end of the list
    if logo['image_path'] is None:
        return (True, 100000, 0)

    # Prioritize logos over icons (True sorts after False)
    is_icon = logo['type'] == 'icon'

    # Closer to zero, more like square. For small images, the shape doesn't
    # matter. All will be compared as if they were perfect squares.
    if logo['orig_width'] < SIZE_PX or logo['orig_height'] < SIZE_PX:
        similarity_to_square = 0
    else:
        similarity_to_square = abs(logo['orig_width'] - logo['orig_height'])

    # Multiplied by -1 to ensure descending sort, i.e. larger is better.
    area = -1 * logo['orig_width'] * logo['orig_height']

    return (is_icon, similarity_to_square, area)


def fetch_icon_urls(args):
    logger_f = logger.getChild('fetch_icon_urls')
    job_id, company_url = args
    logger_f.debug(f'Fetching icon URLs for <ListedJob: {job_id}>, {company_url}')
    try:
        icons = favicon.get(company_url,
                            timeout=REQUEST_TIMEOUT,
                            headers=REQUEST_HEADERS)
        urls = unique(icon.url for icon in icons)
        logger_f.info(f'Icon URLs found for <ListedJob: {job_id}>, {company_url}: {urls!r}')
        return job_id, urls
    except Exception:
        logger_f.exception(f'Fetching icon URLs for <ListedJob: {job_id}>, {company_url} failed')
        return job_id, []


def download_image(image_url):
    logger_d = logger.getChild('download_image')
    logger_d.debug(f'Downloading {image_url}')
    try:
        response = requests.get(image_url,
                                timeout=REQUEST_TIMEOUT,
                                headers=REQUEST_HEADERS)
        response.raise_for_status()

        orig_image = Image.open(BytesIO(response.content))
        orig_width, orig_height = orig_image.size
        if orig_width > MAX_SIZE_PX or orig_height > MAX_SIZE_PX:
            raise ValueError(f'Image too large ({orig_width}x{orig_height} < {MAX_SIZE_PX}x{MAX_SIZE_PX})')

        hash = hashlib.sha1(image_url.encode()).hexdigest()
        image_path = LOGOS_DIR / f'{hash}.png'
        convert_image(orig_image).save(image_path)
        logger_d.info(f"Downloaded {image_url} as {image_path}")

        return image_url, image_path, orig_width, orig_height
    except Exception:
        logger_d.exception(f'Unable to download {image_url}')
        return image_url, None, None, None


def convert_image(image):
    # transparent to white
    image = image.convert('RGBA')
    background = Image.new('RGBA', image.size, (255, 255, 255))
    background.paste(image, (0, 0), image)
    image = background.convert('RGB')

    # trim white
    background = Image.new('RGB', image.size, (255, 255, 255))
    diff = ImageChops.difference(image, background)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    image = image.crop(diff.getbbox())

    # make it a square
    side_size = max(image.width, image.height)
    image = ImageOps.pad(image, (side_size, side_size), color=(255, 255, 255))

    # resize
    image = image.resize((SIZE_PX, SIZE_PX))

    return image


def unique(iterable):
    return list(frozenset(item for item in iterable if item is not None))
