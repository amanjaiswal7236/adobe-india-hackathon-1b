import time
import json
from .config import INPUT_DIR, OUTPUT_DIR
from .document_processor import process_documents
from app.runner import run_batch_heading_extraction

def run_persona_pipeline():
    start_time = time.time()

    persona_path = INPUT_DIR / "challenge1b_input.json"
    with persona_path.open("r", encoding="utf-8") as f:
        persona_data = json.load(f)

    persona = persona_data.get("persona") or persona_data.get("role") or "Unknown persona"
    job = persona_data.get("job_to_be_done") or persona_data.get("task") or "Unknown job"

    run_batch_heading_extraction()

    output = process_documents(persona, job, INPUT_DIR, OUTPUT_DIR)

    output["metadata"]["processing_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    output_path = OUTPUT_DIR / "challenge1b_output.json"

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n1B output saved to: {output_path}")
    print(f"Total time: {round(time.time() - start_time, 2)} seconds")