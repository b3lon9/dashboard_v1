from django.urls import path, re_path
from home import views
from django.contrib.auth import views as auth_views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('vote/',views.vote, name='vote'),
    path('login/',views.login,name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name=''),name='logout'),
    path('register/',views.register_user,name='register'),
    path('user_register_res/',views.user_register_result,name='registerres'),
    path('user_register_idcheck/',views.user_register_idcheck,name='registeridcheck'),
    path('user_register_completed/',views.user_register_completed,name='registercompleted'),
    path('error/',views.error_page,name="error_page")
]