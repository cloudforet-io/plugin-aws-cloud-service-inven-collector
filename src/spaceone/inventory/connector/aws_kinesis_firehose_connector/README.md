# Kinesis Firehose

![KinesisFirehose](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-kinesis-firehose.svg)

**Plugin to collect Kinesis Delivery Stream**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Delivery Stream
  
- Boto3 info
  - Client : firehose
  - API used
    - [list_delivery_streams()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.list_delivery_streams)
    - [describe_delivery_stream()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.describe_delivery_stream)
    - [list_tags_for_delivery_stream()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/firehose.html#Firehose.Client.list_tags_for_delivery_stream)
  
      

### Required Policy
  
<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "firehose:Describe*",
                "firehose:List*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</code>
</pre>