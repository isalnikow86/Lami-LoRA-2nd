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
