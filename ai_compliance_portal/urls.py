"""
URL configuration for ai_compliance_portal project.

The `urlpatterns` list routes URLs to views. For more information see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ai_compliance_portal.views import home  # ✅ Add homepage view

urlpatterns = [
    path('', home),  # ✅ Root homepage
    path('admin/', admin.site.urls),  # Django Admin

    # Agent 1: Compliance QA Agent
    path('agent1/', include('agent1_compliance.urls')),

    # Agent 2: News Intelligence Agent
    path('agent2/', include('agent2_news.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

