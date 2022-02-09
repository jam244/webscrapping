# -*- coding: utf-8 -*-
"""
Created on Sat Jan 29 15:29:43 2022

@author: z004dz0e
"""

import requests
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import time
import pdfplumber
import re
import random
import matplotlib.pyplot as plt

from selenium.webdriver.chrome.options import Options


#filename = "sainsburys_groceries_order_587832131.pdf"

filename = "574476219.pdf"

pattern = re.compile(r"\£\d*\.?\d*$")

baseurl = "https://www.sainsburys.co.uk/shop/gb/groceries"



def parse_pdf(filename):
    items=[]
    with pdfplumber.open(filename) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split("\n"):
                if re.search(pattern, line):
                    line = line[line.index(' ')+1:]
                    line = line[:line.rindex(' ')]
                    items.append(line)
                
    print(items)
    
    return items

sleepseconds = 3


def get_calories(item, driver):
    print("Getting calories for:", item)


    search = driver.find_element(By.ID, "search")
    print(item)
    search.send_keys(item)
    search.send_keys(Keys.RETURN)

    main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pt__content")))
    time.sleep(random.randint(2, 3))
    driver.find_element(By.CLASS_NAME,"pt__content").click()
    
    try:
        main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "nutritionTable")))
    except:
        return -1

    table = driver.find_element(By.CLASS_NAME,"nutritionTable")
    rows= table.find_elements(By.TAG_NAME, "tr")
    calories = -1

    for row in rows:
        col = row.find_elements(By.TAG_NAME,"td")
        for c in col:
            if c.text.endswith("kcal"):
                print(c.text)
                calories = int(c.text[:c.text.rindex('kcal')])
                break

    return calories



def plot_pie(calorie_table):
    labels = list(calorie_table.keys())
    values = list(calorie_table.values())
    fig1, ax1 = plt.subplots(figsize=(20, 12))
    ax1.set_title('Calories per 100g')
    ax1.pie(values, labels=labels, autopct=lambda val: round(val/100.*sum(values), 0))
    #plt.legend(patches, labels, loc="best")
    plt.savefig('pie.png')
    plt.show()
    print(calorie_table)
    
    
if __name__ == "__main__":
    items = parse_pdf(filename)

    sleep(5)
    driver = webdriver.Remote("http://selenium:4444/wd/hub", desired_capabilities=DesiredCapabilities.CHROME)
    driver.get(baseurl)

    cookie_button='//*[@id="onetrust-accept-btn-handler"]'

    main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cookie_button)))
    driver.find_element(By.XPATH, cookie_button).click()
    
    calorie_table={}
    for item in items:
        cal=-1
        for i in range(0,5):
            try:
                cal = get_calories(item, driver)
            except:
                driver.find_element(By.CLASS_NAME,"logo-image").click()
                time.sleep(random.randint(5, 10))
                continue
            break
        if cal != -1:
            calorie_table[item] = cal
        else:
            print("No calorie information for :", item)

        for i in range(5):
            try:
                main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "logo-image")))
            except:
                time.sleep(random.randint(1, 3))
                driver.find_element(By.CLASS_NAME,"logo-image").click()
                continue
        
        print("logo")    
        driver.find_element(By.CLASS_NAME,"logo-image").click()
        time.sleep(random.randint(5, 10))
            
    plot_pie(calorie_table)
    driver.quit()
        
            
    
    
    

