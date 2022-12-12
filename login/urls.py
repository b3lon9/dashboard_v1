from django.urls import path
from login import views

app_name = 'login'
urlpatterns = [
    path('', views.index, name='login'),
    # path('', views.index, name='logout'),
]
