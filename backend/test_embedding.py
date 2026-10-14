from app.services.embedding_services import generate_embedding


chunk = "Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine."

embedding = generate_embedding(chunk)

print("Embedding dimension:", len(embedding))

print("First five values", embedding[:5])
