#!/usr/bin/env bash
# ============================================================
# quick_verify.sh — Elite Studio (v6.5) One-Shot Verification
# Run from project root: bash scripts/quick_verify.sh
# ============================================================
set -e
# Ensure we are in the project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

VENV=".venv"
PYTHON="$VENV/bin/python"

echo "=========================================="
echo " 🚀 Elite Studio v6.5 — Quick Verify"
echo "=========================================="

# ── 1. Activate or create venv ──────────────────────────────
if [ ! -f "$PYTHON" ]; then
    echo "⚙️  No .venv found. Creating..."
    python3 -m venv "$VENV"
fi

source "$VENV/bin/activate"
echo "✅ Python: $(python --version)"

# ── 2. Install / upgrade requirements ────────────────────────
echo ""
echo "📦 Installing all requirements (including chromadb, pytest, etc.)..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# ── 3. Clean stale caches ────────────────────────────────────
echo ""
echo "🧹 Cleaning __pycache__ and .pytest_cache..."
find . -type d -name "__pycache__" \
    -not -path "./.venv/*" \
    -not -path "./unsloth_compiled_cache*" \
    -exec rm -rf {} + 2>/dev/null || true
rm -rf .pytest_cache 2>/dev/null || true

# ── 4. Run tests with coverage ───────────────────────────────
echo ""
echo "🧪 Running test suite with coverage..."
python -m pytest tests/ \
    --cov=langgraph \
    --cov=scripts \
    --cov-report=term-missing \
    --cov-report=xml:coverage.xml \
    -v \
    --tb=short

echo ""
echo "=========================================="
echo " ✅ Verification complete!"
echo "=========================================="
