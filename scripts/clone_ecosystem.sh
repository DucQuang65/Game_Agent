#!/bin/bash
# ============================================================
# clone_ecosystem.sh — Game Agent OS v6.5 Ecosystem Bootstrapper
# Clones all required repositories into study/external/
# Usage: cd <PROJECT_ROOT> && bash scripts/clone_ecosystem.sh
# ============================================================

set -e
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EXTERNAL="$PROJECT_ROOT/study/external"

mkdir -p "$EXTERNAL"
cd "$EXTERNAL"

echo "🔧 Game Agent Environment — Synchronizing Ecosystem Repositories..."

# Count current external repositories
current_count=$(ls -d study/external/*/ 2>/dev/null | wc -l)
echo "Current repository count in study/external: $current_count"

# Targeted repository count
target_count=11

# Verification & Action
if [ "$current_count" -ge "$target_count" ]; then
    echo "✅ Ecosystem is already aligned (Count: $current_count)."
else
    echo "⚠️ Ecosystem mismatch detected. Synchronizing missing assets..."
    
    # 1-7: Existing repositories
    [ ! -d "study/external/claude-skills" ] && git clone --depth 1 https://github.com/alirezarezvani/claude-skills.git study/external/claude-skills
    [ ! -d "study/external/free-claude-code" ] && git clone --depth 1 https://github.com/Alishahryar1/free-claude-code.git study/external/free-claude-code
    [ ! -d "study/external/OpenSpace" ] && git clone --depth 1 https://github.com/HKUDS/OpenSpace.git study/external/OpenSpace
    [ ! -d "study/external/Unity-MCP" ] && git clone --depth 1 https://github.com/IvanMurzak/Unity-MCP.git study/external/Unity-MCP
    [ ! -d "study/external/mcp-unity" ] && git clone --depth 1 https://github.com/CoderGamester/mcp-unity.git study/external/mcp-unity
    [ ! -d "study/external/Open-Code-Godot-Studio" ] && git clone --depth 1 https://github.com/gwtt/Open-Code-Godot-Studio.git study/external/Open-Code-Godot-Studio
    [ ! -d "study/external/Claude-Code-Game-Studios" ] && git clone --depth 1 https://github.com/Donchitos/Claude-Code-Game-Studios.git study/external/Claude-Code-Game-Studios
    
    # 8-11: New Research & Core Assets
    echo "📦 Synchronizing Karpathy Stack & Engine Core..."
    [ ! -d "study/external/llm.c" ] && git clone --depth 1 https://github.com/karpathy/llm.c.git study/external/llm.c
    [ ! -d "study/external/llama2.c" ] && git clone --depth 1 https://github.com/karpathy/llama2.c.git study/external/llama2.c
    [ ! -d "study/external/nanoGPT" ] && git clone --depth 1 https://github.com/karpathy/nanoGPT.git study/external/nanoGPT
    [ ! -d "study/external/openclaw" ] && git clone --depth 1 https://github.com/openclaw/openclaw.git study/external/openclaw
fi

echo ""
echo "=========================================="
echo "✅ Ecosystem synchronization complete."
echo "📂 Data stored in: study/external"
echo "🚀 Next Step: Run RAG indexing via python3 scripts/filter_top_skills.py"
echo "=========================================="
