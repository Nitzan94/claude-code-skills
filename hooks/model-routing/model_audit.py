#!/usr/bin/env python3
# ABOUTME: Audit Agent/Task model routing — reads ~/.claude/agent_model_log.jsonl
# ABOUTME: Run weekly, after a long session, or when reviewing routing discipline
"""
Usage:
    python3 ~/.claude/scripts/model_audit.py          # last 7 days
    python3 ~/.claude/scripts/model_audit.py 30       # last 30 days
    python3 ~/.claude/scripts/model_audit.py all      # all time
"""
import json, os, sys, datetime
from collections import Counter, defaultdict

LOG = os.path.expanduser("~/.claude/agent_model_log.jsonl")
days_arg = sys.argv[1] if len(sys.argv) > 1 else "7"
cutoff = None
if days_arg != "all":
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=int(days_arg))

if not os.path.exists(LOG):
    print(f"No log file at {LOG}. Hook hasn't fired yet.")
    sys.exit(0)

entries = []
with open(LOG) as f:
    for line in f:
        try: e = json.loads(line)
        except: continue
        if cutoff:
            try: ts = datetime.datetime.strptime(e["ts"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
            except: continue
            if ts < cutoff: continue
        entries.append(e)

if not entries:
    print(f"No dispatches in window ({days_arg} days).")
    sys.exit(0)

label = f"last {days_arg} days" if days_arg != "all" else "all time"
print(f"\n{'='*60}\n  Agent/Task dispatches — {label}: {len(entries)}\n{'='*60}\n")

by_model = Counter(e["model"] for e in entries)
print("By model:")
for m, n in by_model.most_common():
    pct = n / len(entries) * 100
    flag = "  <- BLOCKED (drift attempts)" if m == "(unset)" else ""
    print(f"  {m:12}  {n:5}  ({pct:4.1f}%){flag}")

print("\nBy subagent_type x model:")
combo = defaultdict(Counter)
for e in entries:
    combo[e["subagent_type"]][e["model"]] += 1
for sub in sorted(combo, key=lambda s: -sum(combo[s].values())):
    counts = combo[sub]
    total = sum(counts.values())
    parts = ", ".join(f"{m}:{n}" for m,n in counts.most_common())
    print(f"  {sub[:35]:35}  total={total:4}  {parts}")

# Per-project breakdown via cwd
proj = defaultdict(Counter)
for e in entries:
    pname = os.path.basename(e.get("cwd","")) or "?"
    proj[pname][e["model"]] += 1
print("\nBy project (cwd) x model:")
for p in sorted(proj, key=lambda x: -sum(proj[x].values())):
    counts = proj[p]
    total = sum(counts.values())
    parts = ", ".join(f"{m}:{n}" for m,n in counts.most_common())
    print(f"  {p[:25]:25}  total={total:4}  {parts}")

# Drift signal
unset = by_model.get("(unset)", 0)
opus = by_model.get("opus", 0)
sonnet = by_model.get("sonnet", 0)
print(f"\n{'─'*60}")
if unset > 0:
    print(f"  {unset} blocked drift attempt(s) — model forgetting the rule. Good signal that the hook is earning its keep.")
if opus > 0 and sonnet > 0:
    ratio = opus / (opus + sonnet) * 100
    print(f"  Opus/Sonnet ratio: {ratio:.0f}% Opus. Aim is <20% for healthy routing.")
elif opus > 0 and sonnet == 0:
    print(f"  All-Opus dispatches. Either every task genuinely needed reasoning, or routing has slipped. Review subagent_type list above.")
print()
