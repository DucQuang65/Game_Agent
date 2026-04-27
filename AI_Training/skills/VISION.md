---
type: technical_standard
target_engine: Godot 4.6, Godot 4.7, Unity 6
status: verified
---

# 🛠️ Agent Skill: Vision & Screenshot Analysis

# 👁️ Vision Agent — Screenshot Analysis (Gemma3)

## Purpose
Handles cases where logs aren't enough—visual bugs visible on screen:
- Broken or overlapping UI layouts.
- Incorrect Scene Hierarchy nodes or abnormal Inspector values.
- Shader artifacts and visual glitches.

---

## 🧠 Model & VRAM
- **Model**: `gemma3:4b-it-q4_K_M` (~3.5GB VRAM — fits RTX 4060).
- **Rule**: Unload current model (Ollama stop) before loading Gemma3.

---

## 📸 Triggers
- Triggered by Telegram message with an image attachment.
- Tool Agent automatic screenshot (`/vision`).
