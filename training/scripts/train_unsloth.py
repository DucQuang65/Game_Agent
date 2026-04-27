import argparse
from datasets import load_dataset
from unsloth import FastLanguageModel
from transformers import TrainingArguments
from trl import SFTTrainer


def format_example(row):
    instruction = row.get("instruction", "").strip()
    user_input = row.get("input", "").strip()
    output = row.get("output", "").strip()
    prompt = (
        "<|im_start|>system\n"
        "You are a source-grounded game development assistant.\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"Instruction: {instruction}\n"
        f"Input: {user_input}\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
        f"{output}\n"
        "<|im_end|>"
    )
    return {"text": prompt}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--base-model", default="Qwen/Qwen2.5-Coder-7B-Instruct")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-steps", type=int, default=60)
    args = parser.parse_args()

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.base_model,
        max_seq_length=2048,
        load_in_4bit=True,
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
        max_seq_length=2048,
        packing=False,
        args=TrainingArguments(
            per_device_train_batch_size=1,
            gradient_accumulation_steps=8,
            warmup_steps=5,
            max_steps=args.max_steps,
            learning_rate=2e-4,
            bf16=True,
            fp16=False,
            logging_steps=5,
            optim="adamw_8bit",
            weight_decay=0.01,
            lr_scheduler_type="cosine",
            output_dir=args.output_dir,
            save_steps=30,
            report_to="none",
        ),
    )

    trainer.train()
    model.save_pretrained(args.output_dir)
    tokenizer.save_pretrained(args.output_dir)

    # Export to GGUF for Ollama usage
    print("Exporting to GGUF (q4_k_m)...")
    model.save_pretrained_gguf(args.output_dir, tokenizer, quantization_method = "q4_k_m")


if __name__ == "__main__":
    main()
