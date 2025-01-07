from spaceone.inventory.libs.connector import SchematicAWSConnector


class CloudWatchConnector(SchematicAWSConnector):
    service_name = 'cloudwatch'
    cloud_service_group = 'CloudWatch'
    # cloud_service_types = CLOUD_SERVICE_TYPES