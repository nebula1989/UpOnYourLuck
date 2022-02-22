from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views


urlpatterns = [
    path('', views.sticker_index, name="sticker_index"),
    path('ship', views.request_sticker, name='request_sticker'),
    path('<str:username>', views.sticker_index_for_visitor, name="sticker_index_for_visitor"),
    ]
