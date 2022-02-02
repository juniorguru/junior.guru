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
   # TODO 'juniorguru.sync.jobs.pipelines.identifier.Pipeline': 1,
   # TODO 'juniorguru.sync.jobs.pipelines.required_fields_filter.Pipeline': 50,
   # TODO 'juniorguru.sync.jobs.pipelines.description_parser.Pipeline': 100,  # experimenting with Mila and ML
   # TODO 'juniorguru.sync.jobs.pipelines.short_description_filter.Pipeline': 200,
   # TODO 'juniorguru.sync.jobs.pipelines.broken_encoding_filter.Pipeline': 300,
   # TODO 'juniorguru.sync.jobs.pipelines.language_parser.Pipeline': 350,
   # TODO 'juniorguru.sync.jobs.pipelines.language_filter.Pipeline': 400,
   # TODO # 'juniorguru.sync.jobs.pipelines.description_parser.Pipeline': 500,
   # TODO # 'juniorguru.sync.jobs.pipelines.sections_parser.Pipeline': 500,  https://app.circleci.com/pipelines/github/honzajavorek/junior.guru/3047/workflows/033dc5ea-e097-4d73-abea-fcaf7610460b/jobs/19368
   # TODO 'juniorguru.sync.jobs.pipelines.features_parser.Pipeline': 600,
   # TODO 'juniorguru.sync.jobs.pipelines.junior_rank.Pipeline': 650,
   # TODO 'juniorguru.sync.jobs.pipelines.junior_rank_filter.Pipeline': 700,
   # TODO 'juniorguru.sync.jobs.pipelines.sort_rank.Pipeline': 750,
   # TODO 'juniorguru.sync.jobs.pipelines.gender_cleaner.Pipeline': 800,
   # TODO 'juniorguru.sync.jobs.pipelines.emoji_cleaner.Pipeline': 850,
   # TODO 'juniorguru.sync.jobs.pipelines.locations.Pipeline': 860,
   # TODO 'juniorguru.sync.jobs.pipelines.employment_types_cleaner.Pipeline': 900,
   # TODO 'juniorguru.sync.jobs.pipelines.company_logo.Pipeline': 995,
   # TODO 'juniorguru.sync.jobs.pipelines.database.Pipeline': 1000,
}
JUNIORGURU_ITEM_PIPELINES = {
   # TODO 'juniorguru.sync.jobs.pipelines.validity_filter.Pipeline': 1,
   # TODO 'juniorguru.sync.jobs.pipelines.favicon.Pipeline': 990,
   # TODO **{
   # TODO    name: priority for name, priority in ITEM_PIPELINES.items()
   # TODO    if name not in [
   # TODO          'juniorguru.sync.jobs.pipelines.short_description_filter.Pipeline',
   # TODO          'juniorguru.sync.jobs.pipelines.broken_encoding_filter.Pipeline',
   # TODO          'juniorguru.sync.jobs.pipelines.gender_cleaner.Pipeline',
   # TODO          'juniorguru.sync.jobs.pipelines.language_filter.Pipeline',
   # TODO          'juniorguru.sync.jobs.pipelines.junior_rank_filter.Pipeline',
   # TODO    ]
   # TODO },
}

MEDIA_ALLOW_REDIRECTS = True
IMAGES_STORE = 'juniorguru/images'

FEEDS = {
    f'juniorguru/data/jobs/{today:%Y}/{today:%m}/{today:%d}.jsonl': {
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
