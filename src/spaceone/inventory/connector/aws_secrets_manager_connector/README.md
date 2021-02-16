# Secrets Manager

![S3](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Secrets-Manager.svg)

**Plugin to collect Secrets Manager**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Secret
  
- Boto3 info
  - Client : secretsmanager
  - API used
    - [SecretsManager.Paginator.ListSecrets](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager.html#SecretsManager.Paginator.ListSecrets)

### Required Policy
  
<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
              
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:*:{REGION_NAME}:*:*"
        }
    ]
}
</code>
</pre>