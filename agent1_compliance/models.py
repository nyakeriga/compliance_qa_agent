# agent1_compliance/models.py

from django.db import models
import os

class DocumentUpload(models.Model):
    DOC_TYPES = [
        ('pdf', 'PDF Document'),
        ('zip', 'ZIP Archive'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    doc_type = models.CharField(max_length=10, choices=DOC_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.doc_type})"

    def filename(self):
        return os.path.basename(self.file.name)

