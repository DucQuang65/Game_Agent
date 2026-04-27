# Training Starter (RTX 4060, QLoRA)

This folder contains a practical starter to fine-tune a coding assistant for game dev.

## Goal
- Improve tool-use behavior and modern game-dev responses (Godot 4.6/4.7, Unity 6, Vulkan).

## Included
- `data/gamedev_sft_10.jsonl`: small SFT dataset (10 samples)
- `scripts/train_unsloth.py`: QLoRA training script (Unsloth)
- `scripts/check_dataset.sh`: dataset validation
- `requirements-train.txt`: python dependencies

## Quick start
```bash
cd ~/Game_Agent/training
bash scripts/check_dataset.sh
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements-train.txt
python scripts/train_unsloth.py \
  --dataset data/gamedev_sft_10.jsonl \
  --base-model Qwen/Qwen2.5-Coder-7B-Instruct \
  --output-dir outputs/qwen25-gamedev-lora
```

## Notes
- This is a starter run. Expand dataset to 500+ high-quality examples for meaningful gains.
- Keep all private project code local. Only use approved public sources for SFT corpus.
