---
type: technical_standard
target_engine: Godot 4.6, Godot 4.7, Unity 6
status: verified
---

# 🛠️ Agent Skill: Memory & RAG

# 🧠 Memory Layer — ChromaDB + Local Embedding

## Purpose
Solves the "amnesia" problem when calling Ollama models by persisting important context in a local vector database. No cloud leaks, no external dependencies.

---

## 🛠️ Setup (Python + ChromaDB)

```python
import chromadb
from chromadb.utils import embedding_functions

# Local Embedding — all-MiniLM-L6-v2 (22MB, CPU-friendly)
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path="./data/chroma_db")
collection = client.get_or_create_collection("project_code", embedding_function=emb_fn)
```

## 🔍 Key Features
1. **Ingest**: Automatically chunk and index project code.
2. **Query**: Find the most relevant context using cosine similarity.
3. **Save Session**: Persist agent conversation logs for future reference.
