<overview>
Quick reference for all AgentCore CLI commands.
All commands should be prefixed with `uv run agentcore`.
</overview>

<runtime_commands>
## Runtime Commands

### configure
```bash
uv run agentcore configure [OPTIONS]
```
Key options:
- `-e, --entrypoint` - Python entry point file
- `-n, --name` - Agent name (underscores only)
- `--deployment-type` - direct_code_deploy (default) or container
- `--runtime` - PYTHON_3_10 through PYTHON_3_13
- `--disable-memory` - Skip memory setup
- `--disable-otel` - Disable OpenTelemetry
- `--idle-timeout` - Session timeout (60-28800, default: 900)
- `--max-lifetime` - Instance lifetime (60-28800, default: 28800)
- `--protocol` - HTTP, MCP, or A2A
- `--vpc` - Enable VPC networking
- `--subnets` - Comma-separated subnet IDs
- `--security-groups` - Comma-separated security group IDs
- `-r, --region` - AWS region
- `-ni, --non-interactive` - Skip prompts

### deploy
```bash
uv run agentcore deploy [OPTIONS]
```
Options:
- `-a, --agent` - Agent name
- `-l, --local` - Build and run locally
- `-lb, --local-build` - Build locally, deploy to cloud
- `--auto-update-on-conflict` - Auto-update existing agent
- `--env` - Environment variables (KEY=VALUE)

### invoke
```bash
uv run agentcore invoke [PAYLOAD] [OPTIONS]
```
Options:
- `-a, --agent` - Agent name
- `-s, --session-id` - Session ID
- `--prompt` - Prompt text
- `-bt, --bearer-token` - OAuth bearer token
- `-l, --local` - Send to local agent
- `-u, --user-id` - User ID for auth
- `--headers` - Custom headers

### status
```bash
uv run agentcore status [OPTIONS]
```
Options:
- `-a, --agent` - Agent name
- `-v, --verbose` - Verbose JSON output

### destroy
```bash
uv run agentcore destroy [OPTIONS]
```
Options:
- `-a, --agent` - Agent name
- `--dry-run` - Preview destruction
- `--force` - Skip confirmation
- `--delete-ecr-repo` - Delete ECR repository

### stop-session
```bash
uv run agentcore stop-session [OPTIONS]
```
Options:
- `-s, --session-id` - Session ID
- `-a, --agent` - Agent name
</runtime_commands>

<gateway_commands>
## Gateway Commands

### create-mcp-gateway
```bash
uv run agentcore gateway create-mcp-gateway [OPTIONS]
```
Options:
- `--name` - Gateway name
- `--region` - AWS region
- `--role-arn` - IAM role ARN
- `--authorizer-config` - Auth config JSON
- `--enable-semantic-search` - Enable search tool

### create-mcp-gateway-target
```bash
uv run agentcore gateway create-mcp-gateway-target [OPTIONS]
```
Options:
- `--gateway-arn` - Gateway ARN (required)
- `--gateway-url` - Gateway URL (required)
- `--role-arn` - IAM role ARN (required)
- `--name` - Target name
- `--target-type` - lambda, openApiSchema, mcpServer, smithyModel
- `--target-payload` - Target specification
- `--credentials` - API key or OAuth2 credentials

### list-mcp-gateways
```bash
uv run agentcore gateway list-mcp-gateways [OPTIONS]
```

### get-mcp-gateway
```bash
uv run agentcore gateway get-mcp-gateway [OPTIONS]
```
Options: `--id`, `--name`, or `--arn`

### delete-mcp-gateway
```bash
uv run agentcore gateway delete-mcp-gateway [OPTIONS]
```
Options:
- `--id`, `--name`, or `--arn`
- `--force` - Delete all targets first

### update-gateway
```bash
uv run agentcore gateway update-gateway [OPTIONS]
```
Options:
- `--description` - New description
- `--policy-engine-arn` - Policy engine ARN
- `--policy-engine-mode` - LOG_ONLY or ENFORCE
</gateway_commands>

<memory_commands>
## Memory Commands

### create
```bash
uv run agentcore memory create NAME [OPTIONS]
```
Options:
- `--description` - Memory description
- `--event-expiry-days` - Retention days (default: 90)
- `--strategies` - JSON memory strategies
- `--role-arn` - IAM role ARN
- `--encryption-key-arn` - KMS key ARN
- `--wait/--no-wait` - Wait for ACTIVE status

### get
```bash
uv run agentcore memory get MEMORY_ID
```

### list
```bash
uv run agentcore memory list [OPTIONS]
```

### delete
```bash
uv run agentcore memory delete MEMORY_ID [OPTIONS]
```

### status
```bash
uv run agentcore memory status MEMORY_ID
```
</memory_commands>

<identity_commands>
## Identity Commands

### setup-aws-jwt
```bash
uv run agentcore identity setup-aws-jwt [OPTIONS]
```
Options:
- `--audience` - Audience URL (required)
- `--signing-algorithm` - ES384 (recommended) or RS256
- `--duration` - Token duration 60-3600 (default: 300)

### setup-cognito
```bash
uv run agentcore identity setup-cognito [OPTIONS]
```
Options:
- `--auth-flow` - user (USER_FEDERATION) or m2m (M2M)

### create-credential-provider
```bash
uv run agentcore identity create-credential-provider [OPTIONS]
```
Options:
- `--name` - Provider name
- `--type` - cognito, github, google, salesforce
- `--client-id` - OAuth client ID
- `--client-secret` - OAuth client secret
- `--discovery-url` - OIDC discovery URL (for cognito)

### create-workload-identity
```bash
uv run agentcore identity create-workload-identity [OPTIONS]
```

### get-cognito-inbound-token
```bash
uv run agentcore identity get-cognito-inbound-token [OPTIONS]
```
Options for user flow: `--username`, `--password`
Options for m2m: `--client-secret`

### cleanup
```bash
uv run agentcore identity cleanup [OPTIONS]
```
</identity_commands>

<policy_commands>
## Policy Commands

### create-policy-engine
```bash
uv run agentcore policy create-policy-engine --name NAME [OPTIONS]
```

### create-policy
```bash
uv run agentcore policy create-policy [OPTIONS]
```
Options:
- `--policy-engine-id` - Engine ID (required)
- `--name` - Policy name (required)
- `--definition` - Policy definition JSON (required)
- `--validation-mode` - FAIL_ON_ANY_FINDINGS or IGNORE_ALL_FINDINGS

### start-policy-generation
```bash
uv run agentcore policy start-policy-generation [OPTIONS]
```
Options:
- `--policy-engine-id` - Engine ID (required)
- `--name` - Generation name (required)
- `--resource-arn` - Gateway ARN (required)
- `--content` - Natural language policy description (required)

### list-policy-engines / list-policies
```bash
uv run agentcore policy list-policy-engines
uv run agentcore policy list-policies --policy-engine-id ID
```

### delete-policy-engine / delete-policy
```bash
uv run agentcore policy delete-policy-engine --policy-engine-id ID
uv run agentcore policy delete-policy --policy-engine-id ID --policy-id PID
```
</policy_commands>

<other_commands>
## Other Commands

### import-agent
Import from Bedrock Agents:
```bash
uv run agentcore import-agent [OPTIONS]
```
Options:
- `--agent-id` - Bedrock agent ID
- `--agent-alias-id` - Agent alias ID
- `--target-platform` - Platform (strands)
- `--output-dir` - Output directory
- `--deploy-runtime` - Deploy immediately
- `--disable-gateway/memory/code-interpreter/observability` - Skip components

### configure list / set-default
```bash
uv run agentcore configure list
uv run agentcore configure set-default AGENT_NAME
```
</other_commands>

<windows_note>
## Windows Note

Prefix commands with encoding flag to avoid Unicode errors:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore [command]
```
</windows_note>
