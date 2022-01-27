from django.urls import path

from . import views


urlpatterns = [
    # qrcode index url
    path("profile/<str:username>/qrcode", views.index, name="qrcode_index"),

]