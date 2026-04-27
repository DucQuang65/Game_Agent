# 🛡️ Game Agent OS — Security Checklist

## 0) Data Privacy & Log Protection

> [!CAUTION]
> Failure to follow these rules may expose user conversation history to public log files.

### 0.1 Log Rotation Policy
- All files in `logs/` **must** be purged or rotated every **7 days**.
- Configure via `logrotate` or a cron job:
  ```bash
  # /etc/logrotate.d/game-agent
  /home/asus/Game_Agent/logs/*.log {
      daily
      rotate 7
      compress
      missingok
      notifempty
      delaycompress
  }
  ```

### 0.2 Log Anonymization Rules
- **DO NOT** log raw message content from Telegram, API responses, or user prompts.
- Log format must be restricted to: `[timestamp] | [agent_id] | [task_type] | [status]`
- **Example (correct)**: `2026-04-27T14:30Z | coder | code_generation | success`
- **Example (wrong — never do this)**: `User asked: how do I hack...`

### 0.3 Git Safety
- Ensure all of the following are in `.gitignore`:
  - `logs/`, `data/`, `chroma_db/`, `secrets/`, `.env`, `openclaw.json`

---

## 1) Rotate all exposed secrets first

1. Rotate Telegram bot token at BotFather.
2. Rotate Gemini API key in Google AI Studio.
3. Rotate OpenClaw gateway token.

## 2) Apply hardened config safely

1. Backup current config:

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%F-%H%M%S)
```

2. Copy template and fill placeholders:

```bash
cp ./openclaw.hardened.example.json ~/.openclaw/openclaw.json
nano ~/.openclaw/openclaw.json
```

3. Validate and auto-fix:

```bash
$HOME/.npm-global/bin/openclaw doctor --fix
```

4. Re-check sandbox effective policy:

```bash
$HOME/.npm-global/bin/openclaw sandbox explain --json
```

## 3) Lock Telegram DM to your account only

Use your numeric Telegram user ID:

```bash
$HOME/.npm-global/bin/openclaw config set channels.telegram.dmPolicy 'allowlist'
$HOME/.npm-global/bin/openclaw config set channels.telegram.allowFrom '["YOUR_TELEGRAM_USER_ID"]'
```

## 4) Verify web search still works

1. Keep web provider enabled in config:
- tools.web.search.enabled = true
- tools.web.search.provider = duckduckgo

2. Confirm from runtime:

```bash
$HOME/.npm-global/bin/openclaw status
```

## 5) Clean old logs after rotation

Only do this after rotating secrets:

```bash
rm -f ~/.openclaw/logs/*.log
```

## 6) Ongoing hardening

1. Run periodic security audits:

```bash
$HOME/.npm-global/bin/openclaw security audit --deep
```

2. Keep session isolation for DMs:
- session.dmScope = per-channel-peer

3. Keep project boundary instructions in workspace AGENTS file.
