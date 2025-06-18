# agent1_compliance/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('ask/', views.ask_compliance_question, name='ask_compliance_question'),
]
