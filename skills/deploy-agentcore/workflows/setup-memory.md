<required_reading>
Read these reference files NOW:
1. references/architecture.md
2. references/memory-modes.md
</required_reading>

<process>
Step 1: Understand Memory Options

During `agentcore configure`, you choose memory mode:
- NONE - Stateless (skip with --disable-memory)
- STM - Short-term only (within session)
- LTM - Long-term only (across sessions)
- STM_AND_LTM - Both (recommended)

Step 2: Configure with Memory (Standard)

```bash
PYTHONIOENCODING=utf-8 uv run agentcore configure \
    -e agentcore_entry.py \
    -n my_agent
```

When prompted, select memory mode.

Step 3: Configure without Memory

```bash
PYTHONIOENCODING=utf-8 uv run agentcore configure \
    -e agentcore_entry.py \
    -n my_agent \
    --disable-memory
```

Step 4: Create Standalone Memory Resource

For advanced use cases, create memory separately:

```bash
PYTHONIOENCODING=utf-8 uv run agentcore memory create my_memory \
    --description "Agent long-term memory" \
    --event-expiry-days 90 \
    --region us-west-2
```

Step 5: Check Memory Status

```bash
PYTHONIOENCODING=utf-8 uv run agentcore memory list
PYTHONIOENCODING=utf-8 uv run agentcore memory status MEMORY_ID
```

Step 6: Delete Memory

```bash
PYTHONIOENCODING=utf-8 uv run agentcore memory delete MEMORY_ID --wait
```
</process>

<session_management>
Sessions are identified by runtimeSessionId in invoke calls.

Same session ID = same STM context
Different session ID = new STM context (LTM still shared)

```python
# In chat UI
session_id = str(uuid.uuid4())  # New session per chat window

client.invoke_agent_runtime(
    agentRuntimeArn=AGENT_ARN,
    runtimeSessionId=session_id,
    payload=json.dumps({"prompt": prompt})
)
```
</session_management>

<success_criteria>
Memory setup complete when:
- [ ] Memory mode selected during configure
- [ ] Agent retains context within session (STM)
- [ ] Agent recalls across sessions (LTM) if enabled
</success_criteria>
