#!/usr/bin/env bash
# cleanup_project.sh — Game Agent OS Project Restructuring
# Run from project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

echo "🧹 Step 1: Removing cache, stubs, and auto-generated files..."
rm -rf scripts/__pycache__
rm -f unsloth.pyi transformers.pyi
rm -f scripts/vulkan_controller.gd
rm -f scripts/auto_generated_shader_controller.gd

echo "🗑️  Step 2: Deleting redundant documentation..."
rm -f CONSOLIDATED_SOURCE.md
rm -f MANIFEST.md
rm -f ORCHESTRATOR_UPDATE.md
rm -f TRAINING_ACTION_LOG_*.md
rm -f openclaw-security-checklist.md
rm -f docs/ORCHESTRATOR_UPDATE.md
rm -f docs/PORTABILITY.md
rm -f ubuntu_research.md

echo "🗑️  Step 3: Remove duplicate SRS (keep SRS_Text.md as single source of truth)..."
rm -f Game_Agent_SRS.md

echo "📂 Step 4: Create missing directories..."
mkdir -p poc/godot
mkdir -p docs/external

echo "🔀 Step 5: Moving misplaced files..."
mv scripts/CheckoutManager.gd poc/godot/
mv scripts/.wslconfig.template docs/external/
mv AGENT_COMMUNICATION.md docs/
mv AI_GUIDE.md docs/
mv gamedev-agent.Modelfile docs/external/
mv openclaw.hardened.example.json docs/external/

echo "🔀 Step 6: Consolidating mcp config (remove duplicate)..."
# The canonical config is in openclaw_configs/
rm -f mcp/mcp_config.json 2>/dev/null || true

echo ""
echo "✅ Restructuring complete! Final root check:"
ls -la | grep -v "^total" | grep -v "^\." | awk '{print $NF}'
echo ""
echo "📁 Root .md files:"
ls *.md 2>/dev/null
