from datetime import date


today = date.today()
BOT_NAME = 'jobs'

SPIDER_MODULES = ['juniorguru.sync.legacy_jobs.spiders']
NEWSPIDER_MODULE = 'juniorguru.sync.legacy_jobs.spiders'


USER_AGENT = f'JuniorGuruBot/{today.year}.{today.month}.{today.day} (+https://junior.guru)'
ROBOTSTXT_OBEY = True

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'cs;q=0.8,en;q=0.6',
}

DOWNLOADER_MIDDLEWARES = {
   'juniorguru.sync.jobs.monitoring.BackupResponseMiddleware': 530,
   'juniorguru.sync.jobs.proxy.ScrapingProxyMiddleware': 555,
}

EXTENSIONS = {
   'juniorguru.sync.jobs.monitoring.MonitoringExtension': 100,
}

ITEM_PIPELINES = {
   'juniorguru.sync.jobs.pipelines.identifier.Pipeline': 1,
   'juniorguru.sync.jobs.pipelines.required_fields_filter.Pipeline': 50,
   'juniorguru.sync.jobs.pipelines.description_parser.Pipeline': 100,  # experimenting with Mila and ML
   'juniorguru.sync.jobs.pipelines.short_description_filter.Pipeline': 200,
   'juniorguru.sync.jobs.pipelines.broken_encoding_filter.Pipeline': 300,
   'juniorguru.sync.jobs.pipelines.language_parser.Pipeline': 350,
   'juniorguru.sync.jobs.pipelines.language_filter.Pipeline': 400,
   # 'juniorguru.sync.jobs.pipelines.description_parser.Pipeline': 500,
   # 'juniorguru.sync.jobs.pipelines.sections_parser.Pipeline': 500,  https://app.circleci.com/pipelines/github/honzajavorek/junior.guru/3047/workflows/033dc5ea-e097-4d73-abea-fcaf7610460b/jobs/19368
   'juniorguru.sync.jobs.pipelines.features_parser.Pipeline': 600,
   'juniorguru.sync.jobs.pipelines.junior_rank.Pipeline': 650,
   'juniorguru.sync.jobs.pipelines.junior_rank_filter.Pipeline': 700,
   'juniorguru.sync.jobs.pipelines.sort_rank.Pipeline': 750,
   'juniorguru.sync.jobs.pipelines.gender_cleaner.Pipeline': 800,
   'juniorguru.sync.jobs.pipelines.emoji_cleaner.Pipeline': 850,
   'juniorguru.sync.jobs.pipelines.locations.Pipeline': 860,
   'juniorguru.sync.jobs.pipelines.employment_types_cleaner.Pipeline': 900,
   'juniorguru.sync.jobs.pipelines.company_logo.Pipeline': 995,
   'juniorguru.sync.jobs.pipelines.database.Pipeline': 1000,
}
JUNIORGURU_ITEM_PIPELINES = {
   'juniorguru.sync.jobs.pipelines.validity_filter.Pipeline': 1,
   'juniorguru.sync.jobs.pipelines.favicon.Pipeline': 990,
   **{
      name: priority for name, priority in ITEM_PIPELINES.items()
      if name not in [
            'juniorguru.sync.jobs.pipelines.short_description_filter.Pipeline',
            'juniorguru.sync.jobs.pipelines.broken_encoding_filter.Pipeline',
            'juniorguru.sync.jobs.pipelines.gender_cleaner.Pipeline',
            'juniorguru.sync.jobs.pipelines.language_filter.Pipeline',
            'juniorguru.sync.jobs.pipelines.junior_rank_filter.Pipeline',
      ]
   },
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
        },
    },
}

AUTOTHROTTLE_ENABLED = True

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'http_cache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 999]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
