# 📄 Orchestrator Routing — Full Update with 3 New Modules

## Complete Agent Map (after adding Memory + LogParser + Vision)

```
                        ┌─────────────────────────────────────────────────┐
                        │             TASK ROUTING TABLE              │
                        └─────────────────────────────────────────────────┘

 Input                   Agent               Model            Device
 ─────────────────────   ─────────────────   ──────────────   ──────
 General chat        →  chat-agent          llama3.2:3b      CPU
 Task analysis       →  orchestrator        deepseek-r1:7b   GPU
 Write/fix code      →  coder-agent         qwen2.5-coder:7b GPU (swap)
 Read docs/RAG       →  researcher-agent    qwen3:7b         GPU (swap)
 Build/run script    →  tool-agent          (python script)  CPU
 Web search          →  gemini-api          gemini-flash     Cloud
 ─── NEW ─────────────   ─────────────────   ──────────────   ──────
 Query old context   →  memory-layer        all-MiniLM       CPU (embed)
 Read error log      →  log-parser          (regex/script)   CPU
 Analyze screenshot  →  vision-agent        gemma3:4b        GPU (swap)
```

## Complete OpenClaw Configuration (v2.1)

```json
{
  "strategy": "sequential",
  "max_active_gpu_models": 1,
  "auto_unload_idle_seconds": 300,
  "fallback_cpu": true,
  "context_length": 4096,
  "gpu_budget_gb": 8,

  "agents": {
    "chat": {
      "model": "llama3.2:3b",
      "device": "cpu",
      "always_on": true,
      "context": 2048
    },
    "orchestrator": {
      "model": "deepseek-r1:7b-q4_K_M",
      "device": "gpu",
      "always_on": false,
      "context": 4096
    },
    "coder": {
      "model": "qwen2.5-coder:7b",
      "device": "gpu",
      "always_on": false,
      "context": 4096
    },
    "researcher": {
      "model": "qwen3:7b-q4_K_M",
      "device": "gpu",
      "always_on": false,
      "context": 4096,
      "web_search_fallback": "gemini_api"
    },
    "vision": {
      "model": "gemma3:4b-it-q4_K_M",
      "device": "gpu",
      "always_on": false,
      "context": 2048,
      "triggers": ["photo", "screenshot", "image", "/vision"]
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

## Full Pipeline with 3 New Modules

**Scenario A — Bug Fix Request:**
```
User: "fix error in unity"
         │
         ▼
[Chat Agent - CPU]
  Receive input, classify → "log_fix"
         │
         ▼
[Log Parser - CPU]  ← SKILL_log_parser.md
  Read Logs/Editor.log
  Parse 5 most recent errors
  Format compact prompt
         │
         ▼
[Memory Layer - CPU] ← SKILL_memory.md
  Query "bug_history" → retrieve similar past fixes
  Inject context into prompt
         │
         ▼
[Coder Agent - GPU] ← SKILL.md (coder)
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

**Scenario B — Screenshot Analysis:**
```
User: [sends screenshot of broken Unity UI]
         │
         ▼
[Chat Agent - CPU]
  Detect photo → route "vision"
         │
         ▼
[Orchestrator - GPU]  unload → load Gemma3
         │
         ▼
[Vision Agent - GPU] ← SKILL_vision.md
  Resize image
  Gemma3 analyzes frame
  Return error description + suggestions
         │
         ▼
  (if code fix needed) → route to Coder Agent (GPU swap)
         │
         ▼
[Telegram] → User receives result
```

## VRAM Budget Summary

```
State              Active Model             VRAM Used
──────────────     ─────────────────────    ──────────
Idle               llama3.2:3b (CPU)        ~0 GB GPU
General chat       llama3.2:3b (CPU)        ~0 GB GPU
Coding             qwen2.5-coder:7b Q4      ~5.5 GB
Research           qwen3:7b Q4              ~4.5 GB
Reasoning          deepseek-r1:7b Q4        ~4.5 GB
Vision             gemma3:4b Q4             ~4.0 GB
Embedding (RAG)    all-MiniLM (CPU)         ~0 GB GPU
Log Parsing        script (CPU)             ~0 GB GPU
```

> RTX 4060 8GB: All scenarios are safe — no model exceeds 6 GB VRAM allocation.

## Install Additional Dependencies

```bash
# Memory layer
pip install chromadb sentence-transformers --break-system-packages

# Log parser
pip install watchdog --break-system-packages

# Vision
pip install Pillow httpx --break-system-packages
sudo apt install scrot imagemagick  # Screenshot capture tools

# Ollama — pull vision models
ollama pull gemma3:4b-it-q4_K_M
ollama pull nomic-embed-text        # Embedding model — zero GPU VRAM
```
