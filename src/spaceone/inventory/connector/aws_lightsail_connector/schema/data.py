import logging
from schematics import Model
from schematics.types import IntType, ModelType, StringType, BooleanType, FloatType, DateTimeType, ListType, DictType

_LOGGER = logging.getLogger(__name__)


class Tag(Model):
    key = StringType(serialize_when_none=False)
    value = StringType(serialize_when_none=False)


class AddOne(Model):
    name = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    snapshot_time_of_day = StringType(deserialize_from="snapshotTimeOfDay", serialize_when_none=False)
    next_snapshot_time_of_day = StringType(deserialize_from="nextSnapshotTimeOfDay", serialize_when_none=False)


class Location(Model):
    availability_zone = StringType(deserialize_from="availabilityZone", serialize_when_none=False)
    region_name = StringType(deserialize_from="regionName", serialize_when_none=False)


class AddOn(Model):
    name = StringType(serialize_when_none=False)
    status = StringType(serialize_when_none=False)
    snapshot_time_of_day = StringType(deserialize_from="snapshotTimeOfDay", serialize_when_none=False)
    next_snapshot_time_of_day = StringType(deserialize_from="nextSnapshotTimeOfDay", serialize_when_none=False)


class ResourceBase(Model):
    name = StringType()
    arn = StringType()
    support_code = StringType(deserialize_from="SupportCode", serialize_when_none=False)
    created_at = DateTimeType(deserialize_from="createdAt", serialize_when_none=False)
    location = ModelType(Location, serialize_when_none=False)
    resource_type = StringType(deserialize_from="resourceType", serialize_when_none=False,
                               choices=['ContainerService', 'Instance', 'StaticIp', 'KeyPair', 'InstanceSnapshot',
                                        'Domain', 'PeeredVpc', 'LoadBalancer', 'LoadBalancerTlsCertificate', 'Disk',
                                        'DiskSnapshot', 'RelationalDatabase', 'RelationalDatabaseSnapshot',
                                        'ExportSnapshotRecord', 'CloudFormationStackRecord', 'Alarm', 'ContactMethod',
                                        'Distribution', 'Certificate', 'Bucket'])
    tags = ListType(ModelType(Tag), default=[])


class Disk(ResourceBase):
    add_ons = ListType(ModelType(AddOn), deserialize_from='addOns', default=[])
    size_in_gb = IntType(deserialize_from="sizeInGb", serialize_when_none=False)
    is_system_disk = BooleanType(deserialize_from="isSystemDisk", serialize_when_none=False)
    iops = IntType(serialize_when_none=False)
    path = StringType(serialize_when_none=False)
    state = StringType(serialize_when_none=False, choices=['pending', 'error', 'available', 'in-use', 'unknown'])
    attached_to = StringType(deserialize_from="attachedTo", serialize_when_none=False)
    is_attached = BooleanType(deserialize_from="isAttached", serialize_when_none=False)
    attachment_state = StringType(deserialize_from="attachmentState", serialize_when_none=False)
    gb_in_use = IntType(deserialize_from="gbInUse", serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://lightsail.aws.amazon.com/ls/webapp/{region_code}/disks/{self.name}"
        }


class InstanceHardware(Model):
    cpu_count = IntType(deserialize_from="cpuCount", serialize_when_none=False)
    disks = ListType(ModelType(Disk), default=[])
    ram_size_in_gb = FloatType(deserialize_from="ramSizeInGb", serialize_when_none=False)


class MonthlyTransfer(Model):
    gb_per_month_allocated = IntType(deserialize_from="gbPerMonthAllocated", serialize_when_none=False)


class Ports(Model):
    from_port = IntType(deserialize_from="fromPort", serialize_when_none=False)
    to_port = IntType(deserialize_from="toPort", serialize_when_none=False)
    protocol = StringType(serialize_when_none=False, choices=['tcp', 'all', 'udp', 'icmp'])
    access_from = StringType(deserialize_from="accessFrom", serialize_when_none=False)
    access_type = StringType(deserialize_from="accessType", choices=['Public', 'Private'])
    common_name = StringType(deserialize_from="commonName", serialize_when_none=False)
    access_direction = StringType(deserialize_from="accessDirection", choices=['inbound', 'outbound'])
    cidrs = ListType(StringType, default=[])
    ipv6_cidrs = ListType(StringType, deserialize_from="ipv6Cidrs", default=[])
    cidr_list_aliases = ListType(StringType, deserialize_from="cidrListAliases", default=[])


class Networking(Model):
    monthly_transfer = ModelType(MonthlyTransfer, deserialize_from="monthlyTransfer", serialize_when_none=False)
    ports = ListType(ModelType(Ports), default=[])


class InstanceState(Model):
    code = IntType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)


class Instance(ResourceBase):
    add_ons = ListType(ModelType(AddOn), deserialize_from='addOns', default=[])
    blueprint_id = StringType(deserialize_from="blueprintId", serialize_when_none=False)
    blueprint_name = StringType(deserialize_from="blueprintName", serialize_when_none=False)
    bundle_id = StringType(deserialize_from="bundleId", serialize_when_none=False)
    is_static_ip = BooleanType(deserialize_from="isStaticIp", serialize_when_none=False)
    private_ip_address = StringType(deserialize_from="privateIpAddress", serialize_when_none=False)
    public_ip_address = StringType(deserialize_from="publicIpAddress", serialize_when_none=False)
    ipv6_address = ListType(StringType, deserialize_from="ipv6Addresses", default=[])
    hardware = ModelType(InstanceHardware, serialize_when_none=False)
    networking = ModelType(Networking, serialize_when_none=False)
    state = ModelType(InstanceState, serialize_when_none=False)
    username = StringType(serialize_when_none=False)
    ssh_key_name = StringType(deserialize_from="sshKeyName", serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://lightsail.aws.amazon.com/ls/webapp/{region_code}/instances/{self.name}/connect"
        }


class ResourceReceivingAccess(Model):
    name = StringType(serialize_when_none=False)
    resource_type = StringType(deserialize_from="resourceType", serialize_when_none=False)


class BucketAccessRule(Model):
    get_object = StringType(deserialize_from="getObject", choices=['public', 'private'], serialize_when_none=False)
    allow_public_overrides = BooleanType(deserialize_from="allowPublicOverrides", serialize_when_none=False)


class BucketState(Model):
    code = StringType(serialize_when_none=False)
    message = StringType(serialize_when_none=False)


class BucketAccessLogConfig(Model):
    enabled = BooleanType(serialize_when_none=False)
    destination = StringType(serialize_when_none=False)
    prefix = StringType(serialize_when_none=False)


class Bucket(ResourceBase):
    access_rules = ModelType(BucketAccessRule, deserialize_from="accessRules", serialize_when_none=False)
    url = StringType(serialize_when_none=False)
    object_versioning = StringType(deserialize_from="objectVersioning", serialize_when_none=False)
    able_to_update_bundle = BooleanType(deserialize_from="ableToUpdateBundle", serialize_when_none=False)
    readonly_access_accounts = ListType(StringType, deserialize_from="readonlyAccessAccounts", default=[])
    resource_receiving_access = ListType(ModelType(ResourceReceivingAccess),
                                         deserialize_from="resourcesReceivingAccess", default=[])
    state = ModelType(BucketState, serialize_when_none=False)
    access_log_config = ModelType(BucketAccessLogConfig, deserialize_from="accessLogConfig", serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://lightsail.aws.amazon.com/ls/webapp/{region_code}/buckets/{self.name}/objects"
        }


class DiskSnapshot(ResourceBase):
    size_in_gb = IntType(deserialize_from="sizeInGb", serialize_when_none=False)
    state = StringType(serialize_when_none=False, choices=['pending', 'completed', 'error', 'unknown'])
    progress = StringType(serialize_when_none=False)
    from_disk_name = StringType(deserialize_from="fromDiskName", serialize_when_none=False)
    from_disk_arn = StringType(deserialize_from="fromDiskArn", serialize_when_none=False)
    from_instance_name = StringType(deserialize_from="fromInstanceName", serialize_when_none=False)
    from_instance_arn = StringType(deserialize_from="fromInstanceArn", serialize_when_none=False)
    is_from_auto_snapshot = BooleanType(deserialize_from="isFromAutoSnapshot", serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://lightsail.aws.amazon.com/ls/webapp/{region_code}/disks/{self.from_disk_name}/snapshots"
        }


class StaticIP(ResourceBase):
    ip_address = StringType(deserialize_from="ipAddress", serialize_when_none=False)
    attached_to = StringType(deserialize_from="attachedTo", serialize_when_none=False)
    is_attached = BooleanType(deserialize_from="isAttached", serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://lightsail.aws.amazon.com/ls/webapp/{region_code}/static-ips/{self.name}"
        }


class PendingModifiedValues(Model):
    master_user_password = StringType(deserialize_from="masterUserPassword", serialize_when_none=False)
    engine_version = StringType(deserialize_from="engineVersion", serialize_when_none=False)
    backup_retention_enabled = BooleanType(deserialize_from="backupRetentionEnabled", serialize_when_none=False)


class RelationDatabaseHardware(Model):
    cpu_count = IntType(deserialize_from="cpuCount", serialize_when_none=False)
    disk_size_in_gb = IntType(deserialize_from="diskSizeInGb", serialize_when_none=False)
    ram_size_in_gb = FloatType(deserialize_from="ramSizeInGb", serialize_when_none=False)


class MasterEndpoint(Model):
    port = IntType(serialize_when_none=False)
    address = StringType(serialize_when_none=False)


class PendingMaintenanceActions(Model):
    action = StringType(serialize_when_none=False)
    description = StringType(serialize_when_none=False)
    current_apply_date = DateTimeType(deserialize_from="currentApplyDate", serialize_when_none=False)


class RelationDatabase(ResourceBase):
    relation_database_blueprint_id = StringType(deserialize_from="relationalDatabaseBlueprintId",
                                                serialize_when_none=False)
    relation_database_bundle_id = StringType(deserialize_from="relationalDatabaseBundleId", serialize_when_none=False)
    master_database_name = StringType(deserialize_from="masterDatabaseName", serialize_when_none=False)
    hardware = ModelType(RelationDatabaseHardware, serialize_when_none=False)
    state = StringType(serialize_when_none=False)
    secondary_availability_zone = StringType(deserialize_from="secondaryAvailabilityZone", serialize_when_none=False)
    backup_retention_enabled = BooleanType(deserialize_from="backupRetentionEnabled", serialize_when_none=False)
    pending_modified_values = ModelType(PendingModifiedValues, deserialize_from="pendingModifiedValues", serialize_when_none=False)
    engine = StringType(serialize_when_none=False)
    engine_version = StringType(deserialize_from="engineVersion", serialize_when_none=False)
    latest_restorable_time = DateTimeType(deserialize_from="latestRestorableTime", serialize_when_none=False)
    master_user_name = StringType(deserialize_from="masterUsername", serialize_when_none=False)
    parameter_apply_status = StringType(deserialize_from="parameterApplyStatus", serialize_when_none=False)
    preferred_backup_window = StringType(deserialize_from="preferredBackupWindow", serialize_when_none=False)
    preferred_maintenance_window = StringType(deserialize_from="preferredMaintenanceWindow", serialize_when_none=False)
    publicly_accessible = BooleanType(deserialize_from="publiclyAccessible", serialize_when_none=False)
    master_endpoint = ModelType(MasterEndpoint, deserialize_from="masterEndpoint", serialize_when_none=False)
    pending_maintenance_actions = ListType(ModelType(PendingMaintenanceActions), deserialize_from="pendingMaintenanceActions", serialize_when_none=False)
    ca_certificate_identifier = StringType(deserialize_from="caCertificateIdentifier", serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://lightsail.aws.amazon.com/ls/webapp/{region_code}/databases/{self.name}/connect"
        }


class DomainEntry(Model):
    id = StringType(serialize_when_none=False)
    name = StringType(serialize_when_none=False)
    target = StringType(serialize_when_none=False)
    type = StringType(serialize_when_none=False)
    is_alias = BooleanType(deserialize_from="isAlias", serialize_when_none=False)


class Domain(ResourceBase):
    domain_entry = ListType(ModelType(DomainEntry), deserialize_from="domainEntries", default=[])

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://lightsail.aws.amazon.com/ls/webapp/domains/{self.name}"
        }


class Origin(Model):
    name = StringType(serialize_when_none=False)
    resource_type = StringType(deserialize_from="resourceType", serialize_when_none=False,
                               choices=['ContainerService', 'Instance', 'StaticIp', 'KeyPair', 'InstanceSnapshot',
                                        'Domain', 'PeeredVpc', 'LoadBalancer', 'LoadBalancerTlsCertificate', 'Disk',
                                        'DiskSnapshot', 'RelationalDatabase', 'RelationalDatabaseSnapshot',
                                        'ExportSnapshotRecord', 'CloudFormationStackRecord', 'Alarm', 'ContactMethod',
                                        'Distribution', 'Certificate', 'Bucket'])
    region_name = StringType(deserialize_from="regionName", serialize_when_none=False)
    protocol_policy = StringType(deserialize_from="protocolPolicy", choices=["http-only", "https-only"],
                                 serialize_when_none=False)


class DefaultCacheBehavior(Model):
    behavior = StringType(choices=["dont-cache", "cache"], serialize_when_none=False)


class ForwardedCookies(Model):
    option = StringType(serialize_when_none=False, choices=['none', 'allow-list', 'all'])
    header_allow_list = ListType(StringType(choices=['Accept', 'Accept-Charset', 'Accept-Datetime', 'Accept-Encoding',
                                                     'Accept-Language', 'Authorization', 'CloudFront-Forwarded-Proto',
                                                     'CloudFront-Is-Desktop-Viewer', 'CloudFront-Is-Mobile-Viewer',
                                                     'CloudFront-Is-SmartTV-Viewer', 'CloudFront-Is-Tablet-Viewer',
                                                     'CloudFront-Viewer-Country', 'Host', 'Origin', 'Referer']),
                                 default=[])


class ForwardedHeaders(Model):
    option = StringType(serialize_when_none=False, choices=['none', 'allow-list', 'all'])
    header_allow_list = ListType(StringType(choices=['Accept', 'Accept-Charset', 'Accept-Datetime', 'Accept-Encoding',
                                                     'Accept-Language', 'Authorization', 'CloudFront-Forwarded-Proto',
                                                     'CloudFront-Is-Desktop-Viewer', 'CloudFront-Is-Mobile-Viewer',
                                                     'CloudFront-Is-SmartTV-Viewer', 'CloudFront-Is-Tablet-Viewer',
                                                     'CloudFront-Viewer-Country', 'Host', 'Origin', 'Referer']),
                                 default=[])


class ForwardedQueryStrings(Model):
    option = BooleanType(serialize_when_none=False)
    query_string_allow_list = ListType(StringType, default=[])


class CacheBehavior(Model):
    path = StringType(serialize_when_none=False),
    behavior = StringType(serialize_when_none=False, choices=['dont-cache', 'cache'])


class CacheBehaviorSettings(Model):
    default_ttl = IntType(deserialize_from="defaultTTL", serialize_when_none=False)
    minimum_ttl = IntType(deserialize_from="minimumTTL", serialize_when_none=False)
    maximum_ttl = IntType(deserialize_from="maximumTTL", serialize_when_none=False)
    allowed_http_methods = StringType(deserialize_from="allowedHTTPMethods", serialize_when_none=False)
    cached_http_methods = StringType(deserialize_from="cachedHTTPMethods", serialize_when_none=False)
    forwarded_cookies = ModelType(ForwardedCookies, deserialize_from="forwardedCookies", serialize_when_none=False)
    forwarded_headers = ModelType(ForwardedHeaders, deserialize_from="forwardedHeaders", serialize_when_none=False)
    forwarded_query_strings = ModelType(ForwardedQueryStrings, deserialize_from="forwardedQueryStrings",
                                        serialize_when_none=False)


class Distribution(ResourceBase):
    alternative_domain_names = ListType(StringType, deserialize_from="alternativeDomainNames", default=[])
    status = StringType(serialize_when_none=False)
    is_enabled = BooleanType(serialize_when_none=False)
    domain_name = StringType(deserialize_from="domainName", serialize_when_none=False)
    bundle_id = StringType(deserialize_from="bundleId", serialize_when_none=False)
    certificate_name = StringType(deserialize_from="certificateName", serialize_when_none=False)
    origin = ModelType(Origin, deserialize_from="origin", serialize_when_none=False)
    origin_public_dns = StringType(deserialize_from="originPublicDNS", serialize_when_none=False)
    default_cache_behavior = ModelType(DefaultCacheBehavior, deserialize_from="defaultCacheBehavior", serialize_when_none=False)
    cache_behavior_settings = ModelType(CacheBehaviorSettings, deserialize_from="cacheBehaviorSettings", serialize_when_none=False)
    cache_behavior = ListType(ModelType(CacheBehavior), deserialize_from="cacheBehaviors", serialize_when_none=False)
    able_to_update_bundle = BooleanType(deserialize_from="ableToUpdateBundle", serialize_when_none=False)
    ip_address_type = StringType(deserialize_from="ipAddressType", serialize_when_none=False,
                                 choices=['dualstack', 'ipv4'])

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://lightsail.aws.amazon.com/ls/webapp/distributions/{self.name}/"
        }


class ContainerServiceStateDetail(Model):
    code = StringType(serialize_when_none=False,
                      choices=['CREATING_SYSTEM_RESOURCES', 'CREATING_NETWORK_INFRASTRUCTURE',
                               'PROVISIONING_CERTIFICATE', 'PROVISIONING_SERVICE', 'CREATING_DEPLOYMENT',
                               'EVALUATING_HEALTH_CHECK', 'ACTIVATING_DEPLOYMENT', 'CERTIFICATE_LIMIT_EXCEEDED',
                               'UNKNOWN_ERROR'])
    message = StringType(serialize_when_none=False)


class CurrentDeploymentContainerPorts(Model):
    ports = StringType(serialize_when_none=False, choices=['HTTP', 'HTTPS', 'TCP', 'UDP'])


class HealthCheck(Model):
    healthy_threshold = StringType(deserialize_from="healthyThreshold", serialize_when_none=False),
    unhealthy_threshold = StringType(deserialize_from="unhealthyThreshold", serialize_when_none=False)
    timeout_seconds = StringType(deserialize_from="timeoutSeconds", serialize_when_none=False)
    interval_seconds = StringType(deserialize_from="intervalSeconds", serialize_when_none=False)
    path = StringType(deserialize_from="path", serialize_when_none=False)
    success_code = StringType(deserialize_from="successCodes", serialize_when_none=False)


class PublicEndpoint(Model):
    container_name = StringType(deserialize_from="containerName", serialize_when_none=False),
    container_port = StringType(deserialize_from="containerPort", serialize_when_none=False),
    health_check = ModelType(HealthCheck, deserialize_from="healthCheck", serialize_when_none=False)


class ContainerServiceCurrentDeployment(Model):
    version = IntType(serialize_when_none=False)
    state = StringType(serialize_when_none=False, choices=['ACTIVATING', 'ACTIVE', 'INACTIVE', 'FAILED'])
    public_endpoint = ModelType(PublicEndpoint, deserialize_from="publicEndpoint", serialize_when_none=False)
    created_at = DateTimeType(deserialize_from="createdAt", serialize_when_none=False)


class ContainerService(ResourceBase):
    container_service_name = StringType(deserialize_from="containerServiceName", serialize_when_none=False)
    power = StringType(serialize_when_none=False, choices=['nano', 'micro', 'small', 'medium', 'large', 'xlarge'])
    power_id = StringType(deserialize_from="powerId", serialize_when_none=False)
    power_id = StringType(serialize_when_none=False, choices=['PENDING', 'READY', 'RUNNING', 'UPDATING', 'DELETING',
                                                           'DISABLED', 'DEPLOYING'])
    state_detail = ModelType(ContainerServiceStateDetail, deserialize_from="stateDetail", serialize_when_none=False)
    scale = IntType(serialize_when_none=False)
    current_deployment = ModelType(ContainerServiceCurrentDeployment, deserialize_from="currentDeployment")
    next_deployment = ModelType(ContainerServiceCurrentDeployment, deserialize_from="nextDeployment")
    is_disabled = BooleanType(deserialize_from="isDisabled", serialize_when_none=False)
    privateDomainName = StringType(deserialize_from="privateDomainName", serialized_name=False)
    url = StringType(deserialize_from="url", serialize_when_none=False)

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://lightsail.aws.amazon.com/ls/webapp/{region_code}/container-services/{self.name}/deployments"
        }


class InstanceHealthSummary(Model):
    instance_name = StringType(deserialize_from="instanceName", serialize_when_none=False)
    instance_health = StringType(deserialize_from="instanceHealth", serialize_when_none=False, choices=['initial', 'healthy',
                                                                                                        'unhealthy', 'unused', 'draining', 'unavailable'])
    instance_health_region = StringType(deserialize_from="instanceHealthReason", serialize_when_none=False, choices=['Lb.RegistrationInProgress', 'Lb.InitialHealthChecking', 'Lb.InternalError',
                                                                                                                     'Instance.ResponseCodeMismatch', 'Instance.Timeout', 'Instance.FailedHealthChecks',
                                                                                                                     'Instance.NotRegistered', 'Instance.NotInUse', 'Instance.DeregistrationInProgress', 'Instance.InvalidState', 'Instance.IpUnusable'])


class TlsCertificateSummary(Model):
    name = StringType(serialize_when_none=False)
    is_attached = BooleanType(deserialize_from="isAttached", serialize_when_none=False)


class LoadBalancer(ResourceBase):
    dns_name = StringType(deserialize_from="dnsName", serialize_when_none=False)
    state = StringType(deserialize_from="state", serialize_when_none=False, choices=['active', 'provisioning',
                                                                                     'active_impaired', 'failed', 'unknown'])
    protocol = StringType(serialize_when_none=False)
    public_ports = ListType(StringType, deserialize_from="publicPorts", serialize_when_none=False)
    health_check_path = StringType(deserialize_from="healthCheckPath", serialize_when_none=False)
    instance_port = StringType(deserialize_from="instancePort", serialize_when_none=False)
    instance_health_summary = ListType(ModelType(InstanceHealthSummary), default=[], serialize_when_none=False)
    tls_certificate_summary = ListType(ModelType(TlsCertificateSummary), default=[], serialize_when_none=False)
    ip_address_type = StringType(deserialize_from="ipAddressType", serialize_when_none=False, choices=['dualstack', 'ipv4'])

    def reference(self, region_code):
        return {
            "resource_id": self.arn,
            "external_link": f"https://lightsail.aws.amazon.com/ls/webapp/{region_code}/load-balancers/{self.name}/"
        }