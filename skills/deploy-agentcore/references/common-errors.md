<overview>
Common AgentCore deployment errors and solutions.
</overview>

<error name="invalid_agent_name">
Error message:
```
Error: Agent name cannot contain hyphens
```

Cause: Agent names must use underscores, not hyphens.

Fix:
```bash
# Wrong
agentcore configure -n my-agent

# Correct
agentcore configure -n my_agent
```
</error>

<error name="missing_api_key">
Error message:
```
Error: ANTHROPIC_API_KEY not set
```

Cause: API key not available in cloud environment.

Fix: Load from Secrets Manager in entry point:
```python
import boto3

def load_api_key():
    client = boto3.client("secretsmanager", region_name="us-east-1")
    response = client.get_secret_value(SecretId="your-secret-arn")
    os.environ["ANTHROPIC_API_KEY"] = response["SecretString"]

load_api_key()
```
</error>

<error name="memory_mode_typo">
Error message:
```
Error: Invalid memory mode 'LTM_AND_STM'
```

Cause: Wrong order of memory mode.

Fix: Use `STM_AND_LTM` (STM first).
</error>

<error name="windows_encoding">
Error message:
```
UnicodeEncodeError: 'charmap' codec can't encode character
```

Cause: Windows console can't display Unicode characters.

Fix: Prefix commands with encoding:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore deploy
```
</error>

<error name="secrets_access_denied">
Error message:
```
AccessDeniedException: User is not authorized to perform secretsmanager:GetSecretValue
```

Cause: IAM role lacks Secrets Manager permissions.

Fix: Add policy to role:
```json
{
    "Effect": "Allow",
    "Action": ["secretsmanager:GetSecretValue"],
    "Resource": ["arn:aws:secretsmanager:REGION:ACCOUNT:secret:PREFIX-*"]
}
```
</error>

<error name="s3_access_denied">
Error message:
```
AccessDenied: Access Denied
```

Cause: IAM role lacks S3 permissions.

Fix: Add S3 permissions:
```json
{
    "Effect": "Allow",
    "Action": ["s3:GetObject", "s3:PutObject"],
    "Resource": "arn:aws:s3:::YOUR-BUCKET/*"
}
```
</error>

<error name="codebuild_timeout">
Error message:
```
Build timed out
```

Cause: Complex dependencies taking too long.

Fix:
1. Reduce dependencies
2. Use direct_code_deploy instead of container
3. Check CodeBuild logs for specific issues
</error>

<error name="boto3_wrong_parameters">
Error message:
```
Unknown parameter in input: "agentRuntimeId"
```

Cause: Wrong boto3 parameter names.

Fix: Use correct parameters:
```python
# Wrong
client.invoke_agent_runtime(
    agentRuntimeId=...,
    agentRuntimeSessionId=...
)

# Correct
client.invoke_agent_runtime(
    agentRuntimeArn=...,
    runtimeSessionId=...
)
```
</error>

<error name="streaming_body_json">
Error message:
```
JSONDecodeError: Expecting value: line 1 column 1
```

Cause: Trying to JSON parse StreamingBody directly.

Fix: Read body first:
```python
body = response.get('response')
if hasattr(body, 'read'):
    body = body.read().decode('utf-8')
result = json.loads(body)
```
</error>

<error name="docker_hub_rate_limit">
Error message (in CodeBuild logs):
```
429 Too Many Requests
toomanyrequests: You have reached your unauthenticated pull rate limit
```

Cause: Docker Hub limits unauthenticated pulls from CodeBuild.

Fix: Use AWS Public ECR in Dockerfile:
```dockerfile
# Wrong - Docker Hub (rate limited)
FROM python:3.11-slim

# Correct - AWS Public ECR (no rate limit)
FROM public.ecr.aws/docker/library/python:3.11-slim
```
</error>

<error name="missing_dockerfile">
Error message (in CodeBuild logs):
```
failed to read dockerfile: open Dockerfile: no such file or directory
```

Cause: CLI didn't create Dockerfile for container deployment.

Fix: Create Dockerfile manually in project root:
```dockerfile
FROM public.ecr.aws/docker/library/python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir bedrock-agentcore
COPY . .
EXPOSE 8080
CMD ["python", "agentcore_app.py"]
```
</error>

<error name="wrong_boto3_client">
Error message:
```
'AgentsforBedrockRuntime' object has no attribute 'invoke_agent_runtime'
```

Cause: Wrong boto3 client for AgentCore.

Fix: Use correct client name:
```python
# Wrong - Bedrock Agents client
client = boto3.client("bedrock-agent-runtime", region_name=REGION)

# Correct - AgentCore client
client = boto3.client("bedrock-agentcore", region_name=REGION)
```
</error>
