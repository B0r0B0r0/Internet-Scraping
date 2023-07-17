from bs4 import BeautifulSoup as bs
import requests
import sys

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException

# Request to website and download HTML contents
def MediagalaxyScr(link):
    try:
        options = Options()
        options.headless = True

        driver = webdriver.Firefox(options=options)
        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = bs(driver.page_source, "lxml")
        
        ul_tags = soup.find("ul",class_="Products flex flex-wrap relative -mx-1 sm:-mx-2")
        if ul_tags is None:
            driver.quit()
            return "Error"


        li_tags = ul_tags.find_all("li",class_="Products-item w-1/2 sm:w-1/3 p-1 sm:p-2 border-transparent md:border-2 min-h-330px lg:min-h-400px bg-white lg:w-1/4")

        name_list=[]

        for li in li_tags:
            span_tag=li.find("span", class_="Product-name Heading leading-20 text-sm min-h-[68px] line-clamp-3 max-h-[68px]")
            
            name_list.append(str(span_tag.text.strip()))
        


        driver.quit()
        name = ""
        for i in name_list:
            name =name + i + "#"

        return name


    

    except Exception as err:
        return "Error"