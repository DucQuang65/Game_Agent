#!/bin/bash
# Generate IDE Prompt Script
# Usage: ./generate_ide_prompt.sh "Current Issue Description"

ISSUE_DESC=$1
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MASTER_SCHEMA="$PROJECT_ROOT/prompt_master/prompt_master_schema.md"
OUTPUT_FILE="$PROJECT_ROOT/prompt_master/ACTIVE_IDE_PROMPT.md"

if [ -z "$ISSUE_DESC" ]; then
    echo "Error: Please provide an issue description."
    exit 1
fi

echo "--- START OF IDE PROMPT ---" > "$OUTPUT_FILE"
cat "$MASTER_SCHEMA" >> "$OUTPUT_FILE"
echo -e "\n## ⚡ CURRENT TASK\n$ISSUE_DESC" >> "$OUTPUT_FILE"
echo "--- END OF IDE PROMPT ---" >> "$OUTPUT_FILE"

echo "Prompt generated at $OUTPUT_FILE"
echo "You can now copy its content to Cursor, Aider, or Claude Code."
