import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import re

import json
import pickle
import urllib
import html
import numpy as np
from tqdm import tqdm
import urllib.request
import tensorflow as tf
from transformers import TFBertForSequenceClassification
from .crawling_func import *
from tensorflow_addons.optimizers import RectifiedAdam

# home/views.py '키워드 별 긍부정 분류 명세' 뉴스 크롤링 함수
def crawling_news_ksw(keyword:str):
    # API 사용을 위한 정보입력 
    client_id = 'wGaXs74pWvcYaDuk7Och'
    client_secret = 'jeFcJ451Ww'
    encText = urllib.parse.quote(keyword) 
    display_num = "20" # 최대 100
    url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=" + display_num

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        res_body = response.read() 
        res_body_json = json.loads(res_body)
    else:
        print("Error Code:" + rescode) 
        return pd.DataFrame({'title':[], 'text':[], 'link':[], 'cate':[]})

    print("<<-- 뉴스 크롤링 시작 -->>")

    items = res_body_json['items'] 
    links = []
    titles = []
    texts = []
        
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    cnt = 0
    for item in items:
         
        url = item['link']   
        
        if 'naver' in url:

            res = requests.get(url, headers=headers)
            if(res.status_code != 200):
                continue
        
            soup = bs(res.text, "html.parser") 
            news_html = soup.find_all('div','go_trans _article_content')
            
            text = ''
            for tag in news_html: # 카페 게시글
                text += tag.text + ' '
         
            if checking_ADword(text) == False:

                title = item['title']
                for i in range(len(item['title'])):
                    title = title.replace('<b>','')
                    title = title.replace('</b>','')
                    title = html.unescape(title)
                
                titles.append(title)
                texts.append(text)
                links.append(item['link'])
        
                cnt += 1
        
        if cnt == 5:
            break

    print("<<-- 뉴스 크롤링 종료 -->>")
    
    cate = 'news'
    cafe_df = pd.DataFrame({'title':titles, 'text':texts, 'link':links, 'cate':cate})
    return cafe_df

# 뉴스 크롤링
def crawling_news(keyword:str, begin:int,cnt:int) :

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}
    urls = makeUrl(keyword,begin,cnt)

    news_titles = []
    news_url =[]
    news_contents =[]

    for url in urls:
        news_url.append(articles_crawler(url,headers))

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

        if checking_ADword(content) == False:
            news_titles.append(title)
            news_contents.append(content)
        
    cate = 'news'
    news_df = pd.DataFrame({'title':news_titles,'link':final_urls,'text':news_contents, 'cate':cate})
    news_df = news_df.drop_duplicates(keep='first',ignore_index=True)
    return news_df

# 카페 크롤링
def crawling_cafe(keyword:str):
    # API 사용을 위한 정보입력 
    client_id = 'wGaXs74pWvcYaDuk7Och'
    client_secret = 'jeFcJ451Ww'
    encText = urllib.parse.quote(keyword) 
    display_num = "20" # 최대 100
    url = "https://openapi.naver.com/v1/search/cafearticle.json?query=" + encText + "&display=" + display_num

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200): 
        res_body = response.read() 
        res_body_json = json.loads(res_body) 
    else:
        print("Error Code:" + rescode)

    print("<<-- 카페 크롤링 시작 -->>")
    
    items = res_body_json['items']
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
        if(res.status_code != 200):
            continue
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

            for p in p_tags: 
                post += p.text + ' '
            
            if checking_ADword(post) == False:
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

# 블로그 크롤링
def crawling_blog(keyword:str):
    
    # API 사용을 위한 정보입력 
    client_id = 'wGaXs74pWvcYaDuk7Och'
    client_secret = 'jeFcJ451Ww'
    quote = keyword
    encText = urllib.parse.quote(quote) 
    display_num = "20" # 최대 100
    url = "https://openapi.naver.com/v1/search/blog?query=" + encText + "&display=" + display_num

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200): 
        res_body = response.read()
        res_body_json = json.loads(res_body) 

    else:
        print("Error Code:" + rescode)

    print("<<-- 블로그 크롤링 시작 -->>")

    items = res_body_json['items']
    links = []
    titles = []
    for i in range(int(display_num)):
        links.append(items[i]['link']) 
        titles.append(items[i]['title']) 
        
    # 제목 다듬기 (<b></b>태그 제거)
    for i in range(len(titles)):
        titles[i] = titles[i].replace('<b>','')
        titles[i] = titles[i].replace('</b>','')

    # 조립된 블로그 링크들을 담는 리스트
    blog_links = []
    # 각 블로그들의 본문들을 담는 리스트
    contents = []
    # 블로그의 이미지 문장을 담는 리스트
    images = []
    # 블로그의 제목을 담는 리스트
    titles_for_df = []

    for j in range(len(links)):
        url = delete_iframe(links[j])
        text = text_scraping(url)
         
        if checking_ADword(text) == True:
            continue
        
        img_txt = image_scraping(url)
        
        if ad_words_filtering(img_txt) == True:
            continue
        
        blog_links.append(url)
        contents.append(text)
        images.append(img_txt)
        titles_for_df.append(titles[j])

    print("<<-- 블로그 크롤링 끝 -->>") 

    cate = 'blog'

    blog_df = pd.DataFrame({'title':titles_for_df, 'text':contents, 'link':blog_links, 'img':images, 'cate':cate})
    return blog_df

# 광고단어 체크함수 시작
def checking_ADword(data):

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

    return ad_word_detected

# 이미지 속 광고 단어 체크 함수
def ad_words_filtering(stc):

    ad_word_detected = False
    ad_words = ['지원', '원고', '원고료', '제공', '파트너스', '활동', '업체', '브랜드',
                '제작비', '수수료', '지급', '제품', '수수', '고료']
  
    for i in range(len(ad_words)):
        if ad_words[i] in stc:
            ad_word_detected = True
            break

    return ad_word_detected

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
            if len(cafe_df) == 0 :
                break
            cafe_text_lst = cafe_df['text'].to_list()
            break
        except:
            continue

    # 데이터 개수 체크
    print(f'blog\n:{len(blog_df)}\n')
    print(f'cafe\n:{len(cafe_df)}')
    print("crawling done..!")

    return blog_df, cafe_df

model = tf.keras.models.load_model('functions/best_model_RAdam.h5', 
                                   custom_objects = {'RectifiedAdam' : RectifiedAdam, 
                                                     'TFBertForSequenceClassification': TFBertForSequenceClassification})
with open('functions/tokenizer_RADAM.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

MAX_SEQ_LEN = 500

def convert_data(df):
    # BERT 입력으로 들어가는 token, mask, segment 저장용 리스트
    tokens, masks, segments = [], [], []
    
    if len(df) != 0 :
        for X in df['text']: # test용 데이터가 'data' > 'text'로 변경
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
    
    return 0

# 키워드별 긍부정 예측 및 분류 함수
def predict_pos_neg(key1, key2) :
    cd_key1 = convert_data(key1)
    cd_key2 = convert_data(key2)
    
    if cd_key1 != 0 : 
        
        predicted_value = model.predict(cd_key1)
        predicted_label = np.argmax(predicted_value, axis = 1)
        key1['label'] = predicted_label
        
        key1_df_pos = key1[key1['label'] == 0].drop(columns = 'label')
        key1_df_neg = key1[key1['label'] == 1].drop(columns = 'label')

        keyword1_positive = key1_df_pos.to_dict('records')
        keyword1_negative = key1_df_neg.to_dict('records')
    
    else :
        keyword1_positive = []
        keyword1_negative = []

    if cd_key2 != 0 :
        
        predicted_value = model.predict(cd_key2)
        predicted_label = np.argmax(predicted_value, axis = 1)
        key2['label'] = predicted_label
        
        key2_df_pos = key2[key2['label'] == 0].drop(columns = 'label')
        key2_df_neg = key2[key2['label'] == 1].drop(columns = 'label')

        keyword2_positive = key2_df_pos.to_dict('records')
        keyword2_negative = key2_df_neg.to_dict('records')
        
    else :
        keyword2_positive = []
        keyword2_negative = []
    
    return keyword1_positive, keyword1_negative, keyword2_positive, keyword2_negative
