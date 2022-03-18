from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from stickers import views as sticker_views


urlpatterns = [
    # sticker url
    path('sticker/', include('stickers.urls')),
    # create account url
    path("register/", views.register_request, name="register"),
    # login url
    path("login/", views.login_request, name="login"),
    # logout url
    path("logout/", views.logout_request, name="logout"),
    path('dashboard/', views.dashboard, name='user_dashboard'),
    path('profile/', views.profile, name='profile'),
    re_path('followers_count', views.followers_count),
    path('<str:username>/', views.visitor_to_profile, name='visitor_to_profile'),
    path('stickers/<str:username>/', sticker_views.sticker_index_for_visitor, name='visitor_to_qr_code'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/update_security/', views.update_security, name='update_security'),
    re_path('delete_profile', views.delete_profile, name='delete_profile'),
    path('dashboard/followers/', views.view_followers, name='view_followers'),
    path('dashboard/following/', views.view_following, name='view_following'),
]

# Only add this when we in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
