from selenium import webdriver

from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup as bs

from googlesearch import search

import urllib.parse







def PrEvomag(name,q):

   

    

    link="https://www.google.com/search?q=Evomag " + name

        

    

    options = Options()

    options.headless = True

    driver = webdriver.Firefox(options=options)

    driver.get(link)





    soup = bs(driver.page_source, "lxml")



    search = soup.find(id = 'search')

    first_link = search.find('a')

    j = first_link['href']

    

    parsed_link = urllib.parse.urlparse(j)

    domain_name = parsed_link.netloc

    path = parsed_link.path



    if "evomag.ro" not in domain_name:

        q.put("Evomag: NULL")

        return

    if path == "/":

        q.put("Evomag: NULL")

        return

    

    driver.get(j)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    soup = bs(driver.page_source, "lxml")

        

    div_grid = soup.find("div",class_="wrap_inside_container main_body_container")

    if div_grid is None:

        driver.quit()

        q.put("Evomag: NULL")

        return





    container = div_grid.find("div",class_="product_right")

    if container is None:

        driver.quit()

        q.put("Evomag: NULL")

        return



    pret = container.find("div",class_="pret_rons")

    if pret is None:

        q.put("Evomag: NULL")

        return

    pret = pret.text.strip()

    driver.quit()

    q.put("Evomag: " + ''.join(filter(str.isdigit, pret[:-7])) + " RON")

    return