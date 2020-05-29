# -*- coding: utf-8 -*-
import logging
from spaceone.core.service import *
import spaceone.inventory.manager.__init__ as managers
from boto3.session import Session

import concurrent.futures

_LOGGER = logging.getLogger(__name__)
MAX_WORKER = 10
SUPPORTED_RESOURCE_TYPE = ['inventory.CloudService', 'inventory.CloudServiceType']
DEFAULT_REGION = 'ap-northeast-2'


@authentication_handler
class CollectorService(BaseService):
    def __init__(self, metadata):
        super().__init__(metadata)

        self.execute_managers = [
            'DynamoDBConnectorManager',
            'LambdaConnectorManager',
            'CloudFrontConnectorManager',
            'RDSConnectorManager',
            'Route53ConnectorManager',
            'S3ConnectorManager',
            'AutoScalingConnectorManager',
            # 'ElastiCacheConnectorManager',
            'APIGatewayConnectorManager',
            'APIGatewayV2ConnectorManager',
            'DirectConnectConnectorManager',
            # 'WorkSpaceConnectorManager',
            'EFSConnectorManager',
            'DocumentDBConnectorManager',
            'ECSConnectorManager',
            'RedshiftConnectorManager',
            'EKSConnectorManager',
            'SQSConnectorManager',
            'KMSConnectorManager',
            'ECRConnectorManager',
            'CloudTrailConnectorManager',
            'SNSConnectorManager',
            'SecretsManagerConnectorManager',
            'ELBConnectorManager',
            'EIPConnectorManager',
            'EBSConnectorManager',
            'VPCConnectorManager'
        ]

    @transaction
    @check_required(['options', 'secret_data'])
    def verify(self, params):
        """
        Args:
              params:
                - options
                - secret_data
        """
        options = params['options']
        secret_data = params.get('secret_data', {})

        if secret_data != {}:
            self.get_account_id(secret_data)

        return {'options': {
            # 'filter_format':FILTER_FORMAT,
            'supported_resource_type': SUPPORTED_RESOURCE_TYPE
        }}

    @transaction
    @check_required(['options', 'secret_data', 'filter'])
    def list_resources(self, params):
        """
        Args:
            params:
                - options
                - secret_data
                - filter
        """
        params.update({
            'account_id': self.get_account_id(params['secret_data']),
            'regions': self.get_regions(params['secret_data'])
        })

        # for execute_manager in self.execute_managers:
        #     print(f'@@@ {execute_manager} @@@')
        #     _manager = self.locator.get_manager(execute_manager)
        #     yield _manager.collect_resources(**params)

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKER) as executor:
            print("[[[ EXECUTOR START ]]]")
            future_executors = []
            for execute_manager in self.execute_managers:
                print(f'@@@ {execute_manager} @@@')
                _manager = self.locator.get_manager(execute_manager)
                future_executors.append(executor.submit(_manager.collect_resources, **params))

            for future in concurrent.futures.as_completed(future_executors):
                yield future.result()

        # # DynamoDB
        # print('[ DynamoDB ]')
        # dynamodb_manager = self.locator.get_manager('DynamoDBConnectorManager')
        # yield dynamodb_manager.collect_resources(**params)
        #
        #
        # # Lambda
        # print('[ Lambda ]')
        # lambda_manager = self.locator.get_manager('LambdaConnectorManager')
        # yield lambda_manager.collect_resources(**params)
        #
        # # CloudFront
        # print('[ CloudFront ]')
        # cf_manager = self.locator.get_manager('CloudFrontConnectorManager')
        # yield cf_manager.collect_resources(**params)
        #
        # # RDS - 구현중
        # # print('[ RDS ]')
        # # rds_manager = self.locator.get_manager('RDSConnectorManager')
        # # yield rds_manager.collect_resources(**params)
        #
        # # Route53
        # print('[ Route53 ]')
        # r53_manager = self.locator.get_manager('Route53ConnectorManager')
        # yield r53_manager.collect_resources(**params)
        #
        # # S3
        # print('[ S3 ]')
        # s3_manager = self.locator.get_manager('S3ConnectorManager')
        # yield s3_manager.collect_resources(**params)
        #
        # # Auto Scaling
        # print('[ Auto Scaling ]')
        # auto_scaling_manager = self.locator.get_manager('AutoScalingConnectorManager')
        # yield auto_scaling_manager.collect_resources(**params)
        #
        # # ElastiCache - 구현중
        # # ecache_manager = self.locator.get_manager('ElastiCacheConnectorManager')
        # # yield ecache_manager.collect_resources(**params)
        #
        # # API Gateway (REST API)
        # print('[ API Gateway ]')
        # apigw_manager = self.locator.get_manager('APIGatewayConnectorManager')
        # yield apigw_manager.collect_resources(**params)
        #
        # # API Gateway V2 (HTTP, WebSocket)
        # print('[ API Gateway V2 ]')
        # apigwv2_manager = self.locator.get_manager('APIGatewayV2ConnectorManager')
        # yield apigwv2_manager.collect_resources(**params)
        #
        # # Direct Connect - 테스트 필요
        # direct_connect_manager = self.locator.get_manager('DirectConnectConnectorManager')
        # yield direct_connect_manager.collect_resources(**params)
        #
        # # Work Space (NOT YET)
        # # wspace_manager = self.locator.get_manager('WorkSpaceConnectorManager')
        # # yield wspace_manager.collect_resources(**params)
        #
        # # EFS
        # print('[ EFS ]')
        # efs_manager = self.locator.get_manager('EFSConnectorManager')
        # yield efs_manager.collect_resources(**params)
        #
        # # DocumentDB
        # print('[ DocumentDB ]')
        # docdb_manager = self.locator.get_manager('DocumentDBConnectorManager')
        # yield docdb_manager.collect_resources(**params)
        #
        # # ECS
        # print('[ ECS ]')
        # ecs_manager = self.locator.get_manager('ECSConnectorManager')
        # yield ecs_manager.collect_resources(**params)
        #
        # # Redshift
        # print('[ Redshift ]')
        # redshift_manager = self.locator.get_manager('RedshiftConnectorManager')
        # yield redshift_manager.collect_resources(**params)
        #
        # # EKS
        # print('[ EKS ]')
        # eks_manager = self.locator.get_manager('EKSConnectorManager')
        # yield eks_manager.collect_resources(**params)
        #
        # # SQS
        # print('[ SQS ]')
        # sqs_manager = self.locator.get_manager('SQSConnectorManager')
        # yield sqs_manager.collect_resources(**params)
        #
        # # KMS
        # print('[ KMS ]')
        # kms_manager = self.locator.get_manager('KMSConnectorManager')
        # yield kms_manager.collect_resources(**params)
        #
        # # ECR
        # print('[ ECR ]')
        # ecr_manager = self.locator.get_manager('ECRConnectorManager')
        # yield ecr_manager.collect_resources(**params)
        #
        # # CloudTrail
        # print('[ CloudTrail ]')
        # cloud_trail_manager = self.locator.get_manager('CloudTrailConnectorManager')
        # yield cloud_trail_manager.collect_resources(**params)
        #
        # # SNS
        # print('[ SNS ]')
        # sns_manager = self.locator.get_manager('SNSConnectorManager')
        # yield sns_manager.collect_resources(**params)
        #
        # # Secret Manager
        # print('[ Secret Manager ]')
        # secrets_manager = self.locator.get_manager('SecretsManagerConnectorManager')
        # yield secrets_manager.collect_resources(**params)
        #
        # # ELB (리스너, 타겟 미구현 상태)
        # print('[ ELB ]')
        # elb_manager = self.locator.get_manager('ELBConnectorManager')
        # yield elb_manager.collect_resources(**params)
        #
        # # EIP
        # print('[ EIP ]')
        # eip_manager = self.locator.get_manager('EIPConnectorManager')
        # yield eip_manager.collect_resources(**params)
        #
        # # EBS
        # print('[ EBS ]')
        # ebs_manager = self.locator.get_manager('EBSConnectorManager')
        # yield ebs_manager.collect_resources(**params)
        #
        # # VPC
        # print('[ VPC ]')
        # vpc_manager = self.locator.get_manager('VPCConnectorManager')
        # yield vpc_manager.collect_resources(**params)

    @staticmethod
    def get_account_id(secret_data, region=DEFAULT_REGION):
        if 'region_name' not in secret_data:
            secret_data['region_name'] = region

        _session = Session(**secret_data)
        sts_client = _session.client('sts')
        return sts_client.get_caller_identity()['Account']

    @staticmethod
    def get_regions(secret_data, region=DEFAULT_REGION):
        if 'region_name' not in secret_data:
            secret_data['region_name'] = region

        _session = Session(**secret_data)
        ec2_client = _session.client('ec2')
        return list(map(lambda region_info: region_info.get('RegionName'),
                        ec2_client.describe_regions().get('Regions')))
