---
type: technical_standard
status: verified
---

# 🛠️ System Protocol: Environment Portability

To migrate this Agent to another machine while preserving its "intelligence," follow these steps:

## 1. Push Source Code to GitHub
Ensure you have `git add` and `push` the entire `Game_Agent` folder. Critical configuration files are bundled in the `openclaw_configs/` directory.

## 2. Setup on a New Machine (One-Command Setup)
After installing Ollama and OpenClaw on the new machine, run:

```bash
cd Game_Agent
python3 scripts/bootstrap_agent.py
```

**This script will automatically:**
- Copy Agent definitions (`CODER`, `COORDINATOR`, `TELEGRAM`) into `~/.openclaw/`.
- Generate `openclaw.json` from the template.
- `ollama pull` all required models (Qwen 2.5 Coder, Llama 3.2, Gemma 3).
- Re-clone study repositories into `study/` (Godot, Vulkan, Unity...).

## 3. Security Configuration (Mandatory)
After running the script, you **MUST** open `~/.openclaw/openclaw.json` and fill in:
- `botToken`: Your Telegram Bot token.
- `apiKey`: OpenRouter API Key (for Cloud orchestration).
- `allowFrom`: Your Telegram Chat ID.

## 4. Verification (Dry-run)
To verify before executing for real, add the `--dry-run` flag:
```bash
python3 scripts/bootstrap_agent.py --dry-run
```

---
**Note:** Always ensure the new machine has sufficient VRAM (RTX 4060 8GB or higher) for smooth model execution.
