# model-routing

Forces every Claude Code Agent/Task dispatch to specify a model parameter. Kills the silent default where subagents inherit the parent model (almost always Opus) without you ever choosing.

## The problem

When you call the `Agent` tool without passing `model`, the subagent inherits the parent's model. The parent is usually Opus, so the subagent is Opus. You can fan out 70 "look up this small thing" calls and every one of them runs your most expensive tier — and nothing in the harness surfaces it.

On subscription this doesn't show up as money. It shows up as slower iterations, more verbose subagent returns bloating your main thread's cache, and burning through plan limits faster than you need to.

## What's in this folder

| File | Where it goes | What it does |
|---|---|---|
| `rule.md` | `~/.claude/rules/model-routing.md` | Loads with every session — tells the model when to pick each tier |
| `agent-model-check.py` | `~/.claude/hooks/pre-tool-use/agent-model-check.py` | PreToolUse hook: blocks Agent/Task dispatch when `model` is unset, logs every call |
| `model_audit.py` | `~/.claude/scripts/model_audit.py` | Reads the dispatch log, breaks down by model and subagent type |
| `settings-snippet.json` | Merge into `~/.claude/settings.json` | Wires the hook under `PreToolUse` matcher `Agent\|Task` |

## Install

```bash
git clone https://github.com/Nitzan94/claude-code-skills.git
cd claude-code-skills/hooks/model-routing

mkdir -p ~/.claude/rules ~/.claude/hooks/pre-tool-use ~/.claude/scripts
cp rule.md ~/.claude/rules/model-routing.md
cp agent-model-check.py ~/.claude/hooks/pre-tool-use/agent-model-check.py
cp model_audit.py ~/.claude/scripts/model_audit.py
```

Then merge the entry in `settings-snippet.json` into the `hooks.PreToolUse` array in `~/.claude/settings.json`. If you don't have a `~/.claude/settings.json` yet, the snippet is a complete minimal example you can drop in as-is.

Start a fresh Claude Code session and ask it to spawn any Agent — the first attempt should be blocked with the rule explanation. Re-issue with `model: "sonnet"` (or whichever tier fits) and it goes through.

Optional: install the `model-audit` skill from `skills/model-audit/` in this same repo to invoke the audit reader via `/model-audit` instead of running the Python script manually.

## How it works

The hook reads the tool input from stdin, checks `tool_input.model`:

- empty / unset → exit 2 with a stderr message telling the model to specify a tier
- any value (`sonnet`, `haiku`, `opus`) → exit 0, allow

The override path is the same call you make today, just with the parameter set. The hook only blocks the *default* path. Conscious overrides go through clean.

Every dispatch (allowed or blocked) is logged to `~/.claude/agent_model_log.jsonl`. The audit script reads that file:

```bash
python3 ~/.claude/scripts/model_audit.py 7     # last 7 days
python3 ~/.claude/scripts/model_audit.py 30    # last 30 days
python3 ~/.claude/scripts/model_audit.py all   # everything
```

Output shows per-model counts, per-subagent-type breakdown, per-project breakdown, and a drift signal that flags how many dispatches were blocked (i.e. how many times the rule caught you).

## Why this matters more than a CLAUDE.md rule

Rules in `CLAUDE.md` or `~/.claude/rules/` work most of the time, but they drift the moment context pressure kicks in. The model convinces itself "this one needs Opus reasoning" and the discipline quietly evaporates over a long session.

Mechanical enforcement at the harness layer doesn't drift. Make the cheap path easy, the expensive path possible but deliberate. That's the only routing discipline that survives a long session.
