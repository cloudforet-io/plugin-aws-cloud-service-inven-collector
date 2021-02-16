# Amazon MSK

![MSK](https://assets-console-spaceone-stg.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon_MSK.svg)

**Plugin to collect MSK**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Cluster
  - Cluster Configuration
  
- Boto3 info
  - Client : kafka
  - API used
    - [Kafka.Paginator.ListClusters](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Paginator.ListClusters)
    - [Kafka.Paginator.ListConfigurations](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Paginator.ListAliases)
    - [list_nodes()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_nodes)
    - [list_cluster_operations()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_cluster_operations)
    - [list_configuration_revisions()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.list_configuration_revisions)
    - [describe_configuration_revision()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kafka.html#Kafka.Client.describe_configuration_revision)
  

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