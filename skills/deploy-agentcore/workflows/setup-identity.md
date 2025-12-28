<required_reading>
Read these reference files NOW:
1. references/architecture.md
2. references/cli-reference.md
</required_reading>

<process>
Step 1: Choose Identity Method

- **IAM** (default) - Agent uses IAM role, no extra setup
- **Cognito** - User federation or M2M authentication
- **AWS JWT** - Secretless M2M with outbound web identity federation
- **External providers** - GitHub, Google, Salesforce OAuth

Step 2: Setup Cognito (User Federation)

For user-based authentication:

```bash
PYTHONIOENCODING=utf-8 uv run agentcore identity setup-cognito \
    --auth-flow user \
    --region us-west-2
```

Get token for testing:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore identity get-cognito-inbound-token \
    --auth-flow user \
    --pool-id POOL_ID \
    --client-id CLIENT_ID \
    --username USERNAME \
    --password PASSWORD
```

Step 3: Setup Cognito (M2M)

For machine-to-machine authentication:

```bash
PYTHONIOENCODING=utf-8 uv run agentcore identity setup-cognito \
    --auth-flow m2m \
    --region us-west-2
```

Step 4: Setup AWS JWT

For secretless M2M to external services:

```bash
PYTHONIOENCODING=utf-8 uv run agentcore identity setup-aws-jwt \
    --audience "https://your-api.example.com" \
    --signing-algorithm ES384 \
    --duration 300 \
    --region us-west-2
```

List configured JWT:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore identity list-aws-jwt
```

Step 5: Create Credential Provider

For external OAuth providers:

```bash
PYTHONIOENCODING=utf-8 uv run agentcore identity create-credential-provider \
    --name google_provider \
    --type google \
    --client-id "YOUR_CLIENT_ID" \
    --client-secret "YOUR_CLIENT_SECRET" \
    --region us-west-2
```

Supported types: cognito, github, google, salesforce

Step 6: Create Workload Identity

For agent-to-service authentication:

```bash
PYTHONIOENCODING=utf-8 uv run agentcore identity create-workload-identity \
    --name my_workload \
    --region us-west-2
```

Step 7: Configure Agent with Authorizer

During configure, specify authorizer:

```bash
PYTHONIOENCODING=utf-8 uv run agentcore configure \
    -e agentcore_entry.py \
    -n my_agent \
    --authorizer-config '{"type": "cognito", "userPoolId": "POOL_ID", "clientId": "CLIENT_ID"}'
```

Step 8: Invoke with Bearer Token

```bash
PYTHONIOENCODING=utf-8 uv run agentcore invoke \
    --prompt "Hello" \
    --bearer-token "eyJhbG..."
```
</process>

<cleanup>
Remove identity resources:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore identity cleanup --agent my_agent --force
```
</cleanup>

<success_criteria>
Identity setup complete when:
- [ ] Identity provider configured
- [ ] Agent accepts authenticated requests
- [ ] Token validation works correctly
</success_criteria>
