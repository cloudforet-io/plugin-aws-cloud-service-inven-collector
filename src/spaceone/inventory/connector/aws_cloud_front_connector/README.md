# Cloud Front

![CloudFront](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-CloudFront.svg)
**Plugin to collect Cloud Front**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Distribution
  
- Boto3 info
  - Client : cloudfront
  - API used
    - [CloudFront.Paginator.ListDistributions](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeAutoScalingGroups)
    - [list_tags_for_resource()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront.html#CloudFront.Client.list_tags_for_resource)

  
### Required Policy
  
<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "cloudfront:List*",
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</code>
</pre>