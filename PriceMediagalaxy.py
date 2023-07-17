from selenium import webdriver

from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup as bs

from googlesearch import search

import urllib.parse







def PrMediaGalaxy(name,q):

   

  

    link="https://www.google.com/search?q=MediaGalaxy  " + name

        

    

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



    if "mediagalaxy.ro" not in domain_name:

        q.put("MediaGalaxy: NULL")

        return

    if path == "/":

        q.put("MediaGalaxy: NULL")

        return

    

    driver.get(j)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    soup = bs(driver.page_source, "lxml")

        

    div_grid = soup.find("div",class_="flex items-start flex-col space-y-2 md:space-y-0 md:flex-row md:space-x-8 justify-center lg:-mx-3 my-3 mb-14")

    if div_grid is None:

        driver.quit()

        q.put("MediaGalaxy: NULL")

        return





    container = div_grid.find("div",class_="lg:w-1/2 mb-2")

    if container is None:

        driver.quit()

        q.put("MediaGalaxy: NULL")

        return



    pret = container.find("span")

    if pret is None:

        q.put("MediaGalaxy: NULL")

        return

    pret = pret.text.strip()

    driver.quit()

    q.put("MediaGalaxy: " + ''.join(filter(str.isdigit, pret)) + " RON")

    return