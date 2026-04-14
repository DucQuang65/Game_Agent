from __future__ import annotations

import os
import json
from typing import TypedDict, cast
from urllib import request

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE_STANDARD_PATH = os.path.join(PROJECT_ROOT, "memory", "ENGINE_STANDARD.md")

GITHUB_API_URL = "https://api.github.com/repos/godotengine/godot/releases/latest"


class ReleaseInfo(TypedDict):
    tag: str
    body: str
    url: str


def fetch_latest_godot_release() -> ReleaseInfo | None:
    print("Fetching latest Godot release info...")
    try:
        req = request.Request(
            GITHUB_API_URL,
            headers={"User-Agent": "Game_Agent/update_engine_standard"},
        )
        with request.urlopen(req, timeout=10) as response:
            if response.status != 200:
                return None
            payload = response.read().decode("utf-8")
        data = json.loads(payload)
        if not isinstance(data, dict):
            return None

        tag = data.get("tag_name")
        body = data.get("body", "")
        url = data.get("html_url")
        if not isinstance(tag, str) or not isinstance(body, str) or not isinstance(url, str):
            return None

        return cast(ReleaseInfo, {"tag": tag, "body": body, "url": url})
    except Exception as e:
        print(f"Error fetching from GitHub: {e}")
    return None


def update_engine_standard(release_info: ReleaseInfo | None) -> None:
    if not release_info:
        return
    
    # Filter for relevant keywords
    keywords = ["GDScript", "Vulkan", "@export", "CharacterBody", "Shader"]
    lines: list[str] = release_info["body"].split("\n")
    relevant_changes = [l for l in lines if any(k in l for k in keywords)]
    
    if not relevant_changes:
        relevant_changes = ["No major GDScript/Vulkan changes noted in this release body."]

    update_block = f"\n\n## Recent API Changes (Auto-detected: {release_info['tag']})\n"
    update_block += f"*Source: {release_info['url']}*\n\n"
    limited_changes: list[str] = []
    for index, item in enumerate(relevant_changes):
        if index >= 10:
            break
        limited_changes.append(item)
    update_block += "\n".join(limited_changes) # Limit to top 10 items
    update_block += "\n\n---\n"

    with open(ENGINE_STANDARD_PATH, "a", encoding="utf-8") as f:
        f.write(update_block)
    print(f"Updated ENGINE_STANDARD.md with info for {release_info['tag']}")

if __name__ == "__main__":
    info = fetch_latest_godot_release()
    if info:
        update_engine_standard(info)
    else:
        print("Could not update Engine Standard.")
