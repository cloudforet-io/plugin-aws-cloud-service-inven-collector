import time
import logging
from typing import List

from spaceone.inventory.connector.aws_cloud_trail_connector.schema.data import Trail, EventSelector, InsightSelector
from spaceone.inventory.connector.aws_cloud_trail_connector.schema.resource import TrailResource, TrailResponse
from spaceone.inventory.connector.aws_cloud_trail_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import AWSTags

_LOGGER = logging.getLogger(__name__)


class CloudTrailConnector(SchematicAWSConnector):
    service_name = 'cloudtrail'
    trails = []
    cloud_service_group = 'CloudTrail'
    cloud_service_type = 'Trail'
    cloud_service_types = CLOUD_SERVICE_TYPES

    def get_resources(self) -> List[TrailResource]:
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: CloudTrail")
        resources = []
        start_time = time.time()

        resources.extend(self.set_service_code_in_cloud_service_type())

        collect_resource = {
            'request_method': self.request_data,
            'resource': TrailResource,
            'response_schema': TrailResponse
        }

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources][account_id: {self.account_id}] FINISHED: CloudTrail ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[Trail]:
        cloudtrail_resource_type = 'AWS::CloudTrail::Trail'
        response = self.client.describe_trails()

        trails = response.get('trailList', [])
        tags = self._list_tags(trails)

        for raw in trails:
            try:
                if raw['TrailARN'] not in self.trails:
                    raw['event_selectors'] = list(map(lambda event_selector: EventSelector(event_selector, strict=False),
                                                      self._get_event_selector(raw['TrailARN'])))

                    if raw['HasInsightSelectors']:
                        insight_selectors = self._get_insight_selectors(raw.get('Name'))
                        if insight_selectors is not None:
                            raw['insight_selectors'] = InsightSelector(insight_selectors, strict=False)

                    raw.update({
                        'tags': self._match_tags(raw.get('TrailARN'), tags),
                        'cloudtrail': self.set_cloudtrail(region_name, cloudtrail_resource_type, raw['TrailARN'])
                    })

                    trail_vo = Trail(raw, strict=False)
                    self.trails.append(raw['TrailARN'])

                    yield {
                        'data': trail_vo,
                        'name': trail_vo.name,
                        'account': self.account_id
                    }

            except Exception as e:
                resource_id = raw.get('TrailARN', '')
                error_resource_response = self.generate_error(region_name, resource_id, e)
                yield {'data': error_resource_response}

    def _get_event_selector(self, trail_arn):
        response = self.client.get_event_selectors(TrailName=trail_arn)
        return response.get('EventSelectors', [])

    def _list_tags(self, trails):
        tags = []
        trails_from_region = self._sort_trail_from_region(trails)

        for _region in trails_from_region:
            self.reset_region(_region)
            response = self.client.list_tags(ResourceIdList=trails_from_region[_region])
            resource_tag_list = response.get('ResourceTagList', [])
            tags = tags + resource_tag_list

        return tags

    def _get_insight_selectors(self, trail_name):
        response = self.client.get_insight_selectors(TrailName=trail_name)

        insight_selectors = response.get('InsightSelectors', [])
        if len(insight_selectors) == 0:
            return None
        else:
            return insight_selectors[0]

    @staticmethod
    def _match_tags(trail_arn, tags):
        return_tags = []
        try:
            for tag in tags:
                if tag['ResourceId'] == trail_arn:
                    for _tag in tag['TagsList']:
                        return_tags.append(AWSTags(_tag, strict=False))
        except Exception as e:
            _LOGGER.error(e)

        return return_tags

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
