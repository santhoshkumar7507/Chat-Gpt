import chromadb
import os

os.makedirs("memory", exist_ok=True)
client = chromadb.PersistentClient(path="./memory")
collection = client.get_or_create_collection(name="omnimind_memory")

def add_memory(text, uid):
    collection.add(documents=[text], ids=[uid])

def search_memory(query):
    results = collection.query(query_texts=[query], n_results=3)
    return results
