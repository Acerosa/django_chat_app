"""Root URL configuration.

Routes admin, chat app URLs, Django auth views, and redirects '/' to rooms.
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rooms/',include('chatapp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(pattern_name='index', permanent=False)),
]
