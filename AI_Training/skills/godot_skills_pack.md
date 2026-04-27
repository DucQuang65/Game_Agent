# 🛠️ Specialized Skill Pack: Godot Game Studio

This skill pack is derived from `Open-Code-Godot-Studio` and is optimized for Godot 4.6+ development on the Game_Agent OS.

## 🎭 Studio Hierarchy Personas
- **Creative Director**: Guards the game vision and ensures consistency.
- **Technical Director**: Oversees architecture, VRAM management, and Vulkan performance.
- **Producer**: Manages sprint tasks, epics, and story completion.
- **Game Designer**: Balances gameplay mechanics and player evaluation.

## 💻 Technical Specialists
### Godot-GDScript
- **Standards**: Static typing (`var x: int = 0`), Signal callable syntax (`signal.connect(_on_callback)`).
- **Optimization**: Use `RenderingServer` for low-level draws.

### Godot-C# (.NET 8)
- **Patterns**: Dependency Injection (via Chickensoft/GodotGame), Async/Await for non-blocking I/O.
- **Compliance**: Follows modern Godot C# API conventions.

### GDExtension Specialist
- **Focus**: Performance-critical modules in C++ or Rust.
- **Integration**: Managing `.gdextension` configurations and cross-platform builds.

## ⚡ Workflow Commands (Slash-style)
- **/start**: Initialize a new game project or feature epic.
- **/brainstorm**: Multi-perspective brainstorming for game mechanics.
- **/setup-engine**: Configure the Godot project settings (Vulkan, Window, Physics).
- **/evaluator**: Evaluate a GDD from the player's perspective.

## 🧪 Design Validation
- **Player Evaluator**: Analyze if a feature is "fun" or "frustrating" before implementation.
- **Prototype Mode**: Rapid iteration focused on feel over cleanup.
