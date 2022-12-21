from django.urls import path, re_path
from home import views
from django.contrib.auth import views as auth_views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('vote/',views.vote, name='vote'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name=''),name='logout'),
    path('user_register/',views.user_register_page,name='register'),
    path('user_register_res/',views.user_register_result,name='registerres'),
    path('user_register_idcheck/',views.user_register_idcheck,name='registeridcheck'),
    path('user_register_completed/',views.user_register_completed,name='registercompleted'),
]