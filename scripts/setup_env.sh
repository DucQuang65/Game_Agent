#!/bin/bash

# 🛠️ Game Agent Environment Setup
# Automates the installation of dependencies for WSL2/Ubuntu with RTX 4060.

set -e

echo "🚀 Initializing Game Agent Environment..."

# 1. Update System
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Essential Tools
sudo apt-get install -y curl git jq build-essential

# 3. Setup Python Environment
if ! command -v conda &> /dev/null; then
    echo "📦 Installing Miniconda..."
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda
    rm Miniconda3-latest-Linux-x86_64.sh
    source $HOME/miniconda/bin/activate
else
    echo "✅ Miniconda already installed."
fi

# 4. Create Virtual Environment
echo "🐍 Creating .venv_agent..."
python3 -m venv .venv_agent
source .venv_agent/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 5. Install Ollama (Local AI Runtime)
if ! command -v ollama &> /dev/null; then
    echo "🦙 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✅ Ollama already installed."
fi

# 6. Pull Required Models
echo "📥 Pulling models (this may take a while)..."
ollama pull qwen2.5-coder:7b
ollama pull deepseek-r1:7b
ollama pull llama3.2:3b
ollama pull nomic-embed-text

# 7. Setup OpenClaw Configuration
echo "⚙️ Bootstrapping OpenClaw..."
python3 scripts/bootstrap_agent.py

echo "✅ Setup Complete! Please configure your secrets in ~/.openclaw/openclaw.json"
