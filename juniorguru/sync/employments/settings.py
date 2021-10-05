BOT_NAME = 'employments'

SPIDER_MODULES = ['juniorguru.sync.employments.spiders']
NEWSPIDER_MODULE = 'juniorguru.sync.employments.spiders'

USER_AGENT = 'JuniorGuruBot (+https://junior.guru)'
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'juniorguru.sync.employments.pipelines.identify.Pipeline': 1,
    'juniorguru.sync.employments.pipelines.parse_description.Pipeline': 2,
    'juniorguru.sync.employments.pipelines.save.Pipeline': 3,
}

HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'http_cache'
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 999]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
