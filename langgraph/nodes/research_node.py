"""
Research Node v6.0 — Google GenAI optimization layer.
Async parallel file loading + context caching + optional Google grounding.
"""
from typing import Dict, Any, List
import os
import asyncio
import json
import hashlib
from pathlib import Path


# ---------------------------------------------------------------------------
# Token estimation
# ---------------------------------------------------------------------------

def estimate_tokens(text: str) -> int:
    """Lightweight token estimator (~3 chars per token average)."""
    return len(text) // 3


# ---------------------------------------------------------------------------
# Async file loader
# ---------------------------------------------------------------------------

async def _load_file(path: Path) -> str:
    """Load a single file asynchronously via executor."""
    try:
        loop = asyncio.get_event_loop()
        content = await loop.run_in_executor(None, path.read_text, "utf-8")
        return f"[+] FULL FILE: {path.name}\n{content}\n{'=' * 40}\n"
    except Exception as e:
        return f"[!] FAILED: {path.name} — {e}\n"


async def _parallel_fetch(file_paths: List[Path]) -> str:
    """Fetch multiple files concurrently using asyncio.gather."""
    tasks = [_load_file(p) for p in file_paths]
    results = await asyncio.gather(*tasks)
    return "".join(results)


async def _parallel_tool_enrichment(raw_context: str, query: str) -> str:
    """Run lightweight tool-like analyzers in parallel and merge their outputs."""

    async def context_summary_tool() -> str:
        return (
            "[PARALLEL_TOOLS] context_summary: "
            f"chars={len(raw_context)}, tokens~={estimate_tokens(raw_context)}"
        )

    async def intent_tool() -> str:
        lowered = query.lower()
        intent = "recent_update" if any(k in lowered for k in (
            "latest", "patch", "release", "news", "update", "current", "2026", "4.7"
        )) else "general"
        return f"[PARALLEL_TOOLS] intent: {intent}"

    summary, intent = await asyncio.gather(context_summary_tool(), intent_tool())
    return f"{summary}\n{intent}\n"


def _run_async(coro):
    """Execute async logic from sync code with fallback loop handling."""
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


def _cache_file_path(project_root: str) -> Path:
    override = os.environ.get("CONTEXT_CACHE_PATH", "").strip()
    if override:
        return Path(override)
    return Path(project_root) / "data" / "context_cache.json"


def _read_cache(path: Path) -> Dict[str, Dict[str, str]]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text("utf-8"))
    except Exception:
        return {}


def _write_cache(path: Path, cache_payload: Dict[str, Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache_payload), encoding="utf-8")


def _context_fingerprint(file_paths: List[Path]) -> str:
    parts: List[str] = []
    for file_path in sorted(file_paths):
        try:
            stat = file_path.stat()
            parts.append(f"{file_path}:{stat.st_size}:{stat.st_mtime_ns}")
        except OSError:
            parts.append(f"{file_path}:missing")
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def _extract_query(state: Dict[str, Any]) -> str:
    messages = state.get("messages", [])
    if isinstance(messages, list) and messages:
        latest = messages[-1]
        if isinstance(latest, str):
            return latest
    query = state.get("query", "")
    return query if isinstance(query, str) else ""


def _is_grounding_needed(local_context: str, query: str) -> bool:
    local_tokens = estimate_tokens(local_context)
    if local_tokens < int(os.environ.get("MIN_LOCAL_CONTEXT_TOKENS", "1200")):
        return True
    lowered = query.lower()
    return any(k in lowered for k in (
        "latest", "patch", "release", "news", "update", "current", "today", "2026", "4.7"
    ))


def _extract_response_text(response: Any) -> str:
    text = getattr(response, "text", "")
    if isinstance(text, str) and text.strip():
        return text.strip()

    candidates = getattr(response, "candidates", None)
    if not candidates:
        return ""

    snippets: List[str] = []
    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) if content else None
        if not parts:
            continue
        for part in parts:
            part_text = getattr(part, "text", "")
            if part_text:
                snippets.append(str(part_text))

    return "\n".join(snippets).strip()


def _ground_with_google_search(query: str, model: str) -> str:
    """Try native Google Search grounding through official SDK; fallback gracefully."""
    if not query.strip():
        return ""

    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return ""

    try:
        from google import genai
        from google.genai import types
    except Exception:
        return ""

    effective_model = os.environ.get("GOOGLE_GENAI_MODEL", model)
    prompt = (
        "Find the most recent, reliable information for this game-dev query. "
        "Return concise bullet points and cite the source title/URL when available.\n\n"
        f"Query: {query}"
    )

    client = genai.Client(api_key=api_key)

    # Preferred path: native search grounding tool.
    try:
        config = types.GenerateContentConfig(
            temperature=0.2,
            tools=[types.Tool(google_search=types.GoogleSearch())],
        )
        response = client.models.generate_content(
            model=effective_model,
            contents=prompt,
            config=config,
        )
        grounded = _extract_response_text(response)
        if grounded:
            return grounded
    except Exception:
        pass

    # Fallback path: regular generation without tool.
    try:
        response = client.models.generate_content(
            model=effective_model,
            contents=prompt,
        )
        return _extract_response_text(response)
    except Exception:
        return ""


# ---------------------------------------------------------------------------
# Main node
# ---------------------------------------------------------------------------

def researcher_node(state: Dict[str, Any]) -> Dict:
    """
    Research Node: queries Godot 4.7 and Vulkan documentation.
    v5.0: Async parallel file loading with token budget awareness.
    Supports both local Ollama models and Gemini 3.1 Pro (2M context).
    """
    print("--- NODE: RESEARCHER (v6.0 Cached + Grounded) ---")

    # ---- Detect model and set appropriate token budget ----
    model = os.environ.get("ORCHESTRATOR_MODEL", "ollama/gemma4:4b")
    if "gemini" in model:
        token_budget = int(os.environ.get("CONTEXT_WINDOW_LIMIT", "2000000"))
    else:
        token_budget = int(os.environ.get("CONTEXT_LIMIT", "16000"))

    # ---- Gather files from project ----
    project_root = state.get("project_root", ".")
    target_dirs = ["scripts/", "memory/"]
    extensions = {".gd", ".tscn", ".py", ".md"}

    file_paths: List[Path] = []
    for d in target_dirs:
        dir_path = Path(project_root) / d
        if dir_path.exists():
            file_paths.extend(
                f for f in dir_path.rglob("*")
                if f.is_file() and f.suffix in extensions
            )

    # ---- Context cache ----
    cache_enabled = os.environ.get("RESEARCH_CONTEXT_CACHE", "1") != "0"
    fingerprint = _context_fingerprint(file_paths)
    cache_key = hashlib.sha256(
        f"{project_root}|{model}|{token_budget}|{fingerprint}".encode("utf-8")
    ).hexdigest()
    cache_path = _cache_file_path(project_root)
    cache_hit = False

    raw_context = ""
    if cache_enabled:
        cache_store = _read_cache(cache_path)
        cached_entry = cache_store.get(cache_key, {})
        raw_context = cached_entry.get("raw_context", "")
        cache_hit = bool(raw_context)

    if not raw_context:
        if file_paths:
            raw_context = _run_async(_parallel_fetch(file_paths))
        else:
            raw_context = (
                "[SYSTEM] No project files found in target directories.\n"
                "Godot 4.7 optimized the Forward+ renderer for mobile-desktop parity.\n"
                "Vulkan shading rate updates are now available in the RenderingServer.\n"
            )

        if cache_enabled:
            cache_store = _read_cache(cache_path)
            cache_store[cache_key] = {"raw_context": raw_context}
            _write_cache(cache_path, cache_store)

    # ---- Google grounding fallback ----
    query = _extract_query(state)
    grounding_enabled = os.environ.get("ENABLE_GOOGLE_GROUNDING", "1") != "0"
    grounded_context = ""
    if grounding_enabled and _is_grounding_needed(raw_context, query):
        grounded_context = _ground_with_google_search(query, model)
        if grounded_context:
            raw_context += (
                "\n[GOOGLE_GROUNDED_CONTEXT]\n"
                f"{grounded_context}\n"
                f"{'=' * 40}\n"
            )

    # ---- Parallel tool-calling style enrichment ----
    raw_context += _run_async(_parallel_tool_enrichment(raw_context, query))

    # ---- Token budget enforcement ----
    token_count = estimate_tokens(raw_context)
    if token_count > token_budget:
        max_chars: int = token_budget * 3
        truncate_slice = slice(0, max_chars)
        raw_context = raw_context[truncate_slice]
        raw_context += (
            f"\n[!] TRUNCATED: {token_count:,} tokens exceeded "
            f"budget of {token_budget:,}\n"
        )

    # ---- Build final context with metadata header ----
    final_token_count = estimate_tokens(raw_context)
    header = (
        f"[SYSTEM] Model: {model} | Token budget: {token_budget:,}\n"
        f"[SYSTEM] Files loaded: {len(file_paths)} | "
        f"Estimated tokens: {final_token_count:,}\n"
        f"[SYSTEM] Cache hit: {cache_hit} | "
        f"Grounding used: {bool(grounded_context)}\n"
    )
    context = header + raw_context

    return {
        "research_context": context,
        "token_usage": final_token_count,
        "messages": [
            f"Researcher loaded {len(file_paths)} files "
            f"({final_token_count:,} tokens) via async fetch; "
            f"cache_hit={cache_hit}; grounded={bool(grounded_context)}."
        ],
    }
