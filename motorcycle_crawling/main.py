from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from motorcycle_crawling.spiders.motorcycle_listing_page import MotorcycleListingPageSpider


def main():
    settings = get_project_settings()
    configure_logging(settings=settings)
    runner = CrawlerRunner(settings=settings)

    @defer.inlineCallbacks # type: ignore
    def crawl():
        yield runner.crawl(MotorcycleListingPageSpider)
        from motorcycle_crawling.spiders.motorcycle_product_page import MotorcycleProductSpider
        yield runner.crawl(MotorcycleProductSpider)
        reactor.stop() # type: ignore

    crawl()
    reactor.run() # type: ignore

if __name__ == '__main__':
    main()
