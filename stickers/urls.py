from django.urls import path
from django.conf import settings

from . import views


urlpatterns = [
    # create account url
    path('', views.sticker_index, name="sticker_index"),
    #path('shipmysticker', views.ship_my_sticker, name='ship_my_sticker'),
    ]
