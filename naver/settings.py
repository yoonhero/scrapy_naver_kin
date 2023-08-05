BOT_NAME = "naver"

SPIDER_MODULES = ["naver.spiders"]
NEWSPIDER_MODULE = "naver.spiders"


DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}
ROTATING_PROXY_LIST_PATH = 'proxy-list.txt'
ROTATING_PROXY_PAGE_RETRY_TIMES = 5

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS=10
# DOWNLOAD_DELAY = 1
