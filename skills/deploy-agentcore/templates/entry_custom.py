# ABOUTME: AgentCore entry point for custom Python agents
# ABOUTME: Minimal template for any Python-based agent

import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError
from bedrock_agentcore import BedrockAgentCoreApp
from dotenv import load_dotenv

load_dotenv()

os.environ["AGENTCORE_RUNTIME"] = "true"

# === CUSTOMIZE: Update secret ARN (if needed) ===
API_KEY_SECRET = "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:your-agent/api-key-SUFFIX"


def load_secrets() -> None:
    """Load secrets from Secrets Manager."""
    # Add your secret loading logic here
    pass


load_secrets()

app = BedrockAgentCoreApp()


def process_request(prompt: str) -> str:
    """Your custom agent logic."""
    # === CUSTOMIZE: Your agent implementation ===
    #
    # Examples:
    # - Call an LLM API directly
    # - Run a ML model
    # - Process data
    # - Call external APIs

    return f"TODO: Implement your logic. Received: {prompt}"


@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """AgentCore entry point."""
    prompt = payload.get("prompt", "")

    if not prompt:
        return {"error": "No prompt provided", "result": ""}

    try:
        result = process_request(prompt)
        return {"result": result}
    except Exception as e:
        return {"error": str(e), "result": ""}


if __name__ == "__main__":
    app.run()
