# Import the packages
import scrapy
from scrapy.crawler import CrawlerProcess
import os
import json
import re
from w3lib.html import remove_tags
from motorcycle_crawling.spiders.motorcycle_listing_page import custom_settings_dict
from motorcycle_crawling.spiders.motorcycle_listing_page import client


# Open the JSON file containing the URLs to the individual motorbikes
with open(file= os.path.join(os.getcwd(), "listing_page.json"), mode="r") as json_file:
    data = json.load(json_file)

# Get the individual motorcycle URLs
motorcycle_urls = [i["bike_url"] for i in data]

# Define functions to handle missing data
def extract_element_wout_regex(selector):
    try:
        return int(selector.get().strip().replace(" ", ""))
    except AttributeError as err:
        print(err)
        return None

def extract_element_with_regex(pattern, selector):
    try:
        return int(re.findall(pattern=pattern, string=selector.get().strip())[0].replace(" ", ""))
    except AttributeError as err:
        print(err)
        return None

class MotorcycleProductSpider(scrapy.Spider):
    name = 'motorcycle_product_page'
    custom_settings = custom_settings_dict # Standard custom settings of the spider
    custom_settings["FEEDS"] = {"product_page.json":{"format": "json", "overwrite": True}} # Export to a JSON file with an overwrite functionality

    # Define a function to start the crawling process
    def start_requests(self):
        for url in motorcycle_urls:
            yield scrapy.Request(client.scrapyGet(url=url, country_code="de"), callback = self.parse)

    def parse(self, response):
        params = response.xpath("//ul[@class='offer-params__list'][1]")
        for param in params:
            yield {
                "bike_name": response.xpath("//span[@class='offer-title big-text fake-title']/text()").getall()[1].strip(),
                "bike_url": remove_tags(response.headers["Sa-Final-Url"]),
                "image_link": response.css("li.offer-photos-thumbs__item > img::attr(src)").get(),
                "year_of_production": extract_element_wout_regex(selector=param.xpath(".//span[text()='Rok produkcji']/following-sibling::div/text()")),
                "km_driven": extract_element_with_regex(pattern="(.*)km", selector=param.xpath(".//span[text()='Przebieg']/following-sibling::div/text()")),
                "cc": extract_element_with_regex(pattern="\d.\d+", selector=param.xpath(".//span[text()='Pojemność skokowa']/following-sibling::div/text()")), # type: ignore
                "horsepower": extract_element_with_regex(pattern="(.*)KM", selector=param.xpath(".//span[text()='Moc']/following-sibling::div/text()")),
                "price": extract_element_wout_regex(selector=response.css("span.offer-price__number::text"))
            }
