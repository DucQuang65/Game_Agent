# 🏗️ Architecture Design: Checkout Manager (v1.0)
**Project**: Supermarket Simulator
**Standard**: Godot 4.7 / C# & GDScript Hybrid
**Skill Persona**: Senior-Architect

## 1. Overview
The `CheckoutManager` is the central orchestrator for the supermarket's economic throughput. It manages NPC queues, payment processing, and economy signaling.

## 2. Technical Stack
- **Node Type**: `Node3D` (Manager) with `Area3D` for queue detection.
- **Pattern**: Signal-Driven Observer (Zero-Polling).
- **Optimization**: "Ghost NPC" pooling for VRAM safety (only active NPCs have full meshes).

## 3. Component Hierarchy
```text
CheckoutManager (Node)
├── Counter_1 (Node3D)
│   ├── StaticBody3D (Table)
│   └── QueuePath (Path3D)
├── Counter_2 (Node3D)
├── Counter_3 (Node3D)
└── Timer (EconomyBatchUpdate)
```

## 4. NPC Queue & VRAM Optimization
### The "LOD Interaction" Pattern:
- **Outside Interaction Range**: NPCs are simplified state machines with no physics and low-poly/billboard meshes.
- **Inside Queue Range**: `CheckoutManager` assigns a `QueuePosition`. NPC enables `NavigationAgent3D` only if moving.
- **At Counter**: Full high-poly mesh loads for interaction (VRAM prioritization for the RTX 4060).

## 5. Economy Signaling
### Signals:
- `signal payment_started(npc_id: String, amount: float)`
- `signal payment_completed(npc_id: String, new_balance: float)`
- `signal counter_overflow(counter_index: int)`

### Execution:
Using the **Signal-driven pattern**, the `EconomyManager` (separate node) listens for `payment_completed` to perform atomic updates to the store's budget, avoiding race conditions during high-concurrency (multiple checkouts).

## 6. Implementation Checklist
- [/] Create `CheckoutManager.gd` base class.
- [ ] Implement `QueuePath` logic for 3 counters.
- [ ] Setup `EconomyManager` observer.
