from selenium import webdriver

from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup as bs

from googlesearch import search

import urllib.parse







def PrEmag(name,q):

   

  

    link="https://www.google.com/search?q=Emag " + name







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



    if "emag.ro" not in domain_name:

        q.put("Emag: NULL")

        return

    if path == "/":

        q.put("Emag: NULL")

        return

    

    driver.get(j)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    soup = bs(driver.page_source, "lxml")

        

    div_grid = soup.find("div",class_="main-container-inner")

    if div_grid is None:

        driver.quit()

        q.put("Emag: NULL")

        return





    container = div_grid.find("form",class_="main-product-form")

    if container is None:

        driver.quit()

        q.put("Emag: NULL")

        return



    pret = container.find("p",class_="product-new-price")

    if pret is None:

        q.put("Emag: NULL")

        return

    pret = pret.text.strip()

    driver.quit()

    q.put("Emag: " + ''.join(filter(str.isdigit, pret[:-7])) + " RON")

    return