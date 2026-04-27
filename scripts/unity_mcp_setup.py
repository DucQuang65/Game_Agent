#!/usr/bin/env python3
"""
unity_mcp_setup.py — Unity-MCP Automation Helper
Handles Node.js dependency installation and build for the Unity MCP server.
"""
import subprocess
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UNITY_MCP_PATH = PROJECT_ROOT / "study/external/Unity-MCP/server"

def setup_unity_mcp():
    print("--- 🔧 Unity-MCP: Setup Automation ---")
    
    if not UNITY_MCP_PATH.exists():
        print(f"[!] Error: Unity-MCP directory not found at {UNITY_MCP_PATH}")
        print("    Ensure you ran scripts/clone_ecosystem.sh first.")
        return

    try:
        print("[*] Installing Node.js dependencies...")
        subprocess.run(["npm", "install"], cwd=UNITY_MCP_PATH, check=True)
        
        print("[*] Building Unity-MCP server...")
        subprocess.run(["npm", "run", "build"], cwd=UNITY_MCP_PATH, check=True)
        
        print("\n✅ Success: Unity-MCP is built and ready for use via stdio.")
        print("🚀 Tip: Ensure your 'mcp_config.json' points to 'server/dist/index.js'.")
        
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Error during setup: {e}")
    except FileNotFoundError:
        print("\n[!] Error: 'npm' command not found. Please install Node.js in WSL.")

if __name__ == "__main__":
    setup_unity_mcp()
