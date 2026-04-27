#!/usr/bin/env python3
"""
filter_top_skills.py — Gatekeeper v2 Skill Filter
Scans the claude-skills library and ranks skills by Game-Dev relevance.
Outputs a curated SKILLS_MANIFEST.md with the Top 30 active skills.
"""
from pathlib import Path
from typing import TypedDict

# --- CONFIGURATION ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SKILLS_PATH = PROJECT_ROOT / "study/external/claude-skills"
MANIFEST_PATH = PROJECT_ROOT / "SKILLS_MANIFEST.md"
TARGET_COUNT = 30

# Keywords prioritized for Game Agent OS (Godot 4.7 / Unity 6 / Vulkan / RTX 4060)
KEYWORDS = [
    "godot", "unity", "gdscript", "csharp", "shader", "vulkan", "render",
    "physics", "math", "geometry", "pathfinding", "navigation", "ai",
    "state-machine", "architecture", "refactor", "performance", "vram",
    "optimization", "debug", "memory", "clean-code", "pattern", "ecs",
    "security", "review", "test", "ci", "pipeline", "async", "thread",
    "gpu", "compute", "mesh", "texture", "lighting", "animation",
]


class SkillEntry(TypedDict):
    name: str
    path: str
    score: int
    parent: str


def filter_skills():
    if not SKILLS_PATH.exists():
        print(f"[!] Error: Path {SKILLS_PATH} not found.")
        print("    Run: git clone --depth 1 https://github.com/alirezarezvani/claude-skills.git study/external/claude-skills")
        return

    all_skills: list[SkillEntry] = []

    # Scan the entire skill library
    for file in SKILLS_PATH.rglob("*.md"):
        # Skip non-skill files
        if file.name.startswith(".") or "readme" in file.name.lower():
            continue

        try:
            content = file.read_text(errors="ignore").lower()
        except Exception:
            continue

        score = sum(content.count(kw) for kw in KEYWORDS)

        if score > 0:
            try:
                rel_path = file.resolve().relative_to(PROJECT_ROOT)
            except ValueError:
                rel_path = file.resolve()

            all_skills.append({
                "name": file.stem,
                "path": str(rel_path),
                "score": score,
                "parent": file.parent.name,
            })

    # Sort by relevance score descending, take Top N
    top_skills: list[SkillEntry] = sorted(all_skills, key=lambda x: x["score"], reverse=True)[:TARGET_COUNT]

    if not top_skills:
        print("[!] No matching skills found. Check KEYWORDS or SKILLS_PATH.")
        return

    # --- WRITE MANIFEST ---
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write("type: index\n")
        f.write("status: active\n")
        f.write("---\n\n")
        f.write("# 🛠️ System Protocol: Skills Manifest (Gatekeeper v2)\n\n")
        f.write(f"Top {len(top_skills)} skills filtered from {len(all_skills)} candidates.\n\n")
        f.write("## Active Skills (Registered Tools)\n\n")
        f.write("| Rank | Skill Name | Category | Priority | Source Path |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")

        for i, skill in enumerate(top_skills, 1):
            priority = "🔴 Critical" if i <= 5 else ("🟡 High" if i <= 15 else "🟢 Normal")
            f.write(
                f"| {i} | **{skill['name']}** | {skill['parent']} "
                f"| {priority} | `{skill['path']}` |\n"
            )

        f.write("\n## Gatekeeper Protocol\n\n")
        f.write("- **Active Tools**: Only the skills listed above are registered for direct execution.\n")
        f.write("- **Knowledge Library**: All 380+ skills remain in `study/external/claude-skills/` for RAG lookup.\n")
        f.write("- **VRAM Safe**: Skill definitions (~30 entries) consume <1KB of prompt context.\n")
        f.write("- **Zero Bloat**: Unused skills are never loaded into the Agent's working memory.\n")

    print(f"[+] Success: Filtered {len(top_skills)} skills into {MANIFEST_PATH}")
    print(f"    Total candidates scanned: {len(all_skills)}")
    print(f"    Top skill: {top_skills[0]['name']} (score: {top_skills[0]['score']})")


if __name__ == "__main__":
    filter_skills()
