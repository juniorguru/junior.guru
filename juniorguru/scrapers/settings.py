# Scrapy settings for jobs project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'juniorguru'

SPIDER_MODULES = ['juniorguru.scrapers.spiders']
NEWSPIDER_MODULE = 'juniorguru.scrapers.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'JuniorGuruBot (+https://junior.guru)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'juniorguru.scrapers.middlewares.Something': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'juniorguru.scrapers.monitoring.BackupResponseMiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'juniorguru.scrapers.monitoring.MonitoringExtension': 100,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'juniorguru.scrapers.pipelines.required_fields_filter.Pipeline': 100,
   'juniorguru.scrapers.pipelines.short_description_filter.Pipeline': 200,
   'juniorguru.scrapers.pipelines.broken_encoding_filter.Pipeline': 300,
   'juniorguru.scrapers.pipelines.language_parser.Pipeline': 350,
   'juniorguru.scrapers.pipelines.language_filter.Pipeline': 400,
   'juniorguru.scrapers.pipelines.description_parser.Pipeline': 500,
   'juniorguru.scrapers.pipelines.sections_parser.Pipeline': 500,
   'juniorguru.scrapers.pipelines.features_parser.Pipeline': 600,
   'juniorguru.scrapers.pipelines.junior_rank.Pipeline': 650,
   'juniorguru.scrapers.pipelines.junior_rank_filter.Pipeline': 700,
   'juniorguru.scrapers.pipelines.sort_rank.Pipeline': 750,
   'juniorguru.scrapers.pipelines.gender_cleaner.Pipeline': 800,
   'juniorguru.scrapers.pipelines.emoji_cleaner.Pipeline': 850,
   'juniorguru.scrapers.pipelines.location.Pipeline': 860,
   'juniorguru.scrapers.pipelines.employment_types_cleaner.Pipeline': 900,
   'juniorguru.scrapers.pipelines.company_logo.Pipeline': 995,
   'juniorguru.scrapers.pipelines.database.Pipeline': 1000,
}
JUNIORGURU_ITEM_PIPELINES = {
   'juniorguru.scrapers.pipelines.validity_filter.Pipeline': 1,
   'juniorguru.scrapers.pipelines.favicon.Pipeline': 990,
   **{
      name: priority for name, priority in ITEM_PIPELINES.items()
      if name not in [
            'juniorguru.scrapers.pipelines.short_description_filter.Pipeline',
            'juniorguru.scrapers.pipelines.broken_encoding_filter.Pipeline',
            'juniorguru.scrapers.pipelines.gender_cleaner.Pipeline',
            'juniorguru.scrapers.pipelines.language_filter.Pipeline',
            'juniorguru.scrapers.pipelines.junior_rank_filter.Pipeline',
      ]
   },
}

# Media Pipeline
# See https://docs.scrapy.org/en/latest/topics/media-pipeline.html
MEDIA_ALLOW_REDIRECTS = True
IMAGES_STORE = 'juniorguru/data/images'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'http_cache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
