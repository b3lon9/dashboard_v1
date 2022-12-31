from bs4 import BeautifulSoup as bs
import requests
from urllib import request
import pytesseract
from PIL import Image
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = 'C:/Users/USER/AppData/Local/Tesseract-OCR/tesseract.exe'

def makePgNum(num):
        if num == 1:
            return num
        elif num == 0:
            return num+1
        else:
            return num+9*(num-1)

def makeUrl(search, start_pg, end_pg):
    if start_pg == end_pg:
        start_page = makePgNum(start_pg)
        url = "https://search.naver.com/search.naver?where=news&query=" + search + "&start=" + str(start_page)
        return url
    else:
        urls = []
        for i in range(start_pg, end_pg + 1):
            page = makePgNum(i)
            url = "https://search.naver.com/search.naver?where=news&query=" + search + "&start=" + str(page)
            urls.append(url)
        return urls    
    
def makeList(newlist, content):
    for i in content:
        for j in i:
            newlist.append(j)
    return newlist

def news_attrs_crawler(articles,attrs):
    attrs_content=[]
    for i in articles:
        attrs_content.append(i.attrs[attrs])
    return attrs_content

def articles_crawler(url,headers):
    #html 불러오기
    original_html = requests.get(url,headers=headers)
    html = bs(original_html.text, "html.parser")

    url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
    url = news_attrs_crawler(url_naver,'href')
    return url

# iframe태그로 인해 본문을 못긁어오는 현상 발생.
# iframe태그에 명시된 blog url을 뽑아와서 blog로 바로 연결할 수 있도록 url조립
def delete_iframe(url): 
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status() # 문제시 프로그램 종료
    soup = bs(res.text, "html.parser") 

    src_url = "https://blog.naver.com/" + soup.iframe["src"]
    return src_url

# 수집한 블로그 링크를 하나씩 들어가서 본문을 긁어오는 함수 
def text_scraping(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    soup = bs(res.text, "html.parser") 

    # 본문이 담겨있는 태그 : se-main-container
    if soup.find("div", attrs={"class":"se-main-container"}):
        text = soup.find("div", attrs={"class":"se-main-container"}).get_text()
        text = text.replace("\n","") #공백 제거
        return text

    elif soup.find("div", attrs={"id":"postViewArea"}):
        text = soup.find("div", attrs={"id":"postViewArea"}).get_text()
        text = text.replace("\n","") 
        return text
    else:
        return "네이버 블로그는 맞지만, 확인불가"
    
# 블로그 링크로 마지막 이미지의 문장을 탐지한 결과를 불러오는 함수
def image_scraping(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    soup = bs(res.text, "html.parser") 
    
    img = soup.find_all('img', {'class' : ['se-sticker-image', 'se-image-resource']})

    try:
        res = request.urlopen(img[-1]["data-lazy-src"]).read()
        result_l = pytesseract.image_to_string(Image.open(BytesIO(res)), lang='kor+eng')
        return result_l
    except KeyError:
        res = request.urlopen(img[-1]["src"]).read()
        result_l = pytesseract.image_to_string(Image.open(BytesIO(res)), lang='kor+eng')
        return result_l
    except AttributeError:
        return ""
    except IndexError:
        return ""
    except Exception as e:    # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
        print('예외가 발생했습니다.', e)
        return ""
    
    

# image_scraping('https://blog.naver.com//PostView.naver?blogId=riberocjh&logNo=222955435979&redirect=Dlog&widgetTypeCall=true&directAccess=false')