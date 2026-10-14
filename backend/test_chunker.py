from app.services.text_chunker import chunk_text


text = """
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.

Node.js allows JavaScript to run outside the browser.

Node.js uses an event-driven architecture and supports asynchronous I/O.

NPM is the package manager for Node.js and provides access to thousands
of reusable packages.

Node.js can be used to build web servers, APIs and backend applications.
"""

chunks = chunk_text(text)
print(f"Total chunks: {len(chunks)}")

for index, chunk in enumerate(chunks):
    print(f"Chunk {index + 1}:")
    print(chunk)
