from django.shortcuts import render
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from home.models import City
from home.models import Wordcloud


# Create your views here.
def index(request):
    city = City.objects.values()
    city_json = json.dumps(list(city),cls=DjangoJSONEncoder)
    wordcloud = Wordcloud.objects.values()
    wordcloud_json=json.dumps(list(wordcloud),cls=DjangoJSONEncoder)
    
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
    keword1_positive = [{'title' : 'NCT 127 플러스 콘서트 다녀왔습니다',
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
    
    keword1_negative = [{'title' : 'NCT 127 플러스 콘서트 다녀왔습니다',
                         'text' : '갤럭시로 찍었는데 좋아요',
                         'link' : 'https://blog.naver.com/aeyongly/222953745910',
                         'cate' : 'news'}]
    
    keword2_positive = [{'title' : '[2022 마이 블로그 리포트] 올해 활동 데이터로 알아보는 2022 나의 블로그 리듬',
                         'text' : '아이폰내용',
                         'link' : 'https://blog.naver.com/aeyongly/222953745910',
                         'cate' : 'cafe'}]
    
    keword2_negative = [{'title' : 'NCT 127 플러스 콘서트 다녀왔습니다',
                         'text' : '아이폰내용',
                         'link' : 'https://blog.naver.com/aeyongly/222953745910',
                         'cate' : 'blog'}]
    
    
    '''
    바 차트 ()
    positve_bar : 키워드1,키워드2에 대한 각각 긍정 개수
    negative_bar : 키워드1,키워드2에 대한 각각 부정 개수
    
    긍정은 양수, 부정은 음수
    ex1) positve_bar = [키워드1 긍정 개수, 키워드2 긍정 개수]
    
    '''
    
    positve_bar = [8,2]
    negative_bar = [-3,-7]
    
    
    # ---->권석원 context
    
    
    context={
        'city_json':city_json,
        'wordcloud_json':wordcloud_json,
        'keword1_positive':keword1_positive,
        'keword1_negative':keword1_negative,
        'keword2_positive':keword2_positive,
        'keword2_negative':keword2_negative,
        'positve_bar' : positve_bar,
        'negative_bar' : negative_bar,
        
    }
    return render(request, 'home/index.html',context)

@login_required(login_url="/login/")
def pages(request):

    context = {}
    city = City.objects.values()
    city_json = json.dumps(list(city),cls=DjangoJSONEncoder)
    
    wordcloud = Wordcloud.objects.values()
    wordcloud_json=json.dumps(list(wordcloud),cls=DjangoJSONEncoder)
    context={
        'city_json':city_json,
        'wordcloud_json':wordcloud_json,
    }

    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.

    try:
        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))

        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template)

        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')

        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')

        return HttpResponse(html_template.render(context, request))