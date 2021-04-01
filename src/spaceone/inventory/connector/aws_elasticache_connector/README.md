# ElastiCache

![ElastiCache](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-ElastiCache.svg)
**Plugin to collect ElastiCache**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Memcached
  - Redis (include Cluster)
  
- Boto3 info
  - Client : elasticache
  - API used
    - [ElastiCache.Paginator.DescribeCacheClusters¶](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeCacheClusters)
    - [ElastiCache.Paginator.DescribeReplicationGroups](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Paginator.DescribeReplicationGroups)
    - [list_tags_for_resource()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elasticache.html#ElastiCache.Client.list_tags_for_resource)


### Required Policy
  
<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "elasticache:Describe*",
                "elasticache:List*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</code>
</pre>