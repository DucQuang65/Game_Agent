---
type: technical_standard
status: verified
---

# 🛠️ System Protocol: Environment Portability

This document describes how to migrate the agent system to a new machine while preserving all configured intelligence and memory state.

## 1. Push Source Code to GitHub
Ensure you have run `git add` and `push` for the entire `Game_Agent` directory. All critical configuration files are consolidated under `openclaw_configs/`.

## 2. New Machine Setup (One-Command)
After installing Ollama and OpenClaw on the new machine, run the bootstrap script:

```bash
cd Game_Agent
python3 scripts/bootstrap_agent.py
```

**The script will automatically:**
- Copy agent definitions (`CODER`, `COORDINATOR`, `TELEGRAM`) to `~/.openclaw/`.
- Generate `openclaw.json` from the bundled template.
- Run `ollama pull` for all required models (Qwen 2.5, DeepSeek R1, Llama 3.2).
- Clone reference repositories under `study/` (Godot, Vulkan, Unity, etc.).

## 3. Security Configuration (Required)
After running the script, you **MUST** open `~/.openclaw/openclaw.json` and populate the following fields:
- `botToken`: Your Telegram Bot token.
- `apiKey`: Google API Key (required only if using Gemini).
- `allowFrom`: Your Telegram user ID for access control.

## 4. Dry-Run Verification
To preview all actions without making changes, pass the `--dry-run` flag:
```bash
python3 scripts/bootstrap_agent.py --dry-run
```

---
**Note:** Ensure the target machine has sufficient VRAM (RTX 4060 8GB or higher) to run all configured local models at acceptable inference latency.
