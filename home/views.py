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



# Create your views here.
def index(request):
    city = City.objects.values()
    city_json = json.dumps(list(city),cls=DjangoJSONEncoder)
    context={
        'city_json':city_json,
    }
    return render(request, 'home/index.html',context)

@login_required(login_url="/login/")

def pages(request):

    context = {}
    city = City.objects.values()
    city_json = json.dumps(list(city),cls=DjangoJSONEncoder)
    context={
        'city_json':city_json,
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