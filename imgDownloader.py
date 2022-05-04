from itertools import product
import hashlib
from tkinter import image_names
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pathlib
import time
import re
from bs4 import BeautifulSoup
import urllib.request
import time

class MicoletItem:
    def __init__(self, id, price, priceInt, img, url):
        self.id = id
        self.price = price
        self.priceInt = priceInt
        self.img = img.replace("\n", "")
        self.url = url
        
    def __lt__(self, other):
        return self.priceInt < other.priceInt
    
    def __eq__(self, other):
        return self.priceInt == other.priceInt

def main():
    f = open("MicoletSearch.txt", "r")
    lines = f.readlines()
    print(len(lines))
    items = []
    for i in range(0, len(lines), 4):
        id = lines[i]
        price = lines[i+1]
        priceInt = int(lines[i+1].replace(",", ""))
        #print(price)

        img = lines[i+2]
        url = lines[i+3]
        
        item = MicoletItem(id, price, priceInt, img, url)
        items.append(item)
    
    items.sort()
    print(len(items))
    
    #testf = open("debug.txt", "w")
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    testarino = requests.get("https://d30o7qbghf97ws.cloudfront.net/itemimage/4051697/image/list-ce54fc6490cf7542996fcd9a822c2151.jpg", headers=headers)
    #print(testarino.content)
    with open("debug.jpg","wb") as imgStream:
        imgStream.write(testarino.content)
        imgStream.close()
    for item in items:
        print(item.img)
        r = requests.get(item.img, headers=headers)
        fileName = (item.price + " - " + item.id).replace("\n","")
        with open(fileName + ".jpg", "wb") as imgStream:
            imgStream.write(r.content)
            imgStream.close()
        #testf.write("\n"+fileName)
        
        
    #testf.close()

if __name__ == '__main__':
    main()