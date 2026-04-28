---
type: documentation
target_engine: Godot 4.6, Godot 4.7, Unity 6
status: active
---

# 🧠 System Protocol: Game Agent OS

An autonomous, multi-model AI agent system designed for professional game development. Built to run locally on consumer hardware (RTX 4060, 8GB VRAM) using WSL2 and Ollama, the system provides an intelligent assistant capable of self-learning, web research, code generation, and project management through a Telegram interface.

## Architecture

The system operates as a multi-agent orchestration platform powered by [OpenClaw](https://github.com/nichochar/openclaw), with specialized models handling different aspects of game development:

| Agent | Model | Role |
|---|---|---|
| **Executor** | `gamedev-agent` (Qwen 2.5 Coder 7B) | Primary code generation, tool execution, and technical implementation |
| **Strategist** | `deepseek-r1:7b` | Step-by-step reasoning, planning, and self-correction |
| **Communicator** | `llama3.2:3b` | Lightweight chat summarization and user interaction |
| **Embedder** | `nomic-embed-text` | Semantic search and RAG memory indexing |

## Tech Stack

- **Game Engines:** Godot 4.6/4.7 (GDScript, C#), Unity 6
- **Graphics:** Vulkan, Jolt Physics
- **AI Runtime:** Ollama (local inference), OpenClaw (orchestration)
- **Training:** Unsloth (QLoRA fine-tuning), Hugging Face Transformers
- **Interface:** Telegram Bot (DM-based interaction)
- **Memory:** ChromaDB / Session-based RAG with `nomic-embed-text`

## Key Features

- **Self-Learning Agent:** The agent can autonomously search the web, read documentation, and update its own memory (`memory/`) to improve future responses.
- **English-First Communication:** Defaults to English for all interactions. Automatically switches to Vietnamese if the user initiates conversation in Vietnamese.
- **Strict Godot 4.6+ Standard:** Enforces modern Godot 4.x API patterns (e.g., `instantiate()`, `MOUSE_BUTTON_LEFT`, signal callable syntax) via a built-in coding standard (`memory/GODOT_4_6_PLUS_API_STANDARD.md`).
- **Tool Safety:** The agent is prohibited from outputting raw JSON or tool calls in chat. All responses are direct, human-readable text.
- **VRAM-Optimized:** Configured with a 16k context window and 4k max output tokens to ensure stable performance on 8GB GPUs.

## Project Structure

```
Game_Agent/
├── openclaw_configs/       # Portable OpenClaw configuration backups
│   ├── gamedev-agent.Modelfile
│   └── agents/             # Agent persona definitions
├── training/               # Fine-tuning environment (QLoRA)
│   ├── data/               # SFT datasets (gamedev_sft_*.jsonl)
│   ├── scripts/            # Training scripts (train_gemma4.py)
│   └── outputs/            # Model checkpoints and GGUF exports
├── study/                  # Cloned reference repositories
│   ├── tps-demo/           # Godot TPS Demo
│   ├── godot-jolt/         # Jolt Physics for Godot
│   ├── GodotGame/          # Chickensoft C# Game Template
│   ├── FPSSample/          # Unity FPS Sample
│   └── ...                 # Additional study repos
├── prompt_master/          # IDE Agent prompt schemas
├── mcp/                    # Model Context Protocol integrations
├── langgraph/              # LangGraph orchestration experiments
├── memory/                 # Project knowledge base
└── AI_Training/            # Skills and training data
    └── skills/             # Specialized skill definitions
```

## Study Repositories

The agent uses the following cloned repositories as "gold standard" references for code generation:

### Godot 4.6+ (GDScript / Jolt)
- **TPS Demo:** Third-person shooter template
- **Godot Jolt:** Jolt Physics integration
- **Chickensoft GodotGame:** Professional C# architecture with CI/CD
- **LibreQuake:** Retro FPS reference
- **The Mirror:** Large-scale Godot application

### Unity 6 (C# / URP / Multiplayer)
- **FPS Sample:** First-person shooter reference
- **Boat Attack:** Graphics and URP showcase
- **Boss Room:** Multiplayer co-op sample

### Advanced Graphics & Patterns
- **Vulkan Samples:** Low-level rendering reference
- **Arcade / Pyglet:** Python gamedev patterns

## Training

The system supports QLoRA fine-tuning for specialized game development models:

```bash
cd ~/Game_Agent/training
source .venv/bin/activate
python scripts/train_gemma4.py \
  --dataset data/gamedev_sft_10.jsonl \
  --base-model unsloth/gemma-4-E4B-it-unsloth-bnb-4bit \
  --output-dir outputs/gemma-4-e4b-gamedev-v1
```

See [`training/README.md`](training/README.md) for detailed setup instructions.

## Recommended External Tools

The following open-source tools are recommended for extending the agent's capabilities:

| Tool | License | Purpose |
|---|---|---|
| [Open-Game-Agent](https://github.com/colinlevine/open-game-agent) | MIT | MCP + RAG framework for memory-driven game AI |
| [AgentScope](https://github.com/agentscope-ai/agentscope) | Apache 2.0 | Multi-agent orchestration with debate and voice support |
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) | MIT | Autonomous AI software engineer (sandboxed execution) |
| [Aider](https://github.com/Aider-AI/aider) | Apache 2.0 | Terminal-based AI pair programming with Git integration |
| [Mem0](https://github.com/mem0ai/mem0) | Apache 2.0 | Intelligent memory layer for AI agents |
| [Moe](https://github.com/google-deepmind/moe) | Apache 2.0 | Mixture of Experts implementation reference |

## Local Setup & Portability

To set up the project on a new machine:

1. **Clone the repository**: `git clone <repo-url>`
2. **Environment**: Ensure you have Python 3.10+, Node.js, and Ollama installed.
3. **Secrets**: Create a `secrets/` directory in the root. This directory is ignored by Git. Store your API keys and sensitive tokens here.
4. **Configuration**: 
   - Copy `openclaw.json.example` to `~/.openclaw/openclaw.json` (or your preferred location) and fill in your tokens.
   - Run `python scripts/bootstrap_agent.py` to pull models and initialize reference repositories.
5. **Paths**: All scripts are designed to be relative to the project root. Avoid hardcoding absolute paths in new scripts.

## Requirements

- **OS:** Ubuntu (WSL2) or native Linux
- **GPU:** NVIDIA RTX 4060 (8GB VRAM) or equivalent
- **CPU:** Intel i5-13500 or equivalent
- **Software:** Ollama, Node.js (for OpenClaw), Python 3.10+ (for training), Godot 4.6+

## License

This project is for personal and educational use. All study repositories retain their original licenses. Training datasets are derived from publicly available, open-source materials.