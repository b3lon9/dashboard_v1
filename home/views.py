from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder
from home.models import City, Wordcloud, Question, Choice, Vote, User
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount

# Create your views here.


def index(request):
    # currnet_questions = Question.objects.order_by('-pub_date')[:5]
    # question = Question.objects.get(pk=1)
    # count_value = Choice.objects.values()
    # count_value_json=json.dumps(list(count_value),cls=DjangoJSONEncoder)

    #print(list(wordcloud))
    
    if request.method == 'GET':
        
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
            keyword1_positive = [{'title' : 'NCT 127 플러스 콘서트 다녀왔습니다',
                                'text' : '갤럭시로 찍었는데 좋아요',
                                'link' : 'https://blog.naver.com/aeyongly/222953745910',
                                'cate' : 'blog'},
                                {'title' : 'NCT 127 플러스 콘서트 다녀왔습니다',
                                'text' : '갤럭시로 찍었는데 좋아요',
                                'link' : 'https://blog.naver.com/aeyongly/222953745910',
                                'cate' : 'news'},
                                {'title' : 'NCT 127 플러스 콘서트 다녀왔습니다',
                                'text' : '갤럭시로 찍었는데 좋아요',
                                'link' : 'https://blog.naver.com/aeyongly/222953745910',
                                'cate' : 'cafe'},]
            
            keyword1_negative = [{'title' : 'NCT 127 플러스 콘서트 다녀왔습니다',
                                'text' : '갤럭시로 찍었는데 좋아요',
                                'link' : 'https://blog.naver.com/aeyongly/222953745910',
                                'cate' : 'news'}]
            
            keyword2_positive = [{'title' : '[2022 마이 블로그 리포트] 올해 활동 데이터로 알아보는 2022 나의 블로그 리듬',
                                'text' : '아이폰내용',
                                'link' : 'https://blog.naver.com/aeyongly/222953745910',
                                'cate' : 'cafe'}]
            
            keyword2_negative = [{'title' : 'NCT 127 플러스 콘서트 다녀왔습니다',
                                'text' : '아이폰내용',
                                'link' : 'https://blog.naver.com/aeyongly/222953745910',
                                'cate' : 'blog'}]
            
            
            '''
            #### 바 차트 #### 
            positve_bar : 키워드1,키워드2에 대한 각각 긍정 개수
            negative_bar : 키워드1,키워드2에 대한 각각 부정 개수
            
            긍정은 양수, 부정은 음수
            ex1) positve_bar = [키워드1 긍정 개수, 키워드2 긍정 개수]
            
            '''
            
            positve_bar = [8,2]
            negative_bar = [-3,-7]
            
            '''
            #### 라인 차트 #### 
            keyword1_serise : 키워드1과 시간대 별 최저가
            keyword2_serise : 키워드2과 시간대 별 최저가
            serise_xaxis    : 각 최저가에 대한 시간
            
            keyword1_serise의 data와 keyword2_serise의 data의 길이와
            serise_xaxis 길이가 일치해야합니다.
            
            '''
            
            keyword1_serise = {'name' : '갤럭시',
                            'data' : [20, 50, 30, 60, 30, 50]}
            
            keyword2_serise = {'name' : '아이폰',
                            'data' : [60, 30, 65, 45, 67, 35]}
            
            serise_xaxis = ['1/11/2000', '2/11/2000', '3/11/2000', '4/11/2000', '5/11/2000', '6/11/2000']
                            
            
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
            
            keyword1_wordcloud_13 = [{'text': '언리쉬드', 'value': 300}, 
                        {'text': '건담', 'value': 500}, 
                        {'text': 'Z건담', 'value': 200}, 
                        {'text': 'FAZZ', 'value': 700}, 
                        {'text': '머신러닝', 'value': 200}, 
                        {'text': '딥러닝', 'value': 400}, 
                        {'text': '랜덤포레스트', 'value': 240},]
            
            keyword1_wordcloud_13_json=json.dumps(keyword1_wordcloud_13,cls=DjangoJSONEncoder)
            
            keyword2_wordcloud_13 = [{'text': '언리쉬드', 'value': 300}, 
                        {'text': '건담', 'value': 500}, 
                        {'text': 'Z건담', 'value': 200}, 
                        {'text': 'FAZZ', 'value': 700}, 
                        {'text': '머신러닝', 'value': 200}, 
                        {'text': '딥러닝', 'value': 400}, 
                        {'text': '랜덤포레스트', 'value': 240},]
            
            keyword2_wordcloud_13_json=json.dumps(keyword2_wordcloud_13,cls=DjangoJSONEncoder)
            
            keyword1_wordcloud_45 = [{'text': '언리쉬드', 'value': 300}, 
                        {'text': '건담', 'value': 500}, 
                        {'text': 'Z건담', 'value': 200}, 
                        {'text': 'FAZZ', 'value': 700}, 
                        {'text': '머신러닝', 'value': 200}, 
                        {'text': '딥러닝', 'value': 400}, 
                        {'text': '랜덤포레스트', 'value': 240},]
            
            keyword1_wordcloud_45_json=json.dumps(keyword1_wordcloud_45,cls=DjangoJSONEncoder)
            
            keyword2_wordcloud_45 = [{'text': '언리쉬드', 'value': 300}, 
                        {'text': '건담', 'value': 500}, 
                        {'text': 'Z건담', 'value': 200}, 
                        {'text': 'FAZZ', 'value': 1000}, 
                        {'text': '머신러닝', 'value': 200}, 
                        {'text': '딥러닝', 'value': 400}, 
                        {'text': '랜덤포레스트', 'value': 240},]
            
            keyword2_wordcloud_45_json=json.dumps(keyword2_wordcloud_45,cls=DjangoJSONEncoder)
            
            '''
            #### 파이 차트 #### 
            keyword1_pie : 키워드1에 대한 평점 별 개수
            keyword2_pie : 키워드2에 대한 평점 별 개수
            
            0번부터 순서대로 1점 ~ 5점
            
            '''
            
            keyword1_pie = [300,100,10,400,600]
            
            keyword2_pie = [300,100,10,400,600]
            
            # ---->장현광 context

            context={
                # 'currnet_questions':currnet_questions,
                # 'question':question,
                # 'count_value':count_value_json,
                'is_show' : True, # 필수

                'keyword1_positive':keyword1_positive,
                'keyword1_negative':keyword1_negative,
                'keyword2_positive':keyword2_positive,
                'keyword2_negative':keyword2_negative,
                
                'positve_bar' : positve_bar,
                'negative_bar' : negative_bar,
                
                'keyword1_serise' : keyword1_serise,
                'keyword2_serise' : keyword2_serise,
                'serise_xaxis' : serise_xaxis,
                
                'keyword1_wordcloud_13_json':keyword1_wordcloud_13_json,
                'keyword2_wordcloud_13_json':keyword2_wordcloud_13_json,
                'keyword1_wordcloud_45_json':keyword1_wordcloud_45_json,
                'keyword2_wordcloud_45_json':keyword2_wordcloud_45_json,
                
                'keyword1_pie' : keyword1_pie,
                'keyword2_pie' : keyword2_pie,
                
            }

            return render(request, 'home/index.html',context)
        else :
            return render(request, 'home/index.html')
    else:
        return render(request, 'home/index.html',context)

def vote(request):
    # print(request.POST['choice'])
    choice = get_object_or_404(Choice, pk=1)
    question = get_object_or_404(Question, pk=1)
    if Vote.objects.filter(choice=choice, voter=request.user).exists():
        messages.error(request, "Already Voted on this choice")
        return HttpResponseRedirect('/home')
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, '', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        Vote.objects.create(voter=request.user, choice=choice)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # return render(request, 'home/index.html')
        return HttpResponseRedirect('/home')


def user_register_page(request):
    return render(request, 'home/user_register.html')


def user_register_idcheck(request):
    if request.method == "POST":
        username = request.POST['username']
    else:
        username = ''
    idObject = User.objects.filter(username=username)
    idCount = idObject.count()
    if idCount > 0:
        msg = "<font color='red'> 이미 존재하는 ID입니다.</font><input type='hidden' name='IDcheckResult' id='IDCheckResult' value=0/>"
    else:
        msg = "<font color='blue'> 사용가능한 ID입니다.</font><input type='hidden' name='IDcheckResult' id='IDCheckResult' value=1/>"

    return HttpResponse(msg)


def user_register_result(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
    try:
        if User.objects.filter(username=username).count() == 0:
            User.objects.create(username=username, password=password, last_name=last_name
                                , email=email, phone=phone)
            redirection_page = '/home/user_register_completed/'
        else:
            redirection_page = '/home'
    except:
        redirection_page = '/home'

    return HttpResponseRedirect(redirection_page)


def user_register_completed(request):
    return render(request, 'home/user_register_completed_page.html')
