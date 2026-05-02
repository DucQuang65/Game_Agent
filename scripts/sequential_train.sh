#!/bin/bash
# Sequential Ingestion Script

REPOS=(
    "https://github.com/Unity-Technologies/FPSSample"
    "https://github.com/Unity-Technologies/com.unity.multiplayer.samples.coop"
    "https://github.com/Unity-Technologies/BoatAttack"
    "https://github.com/KhronosGroup/Vulkan-Samples"
    "https://github.com/pythonarcade/arcade"
    "https://github.com/pyglet/pyglet"
    "https://github.com/the-mirror-gmbh/the-mirror-godot-app"
    "https://github.com/godot-extended-libraries/godot-vfx-library"
    "https://github.com/godot-shaders/godot-shaders"
)

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
STUDY_DIR="$PROJECT_ROOT/study"
INGEST_SCRIPT="$PROJECT_ROOT/scripts/ingest_repos.py"

mkdir -p "$STUDY_DIR"
cd "$STUDY_DIR"

for REPO in "${REPOS[@]}"; do
    NAME=$(basename "$REPO")
    if [ -d "$NAME" ]; then
        echo "Cleaning up incomplete/existing $NAME..."
        rm -rf "$NAME"
    fi
    echo "------------------------------------------"
    echo "Starting sequential clone of $NAME..."
    git clone --depth 1 "$REPO" "$NAME"
    
    echo "Ingesting $NAME to memory..."
    python3 "$INGEST_SCRIPT"
    
    echo "Finished $NAME. Moving to next..."
done

echo "Sequential training complete!"
