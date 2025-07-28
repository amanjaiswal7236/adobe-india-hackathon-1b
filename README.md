# Connecting the Dots - Round 1B Solution

## Overview
![Adobe-Hackathon-Banner](media/banner.png)
This project implements the persona-driven document intelligence system for Adobe India Hackathon 2025 Round 1B. It extracts and ranks relevant sections from a collection of PDFs based on a given persona and job-to-be-done.

---

### Important Notes

- **Preferred Way to Run:** Running the solution locally inside a Python virtual environment is recommended for development and testing, as the hackathon guidelines do not mandate a strict Docker design.
- **Documentation & Samples:** The detailed methodology is explained in `approach_explanation.md`. Sample output JSON files for the provided test cases are available in the `sample_output/` directory.

---

## Approach Summary

- **Document Processing:** Loads multiple PDFs from the input folder.
- **Section Extraction:** Uses a custom pipeline to extract document sections, titles, and page numbers.
- **Embedding & Ranking:** Utilizes a local sentence-transformers MiniLM model for embedding texts, avoiding any internet dependency.
- **Clustering & Relevance:** Clusters extracted headings, scores relevance based on persona/job embedding similarity, and ranks sections.
- **Offline-First:** All models and dependencies are pre-downloaded and included to comply with no network usage during execution.

## Directory Structure

- `app/`: Core application modules (processing, embedding, clustering, etc.)
- `local_models/`: Contains the pre-downloaded sentence-transformers model used offline.
- `input/`: Place input PDFs and persona/job JSON here before running.
- `output/`: Output JSON files with ranked sections will be written here.
- `requirements.txt`: Python dependencies.
- `Dockerfile`: Container configuration for the offline environment.
- `main.py`: Entry point for running the pipeline.
- `approach_explanation.md`: Detailed explanation of methodology.

## How to Build and Run

### Preferred Way: Run Locally (Recommended for Development and Testing)

Since the hackathon guidelines do not specify exact Docker design constraints beyond offline execution and platform compatibility, running the code locally inside a Python virtual environment is often faster for iterative development and debugging.

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the main script:

```bash
python main.py
```

Make sure your input files are placed in the `input/` directory and outputs will be written to `output/`.

---

### Running with Docker

To ensure environment consistency and compliance with the hackathon’s execution criteria, you can build and run the provided Docker container as follows:

```bash
docker build --platform linux/amd64 -t adobe-1b:v1 .
```

```bash
docker run --rm \
  -v "$(pwd)/input:/app/input" \
  -v "$(pwd)/output:/app/output" \
  --network none \
  adobe-1b:v1
```

---

## Notes

* The solution runs fully offline using local model files stored under `local_models/`.
* No network calls or external API requests are made during execution.
* Input PDFs can be placed individually or in folders under `input/` as needed.
* Outputs are generated as JSON files matching the hackathon’s specified format.
* For faster iteration and debugging, local virtual environment execution is recommended.