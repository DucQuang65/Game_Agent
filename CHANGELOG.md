# 📜 Evolution Log: Changelog

All notable changes to the Game Agent project will be documented here.

## [1.0.0] - 2026-04-05
### 🛡️ Portability & Anonymization (Milestone)
- **Security**: Moved sensitive API documentation and logs to `secrets/` (git-ignored).
- **Portability**: Replaced all hardcoded absolute paths with dynamic root detection in scripts.
- **Anonymization**: Removed all personal identifiers from the codebase.
- **Aesthetic**: Standardized all documentation headers and added YAML frontmatter for agent parsing.
- **Infrastructure**: Added `scripts/setup_env.sh` for automated environment initialization.

## [0.9.0] - 2026-04-03
### 🧠 Multi-Agent Orchestration
- Initial integration of OpenClaw with DeepSeek R1 and Qwen 2.5 Coder.
- Established the `AI_Training/` skill-based architecture.
- Implemented RAG memory layer using ChromaDB.
