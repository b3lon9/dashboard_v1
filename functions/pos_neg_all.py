import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import re
import easyocr
import sys
import os
import json
import pickle
import urllib
import pytesseract
from urllib import request
from PIL import Image
from io import BytesIO
import numpy as np
from tqdm import tqdm
import urllib.request
import tensorflow as tf
from transformers import BertTokenizer, TFBertForSequenceClassification

def crawling_news(keyword:str, begin:int,cnt:int) :
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

    def news_attrs_crawler(articles,attrs):
        attrs_content=[]
        for i in articles:
            attrs_content.append(i.attrs[attrs])
        return attrs_content

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

    def articles_crawler(url):
        #html 불러오기
        original_html = requests.get(i,headers=headers)
        html = bs(original_html.text, "html.parser")

        url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
        url = news_attrs_crawler(url_naver,'href')
        return url

    url = makeUrl(keyword,begin,cnt)

    news_titles = []
    news_url =[]
    news_contents =[]

    for i in url:
        url = articles_crawler(url)
        news_url.append(url)

    def makeList(newlist, content):
        for i in content:
            for j in i:
                newlist.append(j)
        return newlist

    news_url_1 = []

    makeList(news_url_1,news_url)

    final_urls = []
    for i in range(len(news_url_1)):
        if "news.naver.com" in news_url_1[i]:
            final_urls.append(news_url_1[i])
        else:
            pass

    for i in final_urls:
        news = requests.get(i,headers=headers)
        news_html = bs(news.text,"html.parser")

        title = news_html.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
        if title == None:
            title = news_html.select_one("#content > div.end_ct > div > h2")

        content = news_html.select("div#dic_area")
        if content == []:
            content = news_html.select("#articeBody")

        content = ''.join(str(content))

        pattern1 = '<[^>]*>'
        title = re.sub(pattern=pattern1, repl='', string=str(title))
        content = re.sub(pattern=pattern1, repl='', string=content)
        pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
        content = content.replace(pattern2, '')

        news_titles.append(title)
        news_contents.append(content)
        
    cate = 'news'
    news_df = pd.DataFrame({'title':news_titles,'link':final_urls,'text':news_contents, 'cate':cate})
    news_df = news_df.drop_duplicates(keep='first',ignore_index=True)
    
    return news_df

def crawling_cafe(keyword:str):
    #정보입력 
    client_id = 'wGaXs74pWvcYaDuk7Och' # 발급받은 id 입력
    client_secret = 'jeFcJ451Ww' # 발급받은 secret 입력 
    encText = urllib.parse.quote(keyword) 
    display_num = "5" # 최대 100
    url = "https://openapi.naver.com/v1/search/cafearticle.json?query=" + encText + "&display=" + display_num # json 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200): # 잘 응답하면..
        res_body = response.read() # 읽고 받아와서
        res_body_json = json.loads(res_body) # res_body_json에 저장함
        # print(type(res_body_json)) # ..확인용..
    else:
        print("Error Code:" + rescode) # 응답안하면 에러코드 출력
        # return pd.DataFrame({'title':[], 'text':[], 'link':[], 'cate':[]})

    print("<<-- 카페 크롤링 시작 -->>")
    items = res_body_json['items'] # json파일 내부에 item를 뽑아서 items변수에 저장

    links = []
    titles = []
    text = []
        
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

    for item in items:

        url = item['link']   
        title = item['title']
        
        title = title.replace('<b>','')
        title = title.replace('</b>','')
        
        res = requests.get(url, headers=headers)
        res.raise_for_status() # 문제시 프로그램 종료
        soup = bs(res.text, "html.parser") 


        cafe_html = soup.find('script').text
        var_index = cafe_html.find('g_sClubId')
        semi_index = cafe_html.find(';',var_index)

        no_cloud = cafe_html[var_index:semi_index]
        no_cloud = no_cloud[no_cloud.find('"')+1:-1]

        no_post = url[url.rfind('/')+1:]

        articles_path = f'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/{no_cloud}/articles/{no_post}'

        articles_response = requests.get(articles_path,headers=headers)
        
        if(articles_response.status_code == 200):
            articles_json_object = json.loads(articles_response.text)
            html = articles_json_object['result']['article']['contentHtml']
            
            
            soup = bs(html, "html.parser")

            p_tags = soup.find_all('p','se-text-paragraph')

            post = ''

            for p in p_tags: # 카페 게시글
                post += p.text + ' '

            text.append(post)
            links.append(url)
            titles.append(title)
        else:
            articles_json_object = json.loads(articles_response.text)
            print(articles_json_object['result']['reason'])

    print("<<-- 카페 크롤링 종료 -->>")
    
    cate = 'cafe'
    cafe_df = pd.DataFrame({'title':titles, 'text':text, 'link':links, 'cate':cate})
    
    return cafe_df

def crawling_blog(keyword:str):
    
    #정보입력 
    client_id = 'wGaXs74pWvcYaDuk7Och' # 발급받은 id 입력
    client_secret = 'jeFcJ451Ww' # 발급받은 secret 입력 
    quote = keyword # 검색어 입력
    encText = urllib.parse.quote(quote) 
    display_num = "5" # 최대 100
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=" + display_num # json 결과

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200): # 잘 응답하면..
        res_body = response.read() # 읽고 받아와서
        res_body_json = json.loads(res_body) # res_body_json에 저장함
        # print(type(res_body_json)) # ..확인용..

    else:
        print("Error Code:" + rescode) # 응답안하면 에러코드 출력

    print("<<-- 블로그 크롤링 시작 -->>")
    items = res_body_json['items'] # json파일 내부에 item를 뽑아서 items변수에 저장

    links = []
    titles = []
    for i in range(int(display_num)):
        links.append(items[i]['link']) # 링크 하나씩 저장
        titles.append(items[i]['title']) # 제목 하나씩 저장

    # 제목 다듬기 (<b></b>태그 제거)
    for i in range(len(titles)):
        titles[i] = titles[i].replace('<b>','')
        titles[i] = titles[i].replace('</b>','')

    # iframe태그로 인해 본문을 못긁어오는 현상 발생.
    # iframe태그에 명시된 blog url을 뽑아와서 blog로 바로 연결할 수 있도록 url조립
    def delete_iframe(url): 
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
        res = requests.get(url, headers=headers)
        res.raise_for_status() # 문제시 프로그램 종료
        soup = bs(res.text, "html.parser") 

        src_url = "https://blog.naver.com/" + soup.iframe["src"]
        return src_url

    # 조립된 블로그 링크들을 담는 리스트
    blog_links = []

    for j in range(len(links)):
        blog_links.append(delete_iframe(links[j]))

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

    # 각 블로그들의 본문들을 담는 리스트
    contents = []
    
    # 블로그의 이미지 문장을 담는 리스트
    images = []
    
    for o in range(len(blog_links)):
        contents.append(text_scraping(blog_links[o]))
        images.append(image_scraping(blog_links[o]))
        # print(contents[o])

    print("<<-- 블로그 크롤링 끝 -->>") 

    cate = 'blog'

    blog_df = pd.DataFrame({'title':titles, 'text':contents, 'link':blog_links, 'img':images, 'cate':cate})
    
    return blog_df

### 광고단어 체크함수 시작 ###
def checking_ADword(data, x):

    ad_word_detected = False

    word_list = ['성지' , '원고료' , '소정의' , '유플러스로부터', 'SKT로부터',
                '본 포스팅은' , '본 콘텐츠는', '이 포스팅은' , '이 콘텐츠는',
                '제공받아비대면상담' , '최대만족' , '약속드리는' , '금전적 보상',
                '금전적 지원' , '제작비 지원' , '제작비 협찬' , '무료 제공',
                '무료 지원' , '무료 대여' , '할인 지원' , '할인혜택 제공',
                '할인권 지원' , '적립금 지급' , '금전적 지원' , '포인트 지급',
                '전속 모델' , '모델 활동비 지급' , '수익 일부 지급' , '수익 배분',
                '공동구매' , '판매수익의 일부 지급' , '광고비 지급', '수수료 지급'
                '쿠팡 파트너스' , '제공 받습니다' , '일정액의' , '상담받아보세요' , '눌러보기',
                '상담해드리겠습니다' , '카톡문의' ,'지원받아' , '다나와 체험단' , '문의해주세요',
                '경제적 대가' , '유료 광고' , '대가성 광고' , '협찬', '대여받았습니다' , '상업광고',
                ]
    for j in range(len(word_list)):
        if word_list[j] in data:
            ad_word_detected = True
            break

    if ad_word_detected==True:
        return x

# 이미지 속 광고 단어 체크 함수
def ad_words_filtering(stc, x):
    
    ad_word_detected = False
    
    ad_words = ['지원', '원고', '원고료', '제공', '파트너스', '활동', '업체', '브랜드',
                '제작비', '수수료', '지급', '제품', '수수', '고료']
  
    for i in range(len(ad_words)):
        if ad_words[i] in stc:
            ad_word_detected = True
            break

    if ad_word_detected==True:
        return x



### 메인함수 시작 ###
### 메인함수 시작 ###
def AD_filtering(keyword):

    # 블로그 크롤링
    while(True):
        try:
            blog_df = crawling_blog(keyword)
            blog_text_lst = blog_df['text'].to_list()
            break
        except:
            continue

    # 카페 크롤링
    while(True):
        try:
            cafe_df = crawling_cafe(keyword)
            cafe_text_lst = cafe_df['text'].to_list()
            break
        except:
            continue

    # 데이터 개수 체크
    print(f'blog\n:{len(blog_df)}\n')
    print(f'cafe\n:{len(cafe_df)}')
    print("crawling done..!")

    # # 카페/블로그 df에서 'text'(본문)만 뽑아서 리스트화
    # blog_text_lst = blog_df['text'].to_list()
    # cafe_text_lst = cafe_df['text'].to_list()
       
    # filtering ad - blog
    blog_rmv_target = []
    for x in range(len(blog_df)):
        blog_rmv_target.append(checking_ADword(blog_text_lst[x], x))

    # filtering ad - cafe
    cafe_rmv_target = []
    for x in range(len(cafe_df)):
        cafe_rmv_target.append(checking_ADword(cafe_text_lst[x], x))
 
    # None값 제거
    blog_rmv_target = [i for i in blog_rmv_target if i is not None]
    cafe_rmv_target = [i for i in cafe_rmv_target if i is not None]

    # 인덱스값으로 광고글 제거
    for i in range(len(blog_rmv_target)):
        blog_df.drop(blog_rmv_target[i], axis=0, inplace=True)

    for i in range(len(cafe_rmv_target)):
        cafe_df.drop(cafe_rmv_target[i], axis=0, inplace=True)
        
    # 블로그 df에서 'img'만 뽑아서 리스트화
    blog_img_lst = blog_df['img'].to_list()
    
    # image ad filtering
    blog_rmv_target_img = []
    for x in range(len(blog_df)):
        blog_rmv_target_img.append(ad_words_filtering(blog_img_lst[x], x))
        
    blog_rmv_target_img = [i for i in blog_rmv_target_img if i is not None]
    print('img로 rmv할 갯수 : ', len(blog_rmv_target_img))
    
    for i in range(len(blog_rmv_target_img)):
        blog_df.drop(blog_rmv_target_img[i], axis=0, inplace=True)

    # 인덱스 초기화로 정리
    blog_df.reset_index(drop=True, inplace=True)
    cafe_df.reset_index(drop=True, inplace=True)

    return blog_df, cafe_df

model = tf.keras.models.load_model('functions/best_model_adam.h5',
                                        custom_objects={'TFBertForSequenceClassification': TFBertForSequenceClassification})
with open('functions/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

MAX_SEQ_LEN = 500

def convert_data(df):
    # BERT 입력으로 들어가는 token, mask, segment, target 저장용 리스트
    tokens, masks, segments = [], [], []
    
    for X in df['text']: # text로 바꿔야함! -> test용 데이터가 'data'이기 때문
        # token: 입력 문장 토큰화
        token = tokenizer.encode(X, truncation = True, padding = 'max_length', max_length = MAX_SEQ_LEN)
        
        # Mask: 토큰화한 문장 내 패딩이 아닌 경우 1, 패딩인 경우 0으로 초기화
        num_zeros = token.count(0)
        mask = [1] * (MAX_SEQ_LEN - num_zeros) + [0] * num_zeros
        
        # segment: 문장 전후관계 구분: 오직 한 문장이므로 모두 0으로 초기화
        segment = [0]*MAX_SEQ_LEN

        tokens.append(token)
        masks.append(mask)
        segments.append(segment)

    # numpy array로 저장
    tokens = np.array(tokens)
    masks = np.array(masks)
    segments = np.array(segments)

    return [tokens, masks, segments]

def predict_pos_neg(key1, key2) :
    
    predicted_value = model.predict(convert_data(key1))
    predicted_label = np.argmax(predicted_value, axis = 1)
    key1['label'] = predicted_label

    predicted_value = model.predict(convert_data(key2))
    predicted_label = np.argmax(predicted_value, axis = 1)
    key2['label'] = predicted_label

    key1_df_pos = key1[key1['label'] == 0].drop(columns = 'label')
    key1_df_neg = key1[key1['label'] == 1].drop(columns = 'label')

    keyword1_positive = key1_df_pos.to_dict('records')
    keyword1_negative = key1_df_neg.to_dict('records')
    
    key2_df_pos = key2[key2['label'] == 0].drop(columns = 'label')
    key2_df_neg = key2[key2['label'] == 1].drop(columns = 'label')

    keyword2_positive = key2_df_pos.to_dict('records')
    keyword2_negative = key2_df_neg.to_dict('records')
    
    return keyword1_positive, keyword1_negative, keyword2_positive, keyword2_negative

# n1, n2, n3, n4 = predict_pos_neg(crawling_news('아이폰14프로맥스', 1, 2), crawling_news('아이폰se', 1, 2))

# key1_b, key1_c = AD_filtering('아이폰14프로맥스')
key2_b, key2_c = AD_filtering('아이폰se')

# c1, c2, c3, c4 = predict_pos_neg(key1_c, key2_c)
# b1, b2, b3, b4 = predict_pos_neg(key1_b, key2_b)

# keyword1_positive, keyword1_negative, keyword2_positive, keyword2_negative = n1+c1+b1, n2+c2+b2, n3+c3+b3, n4+c4+b4

# print(keyword1_positive)
# print('------------------------------------------------------------------------')
# print(keyword1_negative)
# print('------------------------------------------------------------------------')
# print(keyword2_positive)
# print('------------------------------------------------------------------------')
# print(keyword2_negative)
# print('------------------------------------------------------------------------')