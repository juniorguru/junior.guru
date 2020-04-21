import re
import logging
from pathlib import Path
from urllib.parse import urlparse, unquote_plus


logger = logging.getLogger(__name__)


class SaveDataMiddleware(object):
    output_dir = 'juniorguru/data/jobs/'

    def process_response(self, request, response, spider):
        try:
            response_text = response.text
        except AttributeError:
            logger.debug(f"Unable to save '{response.url}'", extra={'spider': spider})
        else:
            path = Path(self.output_dir) / urlparse(response.url).hostname
            path.mkdir(parents=True, exist_ok=True)
            file = path / url_to_filename(response.url)
            file.write_text(response_text)
            logger.debug(f"Saved '{response.url}' to '{file.absolute()}'", extra={'spider': spider})
        return response


def url_to_filename(url):
    url_parts = urlparse(url)
    url = re.sub(r'[^:]+://', '', url).replace(url_parts.netloc, '')
    url = unquote_plus(re.sub(r'[\/\#\?]', '!', url).strip('!'))
    if re.search(r'\.\w+$', url):
        return url
    return f'{url}.html'
