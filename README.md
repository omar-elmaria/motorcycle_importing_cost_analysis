# motorcycle_importing_cost_analysis
This repo contains a Python script that uses Scrapy to scrape motorcycle attributes off of a Polish website and enter them into an online importing cost estimation tool using Selenium

# The Objective of the Project
1. You first want to scrape motorcycle data from this website (https://www.otomoto.pl/motocykle-i-quady/). Specifically, you want these fields --> Name, Year, Km driven, CC, Horsepower, Price, image link, and listing link. I attached a screenshot showing where I would pull this data from.

Q: Could you please confirm that these are the required fields? One thing I couldn't find is "Horsepower." Could you perhaps share with me a listing where the Horsepower is shown?

2. After crawling the motorcycle data, you then want to use this website (https://www.skatteetaten.no/person/avgifter/bil/importere/regn-ut/) to calculate the importing price of each motorcycle in Norwegian Krone.

Q: Could you tell me which input fields you want to use in the form and also if you want to report the four fields given by the calculator, "Avgift," "Innkjøpspris," "Mva," and "Sum" or just the "Sum"?

Finally, you want to combine the data crawled from the motorcycle website with the data from the calculator into one Excel file. Does this look like an accurate overview of the task?
