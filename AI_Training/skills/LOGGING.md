---
type: technical_standard
target_engine: Godot 4.6, Godot 4.7, Unity 6
status: verified
---

# 🛠️ Agent Skill: Log Parsing & Auto-Fix

# 🔧 Log Parser — Unity / Godot / Unreal Auto-Fix

## Purpose
Eliminate manual log pasting by automating:
1. Reading the latest project log (.godot/logs, Editor.log, Saved/Logs).
2. Classifying errors (compile, runtime, shader, physics).
3. Extracting technical context for the Coder Agent to generate patches.

---

## 📋 Engine Support
- **Unity**: Parses `Editor.log` (CS0246, NullRef, MissingRef).
- **Godot**: Parses `res://` errors and C# compiler output.
- **Unreal**: Parses `UnrealEditor.log`, ShaderCompileError.

---

## 🤖 Integration
- `/log` (Telegram): View the 10 most recent errors.
- `fix [engine] error`: Read logs and generate a code fix automatically.
