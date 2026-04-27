# COMPREHENSIVE SKILL CATALOG: GAME AGENT OS (v6.5)

This document is the "Skill Dictionary" (Skill Catalog) containing a list of all tools, functions, and roles (privileges) that Game Agent OS currently possesses.

---

## 1. STUDIO HIERARCHY (SPECIALIST ROLES)
Inherited from `Claude-Code-Game-Studios`, the Agent can take on the following roles within a Game Studio to direct work:
1. **Director (Creative / Technical Director)**:
   - *Tasks*: Manages project vision, approves workflows, controls quality and risks (especially VRAM constraints).
2. **Lead Architect**:
   - *Tasks*: Draws architectural diagrams, designs directory structures, selects Patterns (such as ECS, Signal-driven) for the project.
3. **Producer**:
   - *Tasks*: Decomposes work into Epics/Stories, manages progress, and reviews completed Tasks.
4. **Specialist Coder**:
   - *Tasks*: Directly writes code, handles game logic, physics, networking, and NPC AI.
5. **QA Validation (Testing Engineer)**:
   - *Tasks*: Runs Unit Tests, monitors performance, and reviews code to ensure Clean Code and stability.
6. **Game Designer**:
   - *Tasks*: Builds gameplay mechanisms, evaluates "player satisfaction" (Player Evaluator).

---

## 2. GODOT CORE SKILLS (ADVANCED GODOT SKILLS)
Integrated from `Open-Code-Godot-Studio`, focusing on Godot 4.6+:
1. **Godot GDScript Master**: Writes standard GDScript 2.0 code, optimizing Typing (`var x: int`) and Signal Callables.
2. **Godot C# / .NET 8 Expert**: Integrates C# into Godot for complex logic, using async/await without blocking the Main Thread.
3. **GDExtension Specialist**: Handles low-level language bridges (C++/Rust) for systems requiring extreme performance.
4. **Godot Shader Wizard**: Programs GLSL / Godot Shaders (Spatial/CanvasItem) for graphics (Forward+).
5. **Godot Physics Tuner**: Optimizes physics systems (Jolt Physics, Collision Matrix).
6. **Godot UI/UX Builder**: Uses flexible Control Nodes, creates responsive interfaces and Animations.

---

## 3. ENGINE BRIDGES (MCP TOOLS FOR DIRECT EDITOR CONTROL)
Through `Unity-MCP` and `godot-mcp` connections, the Agent can perform "Magic Hands" operations directly within the Engine:
1. **Assets & Files**:
   - `assets-find` / `assets-copy` / `assets-get-data`: Search for, copy, and retrieve data (Properties, Serialized fields) for any script, material, or prefab file.
   - `assets-prefab-create` / `assets-prefab-instantiate`: Automatically create or instantiate Prefab/Scene templates into the level.
2. **GameObjects & Nodes**:
   - `gameobject-create` / `gameobject-destroy`: Rapidly initialize Node/GameObject structures.
   - `gameobject-component-add` / `gameobject-modify`: Attach scripts, rename, change tags/layers of entities in the scene.
   - `set-transform`: Precisely align Coordinates (Position), Rotation, and Scale via chat commands.
3. **Scene Management**:
   - `scene-create` / `scene-open` / `scene-save`: Directly open and save working Scenes.
4. **Visual & Debug**:
   - `screenshot-game-view` / `screenshot-scene-view`: Requests the Editor to take a screenshot and send it to the Agent (Vision Model) for UI or lighting analysis.
   - `run_tests`: Executes the Test Runner and collects error logs.

---

## 4. GATEKEEPER SKILLS (ADVANCED ELITE SKILLS)
Filtered from 380 skills according to "Zero Bloat/VRAM Safe" standards, these tools trigger reasoning logic:
1. **Performance-Profiler**: Identifies computation bottlenecks (CPU / GPU).
2. **Memory-Guardian**: Manages VRAM Bloat and prevents memory leaks, especially critical for RTX 4060 configurations.
3. **Math-Geometry-Pro**: Brain tool for solving Vectors, Matrix math, and trigonometry (Cos/Sin) for trajectories or FOV.
4. **Clean-Code-Reviewer**: Provides rigorous reviews to enforce SOLID, DRY, and KISS principles.
5. **Navigation-Master**: Sets up smooth A*, NavigationAgent3D / NavMesh for NPC swarms.
6. **State-Machine-Generator**: Designs Finite State Machine (FSM) systems and Behavior Trees for complex AI logic.
7. **Refactoring-Wizard**: Transforms "Spaghetti" code into decoupled modules.
8. *(Plus specific skills supporting Security, Encryption, Network Sync, CI/CD Actions, etc., automatically pulled up via RAG when needed)*.

---

## 5. WORKFLOW COMMANDS (SLASH COMMANDS)
Users can call project management commands directly in the Terminal:
- `/start` : Begins a project, sets up the repo and basic structure.
- `/brainstorm` : Collects multiple perspectives from different Personas to find a direction for a Feature.
- `/setup-engine` : Configures core settings for Unity or Godot.
- `/sprint-plan` : Breaks down a large system (Epic) into manageable Stories.
- `/design-review` : Evaluates system design before coding.
- `/code-review` : Requests an Agent Audit to point out security or logic errors on a code branch.
