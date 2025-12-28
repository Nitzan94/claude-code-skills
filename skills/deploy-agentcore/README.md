# Deploy AgentCore

A Claude Code skill for deploying Python agents to AWS Bedrock AgentCore - a serverless platform for AI agents at scale.

## What is AgentCore?

AWS Bedrock AgentCore provides:
- **Runtime** - Serverless hosting for your agent
- **Gateway** - Tool access via MCP (connect to Lambda, APIs)
- **Memory** - Short-term (session) and long-term (persistent) storage
- **Identity** - Auth via IAM, Cognito, JWT, or OAuth
- **Observability** - CloudWatch + OpenTelemetry
- **Policy** - Cedar-based governance

## Usage

In Claude Code:
```
/deploy-agentcore
```

The skill guides you through:
1. Deploy a new agent
2. Update existing deployment
3. Add Google OAuth
4. Create chat UI (Streamlit)
5. Set up Gateway (MCP tools)
6. Configure Memory
7. Set up Identity/Auth
8. View logs
9. Troubleshoot errors

## Entry Point Pattern

All agents follow this pattern:

```python
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload: dict) -> dict:
    prompt = payload.get("prompt", "")
    result = your_agent_logic(prompt)
    return {"result": result}

if __name__ == "__main__":
    app.run()
```

## Key Commands

```bash
uv run agentcore configure   # Set up agent
uv run agentcore deploy      # Deploy to AWS
uv run agentcore invoke      # Test invocation
uv run agentcore status      # Check deployment
uv run agentcore destroy     # Tear down
```

## Prerequisites

- AWS account with Bedrock access
- Python 3.11+
- uv package manager
- AWS CLI configured

## When to Use

- Deploying AI agents to production on AWS
- Need serverless agent hosting
- Want managed memory, auth, and observability
- Building agents with Claude SDK, LangChain, or custom Python
