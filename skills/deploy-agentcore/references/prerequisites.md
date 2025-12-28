<overview>
Requirements for deploying agents to AWS Bedrock AgentCore.
</overview>

<aws_requirements>
AWS CLI v2

Install: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Verify:
```bash
aws --version
```

Configure credentials:
```bash
aws configure
```

Required IAM permissions:
- bedrock-agentcore:*
- codebuild:*
- ecr:*
- s3:*
- iam:PassRole
- secretsmanager:GetSecretValue (if using secrets)
</aws_requirements>

<python_requirements>
Python 3.10 or 3.11

Verify:
```bash
python --version
```

Use uv for package management:
```bash
pip install uv
uv --version
```
</python_requirements>

<packages>
Required packages:

```toml
[project]
dependencies = [
    "bedrock-agentcore>=0.1.0",
    "bedrock-agentcore-starter-toolkit>=0.1.0",
]
```

Install:
```bash
uv sync
```
</packages>

<aws_regions>
AgentCore is available in select regions:
- us-west-2 (Oregon) - Recommended
- us-east-1 (N. Virginia)

Check latest availability in AWS documentation.
</aws_regions>

<verification>
Verify all prerequisites:

```bash
aws --version
python --version
uv --version
aws sts get-caller-identity
```

All commands should succeed without errors.
</verification>
