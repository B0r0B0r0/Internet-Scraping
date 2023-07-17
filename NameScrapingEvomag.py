from bs4 import BeautifulSoup as bs
import requests
import sys

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

# Request to website and download HTML contents
def EvomagScr(link):
    try:
        options = Options()
        options.headless = True

        driver = webdriver.Firefox(options=options)
        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = bs(driver.page_source, "lxml")
        
        div_grid = soup.find("div",class_="product_grid")
        if div_grid is None:
            driver.quit()
            return "Error"


        containers = div_grid.find_all("div",class_="nice_product_container")

        name_list=[]

        for ct in containers:

            nameDiv= ct.find("div", class_="npi_name")


            name=nameDiv.find("a")
            name=name.text.strip()
            name_list.append(name)




        driver.quit()
        name = ""
        for i in name_list:
            name = name + i + "#"
        
        return name

        

    except:
        return "Error"