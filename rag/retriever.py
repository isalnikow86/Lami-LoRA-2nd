from rag.database import get_chroma_client
from rag.embedder import get_embedder

def search(query, top_k=3):
    chroma = get_chroma_client("klexikon")
    embedder = get_embedder()
    print(f"🔍 Suche nach: {query}")
    results = chroma.query(query_texts=[query], n_results=top_k, embedding=embedder)
    return results

