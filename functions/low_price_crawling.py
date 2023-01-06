import requests
from bs4 import BeautifulSoup
import json
import datetime

# 최저가데이터 크롤링 함수
def low_price(keyword):
    url = 'https://search.danawa.com/dsearch.php?query=' + keyword
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(res.text, 'html.parser')
    prod_list = soup.find_all('a', 'click_log_product_standard_title_')
    prod_link = prod_list[0]['href']
    pcode_index = prod_link.find('pcode')
    pcode = prod_link[pcode_index+6:pcode_index+14]

    url = 'https://prod.danawa.com/info/ajax/getProductPriceList.ajax.php?productCode=' + pcode
    headers = {'referer':'https://prod.danawa.com/info/?pcode=' + pcode,
               'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    res = requests.get(url, headers=headers)

    json_body = json.loads(res.text)

    series_xaxis_list = []
    keyword_series_list = []
    for result in json_body['3']['result']:
        keyword_series_list.append(result['minPrice']) # 최저가 데이터
        series_xaxis_list.append(result['Fulldate']) # 날짜 데이터

    series_xaxis = []
    for i in series_xaxis_list:
        date = datetime.datetime.strptime(i, "%y-%m-%d")
        change_date = datetime.datetime.strftime(date, "%m/%d/%y")
        series_xaxis.append(change_date)

    keyword1_series = {}
    keyword1_series['name'] = keyword
    keyword1_series['data'] = keyword_series_list
    
    return keyword1_series, series_xaxis

