import os
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STUDY_DIR = os.path.join(PROJECT_ROOT, "study")
MEMORY_DIR = os.path.expanduser("~/.openclaw/workspace/memory")

def generate_study_card(repo_name):
    print(f"Ingesting {repo_name}...")
    repo_path = os.path.join(STUDY_DIR, repo_name)
    
    # Try to read README.md
    readme_path = os.path.join(repo_path, "README.md")
    content = ""
    if os.path.exists(readme_path):
        with open(readme_path, "r", errors="ignore") as f:
            content = f.read(2000) # Read first 2000 chars

    # Create a summary card via a prompt-like structure in memory
    card_path = os.path.join(MEMORY_DIR, f"STUDY_{repo_name.upper()}.md")
    with open(card_path, "w") as f:
        f.write(f"# Study Card: {repo_name}\n\n")
        f.write(f"**Path:** {repo_path}\n\n")
        f.write("## Overview\n")
        f.write(content if content else "No README found.")
        f.write("\n\n## Key Technical Insights (Auto-Ingested)\n")
        f.write("- Review configuration files and directory architecture to understand project conventions.\n")
        f.write("- Use `grep` to search for key functions and entry points.\n")

for item in os.listdir(STUDY_DIR):
    if os.path.isdir(os.path.join(STUDY_DIR, item)) and not item.startswith("."):
        generate_study_card(item)

print("Ingestion complete!")
