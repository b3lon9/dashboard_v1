from django.shortcuts import render, get_object_or_404
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
    city = City.objects.values()
    city_json = json.dumps(list(city), cls=DjangoJSONEncoder)
    wordcloud = Wordcloud.objects.values()
    wordcloud_json = json.dumps(list(wordcloud), cls=DjangoJSONEncoder)
    currnet_questions = Question.objects.order_by('-pub_date')[:5]
    question = Question.objects.get(pk=1)
    count_value = Choice.objects.values()
    count_value_json = json.dumps(list(count_value), cls=DjangoJSONEncoder)

    # <----권석원 context
    '''
    키워드 별 긍부정 분류 명세
    keword1_positive : 키워드1에 대한 긍정 분류 결과
    keword2_positive : 키워드2에 대한 긍정 분류 결과
    
    keword1_negative : 키워드1에 대한 부정 분류 결과
    keword2_negative : 키워드2에 대한 부정 분류 결과
    
    위 변수들은 list(dict()) 형태로 이루어져 있음
    
    dict key : title(제목), text(내용), link(원본 링크), cate(분류)
    
    ex1) keword1_positive[0] : 키워드1에 대한 긍정 분류 결과 0번째 글
    ex2) keword1_positive[0].title : 키워드1에 대한 긍정 분류 결과 0번째 글의 제목
    
    '''
    keword1_positive = [{'title': 'NCT 127 플러스 콘서트 다녀왔습니다',
                         'text': '갤럭시로 찍었는데 좋아요',
                         'link': 'https://blog.naver.com/aeyongly/222953745910',
                         'cate': 'blog'},
                        {'title': 'NCT 127 플러스 콘서트 다녀왔습니다',
                         'text': '갤럭시로 찍었는데 좋아요',
                         'link': 'https://blog.naver.com/aeyongly/222953745910',
                         'cate': 'news'},
                        {'title': 'NCT 127 플러스 콘서트 다녀왔습니다',
                         'text': '갤럭시로 찍었는데 좋아요',
                         'link': 'https://blog.naver.com/aeyongly/222953745910',
                         'cate': 'cafe'}, ]

    keword1_negative = [{'title': 'NCT 127 플러스 콘서트 다녀왔습니다',
                         'text': '갤럭시로 찍었는데 좋아요',
                         'link': 'https://blog.naver.com/aeyongly/222953745910',
                         'cate': 'news'}]

    keword2_positive = [{'title': '[2022 마이 블로그 리포트] 올해 활동 데이터로 알아보는 2022 나의 블로그 리듬',
                         'text': '아이폰내용',
                         'link': 'https://blog.naver.com/aeyongly/222953745910',
                         'cate': 'cafe'}]

    keword2_negative = [{'title': 'NCT 127 플러스 콘서트 다녀왔습니다',
                         'text': '아이폰내용',
                         'link': 'https://blog.naver.com/aeyongly/222953745910',
                         'cate': 'blog'}]

    '''
    바 차트 ()
    positve_bar : 키워드1,키워드2에 대한 각각 긍정 개수
    negative_bar : 키워드1,키워드2에 대한 각각 부정 개수
    
    긍정은 양수, 부정은 음수
    ex1) positve_bar = [키워드1 긍정 개수, 키워드2 긍정 개수]
    
    '''

    positve_bar = [8, 2]
    negative_bar = [-3, -7]

    # ---->권석원 context
    # 장현광 context
    # world cloud: value(단어),count(빈도수)
    # pie-chart: 점수(1~5점),점수 횟수(ex: 1점 10회,2점 30회등)

    context = {
        'city_json': city_json,
        'wordcloud_json': wordcloud_json,
        'currnet_questions': currnet_questions,
        'question': question,
        'count_value': count_value_json,

        'keword1_positive': keword1_positive,
        'keword1_negative': keword1_negative,
        'keword2_positive': keword2_positive,
        'keword2_negative': keword2_negative,
        'positve_bar': positve_bar,
        'negative_bar': negative_bar,

    }

    return render(request, 'home/index.html', context)


def vote(request):
    # print(request.POST['choice'])
    choice = get_object_or_404(Choice, pk=1)
    question = get_object_or_404(Question, pk=1)
    if Vote.objects.filter(choice=choice, voter=request.user).exists():
        messages.error(request, "Already Voted on this choice")
        return HttpResponseRedirect('/home')
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        print("-------------------------------")
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
    idObject = User.object.filter(username__exact=username)
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
        birth_year = int(request.POST['birth_year'])
        birth_month = int(request.POST['birth_month'])
        birth_day = int(request.POST['birth_day'])
    try:
        if username and User.objects.filter(username_exact=username).count() == 0:
            date_of_birth = datetime(birth_year, birth_month, birth_day)
            user = User.objects.create_user(username, password, last_name, email, phone, birth_year,birth_month,birth_day)
            redirection_page = '/home/user_register_completed/'
        else:
            redirection_page = '/home'
    except:
        redirection_page = '/home'

    return HttpResponseRedirect(redirection_page)


def user_register_completed(request):
    return render(request, 'home/user_register_completed_page.html')
