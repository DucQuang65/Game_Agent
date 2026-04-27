---
type: skill
category: memory-architecture
target_engine: Godot 4.6, Godot 4.7, Unity 6
status: active
priority: high
---

# 🧠 Agent Skill: Memory Management & Context Layering

## Purpose
Define how the agent manages long-term project knowledge and short-term session context — without overwhelming the model's context window or leaking private data.

---

## Core Architecture

```
Data Flow:
  Raw Session / Codebase
        │
        ▼
  ChromaDB (data/chroma_db/)     ← Local vector storage, git-ignored
        │
        ├── project_code         ← .cs, .gd, .py files
        ├── bug_history          ← Godot/Unity error logs
        ├── tech_docs            ← Summarized documentation
        └── agent_sessions       ← Conversation context per session
        │
        ▼
  Distillation Process
        │
        ▼
  AI_Training/skills/*.md        ← Public: pure technical knowledge
  memory/*.md                    ← Local only: project-specific notes (git-ignored)
```

## Memory Tiers

| Tier | Storage | Visibility | Lifetime |
|---|---|---|---|
| **Static** | `AI_Training/skills/` | Public (GitHub) | Permanent |
| **Dynamic** | `data/chroma_db/` | Local only | Until `rm -rf` |
| **Session** | ChromaDB `agent_sessions` | Local only | 30 days, then prune |
| **Notes** | `memory/*.md` | Local only (git-ignored) | Manual |

---

## Embedding Configuration

```python
# Use local CPU-safe embedding — never cloud-based
EMBEDDING_MODEL = "nomic-embed-text"   # via Ollama (zero VRAM cost)
# Alternative fallback:
# EMBEDDING_MODEL = "all-MiniLM-L6-v2" (22MB, CPU only)

DB_PATH = PROJECT_ROOT / "data" / "chroma_db"
```

---

## Standards & Rules

### Security
- **No leakage**: Never store raw API keys, credentials, or personal identifiers in any memory file.
- **Sandbox**: `ingest_file()` must verify the target file is inside `PROJECT_ROOT` before reading.
- **Exclusions**: Never ingest `.env`, `*.key`, `*.pem`, or `secrets/` regardless of location.

### Language
- All persistent `AI_Training/skills/*.md` files must be written in **technical English**.
- Session notes in `memory/*.md` may be in any language (they are git-ignored and local only).

### Pruning
- Archive session notes older than **30 days** to `_archive/` (git-ignored).
- Run `rm -rf data/chroma_db && python scripts/ingest_all.py` to rebuild the full index cleanly.

---

## Operational Checklist

```
1. Is the ingested file inside PROJECT_ROOT?
2. Is the file extension on the allowed list (.cs, .gd, .py, .md, .json)?
3. Does the file contain raw credentials? (Skip if yes)
4. Has the session been summarized before closing the task?
5. Have new technical insights been added to AI_Training/skills/?
6. Have sensitive session logs been purged from memory/?
```
