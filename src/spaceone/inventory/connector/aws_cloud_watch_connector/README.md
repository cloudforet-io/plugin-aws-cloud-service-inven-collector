# Cloud Watch

![CloudWatch](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/AWS-Cloud-Watch.svg)

**Plugin to collect Direct Connect**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents

  
- Boto3 info
  - Client : cloudwatch
  - API used
  
  
### Required Policy
  
<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "directconnect:Describe*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</code>
</pre>