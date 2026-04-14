---
type: technical_standard
target_engine: Godot 4.6, Godot 4.7, Unity 6
status: verified
---

# 🛠️ Agent Skill: Core Intelligence

# 🎮 GAME-DEV AGENT OS — Master Skill

> **Version:** 3.0 — Multi-Agent / WSL2 / Gemini WebSearch / Telegram  
> **Target Hardware:** i5-13500 · RTX 4060 8GB · 32GB RAM · Ubuntu 24 / WSL2  
> **Supreme Directive:** Agents MUST NEVER read any files or directories outside `PROJECT_ROOT`.

---

## 🏗️ PART 1 — SYSTEM ARCHITECTURE

### 1.1 Data Flow Diagram

```
Telegram User
     │
     ▼
[Gateway Bot] ───────────────────────────────────────────────
     │                                                       │
     ▼                                                       │
[Chat Agent]  llama3.2:3b  (CPU, always-on)                 │
  • Receive input                                            │
  • Task classification                                      │
  • Basic chat (no reasoning needed)                         │
     │                                                       │
     ▼  (if reasoning/code/research required)                │
[Orchestrator]  deepseek-r1:7b-q4_K_M  (GPU, on-demand)     │
  • Complex task analysis                                    │
  • Decide which agent to call                               │
  • Manage tool chain                                       │
     │                                                       │
     ├──────────────┬─────────────────┬───────────────────  │
     ▼              ▼                 ▼                   ▼ │
[Coder]        [Researcher]      [Tool Agent]       [Game Agent]│
qwen2.5-coder  qwen3:7b-q4_K_M   scripts/bash       (specialized)│
:7b-q4_K_M     + Gemini Search   (deterministic)    Unity/UE/Godot│
GPU swap       GPU swap          CPU                 GPU swap   │
     │              │                 │                   │   │
     └──────────────┴─────────────────┴───────────────────┘   │
                              │                               │
                              ▼                               │
                    [ChromaDB RAG Layer]                      │
                    Chroma / Qdrant local                     │
                    (project knowledge only)                  │
                              │                               │
                              └───────── Result ─────────────┘
```

### 1.2 Model-to-Hardware Mapping

| Agent | Model | Hardware | When to Load |
|---|---|---|---|
| Chat Agent | `llama3.2:3b` | **CPU** — Always on | On Telegram receive |
| Orchestrator | `deepseek-r1:7b-q4_K_M` | **GPU** | Complex tasks |
| Coder | `qwen2.5-coder:7b` | **GPU** (swap) | Generate / fix code |
| Researcher | `qwen3:7b-q4_K_M` | **GPU** (swap) | Docs / RAG / research |
| Vision | `gemma3:4b-it-q4_K_M` | **GPU** (swap) | Screenshot analysis |
| Tool Agent | Python/Bash Scripts | **CPU** | Build, parse log, files |
| Web Search | Gemini API free-tier | **Cloud** | External info |

### 1.3 Absolute VRAM Rules (RTX 4060 8GB)

```
❌ DO NOT load more than one 7B+ model on the GPU simultaneously.
✅ Strategy: Sequential Agent Execution

Standard Workflow:
  1. ollama stop <current_model>   ← Unload immediately
  2. ollama run <new_model>        ← Load required model
  3. Process task
  4. If idle > 5 minutes → ollama stop to free VRAM
```

---

## 🤖 PART 2 — AGENT ORCHESTRATION (OpenClaw)

### 2.1 Standard OpenClaw Config

```json
{
  "strategy": "sequential",
  "max_active_gpu_models": 1,
  "fallback_cpu": true,
  "auto_unload_idle_seconds": 300,
  "agents": {
    "chat": {
      "model": "llama3.2:3b",
      "device": "cpu",
      "always_on": true
    },
    "orchestrator": {
      "model": "deepseek-r1:7b-q4_K_M",
      "device": "gpu",
      "always_on": false
    },
    "coder": {
      "model": "qwen2.5-coder:7b",
      "device": "gpu",
      "always_on": false
    },
    "vision": {
      "model": "gemma3:4b-it-q4_K_M",
      "device": "gpu",
      "always_on": false
    }
  }
}
```

### 2.2 Orchestration Logic

```python
async def run_agent(task_type: str, prompt: str) -> str:
    # 1. Unload old GPU model
    # 2. Load new GPU model via Ollama
    # 3. Execute prompt
    # 4. Return result
```

---

## 🔐 PART 3 — SECURITY & COMPLIANCE

### 3.1 Sandbox Directive
Agents are strictly confined to `PROJECT_ROOT`. Accessing `/etc`, `/usr`, or Windows drives (`/mnt/c`) is a critical security violation.

### 3.2 Blacklist
- **Extensions**: `.so`, `.dll`, `.exe`, `.pak`, `.bin`, `.key`, `.pem`.
- **Directories**: `.git`, `.venv`, `node_modules`, `chroma_db`.

---

## ⚡ PART 4 — QUICK AUDIT CHECKLIST

```
1. Is the file within PROJECT_ROOT?
2. Is the extension on the ALLOWED list?
3. Is a GPU model already active? (If yes, unload first)
4. Does the prompt contain internal secrets/IP?
```
