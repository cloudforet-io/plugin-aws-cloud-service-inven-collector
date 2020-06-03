import time
import logging
from typing import List

from spaceone.inventory.connector.aws_ecr_connector.schema.data import Repository, Image, Tag
from spaceone.inventory.connector.aws_ecr_connector.schema.resource import ECRRepositoryResource, ECRResponse
from spaceone.inventory.connector.aws_ecr_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class ECRConnector(SchematicAWSConnector):
    response_schema = ECRResponse
    service_name = 'ecr'

    @staticmethod
    def _set_image_uri(images, repository_uri):
        for _image in images:
            _image['image_uri'] = f'{repository_uri}:{_image.get("imageTags")[0]}'

        return images

    def get_resources(self) -> List[ECRRepositoryResource]:
        print("** ECR START **")
        start_time = time.time()

        # init cloud service type
        for t in CLOUD_SERVICE_TYPES:
            yield t

        # merge data
        for region_name in self.region_names:
            self.reset_region(region_name)

            # merge data
            for data in self.request_data(region_name):
                yield self.response_schema(
                    {'resource': ECRRepositoryResource({'data': data,
                                                        'reference': ReferenceModel(data.reference)})})

        print(f' ECR Finished {time.time() - start_time} Seconds')

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
                raw.update({
                    'images': list(self._describe_images(raw)),
                    'tags': self.request_tags(raw.get('repositoryArn')),
                    'region_name': region_name,
                    'account_id': self.account_id
                })
                res = Repository(raw, strict=False)

                yield res

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
                raw['image_size_in_megabytes'] = f'{float(raw["imageSizeInBytes"] / 1000000):.2f}'

                image_uri = self._generate_image_uri(repo.get("repositoryUri"), raw.get("imageTags", []))
                if image_uri is not None:
                    raw['image_uri'] = image_uri

                res = Image(raw, strict=False)
                yield res

    def request_tags(self, resource_arn):
        response = self.client.list_tags_for_resource(resourceArn=resource_arn)
        return list(map(lambda tag: Tag(tag, strict=False), response.get('tags', [])))

    @staticmethod
    def _generate_image_uri(repo_uri, image_tags):
        if repo_uri is None or len(image_tags) == 0:
            return None

        return f'{repo_uri}:{image_tags[0]}'
