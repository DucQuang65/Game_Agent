# 🤝 Collaboration Protocol: Contributing

Thank you for your interest in contributing to the Game Agent project! To maintain the system's "Warrior" level performance and "Anonymous Agent" aesthetic, please follow these guidelines.

## 🛠️ Adding New Skills
1. Create a new `.md` file in `AI_Training/skills/`.
2. Follow the standardized header and frontmatter:
   ```markdown
   ---
   type: technical_standard
   target_engine: Godot 4.6/4.7, Unity 6, Vulkan
   status: verified
   ---
   # 🛠️ Agent Skill: [Skill Name]
   ```
3. Ensure all instructions are English-first and engine-specific.

## 🤖 Defining Personas
1. Create a new `.md` file in `AI_Training/agents/`.
2. Use the `agent_persona` type in frontmatter.
3. Define strict tool-use boundaries and tone instructions.

## 🧠 Training Data
1. Add new fine-tuning samples to `training/data/` in `.jsonl` format.
2. Ensure all personal identifiers (names, paths, emails) are stripped before submission.

## 🧪 Testing
- Always validate Godot 4.6+, Unity 6, and Vulkan-related code against `memory/GODOT_4_6_PLUS_API_STANDARD.md` before finalizing a skill.
- Run `grep -ri "personal-identifier"` to ensure no personal leaks remain in your contributions.
