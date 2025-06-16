from chromadb import PersistentClient

def get_chroma_client(collection_name: str):
    client = PersistentClient(path=".chromadb")
    collection = client.get_or_create_collection(name=collection_name)
    return collection
