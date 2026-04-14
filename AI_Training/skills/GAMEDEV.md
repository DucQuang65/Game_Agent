---
type: technical_standard
target_engine: Godot 4.7, Unity 6
status: verified
---

# 🛠️ Agent Skill: Game Development Patterns

## Purpose
This skill provides production-ready architectural patterns for game development in Godot 4.7. It ensures the Agent generates scalable, performant code following industry-standard design patterns.

---

## 🎮 Core Architecture Patterns

### 1. State Machine (Finite State Machine)
**Use for**: NPC AI, Player states, UI flow, Game phases.

```
StateMachine (Node)
├── StateIdle
├── StateShopping
├── StateQueueing
├── StatePaying
└── StateLeaving
```

**Rules**:
- Each state extends a base `State` class with `_enter()`, `_exit()`, `_update()`.
- Transitions use `StringName` identifiers (e.g., `&"Shopping"`).
- States never directly reference other states — always go through `state_machine.transition_to()`.

### 2. Object Pooling
**Use for**: Bullets, particles, NPCs, collectibles — anything spawned/destroyed frequently.

**Rules**:
- Pre-instantiate all objects in `_ready()`.
- Never call `instantiate()` or `queue_free()` during gameplay.
- Toggle visibility + `set_process(false)` / `set_physics_process(false)` to "despawn".
- Pool size = max expected concurrent objects + 10% buffer.

### 3. Singleton/Autoload Pattern
**Use for**: Game Manager, Audio Manager, Save System, Event Bus.

**Rules**:
- Register via Project Settings → Autoload.
- Access pattern: `GameManager.current_score` (direct static reference).
- Keep Autoloads lightweight — they persist across scene changes.

---

## 🏗️ Scene Tree Standards

### Player Controller (3D FPS)
```
Player (CharacterBody3D)
├── CollisionShape3D (Capsule)
├── Head (Node3D)
│   └── Camera3D
├── InteractionRaycast (RayCast3D)
├── MeshInstance3D (Player model)
└── AnimationPlayer
```

### NPC with AI
```
NPC (CharacterBody3D)
├── NavigationAgent3D
├── CollisionShape3D
├── MeshInstance3D (LOD)
├── AnimationPlayer
├── InteractionZone (Area3D)
└── Brain (StateMachine)
```

---

## ⚡ Performance Rules (50+ NPCs @ 60fps on RTX 4060)

| Technique | Savings | When to Use |
|---|---|---|
| Staggered pathfinding | ~80% CPU spikes | > 10 NPCs with NavigationAgent3D |
| Object pooling | Eliminates GC stutter | Any spawn/destroy loop |
| LOD meshes (2-level) | ~60% GPU draw calls | > 20 visible meshes |
| `distance_squared_to()` | Avoids `sqrt()` per frame | All distance comparisons |
| Off-screen culling | ~40% CPU+GPU | NPCs outside camera frustum |
| Single NavigationRegion3D | Zero extra nav computation | Always (one navmesh per level) |

---

## 📦 Inventory System Pattern

**Architecture**: `Dictionary[StringName, int]` for O(1) lookup.

**Required Signals**:
- `item_added(item_id: StringName, quantity: int)`
- `item_removed(item_id: StringName, quantity: int)`
- `inventory_changed`
- `inventory_full`

**Rules**:
- Use `StringName` for item IDs (interned, zero-allocation).
- Use `@export var max_slots: int` for Inspector configuration.
- Provide `get_slot_items() -> Array[Dictionary]` for UI binding.

---

## 🧪 Code Quality Checklist
```
1. Is every variable statically typed? (var x: int = 5, not var x = 5)
2. Does every function have a return type? (func foo() -> void:)
3. Are signals using .emit() syntax? (not emit_signal())
4. Is move_and_slide() called without arguments?
5. Is preload() used instead of load() for known resources?
6. Are physics calculations in _physics_process(), not _process()?
```
