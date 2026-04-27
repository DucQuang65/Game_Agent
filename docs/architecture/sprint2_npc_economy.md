# 📈 Architecture Design: NPC Economy System (v1.0)
**Project**: Supermarket Simulator
**Standard**: Elite Studio / Godot 4.7
**Mathematical Model**: Utility-Based Decision Making

## 1. The Utility Function
NPCs will decide whether to buy an item $i$ based on the formula:
$$U(i) = \frac{W_i \cdot V_i}{P_i}$$

Where:
- $V_i$: Value (Intrinsic priority of the item category).
- $P_i$: Price (Current store price).
- $W_i$: Weight (Dyamic need, e.g., hunger level).

## 2. Decision Logic (Signal-Driven)
The `EconomyManager` will broadcast price changes. NPCs with active "Browsing" state will recalculate $U(i)$ for nearby items.

## 3. Component Hierarchy
```text
EconomyManager (Node)
├── PriceDatabase (Resource-based)
└── NPCGroup (Node)
    ├── NPC_A (Cognition Component)
    └── NPC_B (Cognition Component)
```

## 4. VRAM Optimization (LOD Cognition)
- **High-Priority NPCs** (At checkout/interaction): Full utility calculation every 0.5s.
- **Background NPCs**: Utility calculated only once per "aisle enters" or via low-frequency batch updates to minimize CPU/VRAM overhead.

## 5. First Implementation Task
- Create `NPCCognition.gd` to handle the math logic.
- Create `EconomyDatabase.tres` to store the $V_i$ and $P_i$ values.
