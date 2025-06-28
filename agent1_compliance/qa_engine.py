import os
import fitz  # PyMuPDF
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from nltk.tokenize import sent_tokenize
import openai
import traceback
from PIL import Image
import pytesseract
import io
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── Model and Index Initialization ───
embedding_dim = 768
model = SentenceTransformer('all-mpnet-base-v2')
index = faiss.IndexFlatL2(embedding_dim)

chunks = []
chunk_sources = []

# ─── OpenAI Key & Model Setup ───
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
USE_OPENAI = bool(openai.api_key)

if not USE_OPENAI:
    print("\u26a0\ufe0f OpenAI API key not detected. Smart answering will fallback to local mode.")

def ocr_pdf_page(page):
    try:
        pix = page.get_pixmap(dpi=300)
        img_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"\u274c OCR failed on page: {e}")
        return ""

def extract_text_with_fallback(doc):
    paragraphs = []
    last_header = ""
    for page_number, page in enumerate(doc):
        try:
            text = page.get_text("text").strip()
            if len(text) < 30:
                print(f"\ud83d\udd01 Page {page_number + 1}: Weak text, using OCR...")
                text = ocr_pdf_page(page)
            lines = text.splitlines()
            buffer = []
            for line in lines:
                clean_line = line.strip()
                if re.match(r'^H\d{4}|ST\s*-\s*H\d{4}', clean_line):
                    last_header = clean_line
                elif clean_line:
                    buffer.append(clean_line)

            full_text = " ".join(buffer)
            if full_text:
                sentences = sent_tokenize(full_text)
                window_size = 3
                for i in range(0, len(sentences), 2):  # Sliding window with overlap
                    chunk = " ".join(sentences[i:i+window_size]).strip()
                    if len(chunk) > 40:
                        label = f"[{last_header}]" if last_header else ""
                        paragraphs.append(f"{label} {chunk}")
        except Exception as e:
            print(f"\u274c Page {page_number + 1}: Extraction failed: {e}")
            traceback.print_exc()
    return paragraphs

def process_pdf_file(path, fname):
    local_chunks = []
    local_sources = []
    try:
        doc = fitz.open(path)
        paragraphs = extract_text_with_fallback(doc)
        if not paragraphs:
            print(f"\u26a0\ufe0f Skipped {fname}: no usable content")
            return local_chunks, local_sources
        for para in paragraphs:
            local_chunks.append(para)
            local_sources.append((fname, para))
        print(f"\u2705 Loaded {len(paragraphs)} chunks from {fname}")
        return local_chunks, local_sources
    except Exception as e:
        print(f"\u274c Error processing {fname}: {e}")
        traceback.print_exc()
        return [], []

def load_documents_from_folder(folder_path="media/documents", limit_to=None, max_workers=4):
    global chunks, chunk_sources
    chunks.clear()
    chunk_sources.clear()
    index.reset()

    files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(".pdf") and (not limit_to or f in limit_to)
    ]
    file_paths = [(os.path.join(folder_path, fname), fname) for fname in files]

    print(f"\n\u26a1 Loading {len(file_paths)} PDF(s) with up to {max_workers} threads...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_file = {executor.submit(process_pdf_file, path, fname): fname for path, fname in file_paths}
        for future in as_completed(future_to_file):
            file_chunks, file_sources = future.result()
            chunks.extend(file_chunks)
            chunk_sources.extend(file_sources)

    if chunks:
        try:
            print("\ud83e\uddd0 Encoding all chunks into embeddings...")
            embeddings = model.encode(chunks, normalize_embeddings=True, show_progress_bar=True)
            index.add(np.array(embeddings))
            print(f"\u2705 Indexed {len(chunks)} total chunks from {len(files)} document(s).")
        except Exception as e:
            print(f"\u274c Embedding failed: {e}")
            traceback.print_exc()
    else:
        print("\u26a0\ufe0f No valid chunks were indexed.")

def summarize_context_with_openai(context, query):
    prompt = f"""
You are a professional compliance and HR documentation assistant. Your job is to answer using ONLY the document excerpts below.

\ud83d\udd12 Do not guess, generalize, or fabricate. Only cite and explain based on what's present.
\ud83d\udccc Always quote the policy language directly when possible.
\ud83d\udcc2 Structure your response clearly using sections, bullet points, and tables where appropriate.

If no clear answer exists, say:
"Not enough information in the documents to answer this."

Respond using the following format:

\u2705 **Answer:**  
Begin with a direct answer supported by exact wording from the document.

\ud83d\udcdd **Policy Excerpt:**  
Quote the document’s key line(s) that support the answer.

\u267b\ufe0f **Summary Table:**  
| Field       | Detail                        |
|-------------|-------------------------------|
| Requirement | [What is required?]           |
| Frequency   | [e.g., annually]              |
| Source      | [Document name / section]     |
| Notes       | [Optional explanation]        |

\ud83d\udccc **Sources:** Include all filenames used to derive the answer.

--- DOCUMENT CONTEXT START ---
{context}
--- DOCUMENT CONTEXT END ---

QUESTION: {query}
ANSWER:
"""
    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a professional AI assistant for HR, compliance, training, and auditing."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"\u26a0\ufe0f OpenAI summarization failed: {e}")
        traceback.print_exc()
        return None

def answer_question(query, k=15):
    if not chunks:
        return "\u26a0\ufe0f No document content indexed yet. Please upload and reload documents."

    try:
        query_embedding = model.encode([query], normalize_embeddings=True)
        D, I = index.search(np.array(query_embedding), k=k)

        used_files = set()
        relevant_chunks = []
        for idx in I[0]:
            fname, para = chunk_sources[idx]
            used_files.add(fname)
            relevant_chunks.append(para)

        combined_context = "\n".join(relevant_chunks)

        if USE_OPENAI:
            openai_response = summarize_context_with_openai(combined_context, query)
            if openai_response:
                return f"\ud83d\udcda **Answer:**\n{openai_response}\n\n\ud83d\udccc **Source(s):**\n" + "\n".join(
                    [f"- {fname}" for fname in used_files]
                )

        return "\ud83e\udd16 OpenAI unavailable. Here are top matching document excerpts:\n\n" + combined_context

    except Exception as e:
        print(f"\u274c Error during answering: {e}")
        traceback.print_exc()
        return "\u274c Internal AI engine error. Please check logs or reload documents."
)
    return result

