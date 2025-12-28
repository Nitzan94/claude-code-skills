<overview>
AgentCore memory modes control how agents remember context.
</overview>

<modes>
NONE

No memory. Each invoke is independent. Use for:
- Stateless operations
- One-shot queries
- Testing

STM (Short-Term Memory)

Memory within a session. Cleared when session ends. Use for:
- Single conversation threads
- Temporary context

LTM (Long-Term Memory)

Memory persists across sessions. Use for:
- User preferences
- Historical data
- Learning from interactions

STM_AND_LTM (Recommended)

Both short and long term. Use for:
- Conversational agents
- Personal assistants
- Most production use cases
</modes>

<configuration>
During agentcore configure:

```
? Choose memory mode
> NONE
  STM
  LTM
  STM_AND_LTM
```

Or in .bedrock_agentcore.yaml:
```yaml
memory:
  mode: STM_AND_LTM
```
</configuration>

<sessions>
Sessions are identified by runtimeSessionId in invoke calls.

Same session ID = same STM context
Different session ID = new STM context (LTM still shared)

```python
# Chat UI example
session_id = str(uuid.uuid4())  # New session per chat window

client.invoke_agent_runtime(
    agentRuntimeArn=AGENT_ARN,
    runtimeSessionId=session_id,
    payload=json.dumps({"prompt": prompt})
)
```
</sessions>

<common_error>
Wrong order causes error:

```
Error: Invalid memory mode 'LTM_AND_STM'
```

Correct: `STM_AND_LTM`
</common_error>
