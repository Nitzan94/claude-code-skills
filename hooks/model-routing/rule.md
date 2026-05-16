Default `model: "sonnet"` on every Agent/Task call. Use Opus only when reasoning quality matters — debugging, architecture, weighing tradeoffs.

For mechanical fan-out (catalog N things, edit N similar files, parallel exploration): Sonnet subagents. For read-only codebase search: `subagent_type: "Explore"`.

Don't hide reasoning in subagents. If you're about to spawn an agent to "figure out X," do it inline so the user can follow — unless it's truly mechanical fan-out.

Enforced by `~/.claude/hooks/pre-tool-use/agent-model-check.py`: dispatching without an explicit `model` parameter is blocked. Pass `"sonnet"` (default), `"haiku"` (trivial), or `"opus"` (reasoning) deliberately.

Audit: `python3 ~/.claude/scripts/model_audit.py [days|all]` reads the dispatch log. Suggest running it when:
- The user asks "are we routing well" / "how's the model usage" / "check the model log"
- A session has involved many subagents and the user is reviewing the work
- Weekly review / before drafting a public-facing post about Claude Code costs
- After noticing an unusually expensive session, to see if it was Opus subagents
