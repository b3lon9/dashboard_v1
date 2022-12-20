from django.shortcuts import render, get_object_or_404
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from home.models import City,Wordcloud,Question,Choice


# Create your views here.
def index(request):
    city = City.objects.values()
    city_json = json.dumps(list(city),cls=DjangoJSONEncoder)
    wordcloud = Wordcloud.objects.values()
    wordcloud_json=json.dumps(list(wordcloud),cls=DjangoJSONEncoder)
    currnet_questions = Question.objects.order_by('-pub_date')[:5]
    question = Question.objects.get(pk=1)
    count_value = Choice.objects.values()
    count_value_json=json.dumps(list(count_value),cls=DjangoJSONEncoder)
    context={
        'city_json':city_json,
        'wordcloud_json':wordcloud_json,
        'currnet_questions':currnet_questions,
        'question':question,
        'count_value':count_value_json,
    }

    return render(request, 'home/index.html',context)

def vote(request):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=1)
    print("-----------------------")
    print("nomuhon")
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
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        # return render(request, 'home/index.html')
        return HttpResponseRedirect('/home')