---
name: model-audit
description: "Audit Agent/Task model routing — reads the dispatch log written by the model-routing PreToolUse hook and breaks down spend by model, subagent type, and project. Use when the user asks 'how's the model routing', 'audit my model usage', 'check the dispatch log', 'is the routing hook working', '/model-audit', or before drafting any public-facing post about Claude Code usage. Requires the model-routing hook to be installed first (see hooks/model-routing in this repo)."
---

# /model-audit — Routing Discipline Reader

Reads `~/.claude/agent_model_log.jsonl` (written by the `agent-model-check.py` PreToolUse hook) and shows whether your subagent dispatches are actually using the model tiers you intended.

**Arguments:** "$ARGUMENTS" — either a number of days (`7`, `30`) or the literal word `all`. Default: `7`.

## Step 1: Verify prerequisites

Check that the audit script and log file both exist:

```bash
test -f ~/.claude/scripts/model_audit.py && echo "script: ok" || echo "script: MISSING — install hooks/model-routing from this repo first"
test -f ~/.claude/agent_model_log.jsonl && echo "log: ok" || echo "log: MISSING — hook hasn't fired yet, dispatch any Agent in a fresh session first"
```

If either is missing, tell the user to install `hooks/model-routing/` from the same repo (https://github.com/Nitzan94/claude-code-skills/tree/master/hooks/model-routing) — the skill is the reader; the hook is what writes the data it reads.

## Step 2: Run the audit

Parse the user's arguments. If they said a number, pass it; if they said "all", pass `all`; if they said nothing, default to `7`:

```bash
python3 ~/.claude/scripts/model_audit.py "${ARGS:-7}"
```

## Step 3: Interpret the output

The script's output already includes a drift signal at the bottom. Read it and tell the user in one sentence what it means for their routing discipline:

- **Many `(unset)` entries** → the hook is catching frequent drift attempts. Good — that's the hook earning its keep.
- **Opus/Sonnet ratio above ~20%** → routing has slipped. Suggest scanning the `By subagent_type x model` section for which subagent types are running Opus when they shouldn't.
- **Zero dispatches in window** → either a quiet week, or check whether the hook is still wired (`grep agent-model-check ~/.claude/settings.json`).

Don't add new analysis the script didn't produce. The script is the source of truth; the skill's job is to surface it and frame the interpretation.
