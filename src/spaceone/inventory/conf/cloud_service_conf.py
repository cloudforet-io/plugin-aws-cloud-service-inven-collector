MAX_WORKER = 20
SUPPORTED_FEATURES = ['garbage_collection']
SUPPORTED_SCHEDULES = ['hours']
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType', 'inventory.Region']
DEFAULT_REGION = 'ap-northeast-2'
FILTER_FORMAT = []

CLOUD_SERVICE_GROUP_MAP = {
    'IAM': 'IAMConnectorManager',
    'DynamoDB': 'DynamoDBConnectorManager',
    'Lambda': 'LambdaConnectorManager',
    'CloudFront': 'CloudFrontConnectorManager',
    'RDS': 'RDSConnectorManager',
    'Route53': 'Route53ConnectorManager',
    'S3': 'S3ConnectorManager',
    'AutoScalingGroup': 'AutoScalingConnectorManager',
    'ElastiCache': 'ElastiCacheConnectorManager',
    'APIGateway': 'APIGatewayConnectorManager',
    'DirectConnect': 'DirectConnectConnectorManager',
    'EFS': 'EFSConnectorManager',
    'DocumentDB': 'DocumentDBConnectorManager',
    'ECS': 'ECSConnectorManager',
    'Redshift': 'RedshiftConnectorManager',
    'EKS': 'EKSConnectorManager',
    'SQS': 'SQSConnectorManager',
    'KMS': 'KMSConnectorManager',
    'ECR': 'ECRConnectorManager',
    'CloudTrail': 'CloudTrailConnectorManager',
    'SNS': 'SNSConnectorManager',
    'SecretsManager': 'SecretsManagerConnectorManager',
    'ELB': 'ELBConnectorManager',
    'EIP': 'EIPConnectorManager',
    'EBS': 'EBSConnectorManager',
    'VPC': 'VPCConnectorManager',
    'EC2': 'EC2ConnectorManager',
    'ACM': 'ACMConnectorManager',
    'KinesisDataStream': 'KinesisDataStreamConnectorManager',
    'MSK': 'MSKConnectorManager',
    'KinesisFirehose': 'KinesisFirehoseConnectorManager',
    'Lightsail': 'LightsailConnectorManager'
}