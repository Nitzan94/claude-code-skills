<overview>
IAM policies for AgentCore deployments with external services.
</overview>

<finding_role>
Find your execution role in .bedrock_agentcore.yaml:

```yaml
executionRole: arn:aws:iam::ACCOUNT:role/AmazonBedrockAgentCoreSDKRuntime-REGION-ID
```

The role name is everything after `role/`.
</finding_role>

<applying_policy>
Apply inline policy to role:

```bash
aws iam put-role-policy \
    --role-name YOUR-ROLE-NAME \
    --policy-name CustomAccess \
    --policy-document file://POLICY_FILE.json
```

Available templates:
- templates/policy_minimal.json - Secrets Manager only
- templates/policy_oauth.json - Secrets + S3 for OAuth tokens
- templates/policy_full.json - All common permissions (Secrets, S3, Bedrock, CloudWatch)
</applying_policy>

<secrets_only_policy>
For Secrets Manager access only (use templates/policy_minimal.json):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["secretsmanager:GetSecretValue"],
            "Resource": [
                "arn:aws:secretsmanager:REGION:ACCOUNT:secret:your-agent/*"
            ]
        }
    ]
}
```
</secrets_only_policy>

<oauth_policy>
For Google OAuth with S3 token persistence (use templates/policy_oauth.json):

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["secretsmanager:GetSecretValue"],
            "Resource": [
                "arn:aws:secretsmanager:REGION:ACCOUNT:secret:your-agent/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:PutObject"],
            "Resource": "arn:aws:s3:::your-agent-tokens-ACCOUNT/*"
        }
    ]
}
```
</oauth_policy>

<full_policy>
For comprehensive access (use templates/policy_full.json):

Includes:
- Secrets Manager access
- S3 bucket access
- Bedrock model invocation
- CloudWatch logs

Customize the template for your specific needs.
</full_policy>

<verification>
Verify policy attached:

```bash
aws iam list-role-policies --role-name YOUR-ROLE-NAME
```

Test access:
```bash
aws secretsmanager get-secret-value --secret-id your-secret-arn
```
</verification>
