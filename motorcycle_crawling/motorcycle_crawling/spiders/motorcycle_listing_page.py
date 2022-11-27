# Import the packages
import scrapy
from scrapy.crawler import CrawlerProcess
from dotenv import load_dotenv
from scraper_api import ScraperAPIClient
import os

custom_settings_dict = {
    "FEED_EXPORT_ENCODING": "utf-8", # UTF-8 deals with all types of characters
    "RETRY_TIMES": 3, # Retry failed requests up to 3 times
    "AUTOTHROTTLE_ENABLED": False, # Disables the AutoThrottle extension (recommended to be used with proxy services)
    "RANDOMIZE_DOWNLOAD_DELAY": False, # Should not be used with proxy services. If enabled, Scrapy will wait a random amount of time (between 0.5 * DOWNLOAD_DELAY and 1.5 * DOWNLOAD_DELAY) while fetching requests from the same website
    "CONCURRENT_REQUESTS": 5, # The maximum number of concurrent (i.e. simultaneous) requests that will be performed by the Scrapy downloader
    "DOWNLOAD_TIMEOUT": 60, # Setting the timeout parameter to 60 seconds as per the ScraperAPI documentation
    "ROBOTSTXT_OBEY": False
}

# Load environment variables
load_dotenv()

# Create the scraper API client
client = ScraperAPIClient(api_key=os.getenv(key="SCRAPER_API_KEY"))

class MotorcycleListingPageSpider(scrapy.Spider):
    name = 'motorcycle_listing_page'
    custom_settings = custom_settings_dict # Standard custom settings of the spider
    custom_settings["FEEDS"] = {"listing_page.json":{"format": "json", "overwrite": True}} # Export to a JSON file with an overwrite functionality

    # Define a function to start the crawling process
    def start_requests(self):
        # The home page of the website we want to crawl
        url = "https://www.otomoto.pl/motocykle-i-quady"
        yield scrapy.Request(client.scrapyGet(url=url, country_code="de"), callback = self.parse)
    
    def parse(self, response):
        bikes = response.xpath("//main[@data-testid='search-results']/article")
        for bike in bikes:
            yield {
                "bike_name": bike.xpath(".//h2[@data-testid='ad-title']/a/text()").get(),
                "bike_url": bike.xpath(".//h2[@data-testid='ad-title']/a/@href").get(),
            }
