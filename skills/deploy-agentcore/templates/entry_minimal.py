# ABOUTME: Minimal AgentCore entry point template
# ABOUTME: Bare minimum for any Python-based agent

from typing import Any, Dict
from bedrock_agentcore import BedrockAgentCoreApp

app = BedrockAgentCoreApp()


def process_request(prompt: str) -> str:
    """Your agent logic here."""
    # === CUSTOMIZE: Implement your agent ===
    return f"Received: {prompt}"


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
