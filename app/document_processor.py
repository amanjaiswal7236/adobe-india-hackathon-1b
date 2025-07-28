import json
from .section_utils import extract_full_text, slice_section_text
from .embedding_engine import EmbeddingEngine

def process_documents(persona, job, input_dir, output_dir, top_k=10):
    from .config import OUTPUT_DIR
    model = EmbeddingEngine(device="cpu")
    query_emb = model.embed_query(persona, job)

    pdf_files = list(input_dir.glob("*.pdf"))
    all_sections = []

    for pdf_path in pdf_files:
        json_path = output_dir / (pdf_path.stem + ".json")
        if not json_path.exists():
            print(f"⚠️ Skipping {pdf_path.name} (missing outline)")
            continue

        with json_path.open("r", encoding="utf-8") as f:
            outline_data = json.load(f)

        outline = outline_data.get("outline", [])
        pages_text = extract_full_text(pdf_path)

        for idx, section in enumerate(outline):
            title = section["text"]
            page = section["page"]
            text = slice_section_text(pages_text, outline, idx)
            snippet = text[:300]

            emb = model.embed_section(title, snippet)
            sim = model.similarity(query_emb, emb)

            all_sections.append({
                "document": pdf_path.name,
                "section_title": title,
                "page_number": page,
                "section_text": text,
                "similarity": sim
            })

    all_sections.sort(key=lambda x: x["similarity"], reverse=True)

    output = {
        "metadata": {
            "input_documents": [f.name for f in pdf_files],
            "persona": persona,
            "job_to_be_done": job
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for rank, sec in enumerate(all_sections[:top_k], 1):
        output["extracted_sections"].append({
            "document": sec["document"],
            "section_title": sec["section_title"],
            "importance_rank": rank,
            "page_number": sec["page_number"]
        })
        refined = sec["section_text"].replace("\n", " ").strip()[:500]
        output["subsection_analysis"].append({
            "document": sec["document"],
            "refined_text": refined,
            "page_number": sec["page_number"]
        })

    return output