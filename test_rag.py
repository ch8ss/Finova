from core.rag import load_document, get_vectorstore

# Load the document
docs = load_document("data/uploads/test_business.txt", "txt")
print(f"Loaded {len(docs)} document(s)")

# Store in vectorstore
vectorstore = get_vectorstore(documents=docs)
print("Vectorstore created successfully")

# Query it
results = vectorstore.similarity_search("What is the profit?", k=2)
print("\nSearch results:")
for r in results:
    print(f"  {r.page_content}")
