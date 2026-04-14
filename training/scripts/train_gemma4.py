import argparse
import importlib
import os
from typing import Any, TYPE_CHECKING

# Avoid top-level imports of optional heavy ML libraries so static analyzers
# (Pyre2) don't report missing-module-attribute when the environment
# doesn't have these packages installed. We import them at runtime inside
# `main()` and provide TYPE_CHECKING stubs for type checkers.

if TYPE_CHECKING:
    from datasets import load_dataset  # type: ignore
    from unsloth import FastLanguageModel  # type: ignore
    from transformers import TrainingArguments  # type: ignore
    from trl import SFTTrainer  # type: ignore

# Runtime placeholders
load_dataset: Any = None
FastLanguageModel: Any = None
TrainingArguments: Any = None
SFTTrainer: Any = None

def format_example(row):
    instruction = row.get("instruction", "").strip()
    user_input = row.get("input", "").strip()
    output = row.get("output", "").strip()
    # Gemma 4 Prompt Template (Simulated for 2026)
    prompt = (
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        "You are a Senior Godot 4.6/4.7 Game Developer specializing in Vulkan and C#.\n"
        "<|eot_id|><|start_header_id|>user<|end_header_id|>\n"
        f"Context: {user_input}\n"
        f"Task: {instruction}\n"
        "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
        f"{output}\n"
        "<|eot_id|>"
    )
    return {"text": prompt}

def main():
    parser = argparse.ArgumentParser()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    
    parser.add_argument("--dataset", default=os.path.join(project_root, "training/data/gamedev_sft_10.jsonl"))
    # Use Gemma 4 E4B (Edge optimized) - Standard ID for 8GB VRAM
    parser.add_argument("--base-model", default="unsloth/gemma-4-E4B-it-unsloth-bnb-4bit")
    parser.add_argument("--output-dir", default=os.path.join(project_root, "training/outputs/gemma-4-e4b-gamedev-v1"))
    parser.add_argument("--max-steps", type=int, default=100)
    parser.add_argument("--max-seq-length", type=int, default=2048)
    parser.add_argument("--dataset-num-proc", type=int, default=1, help="Number of processes for dataset mapping.")
    parser.add_argument("--ce-loss-target-gb", type=float, default=0.5, help="CE Loss target GB (increase for 8GB VRAM stability).")
    args = parser.parse_args()

    # Force a small fixed fused CE memory target so training can continue even
    # when free VRAM becomes very low right after model/optimizer allocation.
    os.environ["UNSLOTH_CE_LOSS_TARGET_GB"] = str(args.ce_loss_target_gb)

    # Import heavy dependencies at runtime (when available).
    global load_dataset, FastLanguageModel, TrainingArguments, SFTTrainer
    if load_dataset is None:
        ds_mod = importlib.import_module("datasets")
        load_dataset = ds_mod.load_dataset
    if FastLanguageModel is None:
        unsloth_mod = importlib.import_module("unsloth")
        FastLanguageModel = unsloth_mod.FastLanguageModel
    if TrainingArguments is None:
        transformers_mod = importlib.import_module("transformers")
        TrainingArguments = transformers_mod.TrainingArguments
    if SFTTrainer is None:
        trl_mod = importlib.import_module("trl")
        SFTTrainer = trl_mod.SFTTrainer

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.base_model,
        max_seq_length=args.max_seq_length,
        load_in_4bit=True,
        device_map={"": 0}, # Force GPU 0 to avoid CPU offloading on tight VRAM
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_alpha=16,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing=True,
    )

    ds = load_dataset("json", data_files=args.dataset, split="train")
    ds = ds.map(format_example)

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=ds,
        dataset_text_field="text",
        dataset_num_proc=args.dataset_num_proc,
        max_seq_length=args.max_seq_length,
        packing=False,
        args=TrainingArguments(
            per_device_train_batch_size=1,
            gradient_accumulation_steps=4,
            warmup_steps=10,
            max_steps=args.max_steps,
            learning_rate=2e-4,
            bf16=True,
            logging_steps=1,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="cosine",
            output_dir=args.output_dir,
            save_steps=50,
            report_to="none",
        ),
    )

    print("--- STARTING TRAINING FOR GEMMA 4 (7B) ---")
    trainer.train()
    
    print("--- SAVING MODEL & GGUF ---")
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)
    model.save_pretrained_gguf(args.output_dir, tokenizer, quantization_method = "q4_k_m")
    print(f"Training complete! Model saved to {args.output_dir}")

if __name__ == "__main__":
    main()
