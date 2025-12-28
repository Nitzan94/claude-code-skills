<required_reading>
Read these reference files NOW:
1. references/prerequisites.md
2. references/iam-policies.md
</required_reading>

<process>
Step 1: Understand the Challenge

Local OAuth flow uses filesystem for tokens. Cloud needs:
- Initial credentials in Secrets Manager
- Token persistence in S3 (for refresh)

Step 2: Create S3 Bucket for Tokens

```bash
aws s3 mb s3://your-agent-tokens-ACCOUNT_ID --region us-east-1
```

Step 3: Upload OAuth Credentials to Secrets Manager

Your credentials.json from Google Cloud Console:

```bash
aws secretsmanager create-secret \
    --name "your-agent/google-oauth-credentials" \
    --secret-string file://credentials.json \
    --region us-east-1
```

Step 4: Upload Initial Token to Secrets Manager

Run OAuth flow locally first to get token:

```bash
uv run python setup_google_oauth.py
```

Then upload storage/google_token.json:

```bash
aws secretsmanager create-secret \
    --name "your-agent/google-oauth-token" \
    --secret-string file://storage/google_token.json \
    --region us-east-1
```

Step 5: Modify Google Services Code

Add cloud detection and AWS integration:

```python
import os
import boto3
from botocore.exceptions import ClientError

AWS_REGION = "us-east-1"
GOOGLE_TOKEN_SECRET = "your-agent/google-oauth-token"
GOOGLE_TOKEN_BUCKET = "your-agent-tokens-ACCOUNT_ID"
GOOGLE_TOKEN_KEY = "google_token.json"

class GoogleTools:
    def __init__(self):
        self.is_cloud = os.getenv("AGENTCORE_RUNTIME") == "true"

    def _load_token_from_secrets(self):
        client = boto3.client("secretsmanager", region_name=AWS_REGION)
        response = client.get_secret_value(SecretId=GOOGLE_TOKEN_SECRET)
        return response["SecretString"]

    def _load_token_from_s3(self):
        s3 = boto3.client("s3", region_name=AWS_REGION)
        try:
            response = s3.get_object(Bucket=GOOGLE_TOKEN_BUCKET, Key=GOOGLE_TOKEN_KEY)
            return response["Body"].read().decode("utf-8")
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                return None
            raise

    def _save_token_to_s3(self, token_json):
        s3 = boto3.client("s3", region_name=AWS_REGION)
        s3.put_object(Bucket=GOOGLE_TOKEN_BUCKET, Key=GOOGLE_TOKEN_KEY, Body=token_json)
```

Step 6: Set Environment Variable in Entry Point

```python
os.environ["AGENTCORE_RUNTIME"] = "true"
```

Step 7: Update IAM Policy

Add S3 and Secrets Manager permissions. See templates/policy_oauth.json.

```bash
aws iam put-role-policy \
    --role-name YOUR-ROLE-NAME \
    --policy-name OAuthAccess \
    --policy-document file://policy_oauth.json
```

Step 8: Redeploy

```bash
PYTHONIOENCODING=utf-8 uv run agentcore deploy
```
</process>

<success_criteria>
OAuth integration complete when:
- [ ] Google API calls work in cloud
- [ ] Token refresh succeeds
- [ ] Refreshed tokens persist to S3
- [ ] No OAuth errors in agent responses
</success_criteria>
