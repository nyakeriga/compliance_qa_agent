# agent1_compliance/utils.py

import os, zipfile
from django.core.files.storage import default_storage

def save_uploaded_file(file):
    path = default_storage.save('documents/' + file.name, file)
    return default_storage.path(path)

def extract_zip_to_folder(zip_path):
    extract_to = os.path.splitext(zip_path)[0] + "_extracted"
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to
