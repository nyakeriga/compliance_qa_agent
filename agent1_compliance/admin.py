# agent1_compliance/admin.py

from django.contrib import admin
from .models import DocumentUpload

@admin.register(DocumentUpload)
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'doc_type', 'uploaded_at')
    search_fields = ('title',)

