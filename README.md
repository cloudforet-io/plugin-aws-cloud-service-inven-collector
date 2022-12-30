<h1 align="center">AWS Cloud Service Collector</h1>  

<br/>  
<div align="center" style="display:flex;">  
  <img width="245" src="https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-cloudservice.svg">
  <p> 
    <br>
    <img alt="Version"  src="https://img.shields.io/badge/version-1.15.3-blue.svg?cacheSeconds=2592000"  />    
    <a href="https://www.apache.org/licenses/LICENSE-2.0"  target="_blank"><img alt="License: Apache 2.0"  src="https://img.shields.io/badge/License-Apache 2.0-yellow.svg" /></a> 
  </p> 
</div>    

**Plugin to collect AWS Cloud Services**

> SpaceONE's [plugin-aws-cloud-service-inven-collector](https://github.com/spaceone-dev/plugin-aws-cloud-services) is a convenient tool to get cloud service data from AWS.


Find us also at [Dockerhub](https://hub.docker.com/repository/docker/spaceone/plugin-aws-cloud-service-inven-collector)
> Latest stable version : 1.15.3

Please contact us if you need any further information. (<support@spaceone.dev>)

---

## Collecting Contents

* Table of Contents
    * [API Gateway](/src/spaceone/inventory/connector/aws_api_gateway_connector/README.md)
        * API (REST API / Websocket)
    * [Auto Scaling Group](/src/spaceone/inventory/connector/aws_auto_scaling_connector/README.md)
        * Auto Scaling Group
        * Launch Configuration
        * Launch Template
    * [Cloud Front](/src/spaceone/inventory/connector/aws_cloud_front_connector/README.md)
        * Distribution
    * [Cloud Trail](/src/spaceone/inventory/connector/aws_cloud_trail_connector/README.md)
        * Trail
    * [Direct Connect](/src/spaceone/inventory/connector/aws_direct_connect_connector/README.md)
        * Connection
        * Direct Connect Gateway
        * Virtual Private Gateway
        * LAG
    * [DocumentDB](/src/spaceone/inventory/connector/aws_documentdb_connector/README.md)
        * Cluster
        * Subnet Group
        * Parameter Group
    * [DynamoDB](/src/spaceone/inventory/connector/aws_dynamodb_connector/README.md)
        * Table
    * [EBS](/src/spaceone/inventory/connector/aws_ebs_connector/README.md)
        * Volume
        * Snapshot
    * [EC2](/src/spaceone/inventory/connector/aws_ec2_connector/README.md)
        * Security Group
        * AMI
    * [ECR](/src/spaceone/inventory/connector/aws_ecr_connector/README.md)
        * Repository
    * [ECS](/src/spaceone/inventory/connector/aws_ecs_connector/README.md)
        * Cluster
    * [EFS](/src/spaceone/inventory/connector/aws_efs_connector/README.md)
        * Filesystem
    * [EIP](/src/spaceone/inventory/connector/aws_eip_connector/README.md)
        * EIP
    * [EKS](/src/spaceone/inventory/connector/aws_eks_connector/README.md)
        * Cluster
        * Node Group
    * [ElastiCache](/src/spaceone/inventory/connector/aws_elasticache_connector/README.md)
        * Memcached
        * Redis
    * [ELB](/src/spaceone/inventory/connector/aws_elb_connector/README.md)
        * Load Balancer
        * Target Group
    * [IAM](/src/spaceone/inventory/connector/aws_iam_connector/README.md)
        * Group
        * User
        * Role
        * Policy
        * Identity Provider
        * Access Key
    * [Kinesis Datastream](/src/spaceone/inventory/connector/aws_iam_connector/README.md)
        * Data stream
    * [Kinesis Firehose](/src/spaceone/inventory/connector/aws_iam_connector/README.md)
        * Delivery stream
    * [KMS](/src/spaceone/inventory/connector/aws_kms_connector/README.md)
        * Key
    * [Lambda](/src/spaceone/inventory/connector/aws_lambda_connector/README.md)
        * Function
        * Layer
    * [MSK](/src/spaceone/inventory/connector/aws_msk_connector/README.md)
        * Cluster
        * Cluster Configuration
    * [RDS](/src/spaceone/inventory/connector/aws_rds_connector/README.md)
        * Database
        * Instance
        * Snapshot
        * Subnet Group
        * Option Group
    * [Redshift](/src/spaceone/inventory/connector/aws_redshift_connector/README.md)
        * Cluster
    * [Route53](/src/spaceone/inventory/connector/aws_route53_connector/README.md)
        * Hosted Zone
    * [S3](/src/spaceone/inventory/connector/aws_s3_connector/README.md)
        * Bucket
    * [Secrets Manager](/src/spaceone/inventory/connector/aws_secrets_manager_connector/README.md)
        * Secret
    * [SNS](/src/spaceone/inventory/connector/aws_sns_connector/README.md)
        * Topic
    * [SQS](/src/spaceone/inventory/connector/aws_sqs_connector/README.md)
        * Queue
    * [VPC](/src/spaceone/inventory/connector/aws_vpc_connector/README.md)
        * VPC
        * Subnet
        * Route Table
        * Internet Gateway
        * Egress only internet Gateway
        * NAT Gateway
        * Peer Connection
        * Network ACL
        * Endpoint
        * Transit Gateway
        * Customer Gateway
        * VPN Connection
        * VPN Gateway
    * [Lightsail](/src/spaceone/inventory/connector/aws_lightsail_connector/README.md)
        * Instance
        * Disk
        * Snapshot
        * Bucket
        * Static IP
        * Database
        * Container
        * Load Balancer
        * Distribution
---

## AWS Service Endpoint (in use)

 There is an endpoints used to collect AWS resources information.
AWS endpoint is a URL consisting of a region and a service code. 
<pre>
https://[service-code].[region-code].amazonaws.com
</pre>

We use hundreds of endpoints because we collect information from a lots of regions and services.  

### Region list

Below is the AWS region information.
The regions we collect are not all regions supported by AWS. Exactly, we target the regions results returned by [describe_regions()](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_regions) of AWS ec2 client.

|No.|Region name|Region Code|
|---|------|---|
|1|US East (Ohio)|us-east-2|
|2|US East (N. Virginia)|us-east-1|
|3|US West (N. California)|us-west-1|
|4|US West (Oregon)|us-west-2|
|5|Asia Pacific (Mumbai)|ap-south-1|
|6|Asia Pacific (Osaka)|ap-northeast-3|
|7|Asia Pacific (Seoul)|ap-northeast-2|
|8|Asia Pacific (Singapore)|ap-southeast-1|
|9|Asia Pacific (Sydney)|ap-southeast-2|
|10|Asia Pacific (Tokyo)|ap-northeast-1|
|11|Canada (Central)|ca-central-1|
|12|Europe (Frankfurt)|eu-central-1|
|13|Europe (Ireland)|eu-west-1|
|14|Europe (London)|eu-west-2|
|15|Europe (Paris)|eu-west-3|
|16|Europe (Stockholm)|eu-north-1|
|17|South America (São Paulo)|sa-east-1|



### Service list

The following is a list of services being collected and service code information.

|No.|Service name|Service Code|
|---|------|---|
|1|AWS Certifcate Manager|AWSCertificateManager|
|2|API Gateway (REST API)|AmazonApiGateway|
|3|API Gateway V2 (Websocket)|AmazonApiGateway|
|4|Auto Scaling Group|AmazonEC2|
|5|CloudFront|AmazonCloudFront|
|6|CloudTrail|AWSCloudTrail|
|7|Direct Connect|AWSDirectConnect|
|8|DocumentDB|AmazonDocDB|
|9|DynamoDB|AmazonDynamoDB|
|10|Elastic Block Store (EBS)|AmazonEC2|
|11|EC2 (SecurityGroup, AMI, EIP)|AmazonEC2|
|12|Elastic Container Registry (ECR)|AmazonECR|
|13|Elastic Container Service (ECS)|AmazonECS|
|14|Elastic File System (EFS)|AmazonEFS|
|15|Elastic Kubernetes Service (EKS)|AmazonEKS|
|16|Elasticache|AmazonElastiCache|
|17|Elastic Load Balancer (ELB)|AWSELB|
|18|Identity Access Management (IAM)|-|
|19|Kinesis Data Stream|AmazonKinesis|
|20|Kinesis Firehose|AmazonKinesisFirehose|
|21|Key Management System (KMS)|awskms|
|22|Lambda|AWSLambda|
|21|Managed Streaming for Apache Kafka (MSK)|AmazonMSK|
|22|Relational Database Service (RDS)|AmazonRDS|
|23|Redshift|AmazonRedshift|
|24|Route53|AmazonRoute53|
|25|Simple Cloud Storage (S3)|AmazonS3|
|26|Secrets Manager|AWSSecretsManager|
|27|Simple Notification Service (SNS)|AmazonSNS|
|28|Simple Queue Service (SQS)|AWSQueueService|
|29|Virtual Private Cloud (VPC)|AmazonVPC|
|30|Lightsail|AmazonLightsail|


---

## Authentication Overview

Registered service account on SpaceONE must have certain permissions to collect cloud service data Please, set
authentication privilege for followings:

<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "acm:Describe*",
                "acm:List*",
                "apigateway:GET",
                "application-autoscaling:Describe*",
                "autoscaling:Describe*",
                "cloudfront:List*",
                "cloudtrail:Describe*",
                "cloudtrail:Get*",
                "cloudtrail:List*",
                "cloudwatch:Describe*",
                "cloudwatch:Get*",
                "cloudwatch:List*",
                "directconnect:Describe*",
                "dynamodb:Describe*",
                "dynamodb:List*",
                "ec2:Describe*",
                "ecr:Describe*",
                "ecr:List*",
                "ecs:Describe*",
                "ecs:List*",
                "eks:Describe*",
                "eks:List*",
                "elasticache:Describe*",
                "elasticache:List*",
                "elasticfilesystem:Describe*",
                "elasticloadbalancing:Describe*",
                "firehose:Describe*",
                "firehose:List*",
                "health:Describe*",
                "iam:Get*",
                "iam:List*",
                "kafka:Describe*",
                "kafka:List*",
                "kinesis:Describe*",
                "kinesis:List*",
                "kms:Describe*",
                "kms:Get*",
                "kms:List*",
                "lambda:List*",
                "lambda:Get*",
                "rds:Describe*",
                "rds:List*",
                "redshift:Describe*",
                "route53:List*",
                "s3:Get*",
                "s3:List*",
                "secretsmanager:List*",
                "sns:Get*",
                "sns:List*",
                "sqs:Get*",
                "sqs:List*",
                "Lightsail:Get*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }
    ]
}
</code>
</pre>


---
## Options

### Cloud Service Type : Specify what to collect

If cloud_service_types is added to the list elements in options, only the specified cloud service type is collected.
By default, if cloud_service_types is not specified in options, all services are collected.

The cloud_service_types items that can be specified are as follows.

<pre>
<code>
{
    "cloud_service_types": [
        'IAM',          
        'DynamoDB',     
        'Lambda',       
        'CloudFront',
        'RDS',
        'Route53',
        'S3',
        'AutoScalingGroup',
        'ElastiCache',
        'APIGateway',
        'DirectConnect',
        'EFS',
        'DocumentDB',
        'ECS',
        'Redshift',
        'EKS',
        'SQS',
        'KMS',
        'ECR',
        'CloudTrail',
        'SNS',
        'SecretsManager',
        'ELB',
        'EIP',
        'EBS',
        'VPC',
        'EC2',
        'ACM',
        'KinesisDataStream',
        'KinesisFirehose',
        'MSK',
        'Lightsail'
    ]
}
</code>
</pre>

How to update plugin information using spacectl is as follows.
First, create a yaml file to set options.

<pre>
<code>
> cat update_collector.yaml
---
collector_id: collector-xxxxxxx
options:
  cloud_service_types:
    - EC2
    - RDS
    - ELB
</code>
</pre>

Update plugin through spacectl command with the created yaml file.

### Service Code Mapper : Convert service code in Cloud Service Type what you want.

If `service_code_mappers` is added in options, You can replace the service code specified in the cloud service type.
The service code set by default can be checked in the Service List item of this document.

The `service_code_mappers` items that can be specified are as follows.

<pre>
<code>
{
    "service_code_mappers": {
        "AmazonEC2": "Amazon Elastic Computing",
        "AmazonRDS": "Amazon Relation Database",
    }
}
</code>
</pre>

### Custom Asset URL : Possible to modify icon path of cloud service

If `custom_asset_url` is added in options, You can replace the path of the icon each cloud service type instead of default path.

The `custom_asset_url` items that can be specified are as follows.

<pre>
<code>
{
    "custom_asset_url": "https://CUSTOM_ASSET_URL/..."
}
</code>
</pre>
---
## [Release note](RELEASE.md)
