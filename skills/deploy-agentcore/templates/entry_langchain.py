# ABOUTME: AgentCore entry point for LangChain agents
# ABOUTME: Wraps existing LangChain chain for serverless deployment

import os
from typing import Any, Dict

import boto3
from botocore.exceptions import ClientError
from bedrock_agentcore import BedrockAgentCoreApp
from dotenv import load_dotenv

# LangChain imports - customize based on your setup
# from langchain_anthropic import ChatAnthropic
# from langchain.chains import LLMChain
# from langchain.prompts import PromptTemplate

load_dotenv()

os.environ["AGENTCORE_RUNTIME"] = "true"

# === CUSTOMIZE: Update secret ARN ===
API_KEY_SECRET = "arn:aws:secretsmanager:us-east-1:ACCOUNT:secret:your-agent/api-key-SUFFIX"


def load_api_key() -> None:
    """Load API key from Secrets Manager."""
    if os.getenv("ANTHROPIC_API_KEY"):
        return

    try:
        client = boto3.client("secretsmanager", region_name="us-east-1")
        response = client.get_secret_value(SecretId=API_KEY_SECRET)
        os.environ["ANTHROPIC_API_KEY"] = response["SecretString"]
    except ClientError as e:
        raise RuntimeError(f"Failed to fetch API key: {e}")


load_api_key()

app = BedrockAgentCoreApp()


def run_chain(prompt: str) -> str:
    """Run your LangChain chain."""
    # === CUSTOMIZE: Your LangChain setup ===
    #
    # Example:
    # llm = ChatAnthropic(model="claude-sonnet-4-20250514")
    # template = PromptTemplate.from_template("Answer: {question}")
    # chain = LLMChain(llm=llm, prompt=template)
    # result = chain.run(question=prompt)
    # return result

    return f"TODO: Implement your chain. Received: {prompt}"


@app.entrypoint
def invoke(payload: Dict[str, Any]) -> Dict[str, Any]:
    """AgentCore entry point."""
    prompt = payload.get("prompt", "")

    if not prompt:
        return {"error": "No prompt provided", "result": ""}

    try:
        result = run_chain(prompt)
        return {"result": result}
    except Exception as e:
        return {"error": str(e), "result": ""}


if __name__ == "__main__":
    app.run()
