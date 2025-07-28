# utils/relevance_ranker.py
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')


def is_potential_title(text: str) -> bool:
    if len(text) < 60 and text.isupper():
        return True
    if text.istitle() and len(text.split()) <= 6:
        return True
    return False


def smart_chunk(text, min_len=100, max_len=600):
    """
    Chunk large text into coherent blocks based on empty lines and length.
    """
    raw = text.split('\n\n')  # split on double line breaks
    chunks = []

    buffer = ""
    for para in raw:
        line = para.strip().replace('\n', ' ')
        if not line:
            continue

        buffer += " " + line

        if len(buffer) > max_len:
            chunks.append(buffer.strip())
            buffer = ""
        elif len(buffer) > min_len and line.endswith('.'):
            chunks.append(buffer.strip())
            buffer = ""

    if buffer:
        chunks.append(buffer.strip())

    return chunks


def rank_paragraphs(documents, persona: str, job: str, top_k=5):
    query = f"{persona}. Task: {job}"
    query_embedding = model.encode(query, convert_to_tensor=True)

    ranked_sections = []

    for doc in documents:
        doc_name = doc["document"]
        for page in doc["pages"]:
            page_num = page["page_number"]
            chunks = smart_chunk(page["text"])

            if not chunks:
                continue

            chunk_embeddings = model.encode(chunks, convert_to_tensor=True)
            scores = util.cos_sim(query_embedding, chunk_embeddings)[0]

            for i, score in enumerate(scores):
                chunk = chunks[i]
                # Try to infer a better title using heuristics
                lines = chunk.split(".")
                first_line = lines[0].strip()
                title = first_line[:60] if is_potential_title(first_line) else chunk[:40]

                ranked_sections.append({
                    "document": doc_name,
                    "page_number": page_num,
                    "section_title": title,
                    "refined_text": chunk,
                    "score": float(score)
                })

    ranked_sections.sort(key=lambda x: x["score"], reverse=True)
    return ranked_sections[:top_k]
