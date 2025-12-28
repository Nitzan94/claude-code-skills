<required_reading>
Read these reference files NOW:
1. references/cli-reference.md
</required_reading>

<process>
Step 1: Check Current Status

```bash
PYTHONIOENCODING=utf-8 uv run agentcore status
```

Step 2: Make Code Changes

Edit your entry point file or dependencies as needed.

Step 3: Redeploy

For direct_code_deploy (default):
```bash
PYTHONIOENCODING=utf-8 uv run agentcore deploy
```

For container deployment with dependency changes:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore deploy --force-rebuild-deps
```

Step 4: Test Changes

```bash
PYTHONIOENCODING=utf-8 uv run agentcore invoke --prompt "Test message"
```

Step 5: If Deployment Fails

Check status for errors:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore status --verbose
```

Force rebuild if caching issues:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore deploy --local-build
```
</process>

<tips>
Quick iteration tips:
- Use `--local` flag for local testing before cloud deploy
- direct_code_deploy is faster than container for small changes
- Check CodeBuild console for detailed build logs
- Use `--env KEY=VALUE` to add environment variables
</tips>

<success_criteria>
Update complete when:
- [ ] agentcore deploy succeeds
- [ ] agentcore invoke returns updated behavior
- [ ] No errors in status output
</success_criteria>
