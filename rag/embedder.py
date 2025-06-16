from sentence_transformers import SentenceTransformer

def get_embedder():
    print("🧠 Lade MiniLM Embedder...")
    return SentenceTransformer("all-MiniLM-L6-v2")
