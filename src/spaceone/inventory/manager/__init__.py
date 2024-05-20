from spaceone.inventory.manager.cloudfront_manager import CloudFrontConnectorManager
from spaceone.inventory.manager.lambda_manager import LambdaConnectorManager
from spaceone.inventory.manager.rds_manager import RDSConnectorManager
from spaceone.inventory.manager.api_gateway_manager import APIGatewayConnectorManager

from spaceone.inventory.manager.auto_scaling_manager import AutoScalingConnectorManager
from spaceone.inventory.manager.direct_connect_manager import (
    DirectConnectConnectorManager,
)
from spaceone.inventory.manager.documentdb_manager import DocumentDBConnectorManager
from spaceone.inventory.manager.ecs_manager import ECSConnectorManager
from spaceone.inventory.manager.ecr_manager import ECRConnectorManager
from spaceone.inventory.manager.efs_manager import EFSConnectorManager
from spaceone.inventory.manager.eks_manager import EKSConnectorManager
from spaceone.inventory.manager.redshift_manager import RedshiftConnectorManager
from spaceone.inventory.manager.route53_manager import Route53ConnectorManager
from spaceone.inventory.manager.elasticache_manager import ElastiCacheConnectorManager
from spaceone.inventory.manager.sqs_manager import SQSConnectorManager
from spaceone.inventory.manager.kms_manager import KMSConnectorManager
from spaceone.inventory.manager.cloudtrail_manager import CloudTrailConnectorManager
from spaceone.inventory.manager.sns_manager import SNSConnectorManager
from spaceone.inventory.manager.secrets_manager import SecretsManagerConnectorManager
from spaceone.inventory.manager.elb_manager import ELBConnectorManager

from spaceone.inventory.manager.eip_manager import EIPConnectorManager
from spaceone.inventory.manager.ebs_manager import EBSConnectorManager
from spaceone.inventory.manager.s3_manager import S3ConnectorManager
from spaceone.inventory.manager.dynamodb_manager import DynamoDBConnectorManager
from spaceone.inventory.manager.vpc_manager import VPCConnectorManager

from spaceone.inventory.manager.ec2_manager import EC2ConnectorManager
from spaceone.inventory.manager.iam_manager import IAMConnectorManager
from spaceone.inventory.manager.acm_manager import ACMConnectorManager
from spaceone.inventory.manager.kinesis_data_stream_manager import (
    KinesisDataStreamConnectorManager,
)
from spaceone.inventory.manager.msk_manager import MSKConnectorManager
from spaceone.inventory.manager.kinesis_firehose_manager import (
    KinesisFirehoseConnectorManager,
)
from spaceone.inventory.manager.lightsail_manager import LightsailConnectorManager
