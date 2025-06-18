from django.urls import path
from . import views

urlpatterns = [
    # Web form to upload rule resource file (UI)
    path('resource/', views.upload_resource, name='upload_resource'),

    # Manually trigger fetch + rule match
    path('fetch/', views.fetch_and_react, name='fetch_and_react'),

    # View triggered alerts (UI)
    path('alerts/', views.list_alerts, name='list_alerts'),
]

