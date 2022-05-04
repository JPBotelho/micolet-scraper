from itertools import product
import hashlib
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pathlib
import time
import re
from bs4 import BeautifulSoup
import urllib.request
import time

def main():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.micolet.pt/roupa-homem-segunda-mao?condition=new&page=1&size=m%2Cl&subcategories=106")
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    height = driver.execute_script("return document.body.scrollHeight")
    p = int(height/20)
    for i in range(p):
        driver.execute_script('window.scrollBy(0,20)') # scroll by 20 on each iteration
        #height = driver.execute_script("return document.body.scrollHeight") # reset height to the new height after scroll-triggered elements have been loaded. 
    #page = 

    
    for i in range(1, 2):
        URL = "https://www.micolet.pt/roupa-homem-segunda-mao?condition=new&page=1&size=m%2Cl&subcategories=106"
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        itemDivs = soup.find_all("div", {"class": "col-xs-6 col-md-4"})

        #print(itemDivs)
        for item in itemDivs:
            imageElement = item.findChildren("img", {"class": "img-responsive center-block lazy"}, recursive=True)
            imageUrl = imageElement[0].get("src")
            
            itemID = hashlib.md5(imageUrl.encode("utf-8")).hexdigest()
            print(imageUrl)
            
            #print(imageUrl)
            urlDiv = item.findChildren("a", {"class": "name"}, recursive=True)
            partialUrl = urlDiv[0].get("href")
            finalUrl = "https://www.micolet.pt/" + partialUrl
            #print(finalURL)
            
            tripleDiscountPrice = item.findChildren("span", {"class": "after-price discount"}, recursive=True)
            price = 0
            #no triple discount
            if(len(tripleDiscountPrice) > 0) :
                priceString = tripleDiscountPrice[0].getText() 
                priceString = priceString.replace(" ", "")
                price = priceString.replace("€", "")
            else: 
                doubleDiscountPrice = item.findChildren("span", {"class": "after-price"}, recursive=True)
                priceString = doubleDiscountPrice[0].getText() 
                priceString = priceString.replace(" ", "")
                price = priceString.replace("€", "")
              
            #print(price + " - " + finalUrl)

    
        #print(soup.text)
        #for div in urlDivs:
        #    productURL = "https://www.micolet.pt/" + div.get("href")
        #    
        #    normalPriceDivs = div.findChildren("span", {"class": "after-price discount"}, recursive=True)
        
        #    print(normalPriceDivs)
            
        
            
        


if __name__ == '__main__':
    main()