from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.index, name='welcome_index'),
    path('show-users/', views.show_all_users, name='show-all-users'),
    path('about-us/', views.about_us, name='about-us'),
    re_path('followers_count', views.followers_count, name='followers_count'),
]
