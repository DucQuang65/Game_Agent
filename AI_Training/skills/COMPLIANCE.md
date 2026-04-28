---
type: technical_standard
target_engine: Godot 4.6, Godot 4.7, Unity 6
status: verified
source_license: [Original License]
---

# 🛠️ Agent Skill: Compliance & Legal

# 🛡️ IP & EULA Compliance Guard

## Purpose
This skill provides a rule set for the Agent to self-audit and comply when:
1. **Collecting data** for AI training (nanoGPT, llm.c).
2. **Scanning system files** on Ubuntu.
3. **Referencing external code**.
4. **Creating game content** inspired by other works.

---

## 🟢 GREEN ZONE (Safe — Permitted)

### Training Data
- **Self-authored data**: All `.cs`, `.gd`, `.txt` files in `Game_Project/` where you are the author.
- **Permissive Open Source**: Only ingest code with **MIT**, **Apache 2.0**, **BSD-2/3**, or **Unlicense** licenses.
- **Official Documentation**: Godot, Unity, and Microsoft (.NET) technical docs.
- **Statistical Patterns**: Extracting coding patterns and conventions, not creative expression.

---

## 🔴 RED ZONE (Violations — Strictly Prohibited)

| Action | Reason | Relevant EULA/Law |
|---|---|---|
| Decrypting `.pak`, `.assets`, `.bundle` | Reverse Engineering | Unity ToS §2.4, UE EULA §1(b) |
| Scanning `.so`, `.dll`, `.a` libraries | Accessing binary code | DMCA §1201 |
| Using Asset Store code for training | Asset Store EULA violation | Unity Asset Store EULA §6 |
| Copying sprites/sounds from other games | Copyright infringement | Berne Convention |

---

## 📂 Blacklist

### System (Ubuntu)
- `/proc/`, `/sys/`, `/dev/`, `/bin/`, `/sbin/`, `/lib/`, `/usr/`, `/boot/`, `/root/`, `/etc/`

### Binary Files
- `*.so`, `*.a`, `*.la`, `*.dll`, `*.pak`, `*.assets`, `*.bundle`, `*.ucas`, `*.utoc`

---

## ⚡ Quick Audit Process

```
1. Is the license MIT, Apache, or BSD?
2. Am I extracting a PATTERN or COPYING the original?
3. Is it a binary file (.so, .pak, .dll)?
4. Is the output >70% identical to the source?
```

---
