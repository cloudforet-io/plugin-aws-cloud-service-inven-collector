# Amazon Lightsail

![Lightsail](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Lightsail.svg)

**Plugin to collect Amazon Lightsail**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Instance
  - Container
  - Disk
  - Snapshot
  - Load Balancer
  - Relational Database
  - Static IP
  - Distribution
  - Domain
  
- Boto3 info
  - Client : lightsail
  - API used
    - [Lightsail.Paginator.GetInstances](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lightsail.html#Lightsail.Paginator.GetInstances)
   

### Required Policy
  
<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "Lightsail:Get*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</code>
</pre>