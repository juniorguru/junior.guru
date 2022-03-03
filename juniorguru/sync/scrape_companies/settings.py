BOT_NAME = 'companies'

SPIDER_MODULES = ['juniorguru.sync.scrape_companies.spiders']
NEWSPIDER_MODULE = 'juniorguru.sync.scrape_companies.spiders'

USER_AGENT = 'JuniorGuruBot (+https://junior.guru)'
ROBOTSTXT_OBEY = True

DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'cs;q=0.8,en;q=0.6',
}

DOWNLOADER_MIDDLEWARES = {
   # TODO 'juniorguru.sync.scrape_jobs.monitoring.BackupResponseMiddleware': 530,
   'juniorguru.lib.proxies.ScrapingProxyMiddleware': 555,
}

EXTENSIONS = {
   # TODO 'juniorguru.sync.scrape_jobs.monitoring.MonitoringExtension': 100,
}

ITEM_PIPELINES = {
   'juniorguru.sync.scrape_companies.pipelines.logo.Pipeline': 50,
}

MEDIA_ALLOW_REDIRECTS = True
IMAGES_STORE = 'juniorguru/images'

AUTOTHROTTLE_ENABLED = True

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'http_cache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 999]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
