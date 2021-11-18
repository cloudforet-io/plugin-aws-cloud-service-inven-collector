import time
import logging
from typing import List

from spaceone.inventory.connector.aws_ecr_connector.schema.data import Repository, Image, Tag
from spaceone.inventory.connector.aws_ecr_connector.schema.resource import ECRRepositoryResource, ECRResponse
from spaceone.inventory.connector.aws_ecr_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector

_LOGGER = logging.getLogger(__name__)


class ECRConnector(SchematicAWSConnector):
    service_name = 'ecr'
    cloud_service_group = 'EC2'
    cloud_service_type = 'Repository'

    @staticmethod
    def _set_image_uri(images, repository_uri):
        for _image in images:
            _image['image_uri'] = f'{repository_uri}:{_image.get("imageTags")[0]}'

        return images

    def get_resources(self) -> List[ECRRepositoryResource]:
        _LOGGER.debug("[get_resources] START: ECR")
        resources = []
        start_time = time.time()

        collect_resource = {
            'request_method': self.request_data,
            'resource': ECRRepositoryResource,
            'response_schema': ECRResponse
        }

        # init cloud service type
        for cst in CLOUD_SERVICE_TYPES:
            resources.append(cst)

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)
            resources.extend(self.collect_data_by_region(self.service_name, region_name, collect_resource))

        _LOGGER.debug(f'[get_resources] FINISHED: ECR ({time.time() - start_time} sec)')
        return resources

    def request_data(self, region_name) -> List[Repository]:
        paginator = self.client.get_paginator('describe_repositories')
        response_iterator = paginator.paginate(
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )
        for data in response_iterator:
            for raw in data.get('repositories', []):
                try:
                    raw.update({
                        'images': list(self._describe_images(raw)),
                        'tags': self.request_tags(raw.get('repositoryArn')),
                        'account_id': self.account_id
                    })
                    res = Repository(raw, strict=False)

                    yield res, res.repository_name
                except Exception as e:
                    resource_id = raw.get('repositoryArn', '')
                    error_resource_response = self.generate_error(region_name, resource_id, e)
                    yield error_resource_response, ''

    def _describe_images(self, repo):
        paginator = self.client.get_paginator('describe_images')
        response_iterator = paginator.paginate(
            repositoryName=repo.get('repositoryName'),
            PaginationConfig={
                'MaxItems': 10000,
                'PageSize': 50,
            }
        )

        for data in response_iterator:
            for raw in data.get('imageDetails', []):
                raw.update({
                    # 'image_size_in_megabytes': f'{float(raw["imageSizeInBytes"] / 1000000):.2f}',
                    'image_tags_display': self._generate_image_tags_display(raw.get('imageTags', [])),
                    'image_uri': self._generate_image_uri(repo.get("repositoryUri", ''), raw.get("imageTags", []))
                })

                res = Image(raw, strict=False)
                yield res

    def request_tags(self, resource_arn):
        response = self.client.list_tags_for_resource(resourceArn=resource_arn)
        return list(map(lambda tag: Tag(tag, strict=False), response.get('tags', [])))

    @staticmethod
    def _generate_image_uri(repo_uri, image_tags):
        if image_tags:
            return f'{repo_uri}:{image_tags[0]}'
        else:
            return repo_uri

    @staticmethod
    def _generate_image_tags_display(image_tags):
        if image_tags:
            return image_tags
        else:
            return ['<untagged>']
