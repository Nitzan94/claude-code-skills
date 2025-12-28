<required_reading>
Read these reference files NOW:
1. references/architecture.md
2. references/cli-reference.md
</required_reading>

<process>
Step 1: Understand Gateway Purpose

Gateway is a central access point for AI agents to discover tools.
Use when your agent needs to:
- Call external APIs via MCP
- Access Lambda functions as tools
- Use OpenAPI-defined services

Step 2: Create MCP Gateway

```bash
PYTHONIOENCODING=utf-8 uv run agentcore gateway create-mcp-gateway \
    --name my_agent_gateway \
    --region us-west-2 \
    --enable-semantic-search
```

Note the Gateway ARN from output.

Step 3: Create Gateway Target

For Lambda function:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore gateway create-mcp-gateway-target \
    --gateway-arn "arn:aws:bedrock-agentcore:us-west-2:ACCOUNT:gateway/GATEWAY_ID" \
    --gateway-url "https://gateway-url" \
    --role-arn "arn:aws:iam::ACCOUNT:role/GatewayRole" \
    --name my_lambda_target \
    --target-type lambda \
    --target-payload '{"lambdaArn": "arn:aws:lambda:us-west-2:ACCOUNT:function:MyFunction"}'
```

For OpenAPI:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore gateway create-mcp-gateway-target \
    --gateway-arn "GATEWAY_ARN" \
    --gateway-url "https://gateway-url" \
    --role-arn "ROLE_ARN" \
    --target-type openApiSchema \
    --target-payload '{"schema": "..."}'
```

Step 4: Verify Gateway

```bash
PYTHONIOENCODING=utf-8 uv run agentcore gateway get-mcp-gateway --name my_agent_gateway
PYTHONIOENCODING=utf-8 uv run agentcore gateway list-mcp-gateway-targets --name my_agent_gateway
```

Step 5: Connect Agent to Gateway

In your agent entry point, use the gateway URL to access tools via MCP.
</process>

<cleanup>
To remove gateway:
```bash
PYTHONIOENCODING=utf-8 uv run agentcore gateway delete-mcp-gateway --name my_agent_gateway --force
```
</cleanup>

<success_criteria>
Gateway setup complete when:
- [ ] Gateway created successfully
- [ ] Target(s) added and active
- [ ] Agent can call tools through gateway
</success_criteria>
