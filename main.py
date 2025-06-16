from rag.retriever import search

if __name__ == "__main__":
    frage = input("❓ Frage eingeben: ")
    result = search(frage)
    print("\n🎯 Ergebnisse:")
    for doc, meta in zip(result['documents'][0], result['metadatas'][0]):
        print(f"- [{meta['title']}] {doc[:200]}...")
