---
type: technical_standard
target_engine: OpenClaw Agent Framework
status: initial
---

# Agent Skill: Task Management

## Purpose
This skill defines how the Agent manages persistent tasks using ChromaDB metadata. It allows for cross-session continuity and structured workflow management without adding external infrastructure like Redis.

---

## ChromaDB Task Schema

Tasks are stored as individual documents with specific metadata fields:

| Field | Type | Description |
|---|---|---|
| `task_id` | `string` | Unique UUID or timestamp-based ID. |
| `description` | `string` | Human-readable task description. |
| `status` | `string` | `pending`, `doing`, `done`, `blocked`, `failed`. |
| `priority` | `string` | `low`, `medium`, `high`, `critical`. |
| `agent` | `string` | Assigned agent (e.g., `coder`, `researcher`). |
| `created_at` | `string` | ISO timestamp. |
| `updated_at` | `string` | ISO timestamp. |
| `parent_task` | `string` | (Optional) Task ID for sub-tasks. |

---

## Operational Rules

1. **Self-Correction Logic**: If a task fails, the status must be set to `failed` with a `failure_reason` in metadata. The Orchestrator will then decide whether to retry or re-route.
2. **Context Injection**: Every new session must start by querying `status: doing` tasks to restore "working memory."
3. **Task Completion**: When a task is marked `done`, it is not deleted. It remains for RAG lookup so the Agent can "learn" from how it solved past problems.

---

## CLI Integration (`scripts/warrior.py`)

The `warrior` command interfaces with this skill:
- `warrior add "text"`: Creates a `pending` task.
- `warrior list`: Shows all non-completed tasks.
- `warrior do <id>`: Sets status to `doing`.
- `warrior done <id>`: Sets status to `done` and triggers a session summary.

---

## Consistency Checklist
```
1. Is the task_id unique?
2. Does the status match the allowed enum (pending/doing/done/etc)?
3. Was the updated_at timestamp refreshed?
4. If blocked, is there a clear 'blocker_description'?
```
