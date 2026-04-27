# Game Agent - Working Memory & Developer Guidelines

This file (`AI_GUIDE.md`) serves as the working memory and interaction guideline for the open-source Game Agent multi-model system. It is designed to be read by all AI agents (Cloud & Local) upon initialization.

## Knowledge Transfer Model

This project implements a "Cloud-to-Local Knowledge Waterfall":
1. **Cloud Orchestrators** (e.g., Qwen 3.6 Plus, Gemini) tackle high-context, complex architecture, and R&D tasks.
2. **Knowledge Extraction**: Successful scripts, verified shaders, and project paradigms are extracted and saved into the `memory/` directory as markdown files.
3. **Local Specialists** (e.g., Ollama Qwen 2.5 Coder, Gemma) read these files via the OpenClaw `boot-md` hook. This allows local-only, VRAM-constrained models to execute tasks perfectly without needing to "re-learn" complex logic.

## Project Structure & Memory Bank

When writing code or searching for context, agent models must prioritize referring to these files:

*   `memory/GODOT_4_6_PLUS_API_STANDARD.md`: The primary reference for GDScript syntax. Do not use Godot 3.x or legacy 4.0 API patterns.
*   `memory/SHADER_WATER.md`: Production-ready Vulkan water shader (Godot 4.6+ compatible).
*   `AI_Training/`: Data sets and scripts for local fine-tuning/LoRA (v4.0).
*   `secrets/`: **DO NOT READ OR WRITE.** This folder is git-ignored and contains private API keys.

## Privacy & Public Repository Standards

As an open-source project, all documentation and memory files must remain **anonymized**:
*   Do **NOT** hardcode user names (e.g., `/home/username/`). Use `~` or `$HOME`.
*   Do **NOT** log or save API keys (`sk-ant-xxx`, `sk-or-v1-xxx`, etc.) anywhere other than ignored `.json` configs or the `secrets/` dir.
*   Keep comments and instructions generic and broadly applicable to any developer utilizing this system.

## Godot 4.6+ Technical Guidelines
*   **Performance:** Optimize for mid-range hardware (e.g., 8GB VRAM GPUs like the RTX 4060). Use SDFGI carefully, prefer TAA over MSAA, and optimize Shader vertex loads.
*   **Scripts:** Use `@export` for inspector variables, strongly type everything (`var health: int = 100`), and use `Callable` for signals.
