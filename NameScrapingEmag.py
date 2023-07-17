from bs4 import BeautifulSoup as bs
import requests
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

# Request to website and download HTML contents
def EmagScr(link):
    try:
        options = Options()
        options.headless = True

        driver = webdriver.Firefox(options=options)
        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = bs(driver.page_source, "lxml")
        
        grid = soup.find("div",class_="js-products-container card-collection list-view-updated show-me-a-grid")
        if grid is None:
            driver.quit()
            return "Error"


        containers = grid.find_all("div",class_="card-item card-standard js-product-data")

        name_list=[]

        for ct in containers:  

            p_tag=ct.find("a", class_="card-v2-title semibold mrg-btm-xxs js-product-url")
            
            name_list.append(p_tag.text.split())
        



        driver.quit()
        name = ""
        for i in name_list:
            name = name + i + "#"
        return name


        

    except:
        return "Error"