from django.urls import path, re_path
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('vote/',views.vote, name='vote'),
]