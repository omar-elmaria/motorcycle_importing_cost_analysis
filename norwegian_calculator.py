# Import the packages
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import time
import os
import json
import re

# Day and month of the registration date
dd_mm = "07.07"

# Open the JSON file containing the motorcycle data
with open(file=os.path.join(os.getcwd(), "product_page.json"), mode="r") as json_file:
    data = json.load(json_file)

# Set the chrome options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True) # Keep the browser open after the code terminates
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging']) # Suppress the warning messages

# Instantiate a browser object
driver = webdriver.Chrome(options=chrome_options)

# Define a price conversion function
def convert_currency(amount, from_currency, to_currency):
    converted = requests.get(f"https://api.frankfurter.app/latest?amount={float(amount)}&from={from_currency}&to={to_currency}")
    converted = converted.json()['rates'][to_currency]
    return converted

# Define a function that goes to the Norwegian URL, inputs the parameters, and returns the price
for idx, i in enumerate(data):
    # If one of the main input variables is missing, don't navigate to the website, and set the price in NOK to "None"
    if i["bike_url"] == None or i["year_of_production"] == None or i["km_driven"] == None or i["cc"] == None or i["horsepower"] == None or i["price"] == None:
        i.update({"calculated_price": None})
        print(i) # Print the result
        continue # Continue to the next iteration

    # Navigate to the URL
    driver.get("https://www.skatteetaten.no/person/avgifter/bil/importere/regn-ut")

    # Maximize the window
    driver.maximize_window()

    # Wait for a few seconds for the page to load
    time.sleep(1.5)

    # Input the vehicle type
    driver.switch_to.frame(driver.find_element(By.ID, "iFrameResizer0"))
    select_vehicle_type = Select(driver.find_element(by=By.ID, value='KjoretoyType')) # Click on the drop down menu to display the vehicle types
    select_vehicle_type.select_by_visible_text(text="Motorsykkel") # Click on the vehicle type "Motorsykkel"
    driver.find_element(by=By.XPATH, value="//button[@class='button' and text()='Neste']").click() # Click the next button
    time.sleep(1.5) # Wait for 1.5 seconds until the action is executed

    # Enter the motorcycle type
    select_motorcycle_type = Select(driver.find_element(By.ID, "MotorsykkelType")) # Click on the drop down menu "MotorsykkelType"
    select_motorcycle_type.select_by_visible_text("Motorsykkel") # Click on the motorcycle type "Motorsykkel"
    driver.find_element(by=By.XPATH, value="//button[@class='button' and text()='Neste']").click() # Click the next button
    time.sleep(1.5) # Wait for 1.5 seconds until the action is executed

    # Click "Yes" to indicate that the vehicle is imported
    driver.find_element(by=By.XPATH, value="//label[@class='custom-control-label' and text()='Ja']").click()
    driver.find_element(by=By.XPATH, value="//button[@class='button' and text()='Neste']").click() # Click the next button
    time.sleep(1.5) # Wait for 1.5 seconds until the action is executed

    # Enter the date of registration
    if i["year_of_production"] == 2023:
        year = "2022"
    else:
        year = str(i["year_of_production"])
    driver.find_element(by=By.XPATH, value="//input[@class=' form-control input']").send_keys(f"{dd_mm}.{year}")
    driver.find_element(by=By.XPATH, value="//button[@class='button' and text()='Neste']").click() # Click the next button
    time.sleep(1.5) # Wait for 1.5 seconds until the action is executed

    # Answer the CO2 question
    driver.find_element(by=By.XPATH, value="//label[@class='custom-control-label' and text() = 'Nei']").click()
    driver.find_element(by=By.XPATH, value="//button[@class='button' and text()='Neste']").click() # Click the next button
    time.sleep(1.5) # Wait for 1.5 seconds until the action is executed

    # Enter the price in NOK
    price = convert_currency(i["price"], "PLN", "NOK")
    driver.find_element(By.ID , 'Innkjopspris').send_keys(price)
    driver.find_element(by=By.XPATH, value="//button[@class='button' and text()='Neste']").click() # Click the next button
    time.sleep(1.5) # Wait for 1.5 seconds until the action is executed

    # Enter the cc
    driver.find_element(By.ID, 'SlagvolumCcm').send_keys(i["cc"])
    driver.find_element(by=By.XPATH, value="//button[@class='button' and text()='Neste']").click() # Click the next button
    time.sleep(1.5) # Wait for 1.5 seconds until the action is executed

    # Enter the power unit (HP vs. kW)
    driver.find_element(by=By.XPATH, value="//label[@class='custom-control-label' and text() = 'Hestekrefter (hk)']").click()
    driver.find_element(By.ID, "MotoreffektKw").send_keys(i["horsepower"])
    driver.find_element(by=By.XPATH, value="//button[@class='button' and text()='Neste']").click() # Click the next button
    time.sleep(1.5) # Wait for 1.5 seconds until the action is executed

    # Click on calculate
    driver.find_element(by=By.XPATH, value="//button[@class='button' and text()='Regn ut']").click() # Click the next button
    time.sleep(1.5) # Wait for 1.5 seconds until the action is executed

    # Extract the price
    calculated_price = driver.find_element(by=By.XPATH, value="//div[@class='col-auto']/div[text()='Sum']/following-sibling::div/span").text

    # Append the calculated price to the dictionary
    i.update({"calculated_price": float(re.findall(pattern="(.*),", string=calculated_price)[0].replace(" ", ""))})
    print(i) # print the result
    

# Write the final product to a new JSON file
with open(file="final_dataset.json", mode="w") as file:
    json.dump(data, file)

time.sleep(5)
driver.quit()
