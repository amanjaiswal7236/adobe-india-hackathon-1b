### Round 1B: Persona-Aware Document Section Ranking

#### Objective

Given a user persona and a job-to-be-done, we aim to extract the most relevant sections from a set of PDFs. Each section may span multiple pages and should be semantically aligned with the user's intent.

---

#### Approach

1. **Input Parsing**
   We accept two inputs:
   - A list of PDFs (from content/input/)
   - A JSON file with:
     ```json
     {
       "persona": "...",
       "job_to_be_done": "..."
     }
     ```
   These are combined into a single natural language query prompt.

2. **Section Preprocessing**
   We reuse our Round 1A logic to extract hierarchical section titles and headings via `pdfminer.six`. We map each heading to its respective page content and gather surrounding paragraphs into structured sections.

3. **Embedding & Ranking**
   - We use `sentence-transformers/all-MiniLM-L6-v2` (∼90MB) to embed:
     - Each section title + content preview (first 400 characters)
     - The query: persona + job-to-be-done
   - We compute cosine similarity between query and section embeddings.
   - Top-K sections are selected based on similarity scores.

4. **Output**
   The top-ranked sections (by document, title, and page) along with a cleaned text preview are returned in a strict JSON format:

   ```json
   {
     "output": [
       {
         "document_title": "...",
         "document_filename": "...",
         "section_title": "...",
         "page_number": ...,
         "snippet": "...",
         "score": ...
       }
     ]
   }
    ```

---

#### Design Decisions

* We use a **lightweight, CPU-friendly model** (MiniLM-L6-v2) that offers a strong balance between size and semantic performance. Larger models (like `mpnet` or `bge`) were ruled out due to >1GB size or GPU dependencies.
* We considered using sentence-level extraction with cross-encoders (e.g., `cross-encoder/ms-marco-*`), but this would require quadratic comparisons (O(N×M)) and exceed 60s compute time on CPU.
* We explored TF-IDF as a baseline but dropped it due to lack of semantic context; relevant concepts were often missed due to vocabulary mismatch.
* We avoid any training or fine-tuning to remain stateless, offline, and lightweight.
* The solution is fully deterministic and works without any internet or external service.

---

#### Limitations

* Section boundaries depend on heading detection, which may break if the document uses unconventional formatting.
* The semantic similarity is based only on initial content from each section (limited to 400–500 chars).
* If multiple PDFs contain very short or very long sections, the relevance scoring may favor larger text blocks.

---

## Execution Instructions

### Build (once):

```bash
docker build --platform linux/amd64 -t persona-analyzer:latest .
```

### Run:

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none persona-analyzer:latest
```