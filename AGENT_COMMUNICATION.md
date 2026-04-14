# Agent Communication & Working Memory (v4.0)

## Project Context
- **Name**: Game_Agent
- **Version**: 4.0
- **Engine**: Godot 4.6+ (Vulkan Forward+), Unity 6
- **Hardware**: RTX 4060 8GB VRAM (optimized for < 6.0GB usage)

## Key References
- **Engine Standard**: [GODOT_4_6_PLUS_API_STANDARD.md](memory/GODOT_4_6_PLUS_API_STANDARD.md) — Godot 4.6+ strict typing and API rules.
- **Shader Reference**: [SHADER_WATER.md](memory/SHADER_WATER.md) — Vulkan-compatible water shader.
- **Compliance**: [COMPLIANCE.md](AI_Training/skills/COMPLIANCE.md) — IP and EULA boundaries.
- **Routing**: [ROUTING.md](AI_Training/agents/ROUTING.md) — Agent routing and VRAM budget.

## Session Initialization
This file is the primary context document for the Agent. Read it at the start of every session to load the current architecture, file structure, and safety constraints.

## Conventions
1. **Paths**: Never use absolute local paths. Use `PROJECT_ROOT` or relative paths.
2. **Naming**: Use `ALL_CAPS` for all knowledge files in `memory/` and `skills/`.
3. **Archiving**: Move raw data dumps and superceded files to `_archive/`.
