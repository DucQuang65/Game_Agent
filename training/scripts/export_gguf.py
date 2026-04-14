from __future__ import annotations

import importlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from unsloth import FastLanguageModel  # type: ignore
    from transformers import AutoTokenizer  # type: ignore

model_dir = "./training/outputs/gamedev-qwen-lora-v3"
base_model_name = "Qwen/Qwen2.5-Coder-7B-Instruct"


def _require_attr(module_name: str, attr_name: str):
    """Import optional dependency lazily and return requested attribute."""
    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        raise SystemExit(
            f"Missing dependency '{module_name}'. Install training requirements before exporting GGUF."
        ) from exc

    if not hasattr(module, attr_name):
        raise SystemExit(f"Dependency '{module_name}' does not expose '{attr_name}'.")

    return getattr(module, attr_name)


print("Loading model and adapters...")
FastLanguageModel = _require_attr("unsloth", "FastLanguageModel")
_ = _require_attr("transformers", "AutoTokenizer")

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = model_dir,
    max_seq_length = 2048,
    load_in_4bit = True,
)

print("Exporting to GGUF (q4_k_m)...")
# This will save to the same directory or a subfolder
model.save_pretrained_gguf(model_dir, tokenizer, quantization_method = "q4_k_m")
print("Done!")
