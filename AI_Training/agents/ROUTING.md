---
type: agent_persona
target_engine: Godot 4.6, Godot 4.7, Unity 6
status: verified
---

# 🤖 Agent Persona: Routing

## Agent Map (v4.2 "Local-Only")

| Input | Agent Role | Local Model | Device |
|---|---|---|---|
| Chat & Fast Routing | `routing-agent` | `llama3.2:3b` | CPU |
| Task Analysis & Planning | `reasoning-agent` | `deepseek-r1:7b` | GPU |
| Orchestrator (Logic & Code) | `orchestrator` | `gamedev-agent` (Trained) | GPU |
| Vision & UI Audit | `vision-agent` | `gemma3:4b` | GPU |
| RAG Retrieval Context | `researcher-agent` | Full-File Context (Limit 16K) | GPU |
| Multimodal Embeddings | `memory-layer` | `nomic-embed-text` | CPU |

---

## Quota Fallback Strategy
**N/A**. OpenRouter API has been strictly decoupled from this environment due to rate limiting issues. System relies 100% on local offline models.

---

## VRAM Budget (RTX 4060 8GB) - v4.2 Local
- **Idle**: 0 GB (`llama3.2` on CPU).
- **Coding**: ~5.5 GB (`gamedev-agent`).
- **Vision/Planning**: Unloaded aggressively to prevent OOM. (~4.0 GB)
- **Buffer**: ~2.5 GB reserved for Windows/OS & Godot Editor.
