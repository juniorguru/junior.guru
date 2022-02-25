import os


BOT_NAME = 'companies'

SPIDER_MODULES = ['juniorguru.scrape_companies.spiders']
NEWSPIDER_MODULE = 'juniorguru.scrape_companies.spiders'

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
   'juniorguru.scrape_companies.pipelines.company_logo.Pipeline': 50,
}

MEDIA_ALLOW_REDIRECTS = True
IMAGES_STORE = 'juniorguru/images'

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
