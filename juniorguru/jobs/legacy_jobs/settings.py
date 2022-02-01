from datetime import date

# Scrapy settings for jobs project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jobs'

SPIDER_MODULES = ['juniorguru.sync.jobs.spiders']
NEWSPIDER_MODULE = 'juniorguru.sync.jobs.spiders'


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
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'cs;q=0.8,en;q=0.6',
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'juniorguru.sync.jobs.middlewares.Something': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'juniorguru.sync.jobs.monitoring.BackupResponseMiddleware': 530,
   'juniorguru.sync.jobs.proxy.ScrapingProxyMiddleware': 555,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   'juniorguru.sync.jobs.monitoring.MonitoringExtension': 100,
}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
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

# Media Pipeline
# See https://docs.scrapy.org/en/latest/topics/media-pipeline.html
MEDIA_ALLOW_REDIRECTS = True
IMAGES_STORE = 'juniorguru/images'

# Feeds
today = date.today()
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
HTTPCACHE_IGNORE_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429, 999]
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
