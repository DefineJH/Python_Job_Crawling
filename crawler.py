from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import urllib.parse
import webbrowser
import wordcloud
import matplotlib
import requests
import random
import time
page_num = list()
recruit_page = list()

keywords = dict()

NGWords = ['서울','시','구','학원']



def JobKorea_Search():
    baseUrl = 'https://www.jobkorea.co.kr/Search/?stext='
    plusUrl = input('검색어를 입력하세요 : ')


    url = baseUrl + urllib.parse.quote_plus(plusUrl)

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }
    html = session.get(url, headers=headers).content

    #JobKorea_SearchPage(html,1)
    JobKorea_SearchPage_Debug(html,1)

def JobKorea_SearchPage(html, idx):

    bsObject = bs(html, "html.parser")


    company = bsObject.find_all("a",{"class":"title dev_view"})

    baseRecruit_URL = "https://www.jobkorea.co.kr"

    #게임잡 url 나와서 https://www.jobkorea.co.kr/https://www.gamejob.co.kr/List_GI/GIB_Read.asp?GI_No=190409 와같은 일이 일어날 수도 있음.
    for i in company:
        tempUrl = i.attrs['href']
        if "gamejob" in  tempUrl:
            tempList = tempUrl.split('http')
            recruit_page.append('http' + tempList[-1])
        else:
            recruit_page.append(baseRecruit_URL + tempUrl)  

    idx += 1    
    page = bsObject.select_one("a[page-no*=\"" + str(idx) +"\"]")

    if page != None:
        html = urlopen(baseRecruit_URL + page.attrs["href"])
        JobKorea_SearchPage(html,idx)
    else:
        return

    
def JobKorea_SearchPage_Debug(html, idx):
    bsObject = bs(html, "html.parser")

    company = bsObject.find_all("a",{"class":"title dev_view"})

    baseRecruit_URL = "https://www.jobkorea.co.kr"

    #게임잡 url 나와서 https://www.jobkorea.co.kr/https://www.gamejob.co.kr/List_GI/GIB_Read.asp?GI_No=190409 와같은 일이 일어날 수도 있음.
    for i in company:
        tempUrl = i.attrs['href']
        if "gamejob" in  tempUrl:
            tempList = tempUrl.split('http')
            recruit_page.append('http' + tempList[-1])
        else:
            recruit_page.append(baseRecruit_URL + tempUrl)  
    return



def InspectKeyword(word):
    for elem in NGWords:
        if elem in word:
            return False
    return True


def JobKorea_KeywordListing():

    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }
    for elem in recruit_page:
        rand_value = random.randint(1, 3)
        time.sleep(rand_value)
        html = session.get(elem, headers=headers).content
        bsObject = bs(html, "html.parser")

        tempSelected = bsObject.select("#artKeywordSearch > ul > li")

        for elem2 in tempSelected:
            word = elem2.getText()[1:-1]
            print(word + " is dsds")
            if InspectKeyword(word):
                if word not in keywords:
                    keywords[word] = 0
                keywords[word] += 1



def StartCrawling():
    JobKorea_Search()
    JobKorea_KeywordListing()

    for elem in recruit_page:
        print(elem)
    for key, value in keywords.items():
        print(key, ":", value)

    wordCloud = wordcloud.WordCloud(font_path='font_korean.ttf',background_color='white',width=1000,height=1000).generate_from_frequencies(keywords)

    fig = matplotlib.pyplot.figure()
    matplotlib.pyplot.imshow(wordCloud, interpolation='bilinear')
    matplotlib.pyplot.axis('off')
    matplotlib.pyplot.show()
    matplotlib.pyplot.savefig('img.jpg')

