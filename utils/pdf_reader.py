import fitz  # PyMuPDF
import os

def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            pages.append({
                "page_number": i + 1,
                "text": text
            })
    return pages

def load_documents(input_dir, document_list):
    all_docs = []
    for doc_meta in document_list:
        filename = doc_meta["filename"]
        pdf_path = os.path.join(input_dir, filename)
        pages = extract_text_by_page(pdf_path)
        all_docs.append({
            "document": filename,
            "title": doc_meta["title"],
            "pages": pages
        })
    return all_docs
