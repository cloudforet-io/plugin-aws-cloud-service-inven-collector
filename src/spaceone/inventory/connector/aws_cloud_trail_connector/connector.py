import time
import logging
from typing import List

from spaceone.inventory.connector.aws_cloud_trail_connector.schema.data import Trail, EventSelector, InsightSelector
from spaceone.inventory.connector.aws_cloud_trail_connector.schema.resource import TrailResource, TrailResponse
from spaceone.inventory.connector.aws_cloud_trail_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class CloudTrailConnector(SchematicAWSConnector):
    response_schema = TrailResponse
    service_name = 'cloudtrail'
    cloud_service_group = 'CloudTrail'
    cloud_service_type = 'Trail'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[TrailResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: CloudTrail")
        resources = []
        start_time = time.time()

        try:
            resources.extend(self.set_cloud_service_types())

            # merge data
            for data, tags in self.request_data():
                if getattr(data, 'resource_type', None) and data.resource_type == 'inventory.ErrorResource':
                    # Error Resource
                    resources.append(data)
                else:
                    resources.append(self.response_schema(
                        {'resource': TrailResource({
                            'name': data.name,
                            'data': data,
                            'account': self.account_id,
                            'reference': ReferenceModel(data.reference()),
                            'region_code': data.home_region,
                            'tags': tags
                        })}))

        except Exception as e:
            resource_id = ''
            resources.append(self.generate_error('global', resource_id, e))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: Route53 ({time.time() - start_time} sec)')
        return resources

    def request_data(self) -> List[Trail]:
        cloudwatch_namespace = 'CloudTrailMetrics'
        cloudtrail_resource_type = 'AWS::CloudTrail::Trail'
        response = self.client.describe_trails()

        trails = response.get('trailList', [])
        tags = self._list_tags(trails)

        for raw in trails:
            region_name = raw.get('HomeRegion', '')
            try:
                raw['event_selectors'] = list(map(lambda event_selector: EventSelector(event_selector, strict=False),
                                                  self._get_event_selector(raw['TrailARN'])))

                if raw['HasInsightSelectors']:
                    insight_selectors = self._get_insight_selectors(raw.get('Name'))
                    if insight_selectors is not None:
                        raw['insight_selectors'] = InsightSelector(insight_selectors, strict=False)

                raw.update({
                    'cloudwatch': self.set_cloudwatch(cloudwatch_namespace, None, None, region_name),
                    'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, raw['TrailARN']),
                })

                yield Trail(raw, strict=False), self._match_tags(raw['TrailARN'], tags)

            except Exception as e:
                resource_id = raw.get('TrailARN', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield error_resource_response

    def _get_event_selector(self, trail_arn):
        response = self.client.get_event_selectors(TrailName=trail_arn)
        return response.get('EventSelectors', [])

    def _list_tags(self, trails):
        tags = []
        trails_from_region = self._sort_trail_from_region(trails)

        for _region in trails_from_region:
            self.reset_region(_region)
            response = self.client.list_tags(ResourceIdList=trails_from_region[_region])
            tags.extend(response.get('ResourceTagList', []))

        return tags

    def _get_insight_selectors(self, trail_name):
        response = self.client.get_insight_selectors(TrailName=trail_name)

        insight_selectors = response.get('InsightSelectors', [])
        if len(insight_selectors) == 0:
            return None
        else:
            return insight_selectors[0]

    def _match_tags(self, trail_arn, tags):
        tag_dict = {}

        try:
            for tag in tags:
                if tag['ResourceId'] == trail_arn:
                    tag_dict.update(self.convert_tags_to_dict_type(tag['TagsList']))
        except Exception as e:
            _LOGGER.error(e)

        return tag_dict

    @staticmethod
    def _sort_trail_from_region(trails):
        return_dic = {}

        for _trail in trails:
            trail_arn = _trail.get('TrailARN', '')
            split_trail = trail_arn.split(':')
            try:
                region = split_trail[3]
                if region in return_dic:
                    return_dic[region].append(trail_arn)
                else:
                    return_dic[region] = [trail_arn]
            except IndexError:
                pass

        return return_dic
