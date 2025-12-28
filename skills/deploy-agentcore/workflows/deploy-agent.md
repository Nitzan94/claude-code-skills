<required_reading>
Read these reference files NOW:
1. references/prerequisites.md
2. references/memory-modes.md
</required_reading>

<concepts>
## Deployment Types Explained

AgentCore supports two deployment modes:

**1. direct_code_deploy (default)**
- Packages Python code directly
- Faster iteration, simpler setup
- Limited to standard Python packages
- Best for: Simple agents, quick testing

**2. container (via CodeBuild)**
- Builds Docker container in AWS CodeBuild
- Full control over dependencies and environment
- Supports custom system packages
- Best for: Production agents, complex dependencies
- This is what `agentcore deploy` uses by default now

When you run `agentcore deploy`, it:
1. Creates a ZIP of your code
2. Uploads to S3
3. Triggers CodeBuild to build ARM64 Docker image
4. Pushes image to ECR
5. Deploys container to AgentCore Runtime
</concepts>

<process>
Step 1: Verify Prerequisites

```bash
aws --version          # AWS CLI v2
uv --version           # uv package manager
python --version       # Python 3.10+
aws sts get-caller-identity  # Valid AWS credentials
```

Step 2: Install Dependencies

Add to pyproject.toml:
```toml
dependencies = [
    "bedrock-agentcore>=0.1.0",
    "bedrock-agentcore-starter-toolkit>=0.1.0",
]
```

Run: `uv sync`

Step 3: Create Entry Point

Choose template based on your framework:
- templates/entry_minimal.py - Bare minimum
- templates/entry_claude_sdk.py - For Claude SDK
- templates/entry_langchain.py - For LangChain
- templates/entry_custom.py - For custom agents

Copy template to your project as `agentcore_entry.py` and customize.

Step 4: Store API Keys in Secrets Manager

```bash
# Create secret
aws secretsmanager create-secret \
    --name "your-agent/api-key" \
    --secret-string "your-actual-api-key" \
    --region us-east-1

# Note the ARN from output - you'll need it
```

Add code to load secrets in your agent:
```python
import os
import boto3

def load_secrets():
    """Load API keys from Secrets Manager if not already set."""
    if os.getenv("YOUR_API_KEY"):
        return  # Already set (local dev)

    try:
        client = boto3.client("secretsmanager", region_name="us-east-1")
        response = client.get_secret_value(SecretId="your-agent/api-key")
        os.environ["YOUR_API_KEY"] = response["SecretString"]
        print("[OK] Loaded API key from Secrets Manager")
    except Exception as e:
        print(f"[WARN] Could not load secrets: {e}")

load_secrets()  # Call at module load
```

Step 5: Configure Agent

```bash
PYTHONIOENCODING=utf-8 uv run agentcore configure \
    -e agentcore_entry.py \
    -n your_agent_name
```

Answer prompts:
- Region: us-east-1 or us-west-2
- Memory: STM_AND_LTM (for conversational agents)
- Header allowlist: None (press Enter)

Step 6: Create Dockerfile

Create `Dockerfile` in project root:
```dockerfile
FROM public.ecr.aws/docker/library/python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir bedrock-agentcore aws-opentelemetry-distro>=0.10.0

# Copy application code
COPY . .

EXPOSE 8080

# OpenTelemetry config for observability
ENV OTEL_PYTHON_DISTRO=aws_distro
ENV OTEL_PYTHON_CONFIGURATOR=aws_configurator
ENV AGENT_OBSERVABILITY_ENABLED=true

# Run with OpenTelemetry instrumentation
CMD ["opentelemetry-instrument", "python", "agentcore_entry.py"]
```

IMPORTANT:
- Use `public.ecr.aws` base image to avoid Docker Hub rate limits
- Include `aws-opentelemetry-distro` for observability
- Use `opentelemetry-instrument` wrapper for traces

Step 7: Grant Secrets Manager Access

Get role name from .bedrock_agentcore.yaml (look for `execution_role`), then:

```bash
aws iam put-role-policy \
    --role-name AmazonBedrockAgentCoreSDKRuntime-REGION-SUFFIX \
    --policy-name SecretsManagerAccess \
    --policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Action": ["secretsmanager:GetSecretValue"],
            "Resource": ["arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:your-agent/*"]
        }]
    }' \
    --region us-east-1
```

Step 8: Deploy

```bash
PYTHONIOENCODING=utf-8 uv run agentcore deploy
```

Wait for CodeBuild to complete (2-5 minutes).

Step 9: Test

```bash
PYTHONIOENCODING=utf-8 uv run agentcore invoke '{"prompt": "Hello, test message"}'
```

Step 10: Verify Observability

Wait 5-10 minutes, then check:
- Dashboard: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#gen-ai-observability/agent-core
- Runtime console: https://console.aws.amazon.com/bedrock-agentcore/home?region=us-east-1

If agent doesn't appear in observability, check that:
1. Dockerfile includes OpenTelemetry setup
2. `aws-opentelemetry-distro` is installed
3. CMD uses `opentelemetry-instrument` wrapper
</process>

<troubleshooting>
## Common Issues

**Docker Hub rate limit (429 Too Many Requests)**
- Fix: Use `FROM public.ecr.aws/docker/library/python:3.11-slim`

**API key not loading in cloud**
- Fix: Add Secrets Manager code to agent
- Fix: Add IAM policy to execution role

**Agent not in observability dashboard**
- Fix: Add OpenTelemetry to Dockerfile
- Wait 10 minutes after first invoke

**CodeBuild logs not visible**
- See workflows/troubleshoot.md for log retrieval script
</troubleshooting>

<success_criteria>
Deployment complete when:
- [ ] agentcore deploy shows "Deployment successful"
- [ ] agentcore invoke returns agent response
- [ ] No "Missing API key" errors
- [ ] Agent appears in Runtime console
- [ ] Agent appears in Observability dashboard (after 10 min)
</success_criteria>
