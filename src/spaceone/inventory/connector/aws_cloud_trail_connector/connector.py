import logging
from typing import List

from spaceone.inventory.connector.aws_cloud_trail_connector.schema.data import Trail, EventSelector, InsightSelector, \
    CloudTrailTags
from spaceone.inventory.connector.aws_cloud_trail_connector.schema.resource import TrailResource, TrailResponse
from spaceone.inventory.connector.aws_cloud_trail_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class CloudTrailConnector(SchematicAWSConnector):
    response_schema = TrailResponse
    service_name = 'cloudtrail'
    trails = []

    def get_resources(self) -> List[TrailResource]:
        print("** Cloud Trail START **")
        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)

            # merge data
            for data in self.request_data(region_name):
                yield self.response_schema(
                    {'resource': TrailResource({'data': data,
                                                'reference': ReferenceModel(data.reference)})})

    def request_data(self, region_name) -> List[Trail]:
        response = self.client.describe_trails()

        trails = response.get('trailList', [])
        tags = self._list_tags(trails)

        for raw in trails:
            if raw['TrailARN'] not in self.trails:
                raw['event_selectors'] = list(map(lambda event_selector: EventSelector(event_selector, strict=False),
                                                  self._get_event_selector(raw['Name'])))

                if raw['HasInsightSelectors']:
                    insight_selectors = self._get_insight_selectors(raw.get('Name'))
                    if insight_selectors is not None:
                        raw['insight_selectors'] = InsightSelector(insight_selectors, strict=False)

                raw.update({
                    'account_id': self.account_id,
                    'tags': self._match_tags(raw.get('TrailARN'), tags)
                })

                res = Trail(raw, strict=False)
                self.trails.append(raw['TrailARN'])
                yield res

    def _get_event_selector(self, trail_name):
        response = self.client.get_event_selectors(TrailName=trail_name)
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
        for tag in tags:
            if tag['ResourceId'] == trail_arn:
                for _tag in tag['TagsList']:
                    return_tags.append(CloudTrailTags(_tag, strict=False))

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
