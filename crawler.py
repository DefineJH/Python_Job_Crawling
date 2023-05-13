from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
import urllib.parse
import webbrowser
import wordcloud
import requests
import random
import time
page_num = list()
recruit_page = list()

keywords = dict()

NGWords = ['서울','시','구','학원', '지역' , '경기' ,'병역','개발자', '프로그래머']



def JobKorea_Search(jobName):
    baseUrl = 'https://www.jobkorea.co.kr/Search/?stext='
    plusUrl = jobName


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
        if tempUrl.count("http") == 2:
            continue
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
        if tempUrl.count("http") == 2:
            continue
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
            print(word)
            if InspectKeyword(word):
                if word not in keywords:
                    keywords[word] = 0
                keywords[word] += 1



def StartCrawling(jobName):
    
    JobKorea_Search(jobName)
    JobKorea_KeywordListing()

    for elem in recruit_page:
        print(elem)
    for key, value in keywords.items():
        print(key, ":", value)

    wordCloud = wordcloud.WordCloud(font_path='font_korean.ttf',background_color='white',width=1000,height=1000).generate_from_frequencies(keywords)
    wordCloud.to_file('img.png')


def ConstructInfoSite(keyword):
    html_text_start = """
     <!DOCTYPE html>
     <html>
     <head>
     <title>설명 페이지</title>
     </head>
     <body>
 """    
    html_text_end = """
     </body>
     </html>
 """
    html_middle = ""
    baseUrl = 'https://www.google.com/search?q='
    url = baseUrl +  urllib.parse.quote_plus(keyword)
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }
    html = session.get(url, headers=headers).content
    bsObject = bs(html, "html.parser")
    v = bsObject.select('.yuRUbf')
    wiki = ""
    html_middle += "<div> <h1> 구글검색 </h1> <br>"
    for i in v:
        print(i.select_one('h3').text) # 제목
        print(i.a.attrs['href'])       # 링크
        urls = i.a.attrs['href']
        if "namu" in i.a.attrs['href']:
            wiki += ("<button onclick=\"location.href=\'" + urls + "\'\">나무위키 " + keyword + "검색 </button>")
        elif "wikipedia" in i.a.attrs['href']:
            wiki += ("<button onclick=\"location.href=\'" + urls + "\'\">위키피디아 " + keyword + "검색 </button>")
        else:
            html_middle +="<a href=\""+urls+"\"><h3>"+i.select_one('h3').text+"</h3></a>"

    html_middle += "<div> <h1> 위키 사이트 </h1> <br>"+wiki
    html_middle += "</div>"

    html_middle += "<div> <h1> 추천서적 </h1> <br>"
    #
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
            


    for b in books:
        html_middle += "<a href=\""+b[0]+"\" >"+"<img width=100 src=\""+b[1]+"\"></a><br><p>"+b[2]+"</p>"
        
    html_middle += "</div>"
    f = open("final_page.html",'w')
    f.write(html_text_start + html_middle + html_text_end)

    webbrowser.open("final_page.html")




