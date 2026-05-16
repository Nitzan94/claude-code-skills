#!/usr/bin/env python3
# ABOUTME: Pre-tool-use hook for Agent/Task — block dispatches without explicit model
# ABOUTME: Logs every dispatch to ~/.claude/agent_model_log.jsonl for weekly audit
import json, sys, os, datetime

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # malformed input — don't block, just skip

inp = data.get("tool_input", {}) or {}
model = (inp.get("model") or "").strip()
subagent = (inp.get("subagent_type") or "").strip()
desc = (inp.get("description") or "").strip()
tool_name = data.get("tool_name", "")

log_path = os.path.expanduser("~/.claude/agent_model_log.jsonl")
entry = {
    "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "tool": tool_name,
    "model": model or "(unset)",
    "subagent_type": subagent or "(default)",
    "description": desc[:200],
    "session_id": data.get("session_id", ""),
    "cwd": data.get("cwd", ""),
}
try:
    with open(log_path, "a") as f:
        f.write(json.dumps(entry) + "\n")
except Exception:
    pass  # logging failure must not block the hook

if not model:
    sys.stderr.write(
        "Per ~/.claude/rules/model-routing.md: pass `model` explicitly on every Agent/Task call.\n"
        "  - 'sonnet' (default for mechanical/search/edit work)\n"
        "  - 'haiku' (trivial format/rename/grep-and-summarize)\n"
        "  - 'opus' (multi-file reasoning, debugging, architecture)\n"
        "Re-issue the call with the model parameter set.\n"
    )
    sys.exit(2)

sys.exit(0)
