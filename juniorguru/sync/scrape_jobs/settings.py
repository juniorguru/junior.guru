BOT_NAME = 'jobs'

SPIDER_MODULES = ['juniorguru.sync.scrape_jobs.spiders']
NEWSPIDER_MODULE = 'juniorguru.sync.scrape_jobs.spiders'

USER_AGENT = 'JuniorGuruBot (+https://junior.guru)'
ROBOTSTXT_OBEY = True

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'cs;q=0.8,en;q=0.6',
}

DOWNLOADER_MIDDLEWARES = {
   # TODO 'juniorguru.sync.scrape_jobs.monitoring.BackupResponseMiddleware': 530,
   'juniorguru.lib.proxies.ScrapingProxiesMiddleware': 555,
}

EXTENSIONS = {
   # TODO 'juniorguru.sync.scrape_jobs.monitoring.MonitoringExtension': 100,
}

ITEM_PIPELINES = {
   'juniorguru.sync.scrape_jobs.pipelines.required_fields_filter.Pipeline': 50,
   'juniorguru.sync.scrape_jobs.pipelines.short_description_filter.Pipeline': 100,
   'juniorguru.sync.scrape_jobs.pipelines.broken_encoding_filter.Pipeline': 150,
   'juniorguru.sync.scrape_jobs.pipelines.language_parser.Pipeline': 200,
   'juniorguru.sync.scrape_jobs.pipelines.language_filter.Pipeline': 250,
}

FEED_EXPORTERS = {
   'jsonl.gz': 'juniorguru.sync.scrape_jobs.feeds.GzipJsonLinesItemExporter',
}
FEEDS_DIR = 'juniorguru/data/jobs'
FEEDS = {
    FEEDS_DIR + "/%(year)s/%(month)s/%(day)s/%(name)s.jsonl.gz": {
         'uri_params': 'juniorguru.sync.scrape_jobs.feeds.uri_params',
         'format': 'jsonl.gz',
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

PROXIES_FILE = 'juniorguru/data/proxies.txt'
