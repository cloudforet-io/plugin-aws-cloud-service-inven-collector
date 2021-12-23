# S3

![S3](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-S3.svg)

**Plugin to collect S3**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Bucket
  
- Boto3 info
  - Client : s3, cloudwatch
  - API used
    - [list_buckets()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_buckets)
    - [get_bucket_versioning()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_versioning)
    - [get_bucket_logging()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_logging)
    - [get_bucket_website()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_website)
    - [get_bucket_encryption()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_encryption)
    - [get_object_lock_configuration()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object_lock_configuration)
    - [get_bucket_accelerate_configuration()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_accelerate_configuration)
    - [get_bucket_request_payment()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_request_payment)
    - [get_bucket_notification_configuration()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_notification_configuration)
    - [get_bucket_tagging()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_tagging)
    - [get_bucket_policy_status()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_policy_status)
    - [get_bucket_acl()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_acl)
    - [get_bucket_location()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_bucket_location)
    - [get_metric_data()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.get_metric_data)

### Required Policy
  
<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "s3:ListBucket",
                "s3:ListBucketVersions",
                "s3:ListAllMyBuckets",
                "s3:GetBucketVersioning",
                "s3:GetBucketLogging",
                "s3:GetBucketWebsite",
                "s3:GetEncryptionConfiguration",
                "s3:GetBucketObjectLockConfiguration",
                "s3:GetAccelerateConfiguration",
                "s3:GetBucketRequestPayment"
                "s3:GetBucketNotification",
                "s3:GetBucketTagging",
                "s3:GetBucketPolicyStatus",
                "s3:GetBucketAcl",
                "s3:GetBucketLocation",
                "cloudwatch:GetMetricData"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</code>
</pre>