from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from . import views as user_views
from stickers import views as sticker_views
from contact import views as contact_views


urlpatterns = [
    # sticker url
    path('stickers/', include('stickers.urls')),
    # create account url
    path("register/", user_views.register_request, name="register"),

    # terms and conditions url
    path('register/terms_and_conditions/', user_views.terms_and_conditions, name='terms_and_conditions'),
    path("login/", user_views.login_request, name="login"),
    # logout url
    path("logout/", user_views.logout_request, name="logout"),
    path('dashboard/', user_views.dashboard, name='user_dashboard'),
    path('dashboard/followers/', user_views.view_followers, name='view_followers'),
    path('dashboard/following/', user_views.view_following, name='view_following'),
    path('profile/', user_views.profile, name='profile'),
    re_path('follow_count', user_views.follow_count),
    path('<str:username>/', user_views.visitor_to_profile, name='visitor_to_profile'),
    path('stickers/<str:username>/', sticker_views.sticker_index_for_visitor, name='visitor_to_qr_code'),
    path('profile/update/', user_views.update_profile, name='update_profile'),
    path('profile/update_security/', user_views.update_security, name='update_security'),
    re_path('profile/update_security/delete_profile', user_views.delete_profile, name='delete_profile'),



    re_path('profile/update_security/toggle_two_factor', user_views.toggle_two_factor, name='toggle_two_factor'),
    re_path('login/login_verification', user_views.login_verification, name='login_verification'),

    path('password_reset/', contact_views.password_reset_request, name='password_reset'),
]

# Only add this when we in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
