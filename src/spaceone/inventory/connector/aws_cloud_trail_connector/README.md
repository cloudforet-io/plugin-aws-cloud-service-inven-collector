# Cloud Trail

![CloudTrail](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-cloudtrail.svg)
**Plugin to collect Cloud Trail**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Trail
  
- Boto3 info
  - Client : cloudtrail
  - API used
    - [describe_trails()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.describe_trails)
    - [get_event_selectors()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_event_selectors)
    - [list_tags()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.list_tags)
    - [get_insight_selectors()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudtrail.html#CloudTrail.Client.get_insight_selectors)
  
  
### Required Policy
  
<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "cloudtrail:Describe*",
                "cloudtrail:Get*",
                "cloudtrail:List*",
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</code>
</pre>