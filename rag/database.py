import chromadb
from chromadb.config import Settings
from pathlib import Path

def get_chroma_client(collection_name: str):
    persist_dir = str(Path(".chromadb").resolve())
    print(f"💾 Verwende ChromaDB in {persist_dir}")
    client = chromadb.Client(Settings(
        persist_directory=persist_dir,
        chroma_db_impl="duckdb+parquet",
        anonymized_telemetry=False
    ))
    if collection_name in [c.name for c in client.list_collections()]:
        return client.get_collection(name=collection_name)
    return client.create_collection(name=collection_name)
