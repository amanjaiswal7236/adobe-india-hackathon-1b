from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class EmbeddingEngine:
    def __init__(self, device="cpu"):
        self.model = SentenceTransformer(MODEL_NAME, device=device)

    def embed_query(self, persona, job):
        text = f"Persona: {persona}. Job: {job}"
        return self.model.encode(text, convert_to_tensor=True)

    def embed_section(self, section_title, snippet):
        text = section_title + "\n" + snippet
        return self.model.encode(text, convert_to_tensor=True)

    def similarity(self, emb1, emb2):
        return util.pytorch_cos_sim(emb1, emb2).item()