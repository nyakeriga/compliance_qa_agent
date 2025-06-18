# agent1_compliance/views.py

import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .models import DocumentUpload
from .qa_engine import answer_question
from .utils import extract_zip_to_folder, save_uploaded_file
import json

@csrf_exempt
def upload_document(request):
    if request.method == 'POST':
        doc_file = request.FILES.get('file')
        title = request.POST.get('title', doc_file.name)
        ext = os.path.splitext(doc_file.name)[1].lower()

        doc_type = 'pdf' if ext == '.pdf' else 'zip'
        saved_path = save_uploaded_file(doc_file)

        if doc_type == 'zip':
            extract_zip_to_folder(saved_path)

        DocumentUpload.objects.create(title=title, file=doc_file, doc_type=doc_type)
        return JsonResponse({'message': 'Document uploaded successfully.'})

    return JsonResponse({'error': 'Only POST allowed'}, status=405)

@csrf_exempt
def ask_compliance_question(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        question = body.get('question', '')

        if not question:
            return JsonResponse({'error': 'No question provided.'}, status=400)

        answer = answer_question(question)
        return JsonResponse({'question': question, 'answer': answer})

    return JsonResponse({'error': 'Only POST allowed'}, status=405)

