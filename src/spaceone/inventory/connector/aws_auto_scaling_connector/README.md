# Auto Scaling Group

![AutoScalingGroup](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-EC2-Auto-Scaling.svg)
**Plugin to collect Auto Scaling Group**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Auto Scaling Group
  - Launch Configuration
  - Launch Template
  
- Boto3 info
  - Client : autoscaling, ec2
  - API used
    - [AutoScaling.Paginator.DescribeAutoScalingGroups](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeAutoScalingGroups)
    - [AutoScaling.Paginator.DescribeLaunchConfigurations](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Paginator.DescribeLaunchConfigurations)
    - [EC2.Paginator.DescribeLaunchTemplates](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Paginator.DescribeLaunchTemplates)
    - [describe_launch_template_versions()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_launch_template_versions)
    - [describe_policies()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_policies)
    - [describe_lifecycle_hooks()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_lifecycle_hooks)
    - [describe_notification_configurations()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_notification_configurations)
    - [describe_scheduled_actions()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling.html#AutoScaling.Client.describe_notification_configurations)
  
  
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