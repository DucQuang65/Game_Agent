import subprocess
import time
import json
import os
from typing import TypedDict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE_FILE = os.path.join(PROJECT_ROOT, "data", "model_state.json")
IDLE_TIMEOUT = 300 # 5 minutes


class ModelState(TypedDict):
    active_model: str | None
    last_used: float


def get_state() -> ModelState:
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        active_model = raw.get("active_model") if isinstance(raw, dict) else None
        last_used_raw = raw.get("last_used") if isinstance(raw, dict) else 0
        return {
            "active_model": active_model if isinstance(active_model, str) else None,
            "last_used": float(last_used_raw) if isinstance(last_used_raw, (int, float)) else 0.0,
        }
    return {"active_model": None, "last_used": 0}


def save_state(model_name: str | None) -> None:
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"active_model": model_name, "last_used": time.time()}, f)


def load_model(model_name: str) -> bool:
    state = get_state()
    if state["active_model"] == model_name:
        save_state(model_name)
        return True
    
    # Stop current model if exists
    active_model = state["active_model"]
    if active_model is not None:
        subprocess.run(["ollama", "stop", active_model], check=False)
    
    # Start new model
    res = subprocess.run(["ollama", "run", model_name, "/bye"], check=False)
    if res.returncode == 0:
        save_state(model_name)
        return True
    return False


def maybe_unload() -> None:
    state = get_state()
    active_model = state["active_model"]
    if active_model is None:
        return

    if time.time() - state["last_used"] > IDLE_TIMEOUT:
        print(f"Idle timeout reached for {active_model}. Unloading...")
        subprocess.run(["ollama", "stop", active_model], check=False)
        save_state(None)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "unload":
            maybe_unload()
        else:
            load_model(sys.argv[1])
