from django.urls import path, re_path
from home import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^.*\.*', views.pages, name='pages'),
]

# <a class="dropdown-item" href="{% url 'account_logout' %}"><i class="fa fa-power-off m-r-5 m-l-5"></i> Logout</a>