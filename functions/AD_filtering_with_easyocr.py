### easyocr 사용을 위해서 ###
# pip install easyocr
# pip install git+https://github.com/JaidedAI/EasyOCR.git

from bs4 import BeautifulSoup as bs
import pandas as pd
import urllib.request
import urllib
import requests
import json
import easyocr


### 블로그 크롤링 시작 ###
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

    print("\n<<-- 블로그 크롤링 시작 -->>\n")
    
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
        soup = bs(res.text, "lxml") 

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
        print('check')    
    # 블로그 링크로 마지막 이미지의 문장을 탐지한 결과를 불러오는 함수
    def image_scraping(url):
        reader = easyocr.Reader(['ko','en'], gpu=True)
        
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
        res = requests.get(url, headers=headers)
        soup = bs(res.text, "lxml") 
        
        img = soup.find_all('img', {'class' : ['se-sticker-image', 'se-image-resource']})

        try:
            result_l = reader.readtext(img[-1]["data-lazy-src"], detail=0)
            return "".join(result_l)
        except KeyError:
            result_l = reader.readtext(img[-1]["src"], detail=0)
            return "".join(result_l)
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

    print("\n<<-- 블로그 크롤링 끝 -->>\n") 

    cate = 'blog'
    
    blog_df = pd.DataFrame({'title':titles, 'text':contents, 'link':blog_links, 'img':images, 'cate':cate})
    
    return blog_df


### 카페 크롤링 시작 ###
def crawling_cafe(begin:int,cnt:int, keyword:str):
    print("\n<<-- 카페 크롤링 시작 -->>\n") 
    try:
        err_urls = []
        result_list = []
        cafe_links = []
        titles = []
        idx_lst = []
        idx = -1

        for i in range(cnt):
            start = i * 10 + begin
            quote = keyword # 검색어 입력
            encText = urllib.parse.quote(quote) 
            path = f'https://s.search.naver.com/p/cafe/search.naver?where=article&ie=utf8&query={encText}&prdtype=0&t=0&st=rel&srchby=text&dup_remove=1&cafe_url=&without_cafe_url=&sm=tab_opt&nso_open=0&rev=44&abuse=0&ac=0&aq=0&converted=0&is_dst=0&nlu_query=%7B%22r_category%22%3A%2230%22%7D&nqx_context=&nx_and_query=&nx_search_hlquery=&nx_search_query=&nx_sub_query=&people_sql=0&spq=0&x_tab_article=&is_person=0&start={start}&display=10&prmore=1&_callback=viewMoreContents'
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
            response = requests.get(path, headers=headers)
            
            command_len = len("'viewMoreContents(")
            response_string = response.text[command_len:-2]
            json_object = json.loads(response_string)
            
            soup = bs(json_object['html'], "html.parser")
            elements = soup.find_all('a','api_txt_lines total_tit')        
                            
            for elem in elements: # 검색된 카페 게시글들

                idx+=1

                url = elem.attrs['href'][:elem.attrs['href'].find('?')]
                cafe_links.append(url)
                cafe_response = requests.get(url)

                cafe_soup = bs(cafe_response.text, "html.parser")  
                cafe_html = cafe_soup.find('script').text
            
                var_index = cafe_html.find('g_sClubId')
                semi_index = cafe_html.find(';',var_index)               
                
                no_cloud = cafe_html[var_index:semi_index]
                no_cloud = no_cloud[no_cloud.find('"')+1:-1]
                no_post = url[url.rfind('/')+1:]
                
                articles_path = f'https://apis.naver.com/cafe-web/cafe-articleapi/v2/cafes/{no_cloud}/articles/{no_post}?useCafeId=true&requestFrom=A'

                articles_response = requests.get(articles_path)
                articles_json_object = json.loads(articles_response.text)

                # 본문에 접근을 못하는 경우
                if 'errorCode' in articles_json_object['result']:
                    err_urls.append(url) # err_url에 추가
                    result_list.append('') # 데이터 개수를 맞추기 위해 내용 데이터에 공백추가
                    titles.append('') # 데이터 개수를 맞추기 위해 제목 데이터에 공백추가
                    idx_lst.append(idx) # 없는데이터 행을 제거하기위한 인덱스값 확보
                    continue 

                titles.append(articles_json_object['result']['article']['subject'])
                
                html = articles_json_object['result']['article']['contentHtml']
                soup = bs(html, "html.parser")
                
                p_tags = soup.find_all('p','se-text-paragraph se-text-paragraph-align-')
                
                post = ''
                
                for p in p_tags: # 카페 게시글
                    post += p.text + ' '
                
                if len(post)<10:
                    result_list.append('') # 데이터 개수를 맞추기 위해 내용 데이터에 공백추가
                    idx_lst.append(idx) # 없는데이터 행을 제거하기위한 인덱스값 확보
                    continue 
                    
                result_list.append(post)

        cate = 'cafe'
        cafe_df = pd.DataFrame({'title':titles, 'text':result_list, 'link':cafe_links, 'cate':cate})

        for i in range(len(idx_lst)):
            cafe_df.drop(idx_lst[i], axis=0, inplace=True)
        cafe_df.reset_index(drop=True, inplace=True)

        print("\n<<-- 카페 크롤링 끝 -->>\n") 
                
        return cafe_df
                    
    except requests.exceptions.Timeout as errd:
        print("Timeout Error : ", errd)
    
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting : ", errc)
        
    except requests.exceptions.HTTPError as errb:
        print("Http Error : ", errb)

    # Any Error except upper exception
    except requests.exceptions.RequestException as erra:
        print("AnyException : ", erra)
    
    

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
    # + 블로그 df에서 'text'(본문)만 뽑아서 리스트화
    while(True):
        try:
            blog_df = crawling_blog(keyword)
            blog_text_lst = blog_df['text'].to_list()
            break
        except:
            continue

    # 카페 크롤링
    # + 카페 df에서 'text'(본문)만 뽑아서 리스트화
    while(True):
        try:
            cafe_df = crawling_cafe(1,2,keyword)
            cafe_text_lst = cafe_df['text'].to_list()
            break
        except:
            continue

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


# 실행 예시
# blog_df, cafe_df = AD_filtering('keyword')
blog_df, cafe_df = AD_filtering('s22')

print(blog_df)
print(cafe_df)