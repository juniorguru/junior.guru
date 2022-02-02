import os
from datetime import date


today = date.today()
BOT_NAME = 'jobs'

SPIDER_MODULES = ['juniorguru.jobs.spiders']
NEWSPIDER_MODULE = 'juniorguru.jobs.spiders'


USER_AGENT = f'JuniorGuruBot/{today.year}.{today.month}.{today.day} (+https://junior.guru)'
ROBOTSTXT_OBEY = True

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'cs;q=0.8,en;q=0.6',
}

DOWNLOADER_MIDDLEWARES = {
   # TODO 'juniorguru.jobs.monitoring.BackupResponseMiddleware': 530,
   'juniorguru.jobs.proxies.ScrapingProxyMiddleware': 555,
}

EXTENSIONS = {
   # TODO 'juniorguru.jobs.monitoring.MonitoringExtension': 100,
}

ITEM_PIPELINES = {
   'juniorguru.jobs.pipelines.required_fields_filter.Pipeline': 50,
   'juniorguru.jobs.pipelines.short_description_filter.Pipeline': 100,
   'juniorguru.jobs.pipelines.broken_encoding_filter.Pipeline': 150,
   'juniorguru.jobs.pipelines.language_parser.Pipeline': 200,
   'juniorguru.jobs.pipelines.language_filter.Pipeline': 250,
   'juniorguru.jobs.pipelines.employment_types_cleaner.Pipeline': 300,
   'juniorguru.jobs.pipelines.company_logo.Pipeline': 350,
}

MEDIA_ALLOW_REDIRECTS = True
IMAGES_STORE = 'juniorguru/images'

FEEDS_DIR = 'juniorguru/data/jobs'
FEEDS = {
    f'{FEEDS_DIR}/{today:%Y}/{today:%m}/{today:%d}/%(name)s.jsonl': {
        'format': 'jsonlines',
        'indent': 2,
        'overwrite': True,
        'item_export_kwargs': {
           'ensure_ascii': False,
           'sort_keys': True,
        },
    },
}

AUTOTHROTTLE_ENABLED = True

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'http_cache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 999]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

PROXIES_ENABLED = bool(int(os.getenv('PROXIES_ENABLED', 0)))
PROXIES_USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:81.0) Gecko/20100101 Firefox/81.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Mozilla/5.0 (iPhone; CPU OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/29.0 Mobile/15E148 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15',
]
