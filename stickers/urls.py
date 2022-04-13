from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

import user


from . import views


urlpatterns = [
    path('', views.sticker_index, name="sticker_index"),
    path('shipmysticker/', views.ship_sticker_view, name='ship_my_sticker'),
    path('<str:username>/', views.sticker_index_for_visitor, name="sticker_index_for_visitor"),
    re_path('regenerate_qr_code', user.views.regenerate_qr_code, name='regenerate_qr_code'),
    path('<str:username>/regenerate_user_qr_code', user.views.regenerate_user_qr_code, name='regenerate_user_qr_code')
    ]
