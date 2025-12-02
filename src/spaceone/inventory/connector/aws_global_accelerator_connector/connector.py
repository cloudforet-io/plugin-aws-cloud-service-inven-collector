import logging

from spaceone.core.utils import *
from spaceone.inventory.connector.aws_global_accelerator_connector.schema.service_type import CLOUD_SERVICE_TYPES
from spaceone.inventory.connector.aws_global_accelerator_connector.schema.data import (
    Accelerator,
    EndpointGroup,
    Listener,
    CrossAccountAttachments,
)
from spaceone.inventory.connector.aws_global_accelerator_connector.schema.resource import (
    AcceleratorResource,
    AcceleratorResponse,
    CrossAccountAttachmentsResource,
    CrossAccountAttachmentsResponse,
)
from spaceone.inventory.libs.connector import SchematicAWSConnector
from spaceone.inventory.libs.schema.resource import ReferenceModel

_LOGGER = logging.getLogger(__name__)


class GlobalAcceleratorConnector(SchematicAWSConnector):
    service_name = "globalaccelerator"
    cloud_service_group = "GlobalAccelerator"
    cloud_service_type = "Accelerator"
    cloud_service_types = CLOUD_SERVICE_TYPES
    @property
    def client(self):
        return self.session.client("globalaccelerator", region_name="us-west-2")

    def get_resources(self):
        _LOGGER.debug(f"[get_resources][account_id: {self.account_id}] START: Global Accelerator")
        resources = []
        start_time = time.time()

        resources.extend(self.set_cloud_service_types())

        try:
            accelerators = list(self.request_accelerator_data())
            attachments, attachments_error = self.request_attachments_data()

            for acc in accelerators:
                if getattr(acc, "resource_type",None) and acc.resource_type == "inventory.ErrorResource":
                    resources.append(acc)
                else:
                    resources.append(
                        AcceleratorResponse({
                            "resource": AcceleratorResource({
                                "name": acc.name,
                                "data": acc,
                                "account": self.account_id,
                                "tags": self.list_tags_for_resource(acc.arn),
                                "region_code": "global",
                                "reference" : ReferenceModel(acc.reference())
                            })
                        })
                    )

            for att in attachments:
                if getattr(att, "resource_type", None) == "inventory.ErrorResource":
                    resources.append(att)
                else:
                    resources.append(
                        CrossAccountAttachmentsResponse({
                            "resource": CrossAccountAttachmentsResource({
                                "name": att.name,
                                "data": att,
                                "account": self.account_id,
                                "tags" : self.list_tags_for_resource(att.arn),
                                "region_code": "global",
                                "reference" : ReferenceModel(att.reference())
                            })
                        })
                    )
            resources.extend(attachments_error)

        except Exception as e:
            resources.append(self.generate_error("global", "", e))

        _LOGGER.debug(
            f"[get_resources][account_id: {self.account_id}] FINISHED: Global Accelerator ({time.time() - start_time} sec)"
        )
        return resources


    def request_accelerator_data(self):
        cloudtrail_type = "AWS::GlobalAccelerator::Accelerator"
        # Standard
        paginator = self.client.get_paginator("list_accelerators")
        standard_data = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 50,
            }
        )
        for page in standard_data:
            for raw in page.get("Accelerators", []):
                raw["type"] = "Standard"
                vo = self._process_accelerator(raw)
                yield vo

        # Customised routing
        paginator = self.client.get_paginator("list_custom_routing_accelerators")
        custom_data = paginator.paginate(
            PaginationConfig={
                "MaxItems": 10000,
                "PageSize": 50,
            }
        )
        for page in custom_data:
            for raw in page.get("Accelerators", []):
                raw["type"] = "Customised routing"
                vo = self._process_accelerator(raw)
                yield vo

    def _process_accelerator(self, raw):
        arn = raw.get("AcceleratorArn")
        try:
            if raw["type"] == "Standard":
                listeners, endpoints, errors = self.list_listeners(arn)
            else:
                listeners, endpoints, errors = self.list_custom_routing_listeners(arn)

            raw.update({"listeners": listeners, "endpoints": endpoints})
            raw = self._extract_ip_addresses(raw)
            raw["enabled"] = "True" if raw.get("Enabled") else "False"
            vo = Accelerator(raw, strict=False)
            return vo

        except Exception as e:
            return self.generate_error("global", arn, e)

    def request_attachments_data(self):
        paginator = self.client.get_paginator("list_cross_account_attachments")

        results = []
        error = []
        for page in paginator.paginate():
            for raw in page.get("CrossAccountAttachments", []):
                arn = raw.get("AttachmentArn")
                try:
                    vo = CrossAccountAttachments(raw, strict=False)
                    results.append(vo)
                except Exception as e:
                    error.append(self.generate_error("global", arn, e))
        return results, error

    def list_listeners(self, arn):
        resp = self.client.list_listeners(AcceleratorArn=arn)
        listener_obj, listeners, endpoints, errors = [], [], [], []
        for data in resp.get("Listeners", []):
            l_arn = data.get("ListenerArn")
            try:
                listener_obj = Listener(data, strict=False)
            except Exception as e:
                errors.append(self.generate_error("global", l_arn, e))

            ep_list, ep_err = self.list_endpoints(l_arn)
            endpoints.extend(ep_list)
            errors.extend(ep_err)

            # endpoint region
            listener_obj.endpoint_region = [ep.region for ep in ep_list]
            # port + protocol
            listener_obj.port_display = self._get_port_display(listener_obj)
            listeners.append(listener_obj)

        return listeners, endpoints, errors

    def list_custom_routing_listeners(self, arn):
        resp = self.client.list_custom_routing_listeners(AcceleratorArn=arn)
        listener_obj, listeners, endpoints, errors = [], [], [], []

        for data in resp.get("Listeners", []):
            l_arn = data.get("ListenerArn")
            try:
                listener_obj = Listener(data, strict=False)
            except Exception as e:
                errors.append(self.generate_error("global", l_arn, e))

            ep_list, ep_err = self.list_custom_routing_endpoint_groups(l_arn)
            endpoints.extend(ep_list)
            errors.extend(ep_err)

            # endpoint region
            listener_obj.endpoint_region = [ep.region for ep in ep_list]

            # port + protocol
            listener_obj.port_display = self._get_port_display(listener_obj)
            listeners.append(listener_obj)

        return listeners, endpoints, errors

    def list_endpoints(self, l_arn):
        resp = self.client.list_endpoint_groups(ListenerArn=l_arn)
        endpoints, errors = [], []

        for d in resp.get("EndpointGroups", []):
            try:
                endpoints.append(EndpointGroup(d, strict=False))
            except Exception as e:
                errors.append(self.generate_error("global", d.get("EndpointGroupArn"), e))

        return endpoints, errors

    def list_custom_routing_endpoint_groups(self, l_arn):
        resp = self.client.list_custom_routing_endpoint_groups(ListenerArn=l_arn)
        endpoints, errors = [], []

        for d in resp.get("EndpointGroups", []):
            try:
                endpoints.append(EndpointGroup(d, strict=False))
            except Exception as e:
                errors.append(self.generate_error("global", d.get("EndpointGroupArn"), e))

        return endpoints, errors

    def list_tags_for_resource(self, arn):
        response = self.client.list_tags_for_resource(ResourceArn=arn)
        return self.convert_tags_to_dict_type(response.get("Tags", []))

    @staticmethod
    def _get_port_display(listener_obj):
        proto = (listener_obj.protocol or "").upper()
        port_display = []

        for pr in listener_obj.port_ranges:
            if pr.from_port == pr.to_port:
                base = f"{pr.from_port}"
            else:
                base = f"{pr.from_port}-{pr.to_port}"

            if proto:
                base = f"{base} {proto}"

            port_display.append(base)

        return port_display

    @staticmethod
    def _extract_ip_addresses(raw):
        ipv4 = []
        ipv6 = []

        for ipset in raw.get("IpSets", []):
            family = ipset.get("IpAddressFamily")
            address = ipset.get("IpAddresses", [])

            if family == "IPv4":
                ipv4.extend(address)
            elif family == "IPv6":
                ipv6.extend(address)

        raw["IPv4Addresses"] = ipv4
        raw["IPv6Addresses"] = ipv6

        return raw