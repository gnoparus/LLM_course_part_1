import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection")

collection.add(
    documents=["There is a dog name Ching Ching.", "Ta-waan is a black cat."],
    metadatas=[
        {"source": "dog farm", "url": "https://webserv101/D10001"},
        {"source": "cat house", "url": "https://webserv101/D10001"},
    ],
    ids=["D10001", "C2001"],
)

results = collection.query(query_texts=["What is the name of the cat?"], n_results=1)

print(results)