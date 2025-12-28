<required_reading>
Read this reference file NOW:
1. references/common-errors.md
</required_reading>

<process>
Step 1: Identify Error Type

Check agentcore output for these common errors:

**Invalid agent name**
```
Error: Agent name cannot contain hyphens
```
Fix: Use underscores: `my_agent` not `my-agent`

**Missing API key**
```
Error: ANTHROPIC_API_KEY not set
```
Fix: Load from Secrets Manager in entry point (see templates/entry_claude_sdk.py)

**Memory mode typo**
```
Error: Invalid memory mode 'LTM_AND_STM'
```
Fix: Use `STM_AND_LTM` (correct order)

**Windows encoding**
```
UnicodeEncodeError: 'charmap' codec can't encode character
```
Fix: Prefix command with `PYTHONIOENCODING=utf-8`

**Secrets Manager access denied**
```
AccessDeniedException: User is not authorized to perform secretsmanager:GetSecretValue
```
Fix: Update IAM role policy (see templates/policy.json)

**S3 access denied**
```
AccessDenied: Access Denied
```
Fix: Add S3 permissions to IAM role

Step 2: Check Deployment Status

```bash
PYTHONIOENCODING=utf-8 uv run agentcore status
```

Step 3: Check CodeBuild Logs

If deploy fails during build, get logs via Python (CLI doesn't show them):

```python
import boto3

# Get latest build ID
cb = boto3.client('codebuild', region_name='us-east-1')
builds = cb.list_builds_for_project(projectName='bedrock-agentcore-YOUR_AGENT-builder')
build_id = builds['ids'][0]

# Get build details to find log stream
build = cb.batch_get_builds(ids=[build_id])['builds'][0]
stream = build['logs']['streamName']

# Fetch logs
logs = boto3.client('logs', region_name='us-east-1')
response = logs.get_log_events(
    logGroupName=f"/aws/codebuild/{build['projectName']}",
    logStreamName=stream,
    limit=100
)
for e in response['events']:
    print(e['message'])
```

Or via AWS Console: CloudWatch > Log Groups > /aws/codebuild/PROJECT-NAME

Step 4: Test Locally First

```bash
PYTHONIOENCODING=utf-8 uv run agentcore deploy --local
```

Step 5: Verify IAM Role

Get role from .bedrock_agentcore.yaml:
```yaml
executionRole: arn:aws:iam::ACCOUNT:role/ROLE-NAME
```

Check attached policies in AWS IAM console.

Step 6: Check Secrets

```bash
aws secretsmanager get-secret-value --secret-id "your-secret-arn" --region us-east-1
```

Step 7: Force Rebuild

If caching issues:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore deploy --force-rebuild-deps
```
</process>

<success_criteria>
Issue resolved when:
- [ ] Error message no longer appears
- [ ] agentcore invoke returns expected response
- [ ] No access denied errors in logs
</success_criteria>
