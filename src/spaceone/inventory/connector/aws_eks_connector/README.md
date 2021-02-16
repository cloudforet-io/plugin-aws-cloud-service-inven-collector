# EKS

![EKS](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/cloud-services/aws/Amazon-Elastic-Kubernetes-Service.svg)
**Plugin to collect Security EKS**

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

- Contents
  - Cluster
  
- Boto3 info
  - Client : eks
  - API used
    - [EKS.Paginator.ListClusters](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Paginator.ListClusters)
    - [EKS.Paginator.ListNodegroups](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Paginator.ListNodegroups)
    - [EKS.Paginator.ListUpdates](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Paginator.ListUpdates)
    - [describe_cluster()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Client.describe_cluster)
    - [describe_nodegroup()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Client.describe_nodegroup)
    - [describe_update()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/eks.html#EKS.Client.describe_update)

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