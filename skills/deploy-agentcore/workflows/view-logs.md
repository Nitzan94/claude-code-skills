<required_reading>
Read these reference files NOW:
1. references/architecture.md
</required_reading>

<process>
Step 1: Understand Observability Options

AgentCore provides:
- CloudWatch logs - Standard AWS logging
- OpenTelemetry - Distributed tracing
- AgentCore Console - Visual execution inspection

Step 2: Check OpenTelemetry Status

By default, OpenTelemetry is enabled. To disable during configure:

```bash
PYTHONIOENCODING=utf-8 uv run agentcore configure \
    -e agentcore_entry.py \
    -n my_agent \
    --disable-otel
```

Step 3: View CloudWatch Logs

In AWS Console:
1. Go to CloudWatch > Log groups
2. Find `/aws/agentcore/YOUR_AGENT_NAME`
3. Browse log streams for recent invocations

Via AWS CLI:
```bash
aws logs describe-log-groups --log-group-name-prefix "/aws/agentcore"

aws logs tail "/aws/agentcore/YOUR_AGENT_NAME" --follow
```

Step 4: View AgentCore Status

```bash
PYTHONIOENCODING=utf-8 uv run agentcore status --verbose
```

Returns detailed JSON with:
- Deployment status
- Runtime ARN
- Error messages
- Last deployment time

Step 5: Debug Invocation Errors

For invoke failures, check:

1. Agent status:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore status --verbose
```

2. CloudWatch logs for stack traces

3. IAM permissions if access denied errors

4. Secrets Manager if API key errors

Step 6: Monitor Metrics

Key metrics in CloudWatch:
- Invocations - Total invoke calls
- Duration - Execution time
- Errors - Failed invocations
- Throttles - Rate limit hits

Gateway metrics:
- TargetExecutionTime
- SystemErrors
- UserErrors

Step 7: Enable Detailed Tracing

For production debugging, use AWS X-Ray integration:
1. Enable X-Ray in agent configuration
2. View traces in X-Ray console
3. Analyze execution timeline and dependencies
</process>

<troubleshooting>
Common log patterns to search for:

- "ANTHROPIC_API_KEY" - API key issues
- "AccessDeniedException" - IAM permission issues
- "timeout" - Execution timeout
- "memory" - Memory/session issues
- "Error" - General errors

Filter CloudWatch logs:
```bash
aws logs filter-log-events \
    --log-group-name "/aws/agentcore/YOUR_AGENT" \
    --filter-pattern "ERROR"
```
</troubleshooting>

<success_criteria>
Observability setup complete when:
- [ ] CloudWatch logs accessible
- [ ] Can view invocation history
- [ ] Error messages visible for debugging
</success_criteria>
