import os
from sentence_transformers import SentenceTransformer, util

MODEL_NAME = "all-MiniLM-L6-v2"
LOCAL_MODEL_PATH = "./local_models/all-MiniLM-L6-v2"

class EmbeddingEngine:
    def __init__(self, device="cpu"):
        if os.path.exists(LOCAL_MODEL_PATH):
            print(f"✅ Using local model from: {LOCAL_MODEL_PATH}")
            self.model = SentenceTransformer(LOCAL_MODEL_PATH, device=device)
        else:
            print("⚠️ Local model not found. Downloading from HuggingFace...")
            self.model = SentenceTransformer(MODEL_NAME, cache_folder=LOCAL_MODEL_PATH, device=device)

    def embed_query(self, persona, job):
        text = f"Persona: {persona}. Job: {job}"
        return self.model.encode(text, convert_to_tensor=True)

    def embed_section(self, section_title, snippet):
        text = section_title + "\n" + snippet
        return self.model.encode(text, convert_to_tensor=True)

    def similarity(self, emb1, emb2):
        return util.pytorch_cos_sim(emb1, emb2).item()