import logging

from schematics import Model
from schematics.types import ModelType, StringType, IntType, DateTimeType, serializable, ListType, BooleanType

_LOGGER = logging.getLogger(__name__)


'''
RECORD SET
'''
class GeoLocation(Model):
    continent_code = StringType(deserialize_from="ContinentCode")
    country_code = StringType(deserialize_from="CountryCode")
    subdivision_code = StringType(deserialize_from="SubdivisionCode")


class AliasTarget(Model):
    hosted_zone_id = StringType(deserialize_from="HostedZoneId")
    dns_name = StringType(deserialize_from="DNSName")
    evaluate_target_health = BooleanType(deserialize_from="EvaluateTargetHealth")


class RecordSetResourceRecords(Model):
    value = StringType(deserialize_from="Value")


class RecordSet(Model):
    name = StringType(deserialize_from="Name")
    type = StringType(deserialize_from="Type", choices=("SOA", "A", "TXT", "NS", "CNAME", "MX", "NAPTR", "PTR", "SRV",
                                                        "SPF", "AAAA", "CAA"))
    set_identifier = StringType(deserialize_from="SetIdentifier")
    weight = IntType(deserialize_from="Weight")
    region = StringType(deserialize_from="Region", choices=("us-east-1", "us-east-2", "us-west-1", "us-west-2",
                                                            "ca-central-1", "eu-west-1", "eu-west-2", "eu-west-3",
                                                            "eu-central-1", "ap-southeast-1", "ap-southeast-2",
                                                            "ap-northeast-1", "ap-northeast-2", "ap-northeast-3",
                                                            "eu-north-1", "sa-east-1", "cn-north-1", "cn-northwest-1",
                                                            "ap-east-1", "me-south-1", "ap-south-1"))
    geo_location = ModelType(GeoLocation, deserialize_from="GeoLocation")
    failover = StringType(deserialize_from="Failover", choices=("PRIMARY", "SECONDARY"))
    multi_value_answer = BooleanType(deserialize_from="MultiValueAnswer")
    ttl = IntType(deserialize_from="TTL")
    resource_records = ListType(ModelType(RecordSetResourceRecords), deserialize_from="ResourceRecords")
    alias_target = ModelType(AliasTarget, deserialize_from="AliasTarget")
    health_check_id = StringType(deserialize_from="HealthCheckId")
    display_values = ListType(StringType)
    traffic_policy_instance_id = StringType(deserialize_from="TrafficPolicyInstanceId")


'''
HOSTED ZONE
'''
class Config(Model):
    comment = StringType(deserialize_from="Comment")
    private_zone = BooleanType(deserialize_from="PrivateZone")


class LinkedService(Model):
    service_principal = StringType(deserialize_from="ServicePrincipal")
    description = StringType(deserialize_from="Description")


class HostedZone(Model):
    arn = StringType()
    id = StringType(deserialize_from="Id")
    hosted_zone_id = StringType()
    name = StringType(deserialize_from="Name")
    caller_reference = StringType(deserialize_from="CallerReference")
    config = ModelType(Config,deserialize_from="Config")
    resource_record_set_count = IntType(deserialize_from="ResourceRecordSetCount")
    linked_service = ModelType(LinkedService,deserialize_from="LinkedService")
    type = StringType(default="")
    record_sets = ListType(ModelType(RecordSet))
    account_id = StringType(default="")

    @serializable
    def reference(self):
        return {
            "resource_id": self.arn,
            "external_link": f"https://console.aws.amazon.com/route53/home#resource-record-sets:{self.hosted_zone_id}"
        }
