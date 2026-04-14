#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"
export HF_HUB_ENABLE_HF_TRANSFER=0

./.venv/bin/python scripts/train_gemma4.py 2>&1 | tee -a training.log
