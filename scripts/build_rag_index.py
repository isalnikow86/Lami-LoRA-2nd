from rag.embedder import get_embedder
from rag.database import get_chroma_client
import jsonlines
from pathlib import Path

DATA_FILE = Path("data/klexikon_rag_chunks.jsonl")

if __name__ == "__main__":
    print("📁 Prüfe Datei:", DATA_FILE)
    if not DATA_FILE.exists():
        print("❌ Datei nicht gefunden!")
        exit(1)

    chroma = get_chroma_client("klexikon")
    embedder = get_embedder()

    print("🔁 Lade Daten...")
    with jsonlines.open(DATA_FILE, mode='r') as reader:
        documents = []
        metadatas = []
        ids = []
        count = 0
        for obj in reader:
            documents.append(obj["text"])
            metadatas.append(obj["metadata"])
            ids.append(obj["metadata"]["id"])
            count += 1

    print(f"🔢 Gelesene Einträge: {count}")
    if count == 0:
        print("❌ Keine Daten im JSONL – bitte prüfen.")
        exit(1)

    print("💾 Füge Daten in ChromaDB ein...")
    chroma.add(documents=documents, metadatas=metadatas, ids=ids)
    print("✅ RAG-Datenbank erfolgreich erstellt.")
