from utils.config_loader import load_input_json
from utils.pdf_reader import load_documents
from utils.relevance_ranker import rank_paragraphs
import json
import os
from datetime import datetime

INPUT_DIR = "input"
OUTPUT_DIR = "output"

if __name__ == "__main__":
    config = load_input_json(INPUT_DIR)
    persona = config["persona"]["role"]
    job = config["job_to_be_done"]["task"]
    doc_list = config["documents"]

    documents = load_documents(INPUT_DIR, doc_list)

    print("🔍 Ranking sections based on relevance...")
    top_sections = rank_paragraphs(documents, persona, job, top_k=5)

    # Build JSON Output
    output_json = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in doc_list],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for rank, section in enumerate(top_sections, 1):
        output_json["extracted_sections"].append({
            "document": section["document"],
            "section_title": section["section_title"],
            "importance_rank": rank,
            "page_number": section["page_number"]
        })
        output_json["subsection_analysis"].append({
            "document": section["document"],
            "refined_text": section["refined_text"],
            "page_number": section["page_number"]
        })

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "challenge1b_output.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2)

    print(f"\n✅ Output saved to {output_path}")
