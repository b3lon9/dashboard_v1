from django.urls import path, re_path
from home import views
from django.contrib.auth import views as auth_views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/',views.login_view,name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name=''),name='logout'),
    path('register/',views.register_user,name='register'),
    path('error/',views.error_page,name="error_page")
]