# plugin-aws-cloud-services

![AWS Cloud Services](https://spaceone-custom-assets.s3.ap-northeast-2.amazonaws.com/console-assets/icons/aws-cloudservice.svg)
**Plugin to collect Google Cloud Services**

> SpaceONE's [plugin-aws-cloud-services](https://github.com/spaceone-dev/plugin-aws-cloud-services) is a convenient tool to 
get cloud service data from AWS.


Find us also at [Dockerhub](https://hub.docker.com/repository/docker/spaceone/aws-cloud-services)
> Latest stable version : 1.7

Please contact us if you need any further information. (<support@spaceone.dev>)

---

### Collecting Contents

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
    * [ELB](/src/spaceone/inventory/connector/aws_elb_connector/README.md)
        * Load Balancer
        * Target Group
    * [IAM](/src/spaceone/inventory/connector/aws_iam_connector/README.md)
        * Group
        * User
        * Role
        * Policy
        * Identity Provider
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
    
---
## Authentication Overview

Registered service account on SpaceONE must have certain permissions to collect cloud service data 
Please, set authentication privilege for followings:

<pre>
<code>
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "acm:Describe*",
                "acm:Get*",
                "acm:List*",
                "acm-pca:Describe*",
                "acm-pca:Get*",
                "acm-pca:List*",
                "apigateway:GET",
                "autoscaling:Describe*",
                "autoscaling-plans:Describe*",
                "autoscaling-plans:GetScalingPlanResourceForecastData",
                "athena:List*",
                "athena:Batch*",
                "athena:Get*",
                "cassandra:Select",
                "cloudfront:Get*",
                "cloudfront:List*",
                "cloudwatch:Describe*",
                "cloudwatch:Get*",
                "cloudwatch:List*",
                "connect:List*",
                "connect:Describe*",
                "connect:GetFederationToken",
                "directconnect:Describe*",
                "dynamodb:BatchGet*",
                "dynamodb:Describe*",
                "dynamodb:Get*",
                "dynamodb:List*",
                "dynamodb:Query",
                "dynamodb:Scan",
                "ec2:Describe*",
                "ec2:Get*",
                "ec2:SearchTransitGatewayRoutes",
                "ec2messages:Get*",
                "ecr:BatchCheck*",
                "ecr:BatchGet*",
                "ecr:Describe*",
                "ecr:Get*",
                "ecr:List*",
                "ecs:Describe*",
                "ecs:List*",
                "eks:Describe*",
                "eks:List*",
                "elasticache:Describe*",
                "elasticache:List*",
                "elasticfilesystem:Describe*",
                "elasticloadbalancing:Describe*",
                "es:Describe*",
                "es:List*",
                "es:Get*",
                "es:ESHttpGet",
                "es:ESHttpHead",
                "fsx:Describe*",
                "fsx:List*",
                "health:Describe*",
                "iam:Generate*",
                "iam:Get*",
                "iam:List*",
                "iam:Simulate*",
                "kafka:Describe*",
                "kafka:List*",
                "kafka:Get*",
                "lambda:List*",
                "lambda:Get*",
                "rds:Describe*",
                "rds:List*",
                "rds:Download*",
                "redshift:Describe*",
                "redshift:GetReservedNodeExchangeOfferings",
                "redshift:View*",
                "route53:Get*",
                "route53:List*",
                "route53:Test*",
                "route53domains:Check*",
                "route53domains:Get*",
                "route53domains:List*",
                "route53domains:View*",
                "route53resolver:Get*",
                "route53resolver:List*",
                "s3:Get*",
                "s3:List*",
                "secretsmanager:List*",
                "secretsmanager:Describe*",
                "secretsmanager:GetResourcePolicy",
                "sns:Get*",
                "sns:List*",
                "sns:Check*",
                "sqs:Get*",
                "sqs:List*",
                "sqs:Receive*",
                "storagegateway:Describe*",
                "storagegateway:List*",
                "tag:Get*",
                "trustedadvisor:Describe*",
                "workspaces:Describe*"
            ],
            "Effect": "Allow",
            "Resource": "arn:aws:*:{aws region code}:*:*"
        }
    ]
}
</code>
</pre>
