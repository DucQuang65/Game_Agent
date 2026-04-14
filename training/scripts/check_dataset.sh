#!/usr/bin/env bash
set -euo pipefail

DATASET="${1:-data/gamedev_sft_10.jsonl}"

if [[ ! -f "$DATASET" ]]; then
  echo "Missing dataset: $DATASET"
  exit 1
fi

LINES=$(wc -l < "$DATASET")
if [[ "$LINES" -lt 5 ]]; then
  echo "Dataset too small: $LINES lines"
  exit 1
fi

awk 'NF{print}' "$DATASET" | jq -c . >/dev/null

echo "Dataset OK: $DATASET ($LINES lines)"
