# motorcycle_importing_cost_analysis
This repo contains a Python script that uses Scrapy to scrape motorcycle attributes off of a Polish website and enter them into an online importing cost estimation tool using Selenium

# 1. The Objective of the Project
**First**, scrape motorcycle attributes from this [website](https://www.otomoto.pl/motocykle-i-quady/). Specifically, we want these fields --> `Name`, `Year`, `Km driven`, `CC`, `Horsepower`, `Price`, `Image Link`, and `Listing Link`. The screenshot below shows an example of a motorcyle listing.

![image](https://user-images.githubusercontent.com/98691360/204088616-48ae8248-3bd6-42c6-9700-1c3aebddab53.png)

After crawling the motorcycle attributes, we want to use this [website](https://www.skatteetaten.no/person/avgifter/bil/importere/regn-ut/) to calculate the total price of each motorcycle in **Norwegian Krone** including VAT, duties and fees. This website has several fields that must be populated to display the **full import price** of the motorcycle

![image](https://user-images.githubusercontent.com/98691360/204088960-58c59bb0-64ae-4895-b43c-07bacdec17fc.png)

**Finally**, we want to combine the data crawled from the motorcycle website with the price from the calculator into one JSON/CSV file.

## 1.1 Scraping Methodology - Motorcycle Attributes
To scrape the data off of the Polish [website](https://www.skatteetaten.no/person/avgifter/bil/importere/regn-ut/), I used the scrapy framework with ScraperAPI. ScraperAPI is a proxy solution for web crawling that is designed to make scraping the web at scale as simple as possible. It does that by removing the hassle of finding high quality proxies, rotating proxy pools, detecting bans, solving CAPTCHAs, and managing geotargeting, and rendering Javascript. I explained how to integrate ScraperAPI with scrapy in multiple other project descriptions. You can check any of these projects to get an overview on how to do that...
- [ecommerce_furniture_website_scraper](https://github.com/omar-elmaria/ecommerce_furniture_website_scraper)
- [amazon_luwak_coffee_scraper](https://github.com/omar-elmaria/amazon_luwak_coffee_scraper)
- [fiverr_scraper](https://github.com/omar-elmaria/fiverr_scraper)

The Scrapy code is located in this path `motorcycle_crawling\motorcycle_crawling\spiders`. It is composed of two Py files, `motorcycle_listing_page.py` and `motorcycle_product_page.py`. The first Py script scrapes the listing page for the **motorcycle name** and **product page URL**. The second Py script takes the output of the first script and crawls all the other fields mentioned above in **section 1**. An exercpt of the scraped dataset is shown below...

![image](https://user-images.githubusercontent.com/98691360/204089737-5a7cee6a-5914-4c4f-b099-f28d6f8c791d.png)

## 1.2 Inputting Data Into the Import Price Calculator
For this part, I chose **Python Selenium**, which is a powerful tool for controlling web browsers via code. The steps I had to automate are shown in the GIF below.

![norwegian_calculator_steps](https://user-images.githubusercontent.com/98691360/204093926-7a5b4f40-9241-4077-8e55-c9819570bcf0.gif)

The Selenium code is located in this file `norwegian_calculator.py`. The input to this script is the dataset scraped from the Polish website. In addition, the motorcycle prices in PLN need to be converted to NOK. To do this, we can use the **frankfurter app** API each time we want to calculated the import price. The APIreturns the converted price in JSON format

```python
def convert_currency(amount, from_currency, to_currency):
    converted = requests.get(f"https://api.frankfurter.app/latest?amount={float(amount)}&from={from_currency}&to={to_currency}")
    converted = converted.json()['rates'][to_currency]
    return converted
```

After the Selenium code terminates, a column is appended to the data frame containing the scraped data. This column is called `calculated_price` and shows the **import price** in NOK. An exercpt of the **full dataset** is shown below...

![image](https://user-images.githubusercontent.com/98691360/204143300-9e2db64e-bd6d-41a1-ad2c-511da93cbfe7.png)

**Note:** Whenever one of the attributes required to calculate the price is missing, the `calculated_price` is set to **None**. For the sake of demonstration, I chose to run the script for the **first 8 entries** only. For that reason, `final_dataset.json` does not contain the `calculated_price` for all scraped motorcycles. However, the code is configured to loop over **all the entries** in `product_page.json`

# 2. Questions?
If you have any questions or wish to build a scraper for a particular use case (e.g., Competitive Intelligence or price comparison), feel free to contact me on [LinkedIn](https://www.linkedin.com/in/omar-elmaria/)
