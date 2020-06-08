import time
import logging
from typing import List
from botocore.exceptions import ClientError

from spaceone.inventory.connector.aws_s3_connector.schema.data import Bucket, Versioning, ServerAccessLogging, \
    WebsiteHosting, ObjectLock, Encryption, Tags, TransferAcceleration, NotificationConfiguration, RequestPayment
from spaceone.inventory.connector.aws_s3_connector.schema.resource import BucketResource, BucketResponse
from spaceone.inventory.connector.aws_s3_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class S3Connector(SchematicAWSConnector):
    response_schema = BucketResponse
    service_name = 's3'

    def get_resources(self) -> List[BucketResource]:
        print("** S3 START **")
        resources = []
        start_time = time.time()

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        # merge data
        for data in self.request_data():
            resources.append(self.response_schema(
                {'resource': BucketResource({'data': data,
                                             'reference': ReferenceModel(data.reference)})}))

        print(f' S3 Finished {time.time() - start_time} Seconds')
        return resources

    def request_data(self) -> List[Bucket]:
        response = self.client.list_buckets()

        for raw in response.get('Buckets', []):
            bucket_name = raw.get('Name')

            raw.update({
                'arn': self.generate_arn(service=self.service_name, region="", account_id="", resource_type=bucket_name, resource_id="*"),
                'account_id': self.account_id
            })

            if region_name := self.get_bucket_location(bucket_name):
                raw.update({'region_name': region_name})

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

            if transfer_acceleration := self.get_transfer_acceleration(bucket_name):
                raw.update({'transfer_acceleration': transfer_acceleration})

            if request_payment := self.get_request_payment(bucket_name):
                raw.update({'request_payment': request_payment})

            if notification_configurations := self.get_notification_configurations(bucket_name):
                raw.update({'notification_configurations': notification_configurations})

            if tags := self.get_tags(bucket_name):
                raw.update({'tags': tags})

            # object_count, object_total_size = self.get_object_info(bucket_name)
            #
            # raw.update({
            #     'object_count': object_count,
            #     'object_total_size': object_total_size
            # })

            res = Bucket(raw, strict=False)
            yield res

    def get_bucket_versioning(self, bucket_name):
        response = self.client.get_bucket_versioning(Bucket=bucket_name)

        if status := response.get('Status'):
            version = {
                'status': status,
                'mfa_delete': response.get('MFADelete')
            }
            return Versioning(version, strict=False)

        return None

    def get_server_access_logging(self, bucket_name):
        response = self.client.get_bucket_logging(Bucket=bucket_name)

        if access_logging := response.get('LoggingEnabled'):
            return ServerAccessLogging(access_logging, strict=False)

        return None

    def get_website_hosting(self, bucket_name):
        try:
            response = self.client.get_bucket_website(Bucket=bucket_name)
            del response['ResponseMetadata']
            return WebsiteHosting(response, strict=False)

        except ClientError as e:
            return None

    def get_encryption(self, bucket_name):
        try:
            response = self.client.get_bucket_encryption(Bucket=bucket_name)

            if encryption := response.get('ServerSideEncryptionConfiguration'):
                return Encryption(encryption, strict=False)
            else:
                return None
        except ClientError as e:
            return None

    def get_object_lock(self, bucket_name):
        try:
            response = self.client.get_object_lock_configuration(Bucket=bucket_name)

            if object_lock := response.get('ObjectLockConfiguration'):
                return ObjectLock(object_lock, strict=False)
            else:
                return None
        except ClientError as e:
            return None

    def get_transfer_acceleration(self, bucket_name):
        response = self.client.get_bucket_accelerate_configuration(Bucket=bucket_name)

        if transfer_acceleration := response.get('Status'):
            return TransferAcceleration({'transfer_acceleration': transfer_acceleration}, strict=False)

        return None

    def get_request_payment(self, bucket_name):
        response = self.client.get_bucket_request_payment(Bucket=bucket_name)

        if payer := response.get('Payer'):
            return RequestPayment({'request_payment': payer}, strict=False)

        return None

    def get_notification_configurations(self, bucket_name):
        response = self.client.get_bucket_notification_configuration(Bucket=bucket_name)

        sns = self.set_notification('SNS Topic', 'TopicArn', response.get('TopicConfigurations', []))
        que = self.set_notification('Queue', 'QueueArn', response.get('QueueConfigurations', []))
        func = self.set_notification('Lambda Function', 'LambdaFunctionArn', response.get('LambdaFunctionConfigurations', []))

        total_noti = sns + que + func

        if len(total_noti) > 0:
            return total_noti
        else:
            return None

    def get_tags(self, bucket_name):
        try:
            response = self.client.get_bucket_tagging(Bucket=bucket_name)
            return list(map(lambda tag: Tags(tag, strict=False), response.get('TagSet', [])))
        except ClientError as e:
            return None

    def get_bucket_location(self, bucket_name):
        response = self.client.get_bucket_location(Bucket=bucket_name)
        return response.get('LocationConstraint')

    def get_object_info(self, bucket_name):
        object_count = 0
        object_total_size = 0

        paginator = self.client.get_paginator('list_objects_v2')
        response_iterator = paginator.paginate(
            Bucket=bucket_name,
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            object_count = object_count + data.get('KeyCount', 0)

            for raw in data.get('Contents', []):
                object_total_size = object_total_size + raw.get('Size', 0)

        return object_count, object_total_size

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
