# Kinesis Data Stream

![KinesisDataStream](https://assets-console-spaceone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon_Kinesis_Firehose.svg)

**Plugin to collect Kinesis Data Stream**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Data Stream
  
- Boto3 info
  - Client : kinesis
  - API used
    - [Kinesis.Paginator.ListStreams](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Paginator.ListStreams)
    - [describe_stream()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.describe_stream)
    - [list_stream_consumers()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.list_stream_consumers)
    - [list_tags_for_stream()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesis.html#Kinesis.Client.list_tags_for_stream)
  
      

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