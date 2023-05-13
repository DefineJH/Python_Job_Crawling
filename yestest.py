from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
import urllib.parse
import webbrowser
import wordcloud
import requests
import random
import time
keyword = 'html'
books = list()
baseUrl = 'http://www.yes24.com/searchcorner/Search?keywordAd=&keyword=&domain=ALL&qdomain=%C0%FC%C3%BC&Wcode=001_005&query='

enc = urllib.parse.quote(keyword)
url = baseUrl + urllib.parse.quote_plus(keyword,encoding="euc-kr")
print(enc)
print(url)

session = HTMLSession()


resp = session.get(url)
resp.html.render()
html = resp.html.html


bsObject = bs(html, "html.parser")
print(bsObject.string)
v = bsObject.select('.lnk_img')
for elem in v:
    print(elem["href"])
    tempURL = "http://www.yes24.com" +  elem['href']
    imgTag = elem.select_one('.img_bdr').select('img')
    for img in imgTag:
        tempImg = img["src"]
        tempName = img["alt"]
        if tempImg != "https://image.yes24.com/sysimage/renew/loadSpace.png":
            books.append([tempURL,tempImg,tempName])

        