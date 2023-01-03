from eunjeon import Mecab 
from collections import Counter
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import datetime
import json
import requests
import re

# Mecab = Mecab(dicpath=r"C:/mecab/mecab-ko-dic")
Mecab = Mecab()

## 토큰화 및 불용어 처리 ##
def text_preprocessing(text:str):

  # 한글/영어만 남기고 제거
  txt = re.sub('[^가-힣a-z]', ' ', text)
  token = Mecab.nouns(txt)

  # 불용어 정의
  stopwords = ['원','정도','개','검증','것','다음','하루','탱이','겨자','배송','텍','도착','확인','조립','생각','대비','하나','박스',
               '비닐','미개','장착','물건','생산','판매','만','설치','할인','주문','테스트','모니터','화질','필요','발송','본체',
               '만큼','부분','투명','결과','시리얼','넘버','일','택배','옥션','께','소개','기분','데','최저','여기','이마트','걸로',
               '아이','마음','수령','조립도','기본','부탁','세일','쿠폰','샤','하락','최근','처제','구동','보조','내요','브랜드','인증',
               '시험','특별','문의','중고','리퍼','일자','달','년','광복절','연휴','취소','염려','자분','처리','날짜','파스','타임',
               '스파이','때','키보드','마스터','우리','고딩','아들','아빠','공부','시간','인강','주말','보충','학원','강의','엘든',
               '실행','텍스','질감','만일','이것저것','캐쉬','제고','전화','인','완전','파이어','스트라이크','통과','재품','일치','기계',
               '개월','이것','절반','비교','사이트','판매자','개당','차액','공짜','상식','수년','컴','최저가','봉인','사이','송사',
               '선택','평상시','방어','화면','조금','대부분','총알','토막','지장','전','스크린','용도','반응','개인','적용','주전',
               '초반','조명','급','피','막눈','실사','사진','생명','가지','중학생','이용','공식','신경','파손','백만','포인트','개꿀',
               '시국','고급','생일','방법','대로','흔적','처음','최신','시리즈','조카','흰색','아가','수','뽁','와이프','밀봉','거',
               '자막','이눔','한진','나','방문','자리','차지','미','게','며칠','삥','안벽','특가','입니다','부자','이틀','갑사','전이',
               '카','틈','히','검색','기장','친절','기존','맛','둘','도','대','놈','값','날','습','렴','밖','맘','쳐','월','번가','리',
               '여러분','짜리','주일','대신','쉐','겉','처','장사','진자','구','성품','별','여긴','봉투','차','기사','나중','번','이게',
               '처분','건데','주관','의견','소지','등록','게시','제한','로젠','목요일','예정','완료','작성','수정','고문','정신','건지',
               '묶음','과정','누락','경우','연락','장난아','돌고래','헤드폰','얘기','내','이름','홈페이지','은','사람','직후','질문',
               '메뉴','비늘','회사','자체','폼','럽','부','얼','속','십','답','백','이번','엠','리뷰','이벤트','때문','콘센트','듯','사망',
               '실제','국민','글','추가','글자','팩토리','참고','환경','속도','유지','연결','지직','수고','배','이거','부품','교환','발생',
               '전체','프로','코드','고려','택','결제','오전','네이버','벡','단독','스위치','밑','보유','스팀','에서','중','오후','재고',
               '소문','일반','당일','인식','옆면','한몫','첨부','쿨링','비면','당시','지연','이임','기준','로스트','아크','업데이트','패드',
               '신청','체험','지수','항목','귀','기타','스피커','헤드셋','음량','물품','구멍','랍','앞','종류','고등학생','아래','최대',
               '라인','이하','로드','알트','등','구비','만대','최소','아이비','브릿지','하드','문후','오랫동안','일정','앤썸','거기','전날',
               '크기','마이크','닉스','퀘이사','아침','색깔','다나와','갈','자금','길비','틈새','후','별개','지금','완충','따름','네모',
               '아참','원부','마크','어디','담날','애','문구','마우스','선착순','마감','도움','유튜브','판넬','제로','건','아토','끝판',
               '소비자','껀','지급','가능','아무','옆','불빛','마개','가유','플','소식','창원','려고','업','무튼','도배','변경','후반',
               '보고','대체','문안','현역','활동','국내','바람','연구실','시전','매진','낭','상담','직원','개봉','동해','백두산','하느님',
               '보우','나라','만세','무궁화','삼천리','화려','강산','대한','보전','보장','보통','시문','제업','당신','세계','토요일',
               '화요일','곳','비프','음도','이랑','불가','통운','스마일','데이','절차','월요일','요설','응모','모던','어페어','로고','달째',
               '능력','아영','세상','에어','당장','에이에스','템','남편','입','이야기','키트','동보','용검','사리','네영','씨','버전','송시',
               '텐데','금요일','책상','그','풀','시','존','운','딘','길','여','침','슈팅','가전','겁니다','쇼킹','일시불','가전제품','드라이',
               '조차','그분','한마디','동안','동네','쿠팡','욜','이후','뭘까요','보단','오늘','출발','문','사용','센터','고객','닷컴','사전',
               '서비스','별도','관련','혜택','준비','중간','담당','답변','접수','수요일','예전','크레','무이자','싸이트','해당','사업',
               '상담원','사항','안내','자기','이제','내용','후기','번호','퇴근','공지','이해','진행','해결','계기','대처','사후','대기',
               '통신사','수신','상태','대응','제휴','카드','보험','상품권','옵션','부서','전회','위','꺼','원론','잘못','팀장','인양','욕심',
               '명예훼손','책임','태도','말투','공유','진심','오케이','반차','시작','이건','겨울','야외','효율','소요','노트','사과','휴가',
               '타사','요청','대우','회피','다이렉트','핑계','거짓말','일상','최종','거지','립니','중순','식','비용','운반','기름','인건비',
               '오염','사은품','광고','마지막','모델','색감','돌리지','영향','투','케이스','소모품','지속','수리','아내','수강','하루하루',
               '회수','거립니다','배신감','화','포함','상술','출고','지시','디스','인정','적정','정보','해결책','소스','누출','말','파악',
               '품절','재입','의미','베이퍼','의혹','해명','입장','요번','트레이드','누구','명시','안','약간','배송지','첫마디','물류','작업',
               '노력','기입','연락처','기록','현혹','스','검사','유리판','저것','알콜','스티커','일부','항의','검사원','수거','이젠','억지',
               '계절','조언','순식간','존재','소모','목금','일월','업무','지도','설명','인상','사양','영상','예정일','카톡','일전','공홈',
               '물량','부족','약정','현관','메시지','사용료','요금제','삼성카드','청구','인도','도로','믿음','사와','소통','장상태','가심',
               '거실','쇼파','문한','상자','비고','수준','까지','사옹','년차','그때','뭔지','좌파','집권','불행','계양','아치','개념','인간',
               '사회','잡음','합리','방안','신뢰','조회','실수','문자','줄','저','시점','고민','지역','별거','느낌','개통','이타','동봉',
               '뭐','컨','솜','네','과','밍','밤','푀','이전','이상','결정','얼마','제외','차이','이유','직전','계정','기간','어버이날','선호',
               '기회','이중','점','일요일','저녁','분실','무엇','동일','경험','배경','커버','알뜰','전용','기업','컬러','아버님','참여','아기',
               '손','남자','어머니','젤리','발견','주사','자료','화이팅','엄마','로그인','시중','영어','사용법','제기','그날','비치','부재중',
               '주식','뱅킹','보람','요즘','여지','주변','검정','건가요','스타일','등등','오랫만','가구','근무','약분','관비','메세지','기재',
               '복귀','레일','예상','와치','동영상','효과','애용','행복','스탠딩','가량','헤르츠','헤비','여름','와트','체감','가족','쓰레기',
               '그것','고가품','보관','저희','주택','대만','전부','가이드','기포','건가','딸아이','종일','운영','케어','바지','주머니','올해',
               '월이','기변','산지','신랑','안심','해외','평생','뭔가','나름','해택','플로','파일','단말기','이동','동생','중고품','거래','대면',
               '사무실','자동차','사유','저조','노출','셔터','초','출시','와중','발표','마이','플랜','취향','수화','티','자판','오타','칩','매장',
               '감안','한국어','설명서','전공','본인','오픈','상황','제','안정','편안','추후','평가','폭풍','타이밍','싸움','품목','현재','국제',
               '안감','급성장','우롱','걸까요','어려움','위치','대리점','전달','앞면','은색','산란','근대','꼼꼼이','미지급','활용','그림자',
               '지우기','반사','전문가','맨몸','결론','팬텀','주간','최악','케이','판매처','무료','뷰','취급','가관','위험','순조','한참','버튼',
               '익일','시인','각종','소모량','차후','측','집안','컴퓨터','열일','사랑','응원','짐','햇볕','주위','아래쪽','가로','답글','일후',
               '여닫이','형태','투리','부위','성만','요구','수용','영업','이익','진짜','사야','산','사니','가입','근접','물체','외각','커싱',
               '본격','함정','길이','초고','속충','선도','클릭','보상금','대한민국','중국','중소기업','라이트','전반','모서리','이걸로','장바구니',
               '쇼핑백','로','제품군','주','고요','나머지','가게','매료','마켓','어머님','군데','인등','인물사진','금','재주','상하좌우','주의',
               '돌','패턴','위주','미니','뭘','맞춤','인과','팟','버스','쇼핑','누가','박싱','단자','빅','사기전','사기','여유','종이','가방',
               '장기간','여행','싸이','플랫','한수','버즈','약속','베이비핑크','김','클락','실화','친구','변동','굴뚝','핸들링','아이콘','키패드',
               '리트','일상생활','결국','커플','대안','명성','공인','증서','자연','적립','성어','납부','내기','여자','보정','건데요','이프',
               '정성','삼중','아버지','장만','유리','정부','개고생','날개','양보','기념','보급','공시','지원금','폰트','트릴','조심','여기저기',
               '오랜만','송문','캡','우체국','요','손안','성지','청','신','조월','기도','물감','방울','대접','체제','목적','치안','봉새','미련',
               '핑','장소','유트','여니','응답','깃털','동종','시도','사인','바요','지향','은근','새벽','점심','구성','프라자','오른쪽','왼쪽','저장',
               '즈','적','띠','갤','적','띠','갤','짱']

  # 필터링
  token = [t for t in token if t not in stopwords]

  # 한글자인 토큰 제거
  for i,v in enumerate(token):
    if len(v)<2:
        del token[i]

  return token


### 데이터 크롤링 ###
def crawling_rating_data(keyword:str):
  rating_df = pd.DataFrame(columns=['리뷰','별점'])
  review_list, star_list = [],[]
  
  url = 'https://search.danawa.com/dsearch.php?query=' + keyword
  headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
  res = requests.get(url, headers=headers)
  
  soup = BeautifulSoup(res.text, 'html.parser')
  prod_list = soup.find_all('a', 'click_log_product_standard_title_')
  prod_link = prod_list[0]['href']
  pcode_index = prod_link.find('pcode')
  pcode = prod_link[pcode_index+6:pcode_index+14]
  
  for page in range(1,20):
    url = 'https://prod.danawa.com/info/dpg/ajax/companyProductReview.ajax.php?prodCode=' + pcode + '&page={}&limit=10&score=0&sortType=&onlyPhotoReview=&usefullScore=Y&innerKeyword=&subjectWord=0&subjectWordString=&subjectSimilarWordString='.format(page)
    headers = {'referer':'https://prod.danawa.com/info/?pcode=' + pcode,
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)
    
    # soup 객체 만들기
    soup = BeautifulSoup(res.text, "html.parser")
    reviews = soup.find_all('div', 'atc')
    stars = soup.find_all('span', 'star_mask')

    for rs in zip(reviews, stars[5:]):
      review_list.append(rs[0].text)
      star_list.append(rs[1].text)

  # df 생성 및 반환
  rating_df = pd.DataFrame({'리뷰':review_list, '별점':star_list})
  return rating_df



### 메인함수 시작 ###
### 메인함수 시작 ###
def starRating_classisification(keyword1:str, keyword2:str):

  # 크롤링으로 받아오는 데이터 => {'리뷰', '별점'}
  # 검색어에 대한 크롤링 진행 후 데이터프레임(df_A, df_B) 생성
  df_A = crawling_rating_data(keyword1)
  df_B = crawling_rating_data(keyword2)

  # 별점데이터 1~5 점으로 변경
  df_A.replace({'20점':1,"40점":2,"60점":3,"80점":4,"100점":5}, inplace=True)
  df_B.replace({'20점':1,"40점":2,"60점":3,"80점":4,"100점":5}, inplace=True)

  # 별점별 리뷰만 저장 및 인덱스 리셋
  df_A_1 = df_A[df_A['별점']==1]['리뷰'].reset_index(drop=True)
  df_A_2 = df_A[df_A['별점']==2]['리뷰'].reset_index(drop=True)
  df_A_3 = df_A[df_A['별점']==3]['리뷰'].reset_index(drop=True)
  df_A_4 = df_A[df_A['별점']==4]['리뷰'].reset_index(drop=True)
  df_A_5 = df_A[df_A['별점']==5]['리뷰'].reset_index(drop=True)

  df_B_1 = df_B[df_B['별점']==1]['리뷰'].reset_index(drop=True)
  df_B_2 = df_B[df_B['별점']==2]['리뷰'].reset_index(drop=True)
  df_B_3 = df_B[df_B['별점']==3]['리뷰'].reset_index(drop=True)
  df_B_4 = df_B[df_B['별점']==4]['리뷰'].reset_index(drop=True)
  df_B_5 = df_B[df_B['별점']==5]['리뷰'].reset_index(drop=True)

  # 파이차트를 위한 평점별 개수 수집
  keyword1_pie = [len(i) for i in [df_A_1, df_A_2, df_A_3, df_A_4, df_A_5]]
  keyword2_pie = [len(i) for i in [df_B_1, df_B_2, df_B_3, df_B_4, df_B_5]]

  # 각 별점에 해당하는 빈 문자열 생성
  df_A_text1, df_A_text2, df_A_text3, df_A_text4, df_A_text5 = '', '', '', '', ''
  df_B_text1, df_B_text2, df_B_text3, df_B_text4, df_B_text5 = '', '', '', '', ''

  # 각 별점들의 리뷰들을 하나의 문자열로 합쳐 리턴하는 함수
  def review_tokenizer(data):
    text = ''
    for i in range(len(data)):
      text += data[i]
    return text

  # 이전에 정의된 함수 적용
  df_A_text1 = review_tokenizer(df_A_1)
  df_A_text2 = review_tokenizer(df_A_2)
  df_A_text3 = review_tokenizer(df_A_3)
  df_A_text4 = review_tokenizer(df_A_4)
  df_A_text5 = review_tokenizer(df_A_5)

  df_B_text1 = review_tokenizer(df_B_1)
  df_B_text2 = review_tokenizer(df_B_2)
  df_B_text3 = review_tokenizer(df_B_3)
  df_B_text4 = review_tokenizer(df_B_4)
  df_B_text5 = review_tokenizer(df_B_5)

  # 불용어 처리 후 토큰 저장
  # text_preprocessing(text:str)
  A_token_1 = text_preprocessing(df_A_text1)
  A_token_2 = text_preprocessing(df_A_text2)
  A_token_3 = text_preprocessing(df_A_text3)
  A_token_4 = text_preprocessing(df_A_text4)
  A_token_5 = text_preprocessing(df_A_text5)
  
  B_token_1 = text_preprocessing(df_B_text1)
  B_token_2 = text_preprocessing(df_B_text2)
  B_token_3 = text_preprocessing(df_B_text3)
  B_token_4 = text_preprocessing(df_B_text4)
  B_token_5 = text_preprocessing(df_B_text5)

  # 긍부정( 1~3 / 4~5 )으로 토큰 나눔
  A_neg_token = A_token_1 + A_token_2 + A_token_3
  A_pos_token = A_token_4 + A_token_5

  B_neg_token = B_token_1 + B_token_2 + B_token_3
  B_pos_token = B_token_4 + B_token_5

  # 토큰 개수 카운트
  A_final_neg = Counter(A_neg_token)
  A_final_pos = Counter(A_pos_token)
  B_final_neg = Counter(B_neg_token)
  B_final_pos = Counter(B_pos_token)

  # 상품별 토큰 딕셔너리로 변환 => {(토큰1:count) , (토큰2:count) , ...}
  keyword1_13_dict = dict(A_final_neg.most_common())
  keyword1_45_dict = dict(A_final_pos.most_common())
  keyword2_13_dict = dict(B_final_neg.most_common())
  keyword2_45_dict = dict(B_final_pos.most_common())

  # 딕셔너리에서 key와 value를 각각 리스트로 뽑아서 저장
  keyword1_13_keys = [i for i in keyword1_13_dict.keys()]
  keyword1_45_keys = [i for i in keyword1_45_dict.keys()]
  keyword2_13_keys = [i for i in keyword2_13_dict.keys()]
  keyword2_45_keys = [i for i in keyword2_45_dict.keys()]
  keyword1_13_values = [i for i in keyword1_13_dict.values()]
  keyword1_45_values = [i for i in keyword1_45_dict.values()]
  keyword2_13_values = [i for i in keyword2_13_dict.values()]
  keyword2_45_values = [i for i in keyword2_45_dict.values()]

  # minmax scaling 적용을 위한 데이터프레임화
  keyword1_13_df = pd.DataFrame({'text':keyword1_13_keys, 'value':keyword1_13_values})
  keyword1_45_df = pd.DataFrame({'text':keyword1_45_keys, 'value':keyword1_45_values})
  keyword2_13_df = pd.DataFrame({'text':keyword2_13_keys, 'value':keyword2_13_values})
  keyword2_45_df = pd.DataFrame({'text':keyword2_45_keys, 'value':keyword2_45_values})

  # minmax scaling 적용 후 *1000
  def scaling_data(df):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df[['value']].values)*1000
    return scaled_data.flatten().tolist()

  keyword1_13_valsc = scaling_data(keyword1_13_df)
  keyword1_45_valsc = scaling_data(keyword1_45_df)
  keyword2_13_valsc = scaling_data(keyword2_13_df)
  keyword2_45_valsc = scaling_data(keyword2_45_df)

  # 명세에 맞게 수정 [{'text':text, 'value':value}] 
  keyword1_wordcloud_13 = []
  keyword1_wordcloud_45 = []
  keyword2_wordcloud_13 = []
  keyword2_wordcloud_45 = []

  for i in range(len(keyword1_13_keys)):
    keyword1_wordcloud_13.append({'text':keyword1_13_keys[i], 'value':keyword1_13_valsc[i]})

  for i in range(len(keyword1_45_keys)):
    keyword1_wordcloud_45.append({'text':keyword1_45_keys[i], 'value':keyword1_45_valsc[i]})

  for i in range(len(keyword2_13_keys)):
    keyword2_wordcloud_13.append({'text':keyword2_13_keys[i], 'value':keyword2_13_valsc[i]})

  for i in range(len(keyword2_45_keys)):
    keyword2_wordcloud_45.append({'text':keyword2_45_keys[i], 'value':keyword2_45_valsc[i]})

  # 메인함수 리턴
  return keyword1_wordcloud_13[:13], keyword1_wordcloud_45[:13], keyword2_wordcloud_13[:13], keyword2_wordcloud_45[:13], keyword1_pie, keyword2_pie
