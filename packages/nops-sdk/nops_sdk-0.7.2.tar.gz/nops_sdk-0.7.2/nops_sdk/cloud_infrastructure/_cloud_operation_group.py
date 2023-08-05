from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from decimal import Decimal
from functools import cached_property

from botocore.exceptions import BotoCoreError
from botocore.exceptions import ClientError

from nops_sdk.api._api_request import APIRequest
from nops_sdk.api._api_request import RequestMethods
from nops_sdk.api._boto_session import get_boto_session
from nops_sdk.cloud_infrastructure import CloudOperation
from nops_sdk.cloud_infrastructure import Instance
from nops_sdk.cloud_infrastructure._resource import Resource
from nops_sdk.cloud_infrastructure.enums import AWSRegion

logger = logging.getLogger(__name__)


@dataclass
class CloudOperationGroup:
    """A container used to encapsulate gnarly details of making and parsing nOps
    API requests/responses for a group of Cloud Operations. The goal it accomplishes
    is to cut down external request numbers.

    Args:
        operations: a list of :class:`CloudOperations`
    """

    operations: list[CloudOperation]

    def populate_ami_usage_operation(self, region: AWSRegion):
        """Get AMI image descriptions from AWS and populate :py:attr:`instance.ami.usage_operation` fields.
        This is needed for determining the OS of the server and thus its price."""
        image_ids = list({instance.ami.aws_id for instance in self._instances if instance.ami})
        images = self._get_ami_specs_from_aws(image_ids, region)
        for image in images:
            for instance in self._instances:
                if instance.ami and instance.ami.aws_id == image["ImageId"]:
                    instance.ami.usage_operation = image["UsageOperation"]

    def api_request(self, aws_region: AWSRegion):
        """Export this :class:`CloudOperationGroup` to an instance of :class:`APIRequest` with relevant query params.

        Args:
            aws_region
        Returns:
            APIRequest
        """
        query = {id: resource.to_db_query(aws_region) for id, resource in self._resources_map.items()}
        params = {"query": json.dumps(query)}
        return APIRequest(method=RequestMethods.GET, endpoint="/c/aws_pricing_search/", params=params)

    def populate_cost_from_api_response(self, api_response: dict[str, str]):
        for id, resource in self._resources_map.items():
            if id in api_response:
                resource.unit_of_price = api_response[id]["unit"]
                resource.price_per_unit = Decimal(str(api_response[id]["priceperunit"]))

    def _get_ami_specs_from_aws(self, image_ids: list[str], region: AWSRegion) -> list:
        session = get_boto_session()
        client = session.client("ec2", region_name=region.value)
        try:
            images = client.describe_images(ImageIds=image_ids)["Images"]
            return images or []
        except (BotoCoreError, ClientError):
            logger.error("Failed to retrieve AMI images specs", exc_info=True)
            return []

    @cached_property
    def _resources_map(self) -> dict[str, Resource]:
        """Produce a `{domain_id: Resource}` of all resources of this groups' operations.

        Returns:
            resources_map: a dict containing all the resources of this operation group.
        """
        resources_map = {}
        for op in self.operations:
            resources_map.update(op.resources())
        return resources_map

    @cached_property
    def _instances(self) -> list[Instance]:
        """Produce a list of all Instances of this groups' operations.

        Returns:
            list[Instance]
        """
        return [
            instance
            for operation in self.operations
            for instance in operation.resources().values()
            if isinstance(instance, Instance)
        ]
