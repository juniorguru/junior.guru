import hashlib
from pathlib import Path
from multiprocessing import Process, JoinableQueue as Queue
from queue import Empty
from io import BytesIO

import requests
import favicon
from PIL import Image, ImageChops, ImageOps, UnidentifiedImageError

from juniorguru.lib.tasks import sync_task
from juniorguru.models import db, ListedJob
from juniorguru.lib import loggers


MAX_SIZE_PX = 1000

SIZE_PX = 100

ROOT_DIR = Path(__file__).parent.parent

LOGOS_DIR = ROOT_DIR / 'images' / 'logos-jobs'

WORKERS = 4

# https://docs.python-requests.org/en/master/user/advanced/#timeouts
REQUEST_TIMEOUT = (3.05, 5)

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


class ImageException(Exception):
    pass


@sync_task()
@db.connection_context()
def main():
    # Start
    path_queue = Queue()
    Process(target=_persistor, args=(path_queue,), daemon=True).start()
    Path(LOGOS_DIR).mkdir(exist_ok=True, parents=True)

    # Step 1: Go through all listed jobs and download company logos for them
    jobs = list(ListedJob.listing())
    logger.info(f'Downloading company logos for {len(jobs)} listed jobs')
    if jobs:
        url_queue = Queue()
        for job in jobs:
            for url in job.company_logo_urls:
                url_queue.put((url, job.id))

        downloaders = []
        for downloader_id in range(WORKERS):
            proc = Process(target=_downloader, args=(downloader_id, url_queue, path_queue))
            downloaders.append(proc)
            proc.start()

        for joinable in downloaders + [url_queue]:
            joinable.join()

    # Step 2: Go through all listed jobs and try at least favicons
    jobs = list(ListedJob.favicon_listing())
    logger.info(f'Downloading favicons for {len(jobs)} listed jobs')
    if jobs:
        url_queue = Queue()
        for job in jobs:
            logger.debug(f'Analyzing {job.company_url}')
            favicon_urls = get_favicons(job.company_url)
            logger.debug(f'Found {len(favicon_urls)} favicon URLs at {job.company_url}')
            for url in favicon_urls:
                url_queue.put((url, job.id))

        downloaders = []
        for downloader_id in range(WORKERS):
            proc = Process(target=_downloader, args=(downloader_id, url_queue, path_queue))
            downloaders.append(proc)
            proc.start()

        for joinable in downloaders + [url_queue]:
            joinable.join()

    # Finish
    path_queue.join()


def _downloader(id, url_queue, path_queue):
    logger_d = logger.getChild(f'downloaders.{id}')
    logger_d.debug('Starting')
    try:
        while True:
            url, job_id = url_queue.get(timeout=0.5)
            logger_d.debug(f"Downloading {url}")
            try:
                response = requests.get(url,
                                        timeout=REQUEST_TIMEOUT,
                                        headers=REQUEST_HEADERS)
                response.raise_for_status()

                orig_image = Image.open(BytesIO(response.content))
                width, height = orig_image.size
                if width > MAX_SIZE_PX or height > MAX_SIZE_PX:
                    raise ImageException(f'Image too large ({width}x{height} < {MAX_SIZE_PX}x{MAX_SIZE_PX})')

                image = convert_image(orig_image)
                buffer = BytesIO()
                image.save(buffer, 'PNG')
                buffer.seek(0)

                hash = hashlib.sha1(url.encode()).hexdigest()
                logo_path = LOGOS_DIR / f'{hash}.png'
                logo_path.write_bytes(buffer)

                logger_d.info(f"Downloaded {url} as {logo_path}")
                path_queue.put((logo_path, job_id))
            except Exception:
                logger_d.exception(f'Unable to download {url} (job ID {job_id})')
            finally:
                url_queue.task_done()
    except Empty:
        logger_d.debug('Nothing else to download, closing')


def _persistor(path_queue):
    logger_p = logger.getChild('persistor')
    logger_p.debug("Starting")
    try:
        while True:
            path, job_id = path_queue.get()
            try:
                job = ListedJob.get(job_id)
                logger_p.debug(f"Updating {job!r}")
                job.company_logo_path = str(path.relative_to(ROOT_DIR))
                job.save()
            finally:
                del job
                path_queue.task_done()
    finally:
        logger_p.debug("Closing persistor")


def get_favicons(company_url):
    try:
        icons = favicon.get(company_url,
                            timeout=REQUEST_TIMEOUT,
                            headers=REQUEST_HEADERS)
        return unique(icon.url for icon in icons)
    except Exception:
        logger.exception('Favicon lookup has failed')
        return []


def unique(iterable):
    return list(frozenset(filter(None, iterable)))


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
