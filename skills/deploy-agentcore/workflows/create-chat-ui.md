<required_reading>
Read these reference files NOW:
1. references/prerequisites.md
</required_reading>

<process>
Step 1: Get Agent ARN

From .bedrock_agentcore.yaml:
```yaml
agentRuntimeArn: arn:aws:bedrock-agentcore:REGION:ACCOUNT:runtime/AGENT_NAME-ID
```

Step 2: Add Streamlit Dependency

Add to pyproject.toml:
```toml
dependencies = [
    "streamlit>=1.52.1",
]
```

Run: `uv sync`

Step 3: Create Chat UI

Copy templates/chat_ui.py to your project and update:
- AGENT_ARN - Your agent's ARN
- REGION - Your deployment region

Step 4: Configure AWS Credentials

Ensure boto3 can access your AWS credentials:
- AWS CLI configured (`aws configure`)
- Or environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

Step 5: Run Locally

```bash
uv run streamlit run chat_ui.py
```

Opens browser at http://localhost:8501

Step 6: Key boto3 API Details

```python
import boto3
client = boto3.client("bedrock-agentcore", region_name=REGION)

response = client.invoke_agent_runtime(
    agentRuntimeArn=AGENT_ARN,       # Not agentRuntimeId
    runtimeSessionId=session_id,      # Not agentRuntimeSessionId
    payload=json.dumps({"prompt": prompt})
)

# Response is StreamingBody
body = response.get('response')
if hasattr(body, 'read'):
    body = body.read().decode('utf-8')
result = json.loads(body)
```

Step 7: Production Deployment (Optional)

For public access, deploy to:
- Streamlit Community Cloud
- AWS App Runner
- Any Python hosting (Heroku, Railway, etc.)
</process>

<success_criteria>
Chat UI complete when:
- [ ] Streamlit runs without errors
- [ ] Messages send to agent
- [ ] Responses display correctly
- [ ] Session persists across messages
</success_criteria>
