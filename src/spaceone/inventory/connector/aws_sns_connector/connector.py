import time
import logging
from typing import List

from spaceone.inventory.connector.aws_sns_connector.schema.data import Topic, Subscription, TopicKMS
from spaceone.inventory.connector.aws_sns_connector.schema.resource import TopicResource, TopicResponse
from spaceone.inventory.connector.aws_sns_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import AWSTags

_LOGGER = logging.getLogger(__name__)


class SNSConnector(SchematicAWSConnector):
    service_name = 'sns'
    _kms_client = None
    kms_keys = None
    cloud_service_group = 'SNS'
    cloud_service_type = 'Topic'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[TopicResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: SNS")
        resources = []
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_data,
            'resource': TopicResource,
            'response_schema': TopicResponse
        }

        resources.extend(self.set_service_code_in_cloud_service_type())

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: SNS ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[Topic]:
        cloudtrail_resource_type = 'AWS::SNS::Topic'
        paginator = self.client.get_paginator('list_topics')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000
            }
        )

        for data in response_iterator:
            for raw in data.get('Topics', []):
                try:
                    topic_arn = raw.get('TopicArn')
                    topic_response = self.client.get_topic_attributes(TopicArn=topic_arn)
                    topic = topic_response.get('Attributes')

                    subscription_response = self.client.list_subscriptions_by_topic(TopicArn=topic_arn)
                    tags_response = self.client.list_tags_for_resource(ResourceArn=topic_arn)

                    topic.update({
                        'subscriptions': list(map(lambda subscription: Subscription(subscription, strict=False),
                                                  subscription_response.get('Subscriptions', []))),
                        'tags': list(map(lambda tag: AWSTags(tag, strict=False), tags_response.get('Tags', []))),
                        'name': self._get_name_from_arn(topic_arn),
                        'region_name': region_name,
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, raw['TopicArn'])
                    })

                    if topic.get('KmsMasterKeyId', None) is not None:
                        kms = self.request_kms(topic.get('KmsMasterKeyId'))
                        if kms is not None:
                            topic['kms'] = kms

                    topic_vo = Topic(topic, strict=False)
                    yield {
                        'data': topic_vo,
                        'name': topic_vo.name,
                        'account': self.account_id
                    }
                    
                except Exception as e:
                    resource_id = raw.get('TopicArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield {'data': error_resource_response}

    @property
    def kms_client(self):
        if self._kms_client is None:
            self._kms_client = self.session.client('kms')

        return self._kms_client

    def request_kms(self, alias):
        if self.kms_keys is None:
            self.kms_keys = self.list_aliases()

        _kms = self.search_kms_from_alias(alias)

        if _kms is not None:
            response = self.kms_client.describe_key(KeyId=_kms.get('TargetKeyId', ''))
            key_meta = response.get('KeyMetadata')

            kms_dict = {
                'kms_id': key_meta.get('KeyId', ''),
                'description': key_meta.get('Description', ''),
                'arn': key_meta.get('Arn', ''),
                'account_id': key_meta.get('AWSAccountId', ''),
                'encryption': 'Configured',
                'alias' : _kms.get('AliasName', '')
            }

            return TopicKMS(kms_dict, strict=False)

        return None

    def list_aliases(self):
        aliases = []
        paginator = self.kms_client.get_paginator('list_aliases')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000
            }
        )

        for data in response_iterator:
            for raw in data.get('Aliases', []):
                aliases.append(raw)

        return aliases

    def search_kms_from_alias(self, alias):
        match_kms = [key for key in self.kms_keys if key["AliasName"] == alias]

        if len(match_kms) > 0:
            return match_kms[0]

        return None

    @staticmethod
    def _get_name_from_arn(arn):
        return arn.split(':')[-1]
