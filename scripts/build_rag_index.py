### 📁 Datei: requirements.txt
chromadb
sentence-transformers
jsonlines


### 📁 Datei: scripts/build_rag_index.py
from rag.embedder import get_embedder
from rag.database import get_chroma_client
import jsonlines
from pathlib import Path

DATA_FILE = Path("data/klexikon_rag_chunks.jsonl")

if __name__ == "__main__":
    chroma = get_chroma_client("klexikon")
    embedder = get_embedder()

    print("🔁 Lade Daten...")
    with jsonlines.open(DATA_FILE, mode='r') as reader:
        documents = []
        metadatas = []
        ids = []
        for obj in reader:
            documents.append(obj["text"])
            metadatas.append(obj["metadata"])
            ids.append(obj["metadata"]["id"])

    print(f"🔢 {len(documents)} Dokumente werden eingefügt...")
    chroma.add_texts(documents=documents, metadatas=metadatas, ids=ids, embedding=embedder)
    print("✅ RAG-Datenbank erfolgreich erstellt.")


### 📁 Datei: rag/embedder.py
from sentence_transformers import SentenceTransformer

def get_embedder():
    print("🧠 Lade MiniLM Embedder...")
    return SentenceTransformer("all-MiniLM-L6-v2")


### 📁 Datei: rag/database.py
import chromadb
from chromadb.config import Settings
from pathlib import Path

def get_chroma_client(collection_name: str):
    persist_dir = str(Path(".chromadb").resolve())
    print(f"💾 Verwende ChromaDB in {persist_dir}")
    client = chromadb.Client(Settings(persist_directory=persist_dir, chroma_db_impl="duckdb+parquet", anonymized_telemetry=False))
    if collection_name in [c.name for c in client.list_collections()]:
        return client.get_collection(name=collection_name)
    return client.create_collection(name=collection_name)


### 📁 Datei: rag/retriever.py
from rag.database import get_chroma_client
from rag.embedder import get_embedder


def search(query, top_k=3):
    chroma = get_chroma_client("klexikon")
    embedder = get_embedder()
    print(f"🔍 Suche nach: {query}")
    results = chroma.query(query_texts=[query], n_results=top_k, embedding=embedder)
    return results


### 📁 Datei: main.py
from rag.retriever import search

if __name__ == "__main__":
    frage = input("❓ Frage eingeben: ")
    result = search(frage)
    print("\n🎯 Ergebnisse:")
    for doc, meta in zip(result['documents'][0], result['metadatas'][0]):
        print(f"- [{meta['title']}] {doc[:200]}...")
