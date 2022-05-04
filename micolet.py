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
   
    soldOut = False
    iterator = 0
    
    outputFile = open("MicoletSearch.txt","w")
    
    for i in range(1, 50):
        if(soldOut):
            break
        URL = f"https://www.micolet.pt/roupa-homem-segunda-mao?condition=new&page={i}&size=m%2Cl&subcategories=106"

        driver.get(URL)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        height = driver.execute_script("return document.body.scrollHeight")
        p = int(height/20)
        for i in range(p):
            driver.execute_script('window.scrollBy(0,20)') # scroll by 20 on each iteration
            #height = driver.execute_script("return document.body.scrollHeight") # reset height to the new height after scroll-triggered elements have been loaded. 
        #page = 
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        itemDivs = soup.find_all("div", {"class": "col-xs-6 col-md-4"})

        #print(itemDivs)
        for item in itemDivs:
            iterator+=1
            addToCartElement = item.findChildren("div", {"class": "thumb-add-to-cart"}, recursive=True)
            #print(itemDivs)
            if(len(addToCartElement) == 0):
                print("ESGOTADO")
                soldOut = True
                break
            imageElement = item.findChildren("img", {"class": "img-responsive center-block lazy"}, recursive=True)
            
            
            #URL
            imageUrl = imageElement[0].get("src")
            
            #ItemID
            iteratorString = str(iterator)
            itemID = iteratorString.zfill(5)
            
            print(itemID)
            
            urlDiv = item.findChildren("a", {"class": "name"}, recursive=True)
            partialUrl = urlDiv[0].get("href")
            
            #Final price
            price = 0
            #no triple discount
            tripleDiscountPrice = item.findChildren("span", {"class": "after-price discount"}, recursive=True)

            if(len(tripleDiscountPrice) > 0) :
                priceString = tripleDiscountPrice[0].getText() 
                priceString = priceString.replace(" ", "")
                price = priceString.replace("€", "")
            else: 
                doubleDiscountPrice = item.findChildren("span", {"class": "after-price"}, recursive=True)
                priceString = doubleDiscountPrice[0].getText() 
                priceString = priceString.replace(" ", "")
                price = priceString.replace("€", "")  

            finalUrl = "https://www.micolet.pt/" + partialUrl
                
            outputFile.write(itemID)
            outputFile.write("\n"+price)
            outputFile.write("\n"+imageUrl)
            outputFile.write("\n"+finalUrl+"\n")

            #Item URL

            
            
                 


if __name__ == '__main__':
    main()