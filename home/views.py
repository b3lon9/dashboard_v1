from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import json
import random
from django.core.serializers.json import DjangoJSONEncoder
from home.models import Wordcloud, Community, UserEtc
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from argon2 import PasswordHasher
from login.forms import LoginForm, SignUpForm
# from functions.AD_filtering_with_easyocr import AD_filtering
from functions.starRating_clas import starRating_classisification
from functions.low_price_crawling import low_price
from functions.pos_neg_all import *
# Create your views here.

import time

def index(request):
    
    # profile img path
    try:
        user = UserEtc.objects.get(user_id=request.user.username)
        user_img = user.user_img    
        user_id = user.user_id
    except:
        user_img = ''
        user_id = request.user.username
        print('not exist user ', request.user.username)
        
        
    context = {}
    if request.POST: # 게시글 입력
        
        context = eval(request.POST['context'])
        keyword = ''
        text = ''
        
        for key in list(request.POST):
            if 'csrfmiddlewaretoken' == key: 
                continue
            else :          
                if 'chk_info' in key:
                    keyword = request.POST['chk_info_key']
                elif 'text' == key:
                    text = request.POST['text'].strip()
        
        comm_qry = Community.objects.filter(uid=request.user) & \
        Community.objects.filter(key1=request.GET['keyword1']) & \
        Community.objects.filter(key2=request.GET['keyword2'])
        
        if comm_qry:    # 수정
            comm = comm_qry[0]
            comm.cur_key = keyword
            comm.text = text
        else:          # 추가
            comm = Community(
                uid     = request.user,
                key1    = request.GET['keyword1'],
                key2    = request.GET['keyword2'],
                cur_key = keyword,
                text    = text
            )
            
        comm.save()
        
        # <----커뮤니티/투표 context
        
        comm_qry_key1 = Community.objects.filter(cur_key=request.GET['keyword1']) & \
        Community.objects.filter(key1=request.GET['keyword1']) & \
        Community.objects.filter(key2=request.GET['keyword2'])
        
        comm_qry_key2 = Community.objects.filter(cur_key=request.GET['keyword2']) & \
        Community.objects.filter(key1=request.GET['keyword1']) & \
        Community.objects.filter(key2=request.GET['keyword2'])
        
        vote = [len(comm_qry_key1), len(comm_qry_key2)]
        
        # ---->커뮤니티/투표 context
        
        context['vote'] = vote
        context['comm_qry_key1'] = comm_qry_key1
        context['comm_qry_key2'] = comm_qry_key2
         
        tmp_context = {key:value for key,value in context.items() if 'comm_qry_key' not in key}
        
        context['context'] = tmp_context
          
        return render(request, 'home/index.html',context)
                

    
    if len(request.GET) > 0:
        # <----권석원 context
        '''
        #### 키워드 별 긍부정 분류 명세 #### 
        keword1_positive : 키워드1에 대한 긍정 분류 결과
        keword2_positive : 키워드2에 대한 긍정 분류 결과
        
        keword1_negative : 키워드1에 대한 부정 분류 결과
        keword2_negative : 키워드2에 대한 부정 분류 결과
        
        위 변수들은 list(dict()) 형태로 이루어져 있음
        
        dict key : title(제목), text(내용), link(원본 링크), cate(분류)
        
        ex1) keword1_positive[0] : 키워드1에 대한 긍정 분류 결과 0번째 글
        ex2) keword1_positive[0].title : 키워드1에 대한 긍정 분류 결과 0번째 글의 제목
        
        '''
        
        #n1, n2, n3, n4 = predict_pos_neg(crawling_news(request.GET['keyword1'], 1, 2), crawling_news(request.GET['keyword2'], 1, 2))
        n1, n2, n3, n4 = predict_pos_neg(crawling_news_ksw(request.GET['keyword1']), crawling_news_ksw(request.GET['keyword2']))
        
        key1_b, key1_c = AD_filtering(request.GET['keyword1'])
        key2_b, key2_c = AD_filtering(request.GET['keyword2'])

        c1, c2, c3, c4 = predict_pos_neg(key1_c, key2_c)
        b1, b2, b3, b4 = predict_pos_neg(key1_b, key2_b)
        
        keyword1_positive, keyword1_negative, keyword2_positive, keyword2_negative = n1+c1+b1, n2+c2+b2, n3+c3+b3, n4+c4+b4

        
        '''
        #### 바 차트 #### 
        positve_bar : 키워드1,키워드2에 대한 각각 긍정 개수
        negative_bar : 키워드1,키워드2에 대한 각각 부정 개수
        
        긍정은 양수, 부정은 음수
        ex1) positve_bar = [키워드1 긍정 개수, 키워드2 긍정 개수]
        
        '''
        
        positve_bar = [len(keyword1_positive), len(keyword2_positive)]
        negative_bar = [-len(keyword1_negative), -len(keyword2_negative)]
        
        '''
        #### 라인 차트 #### 
        keyword1_serise : 키워드1과 시간대 별 최저가
        keyword2_serise : 키워드2과 시간대 별 최저가
        serise_xaxis    : 각 최저가에 대한 시간
        
        keyword1_serise의 data와 keyword2_serise의 data의 길이와
        serise_xaxis 길이가 일치해야합니다.
        
        '''
        
        keyword1_series_, series_xaxis_ = low_price(request.GET['keyword1'])        
        keyword2_series_, _ = low_price(request.GET['keyword2'])
        
        keyword1_serise = keyword1_series_
        keyword2_serise = keyword2_series_
        serise_xaxis = series_xaxis_

        # print(keyword1_serise)
        # print(keyword2_serise)
        # print(serise_xaxis)

        # keyword1_serise = {'name' : '갤럭시',
        #                 'data' : [20, 50, 30, 60, 30, 50]}
        
        # keyword2_serise = {'name' : '아이폰',
        #                 'data' : [60, 30, 65, 45, 67, 35]}
        
        # serise_xaxis = ['1/11/2000', '2/11/2000', '3/11/2000', '4/11/2000', '5/11/2000', '6/11/2000']
      
        
        # ---->권석원 context
        
        # <----장현광 context
        '''
        #### 워드 클라우드 #### 
        keyword1_wordcloud_13 : 키워드1 에 대한 1~3점 평점 키워드
        keyword2_wordcloud_13 : 키워드2 에 대한 1~3점 평점 키워드
        keyword1_wordcloud_45 : 키워드1 에 대한 4~5점 평점 키워드
        keyword2_wordcloud_45 : 키워드2 에 대한 4~5점 평점 키워드
        
        위 변수들은 list(dict()) 형태로 이루어져 있음
        
        dict key : text(평점), value(개수)
        
        minmax scaling 후에 1000 을 곱하면 될 것 같아요
        
        '''

        # 키워드를 어디서 받는건지 몰라서 일단은 'S22'
        # S22만 키워드로 주면 아이폰14를 같이 크롤링해서 데이터를 반환합니다

        keyword1_wordcloud_13_, keyword1_wordcloud_45_, keyword2_wordcloud_13_, keyword2_wordcloud_45_, keyword1_pie_, keyword2_pie_ = starRating_classisification(request.GET['keyword1'],request.GET['keyword2'])
  
        keyword1_wordcloud_13 = keyword1_wordcloud_13_
        #keyword1_wordcloud_13_json=json.dumps(keyword1_wordcloud_13,cls=DjangoJSONEncoder)
        
        keyword2_wordcloud_13 = keyword2_wordcloud_13_
        #keyword2_wordcloud_13_json=json.dumps(keyword2_wordcloud_13,cls=DjangoJSONEncoder)
        
        keyword1_wordcloud_45 = keyword1_wordcloud_45_
        #keyword1_wordcloud_45_json=json.dumps(keyword1_wordcloud_45,cls=DjangoJSONEncoder)
        
        keyword2_wordcloud_45 = keyword2_wordcloud_45_
        #keyword2_wordcloud_45_json=json.dumps(keyword2_wordcloud_45,cls=DjangoJSONEncoder)
        
        '''
        #### 파이 차트 #### 
        keyword1_pie : 키워드1에 대한 평점 별 개수
        keyword2_pie : 키워드2에 대한 평점 별 개수
        
        0번부터 순서대로 1점 ~ 5점
        
        '''
        
        keyword1_pie = keyword1_pie_
        
        keyword2_pie = keyword2_pie_
        
        # ---->장현광 context
        
        
        # <----커뮤니티/투표 context
        
        comm_qry_key1 = Community.objects.filter(cur_key=request.GET['keyword1']) & \
        Community.objects.filter(key1=request.GET['keyword1']) & \
        Community.objects.filter(key2=request.GET['keyword2'])
        
        comm_qry_key2 = Community.objects.filter(cur_key=request.GET['keyword2']) & \
        Community.objects.filter(key1=request.GET['keyword1']) & \
        Community.objects.filter(key2=request.GET['keyword2'])
        
        vote = [len(comm_qry_key1), len(comm_qry_key2)]
        
        # ---->커뮤니티/투표 context
        
        
        
        context={
            'profile_img':user_img,
            'profile_id':user_id,
            # 'currnet_questions':currnet_questions,
            # 'question':question,
            # 'count_value':count_value_json,
            'is_show' : True, # 필수
            'keyword1' : request.GET['keyword1'],
            'keyword2' : request.GET['keyword2'],

            'keyword1_positive' : keyword1_positive,
            'keyword1_negative' : keyword1_negative,
            'keyword2_positive' : keyword2_positive,
            'keyword2_negative' : keyword2_negative,
            
            'positve_bar' : positve_bar,
            'negative_bar' : negative_bar,
            
            'keyword1_serise' : keyword1_serise,
            'keyword2_serise' : keyword2_serise,
            'serise_xaxis' : serise_xaxis,
            
            'keyword1_wordcloud_13_json' : keyword1_wordcloud_13,
            'keyword2_wordcloud_13_json' : keyword2_wordcloud_13,
            'keyword1_wordcloud_45_json' : keyword1_wordcloud_45,
            'keyword2_wordcloud_45_json' : keyword2_wordcloud_45,
            
            'keyword1_pie' : keyword1_pie,
            'keyword2_pie' : keyword2_pie,
            
            'vote' : vote,
            'comm_qry_key1' : comm_qry_key1,
            'comm_qry_key2' : comm_qry_key2,
            
        }
        
        
        tmp_context = {key:value for key,value in context.items() if 'comm_qry_key' not in key}
        
        context['context'] = tmp_context
        


        return render(request, 'home/index.html',context)
    else :
        return render(request, 'home/index.html', {'profile_img':user_img, 'profile_id':user_id,})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            raw_img = form.cleaned_data.get("img")
            user = authenticate(username=username, password=raw_password,imgfile=raw_img)

            # user_id API / 일반 로그인 ID구분 필요
            obj = UserEtc.objects.create(
                user_id = username,
                user_img = request.FILES['img'],
                user_rd = timezone.datetime.now()
            )
            obj.save()
            
            msg = 'User created successfully.'
            success = True

            # return redirect("/login/")

        else:
            msg = form.errors
    else:
        form = SignUpForm()

    return render(request, "register.html", {"form": form, "msg": msg, "success": success})


def error_page(request):
    return render(request,'home/page-404.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST['login_id']
        password = request.POST['login_pw']
        
        try:
            # users = User.objects.get(username=username)
            # user_pw = users.password
            # if PasswordHasher().verify(user_pw,password):
            #     redirection_page = '/home/'
            # else:
            #     redirection_page = '/home/error'
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                redirection_page = '/home/'
            else:
                redirection_page = '/home/error'
        except:
            redirection_page = '/home/error'
    return HttpResponseRedirect(redirection_page)
