#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CONFIG_SRC = os.path.join(PROJECT_ROOT, "openclaw_configs")
OPENCLAW_DIR = os.path.expanduser("~/.openclaw")
AGENTS_DIR = os.path.join(OPENCLAW_DIR, "workspace/agents")
MODELS = [
    "qwen2.5-coder:7b",
    "deepseek-r1:7b",
    "llama3.2:3b",
    "nomic-embed-text:latest"
]
STUDY_REPOS = {
    "BoatAttack": "https://github.com/Unity-Technologies/BoatAttack.git",
    "FPSSample": "https://github.com/Unity-Technologies/FPSSample.git",
    "GodotGame": "https://github.com/godotengine/tps-demo.git", # Example
    "Vulkan-Samples": "https://github.com/KhronosGroup/Vulkan-Samples.git",
    "godot-jolt": "https://github.com/godot-jolt/godot-jolt.git"
}

def run_cmd(cmd):
    print(f"Executing: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def setup_configs(dry_run=False):
    print("--- Setting up OpenClaw Configs ---")
    if not os.path.exists(OPENCLAW_DIR):
        if not dry_run: os.makedirs(OPENCLAW_DIR)
        print(f"Created {OPENCLAW_DIR}")
    
    if not os.path.exists(AGENTS_DIR):
        if not dry_run: os.makedirs(AGENTS_DIR)
        print(f"Created {AGENTS_DIR}")

    # Copy Agents
    agent_src = os.path.join(CONFIG_SRC, "agents")
    if os.path.exists(agent_src):
        for f in os.listdir(agent_src):
            src_file = os.path.join(agent_src, f)
            dst_file = os.path.join(AGENTS_DIR, f)
            print(f"Copying {f} to {AGENTS_DIR}")
            if not dry_run: shutil.copy2(src_file, dst_file)
    
    # Copy openclaw.json.example if openclaw.json doesn't exist
    json_dst = os.path.join(OPENCLAW_DIR, "openclaw.json")
    if not os.path.exists(json_dst):
        json_src = os.path.join(CONFIG_SRC, "openclaw.json.example")
        print(f"Creating initial openclaw.json from template...")
        if not dry_run: shutil.copy2(json_src, json_dst)
        print("IMPORTANT: Please update tokens in ~/.openclaw/openclaw.json")
    else:
        print("Note: ~/.openclaw/openclaw.json already exists. Skipping.")

def pull_models(dry_run=False):
    print("\n--- Ollama Models Setup ---")
    for model in MODELS:
        cmd = f"ollama pull {model}"
        if dry_run:
            print(f"[Dry-run] Would execute: {cmd}")
        else:
            run_cmd(cmd)
    
    # Create custom gamedev-agent
    modelfile = os.path.join(CONFIG_SRC, "gamedev-agent.Modelfile")
    if os.path.exists(modelfile):
        cmd = f"ollama create gamedev-agent -f {modelfile}"
        if dry_run:
            print(f"[Dry-run] Would execute: {cmd}")
        else:
            run_cmd(cmd)

def clone_study(dry_run=False):
    print("\n--- Study Repositories Setup ---")
    study_dir = os.path.join(PROJECT_ROOT, "study")
    if not os.path.exists(study_dir):
        if not dry_run: os.makedirs(study_dir)
    
    for name, url in STUDY_REPOS.items():
        dst_path = os.path.join(study_dir, name)
        if not os.path.exists(dst_path):
            cmd = f"git clone --depth 1 {url} {dst_path}"
            if dry_run:
                print(f"[Dry-run] Would execute: {cmd}")
            else:
                run_cmd(cmd)
        else:
            print(f"Repo {name} already exists. Skipping.")

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    if dry_run:
        print("!!! DRY RUN MODE !!!")
    
    setup_configs(dry_run)
    pull_models(dry_run)
    clone_study(dry_run)
    
    print("\nSetup complete! Remember to check your API keys and restart OpenClaw.")
