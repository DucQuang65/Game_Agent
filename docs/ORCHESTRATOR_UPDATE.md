# 🔄 Orchestrator Routing — Full Update for v4.0

## Complete Agent Map (v4.0 — Cloud-Local Hybrid)

```
                        ┌─────────────────────────────────────────────┐
                        │             TASK ROUTING TABLE              │
                        └─────────────────────────────────────────────┘

 Input                   Agent               Model            Device
 ─────────────────────   ─────────────────   ──────────────   ──────
 Chat / Small Talk    →  chat-agent          llama3.2:3b      CPU
 Task Analysis        →  orchestrator        qwen-3.6-plus    Cloud (OpenRouter)
 Code / Debug         →  coder-agent         qwen2.5-coder:7b GPU (swap)
 Research / Docs      →  researcher-agent    qwen-3.6-plus    Cloud
 Build / Run script   →  tool-agent          (python script)  CPU
 Web search           →  OpenRouter/DDG      (cloud/local)    Cloud/CPU
 ─── NEW ─────────────   ─────────────────   ──────────────   ──────
 Query old context    →  memory-layer        all-MiniLM       CPU (embed)
 Read error logs      →  log-parser          (regex/script)   CPU
 Screenshot analysis  →  vision-agent        gemma3:4b        GPU (swap)
```

## OpenClaw Config (v4.0)

```json
{
  "strategy": "sequential",
  "max_active_gpu_models": 1,
  "auto_unload_idle_seconds": 300,
  "fallback_cpu": true,
  "gpu_budget_gb": 8,

  "agents": {
    "chat": {
      "model": "llama3.2:3b",
      "device": "cpu",
      "always_on": true,
      "context": 2048
    },
    "orchestrator": {
      "model": "qwen-3.6-plus:free",
      "device": "cloud",
      "always_on": false,
      "context": 1000000
    },
    "coder": {
      "model": "qwen2.5-coder:7b",
      "device": "gpu",
      "always_on": false,
      "context": 4096
    },
    "researcher": {
      "model": "qwen-3.6-plus:free",
      "device": "cloud",
      "always_on": false,
      "context": 1000000,
      "web_search_fallback": "duckduckgo"
    },
    "vision": {
      "model": "gemma3:4b-it-q4_K_M",
      "device": "gpu",
      "always_on": false,
      "context": 2048,
      "triggers": ["photo", "screenshot", "/vision"]
    },
    "log_parser": {
      "model": null,
      "device": "cpu",
      "always_on": false,
      "script": "tools/log_parser.py",
      "triggers": ["log", "error", "fix error", "/log"]
    },
    "memory": {
      "model": "nomic-embed-text",
      "device": "cpu",
      "always_on": true,
      "db_path": "${PROJECT_ROOT}/data/chroma_db"
    }
  },

  "pipeline": {
    "pre_process": ["memory.query_context"],
    "post_process": ["memory.save_session"]
  }
}
```

## Full Pipeline — Error Fix Flow

```
User: "fix this Unity error"
         │
         ▼
[Chat Agent - CPU]
  Receive input, classify → "log_fix"
         │
         ▼
[Log Parser - CPU]  ← LOGGING.md
  Read Logs/Editor.log
  Parse 5 most recent errors
  Format concise prompt
         │
         ▼
[Memory Layer - CPU] ← MEMORY.md
  Query "bug_history" → find previous similar fixes
  Add context to prompt
         │
         ▼
[Coder Agent - GPU] ← CORE.md
  Receive: errors + memory context
  Generate patch code
         │
         ▼
[Memory Layer - CPU]
  Save result to "bug_history"
         │
         ▼
[Telegram] → User receives patch
```

## VRAM Budget Overview

```
State             Model active           VRAM Used
──────────────    ─────────────────────  ──────────
Idle              llama3.2:3b (CPU)      ~0 GB GPU
Chat              llama3.2:3b (CPU)      ~0 GB GPU
Coding            qwen2.5-coder:7b Q4   ~5.5 GB
Orchestrator      qwen-3.6-plus (Cloud)  ~0 GB GPU
Vision            gemma3:4b Q4           ~4.0 GB
Embedding (RAG)   all-MiniLM (CPU)       ~0 GB GPU
Log Parse         script (CPU)           ~0 GB GPU
```

> RTX 4060 8GB: Safe for all scenarios — no model exceeds 6GB.

## Additional Dependencies

```bash
# Memory layer
pip install chromadb sentence-transformers --break-system-packages

# Log parser
pip install watchdog --break-system-packages

# Vision
pip install Pillow httpx --break-system-packages
sudo apt install scrot imagemagick  # Screenshot tools

# Ollama — pull vision model
ollama pull gemma3:4b-it-q4_K_M
ollama pull nomic-embed-text        # Embedding — zero GPU VRAM cost
```
