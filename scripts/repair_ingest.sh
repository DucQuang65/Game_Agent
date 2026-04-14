#!/bin/bash
# Repair Script for Missing/Failed Repos

REPOS=(
    "https://github.com/the-mirror-gmbh/the-mirror-godot-app"
    "https://github.com/ring-storm/LibreQuake"
    "https://github.com/godot-extended-libraries/godot-vfx-library"
    "https://github.com/godot-shaders/godot-shaders"
)

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STUDY_DIR="$PROJECT_ROOT/study"
INGEST_SCRIPT="$PROJECT_ROOT/scripts/ingest_repos.py"

for REPO in "${REPOS[@]}"; do
    NAME=$(basename "$REPO")
    echo "------------------------------------------"
    echo "Repairing/Cloning $NAME..."
    rm -rf "$NAME"
    git clone --depth 1 "$REPO" "$NAME"
    
    echo "Ingesting $NAME..."
    python3 "$INGEST_SCRIPT"
done

echo "Repair complete!"
