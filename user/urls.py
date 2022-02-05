from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    # create account url
    path("register", views.register_request, name="register"),
    # login url
    path("login", views.login_request, name="login"),
    # logout url
    path("logout", views.logout_request, name="logout"),
    path('dashboard', views.dashboard, name='user_dashboard'),
    path('profile', views.profile, name='profile'),
    path('profile/<str:username>', views.visitor_to_profile, name='visitor_to_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
]

# Only add this when we in debug mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
