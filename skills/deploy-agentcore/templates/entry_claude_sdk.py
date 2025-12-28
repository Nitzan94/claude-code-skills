# ABOUTME: AgentCore entry point for Claude Agent SDK based agents
# ABOUTME: Wraps existing SDK agent for serverless deployment

import asyncio
import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError
from bedrock_agentcore import BedrockAgentCoreApp
from dotenv import load_dotenv

# Your existing imports - adjust based on your SDK
# Option 1: Claude Agent SDK (pip install claude-agent-sdk)
# from claude_sdk import Agent
# Option 2: Anthropic SDK with tool use
# from anthropic import Anthropic
# from tools.your_tools import YourTools  # Add your tools

load_dotenv()

# Mark as cloud environment (for conditional logic in tools)
os.environ["AGENTCORE_RUNTIME"] = "true"

# === CUSTOMIZE: Update secret ARN ===
ANTHROPIC_KEY_SECRET = "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:your-agent/anthropic-key-SUFFIX"


def load_anthropic_key_from_secrets() -> None:
    """Load API key from Secrets Manager if not already set."""
    if os.getenv("ANTHROPIC_API_KEY"):
        return

    try:
        client = boto3.client("secretsmanager", region_name="us-east-1")
        response = client.get_secret_value(SecretId=ANTHROPIC_KEY_SECRET)
        os.environ["ANTHROPIC_API_KEY"] = response["SecretString"]
    except ClientError as e:
        raise RuntimeError(f"Failed to fetch API key: {e}")


load_anthropic_key_from_secrets()

app = BedrockAgentCoreApp()


async def run_agent_query(prompt: str) -> str:
    """Run the agent with given prompt."""
    # === CUSTOMIZE: Your agent implementation ===
    # Example with Anthropic SDK:
    # from anthropic import Anthropic
    # client = Anthropic()
    # response = client.messages.create(
    #     model="claude-sonnet-4-20250514",
    #     max_tokens=4096,
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # return response.content[0].text
    
    return f"TODO: Implement your agent. Received: {prompt}"


@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """AgentCore entry point."""
    prompt = payload.get("prompt", "")

    if not prompt:
        return {"error": "No prompt provided", "result": ""}

    try:
        result = asyncio.run(run_agent_query(prompt))
        return {"result": result}
    except Exception as e:
        return {"error": str(e), "result": ""}


if __name__ == "__main__":
    app.run()
