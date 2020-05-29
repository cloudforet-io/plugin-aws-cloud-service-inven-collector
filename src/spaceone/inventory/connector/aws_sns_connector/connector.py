import logging
from typing import List

from spaceone.inventory.connector.aws_sns_connector.schema.data import Topic, Subscription, Tags, TopicKMS
from spaceone.inventory.connector.aws_sns_connector.schema.resource import TopicResource, TopicResponse
from spaceone.inventory.connector.aws_sns_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class SNSConnector(SchematicAWSConnector):
    response_schema = TopicResponse
    service_name = 'sns'
    _kms_client = None
    kms_keys = None

    def get_resources(self) -> List[TopicResource]:
        print("** SNS START **")
        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)

            # merge data
            for data in self.request_data(region_name):
                yield self.response_schema(
                    {'resource': TopicResource({'data': data,
                                                'reference': ReferenceModel(data.reference)})})

    def request_data(self, region_name) -> List[Topic]:
        paginator = self.client.get_paginator('list_topics')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000
            }
        )

        for data in response_iterator:
            for raw in data.get('Topics', []):
                topic_arn = raw.get('TopicArn')
                topic_response = self.client.get_topic_attributes(TopicArn=topic_arn)
                topic = topic_response.get('Attributes')

                subscription_response = self.client.list_subscriptions_by_topic(TopicArn=topic_arn)
                tags_response = self.client.list_tags_for_resource(ResourceArn=topic_arn)

                topic['subscriptions'] = list(map(lambda subscription: Subscription(subscription, strict=False),
                                                  subscription_response.get('Subscriptions', [])))

                topic['tags'] = list(map(lambda tag: Tags(tag, strict=False), tags_response.get('Tags', [])))
                topic['name'] = self._get_name_from_arn(topic_arn)
                topic['region_name'] = region_name
                topic['account_id'] = self.account_id

                if topic.get('KmsMasterKeyId', None) is not None:
                    kms = self.request_kms(topic.get('KmsMasterKeyId'))
                    if kms is not None:
                        topic['kms'] = kms

                res = Topic(topic, strict=False)
                yield res

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
