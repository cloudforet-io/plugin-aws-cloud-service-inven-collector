import time
import logging
from typing import List
from spaceone.core import utils
from datetime import datetime, timedelta
from spaceone.inventory.connector.aws_s3_connector.schema.data import Bucket, Versioning, ServerAccessLogging, \
    WebsiteHosting, ObjectLock, Encryption, TransferAcceleration, NotificationConfiguration, RequestPayment
from spaceone.inventory.connector.aws_s3_connector.schema.resource import BucketResource, BucketResponse
from spaceone.inventory.connector.aws_s3_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel
from spaceone.inventory.libs.schema.resource import CloudWatchModel

_LOGGER = logging.getLogger(__name__)


class S3Connector(SchematicAWSConnector):
    response_schema = BucketResponse
    service_name = 's3'
    cloud_service_group = 'S3'
    cloud_service_type = 'Bucket'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[BucketResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: S3")
        resources = []
        start_time = time.time()

        try:
            resources.extend(self.set_cloud_service_types())

            # merge data
            for data in self.request_data():
                if getattr(data, 'resource_type', None) and data.resource_type == 'inventory.ErrorResource':
                    # Error Resource
                    resources.append(data)
                else:
                    # This is Global API, yet set up its region for bucket
                    if getattr(data, 'set_cloudwatch', None):
                        data.cloudwatch = CloudWatchModel(data.set_cloudwatch())
    
                    bucket_resource = {
                        'name': data.name,
                        'data': data,
                        'account': self.account_id,
                        'tags': self.get_tags(data.name),
                        'instance_size': float(data.size),
                        'reference': ReferenceModel(data.reference())
                    }
    
                    if data.get('region_name'):
                        bucket_resource.update({
                            'region_code': data.get('region_name'),
                        })
    
                    resources.append(self.response_schema({'resource': BucketResource(bucket_resource)}))
        except Exception as e:
            resource_id = ''
            resources.append(self.generate_error('global', resource_id, e))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: S3 ({time.time() - start_time} sec)')
        return resources

    def request_data(self) -> List[Bucket]:
        cloudwatch_namespace = 'AWS/S3'
        cloudwatch_dimension_name = 'BucketName'
        cloudtrail_resource_type = 'AWS::S3::Bucket'
        response = self.client.list_buckets()

        for raw in response.get('Buckets', []):
            bucket_name = raw.get('Name')

            try:
                region_name = self.get_bucket_location(bucket_name)

                raw.update({
                    'arn': self.generate_arn(service=self.service_name,
                                             region="",
                                             account_id="",
                                             resource_type=bucket_name,
                                             resource_id="*"),
                    'region_name': region_name,
                    'cloudwatch': self.set_cloudwatch(cloudwatch_namespace, cloudwatch_dimension_name,
                                                      raw['Name'], region_name),
                    'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, raw['Name']),
                })

                if versioning := self.get_bucket_versioning(bucket_name):
                    raw.update({'versioning': versioning})

                if server_access_logging := self.get_server_access_logging(bucket_name):
                    raw.update({'server_access_logging': server_access_logging})

                if website_hosting := self.get_website_hosting(bucket_name):
                    raw.update({'website_hosting': website_hosting})

                if encryption := self.get_encryption(bucket_name):
                    raw.update({'encryption': encryption})

                if object_lock := self.get_object_lock(bucket_name):
                    raw.update({'object_lock': object_lock})

                if public_access := self.get_bucket_public_access(bucket_name):
                    raw.update({'public_access': public_access})

                if transfer_acceleration := self.get_transfer_acceleration(bucket_name):
                    raw.update({'transfer_acceleration': transfer_acceleration})

                if request_payment := self.get_request_payment(bucket_name):
                    raw.update({'request_payment': request_payment})

                if notification_configurations := self.get_notification_configurations(bucket_name):
                    raw.update({'notification_configurations': notification_configurations})

                if region_name:
                    count, size = self.get_count_and_size(bucket_name, region_name)
                    
                    raw.update({
                        'object_count': count,
                        'object_total_size': size,
                        'size': size
                    })

                yield Bucket(raw, strict=False)
                
            except Exception as e:
                resource_id = raw.get('Name', '')
                error_resource_response = self.generate_error('global', resource_id, e)
                yield error_resource_response

    def get_bucket_versioning(self, bucket_name):
        try:
            response = self.client.get_bucket_versioning(Bucket=bucket_name)

            if status := response.get('Status'):
                version = {
                    'status': status,
                    'mfa_delete': response.get('MFADelete')
                }
                return Versioning(version, strict=False)
            else:
                return None
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Bucket Versioning] {e}')
            return None

    def get_server_access_logging(self, bucket_name):
        try:
            response = self.client.get_bucket_logging(Bucket=bucket_name)

            if access_logging := response.get('LoggingEnabled'):
                return ServerAccessLogging(access_logging, strict=False)
            else:
                return None
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Server Access Logging] {e}')
            return None

    def get_website_hosting(self, bucket_name):
        try:
            response = self.client.get_bucket_website(Bucket=bucket_name)
            del response['ResponseMetadata']
            return WebsiteHosting(response, strict=False)
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Website Hosting] {e}')
            return None

    def get_encryption(self, bucket_name):
        try:
            response = self.client.get_bucket_encryption(Bucket=bucket_name)

            if encryption := response.get('ServerSideEncryptionConfiguration'):
                return Encryption(encryption, strict=False)
            else:
                return None
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Encryption] {e}')
            return None

    def get_object_lock(self, bucket_name):
        try:
            response = self.client.get_object_lock_configuration(Bucket=bucket_name)

            if object_lock := response.get('ObjectLockConfiguration'):
                return ObjectLock(object_lock, strict=False)
            else:
                return None
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Object Lock] {e}')
            return None

    def get_transfer_acceleration(self, bucket_name):
        return_value = None
        try:
            response = self.client.get_bucket_accelerate_configuration(Bucket=bucket_name)
            if transfer_acceleration := response.get('Status'):
                return_value = TransferAcceleration({'transfer_acceleration': transfer_acceleration}, strict=False)
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Transfer Acceleration] {e}')

        return return_value

    def get_request_payment(self, bucket_name):
        try:
            response = self.client.get_bucket_request_payment(Bucket=bucket_name)
            
            if payer := response.get('Payer'):
                return RequestPayment({'request_payment': payer}, strict=False)
            else:
                return None
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Request Payment] {e}')
            return None

    def get_notification_configurations(self, bucket_name):
        try:
            response = self.client.get_bucket_notification_configuration(Bucket=bucket_name)

            sns = self.set_notification('SNS Topic', 'TopicArn', response.get('TopicConfigurations', []))
            que = self.set_notification('Queue', 'QueueArn', response.get('QueueConfigurations', []))
            func = self.set_notification('Lambda Function', 'LambdaFunctionArn',
                                         response.get('LambdaFunctionConfigurations', []))

            total_noti = sns + que + func

            if len(total_noti) > 0:
                return total_noti
            else:
                return None
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Notification Configuration] {e}')
            return None

    def get_tags(self, bucket_name):
        try:
            response = self.client.get_bucket_tagging(Bucket=bucket_name)
            return self.convert_tags_to_dict_type(response.get('TagSet', []))
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Tags] {e}')
            return {}

    def get_bucket_public_access(self, bucket_name):
        public_access = False
        try:
            response = self.client.get_bucket_policy_status(Bucket=bucket_name)
            policy_status = response.get('PolicyStatus', {})
            public_access = policy_status.get('IsPublic', False)
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Bucket Policy Status] {e}')
            public_access = self.get_bucket_acl_info(bucket_name)

        return "Public" if public_access else "Private"

    def get_bucket_acl_info(self, bucket_name):
        response = False
        try:
            acl = self.client.get_bucket_acl(Bucket=bucket_name)
            for grants in acl.get('Grants', []):
                uri = grants.get('Grantee').get('URI')
                if uri is not None and uri.endswith('AllUsers'):
                    response = True
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Bucket ACL] {e}')
            pass
        return response

    def get_bucket_location(self, bucket_name):
        try:
            response = self.client.get_bucket_location(Bucket=bucket_name)

            location = response.get('LocationConstraint')
            
            if location is None:
                location = 'us-east-1'  # Client response is None when bucket is located in 'us-east-1'
            
            return location

        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Bucket Location] {e}')
            return ''

    def get_count_and_size(self, bucket_name, region_name):
        try:
            cloudwatch_client = self.session.client('cloudwatch', region_name=region_name)

            count = self.get_object_count(cloudwatch_client, bucket_name)
            size = self.get_object_total_size(cloudwatch_client, bucket_name)

            return count, size
        except Exception as e:
            _LOGGER.error(f'[S3 {bucket_name}: Get Count, Size] {e}')
            return 0, 0

    def get_object_count(self, cw_client, bucket_name):
        count_dimensions = [{"Name": "BucketName", "Value": bucket_name},
                            {"Name": "StorageType", "Value": "AllStorageTypes"}]

        count_param = self._get_metric_param('NumberOfObjects', count_dimensions)
        return int(self.get_metric_data(cw_client, count_param))

    def get_object_total_size(self, cw_client, bucket_name):
        total_size = 0.0

        storage_types = [
            'StandardStorage',
            'IntelligentTieringFAStorage',
            'IntelligentTieringIAStorage',
            'IntelligentTieringAAStorage',
            'IntelligentTieringAIAStorage',
            'IntelligentTieringDAAStorage',
            'StandardIAStorage',
            'StandardIASizeOverhead',
            'StandardIAObjectOverhead',
            'OneZoneIAStorage',
            'OneZoneIASizeOverhead',
            'ReducedRedundancyStorage',
            'GlacierInstantRetrievalStorage',
            'GlacierStorage',
            'GlacierStagingStorage',
            'GlacierObjectOverhead',
            'GlacierS3ObjectOverhead',
            'DeepArchiveStorage',
            'DeepArchiveObjectOverhead',
            'DeepArchiveS3ObjectOverhead',
            'DeepArchiveStagingStorage'
        ]

        for storage_type in storage_types:
            size_dimensions = [{"Name": "BucketName", "Value": bucket_name},
                               {"Name": "StorageType", "Value": storage_type}]

            size_param = self._get_metric_param('BucketSizeBytes', size_dimensions)
            total_size += float(self.get_metric_data(cw_client, size_param))
            time.sleep(0.3)

        return total_size

    @staticmethod
    def get_metric_data(client, params):
        metric_id = f'metric_{utils.random_string()[:12]}'
        extra_opts = {}

        if params.get('limit'):
            extra_opts['MaxDatapoints'] = params.get('limit')

        response = client.get_metric_data(
            MetricDataQueries=[{
                'Id': metric_id,
                'MetricStat': {
                    'Metric': {
                        'Namespace': params.get('namespace'),
                        'MetricName': params.get('metric_name'),
                        'Dimensions': params.get('dimensions')
                    },
                    'Period': params.get('period'),
                    'Stat': params.get('stat')
                }
            }],
            StartTime=params.get('start'),
            EndTime=params.get('end'),
            ScanBy='TimestampAscending',
            **extra_opts
        )

        results = response.get('MetricDataResults', [])
        target_value = results[0].get('Values') if len(results) > 0 else []
        return target_value[len(target_value)-1] if len(target_value) > 0 else 0.0

    @staticmethod
    def _get_metric_param(metric_name, dimensions):
        end = datetime.utcnow()

        return {'id': f'metric_{utils.random_string()[:12]}',
                'namespace': 'AWS/S3',
                'dimensions': dimensions,
                'start': end - timedelta(days=7),
                'end': datetime.utcnow(),
                'period': 10800,
                'metric_name': metric_name,
                'stat': 'Average'
        }

    @staticmethod
    def set_notification(notification_type, arn_key, confs):
        configurations = []

        for _conf in confs:
            dic = {
                'id': _conf.get('Id', ''),
                'notification_type': notification_type,
                'arn': _conf.get(arn_key, ''),
                'events': _conf.get('Events', []),
            }

            if _conf.get('Filter'):
                dic.update({
                    'filter': _conf.get('Filter')
                })

            configurations.append(NotificationConfiguration(dic, strict=False))

        return configurations
