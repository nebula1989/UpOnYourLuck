from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='welcome_index'),
    path('show-users/', views.show_all_users, name='show-all-users'),
    path('show-users/followers_count', views.followers_count, name='followers_count'),
]
