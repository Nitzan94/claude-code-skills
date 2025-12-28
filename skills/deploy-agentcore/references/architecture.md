<overview>
Amazon Bedrock AgentCore is a serverless platform for deploying AI agents at scale.
AgentCore services are modular and composable - use together or independently.
Works with any model (Bedrock or external) and any agent framework.
</overview>

<components>
## Runtime

Serverless hosting for agents. Features:
- Complete session isolation with low latency
- Long-running workloads up to 8 hours
- Agent-to-Agent (A2A) protocol support
- Auto-scaling based on demand

### Deployment Modes

**1. direct_code_deploy**
- Packages Python code into a ZIP
- AWS builds and runs it directly
- Faster iteration (no Docker build)
- Limited: only standard Python packages
- Best for: prototyping, simple agents

**2. container (via CodeBuild)** - RECOMMENDED
- You provide a Dockerfile
- CodeBuild builds ARM64 Docker image
- Image pushed to ECR
- Container deployed to AgentCore
- Full control over environment
- Best for: production, complex dependencies

How container deployment works:
```
Your Code + Dockerfile
        ↓
   Upload to S3
        ↓
   CodeBuild (ARM64)
        ↓
   Docker Image → ECR
        ↓
   AgentCore Runtime
```

Key configuration:
- `--idle-timeout` - Session idle timeout (60-28800 seconds, default: 900)
- `--max-lifetime` - Maximum instance lifetime (60-28800 seconds, default: 28800)
- `--runtime` - Python version (PYTHON_3_10 through PYTHON_3_13)
- `--protocol` - Agent protocol (HTTP, MCP, A2A)

## Gateway

Central access point for AI agents to discover and interact with tools.
Handles authentication, request routing, and protocol translation.

Target types:
- `lambda` - AWS Lambda functions
- `openApiSchema` - OpenAPI specifications
- `mcpServer` - MCP servers
- `smithyModel` - Smithy models

Features:
- Semantic search tool (--enable-semantic-search)
- MCP protocol translation
- Multiple targets per gateway

Commands:
```bash
uv run agentcore gateway create-mcp-gateway --name MyGateway
uv run agentcore gateway create-mcp-gateway-target --gateway-arn ARN --target-type lambda
uv run agentcore gateway list-mcp-gateways
```

## Memory

Track short-term and long-term memory operations.

Modes:
- `NONE` - No memory, stateless
- `STM` - Short-term memory (within session)
- `LTM` - Long-term memory (across sessions)
- `STM_AND_LTM` - Both (recommended for conversational agents)

Configuration:
- `--disable-memory` - Skip memory during configure
- `--event-expiry-days` - Event retention (default: 90)

Commands:
```bash
uv run agentcore memory create my_memory --event-expiry-days 30
uv run agentcore memory list
uv run agentcore memory status MEMORY_ID
```

## Identity

Secure authentication for agents to access resources and services.

Methods:
- AWS IAM - Default, uses IAM roles
- Cognito - User federation or M2M auth
- AWS JWT - Outbound web identity federation (secretless M2M)
- External providers - GitHub, Google, Salesforce

Commands:
```bash
uv run agentcore identity setup-cognito --auth-flow user
uv run agentcore identity setup-aws-jwt --audience URL --signing-algorithm ES384
uv run agentcore identity create-credential-provider --type google --client-id ID
```

Authorizer config during deploy:
```bash
uv run agentcore configure --authorizer-config '{"type": "cognito", ...}'
```

## Observability

Real-time visibility into agent execution and metrics.

Features:
- Step-by-step execution visualization
- Metadata tagging and custom scoring
- Trajectory inspection
- CloudWatch dashboards
- OpenTelemetry compatible

### Setup for Container Deployment

1. Add to requirements.txt:
```
aws-opentelemetry-distro>=0.10.0
```

2. Add to Dockerfile:
```dockerfile
ENV OTEL_PYTHON_DISTRO=aws_distro
ENV OTEL_PYTHON_CONFIGURATOR=aws_configurator
ENV AGENT_OBSERVABILITY_ENABLED=true

CMD ["opentelemetry-instrument", "python", "your_app.py"]
```

3. After deploy, check dashboard (wait 5-10 min):
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#gen-ai-observability/agent-core

Metrics categories:
- Usage: TargetType, IngressAuthType, EgressAuthType, RequestsPerSession
- Invocation: Invocations, ConcurrentExecutions, Sessions
- Performance: Latency, Duration, TargetExecutionTime
- Errors: Throttles, SystemErrors, UserErrors

Configuration:
- `--disable-otel` - Disable OpenTelemetry during configure

## Policy

Cedar-based policies for governance and authorization.

Features:
- Policy engines for centralized management
- Natural language policy generation
- Validation modes (FAIL_ON_ANY_FINDINGS, IGNORE_ALL_FINDINGS)

Commands:
```bash
uv run agentcore policy create-policy-engine --name MyEngine
uv run agentcore policy create-policy --policy-engine-id ID --name MyPolicy --definition '{...}'
uv run agentcore policy start-policy-generation --content "Allow read access to..."
```

## Code Interpreter & Browser

Managed environments for agent capabilities:
- **Code Interpreter** - Isolated environment for agent-generated code
- **Browser** - Managed web browser instances for automation

## VPC & Security

Enterprise features (GA):
- VPC support
- AWS PrivateLink
- CloudFormation support
- Resource tagging
</components>

<regions>
Available regions:
- us-west-2 (Oregon) - Recommended
- us-east-1 (N. Virginia)

Check AWS documentation for latest availability.
</regions>
