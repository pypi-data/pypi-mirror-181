from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from decimal import Decimal
from typing import Optional

from nops_sdk.cloud_infrastructure import Ami
from nops_sdk.cloud_infrastructure._resource import Resource
from nops_sdk.cloud_infrastructure.enums import AWSRegion


@dataclass
class Instance(Resource):
    """
    Designates an AWS EC2 instance

    Args:
        instance_type: an identifier of resource instance (e.g. t2.micro)
        unit_of_price: the unit of measurement for price (e.g. Hr in $1/Hr)
        price_per_unit: price of the resource for the specified unit
        ami: the AWS AMI associated with this image
    """

    instance_type: Optional[str] = ""
    unit_of_price: Optional[str] = field(default_factory=str)
    price_per_unit: Optional[Decimal] = field(default_factory=Decimal)
    ami: Optional[Ami] = None
    related_resources: Optional[dict[str, Resource]] = field(default_factory=lambda: {})

    def __str__(self) -> str:
        return f"{self.instance_type} EC2 instance"

    @classmethod
    def from_raw_input(cls, spec_item: dict[str, str]) -> "Instance":
        """Build a class instance from raw input.

        Args:
            spec_item
        Returns:
            instance
        """
        instance = Instance(instance_type=spec_item["instance_type"])
        if "ami" in spec_item:
            instance.ami = Ami(aws_id=spec_item["ami"])
        return instance

    def to_db_query(self, region: AWSRegion) -> dict[str, str]:
        query = {
            "region_code": region.value,
            "service_code": "AmazonEC2",
            "instance_type": self.instance_type,
            "unit": "Hrs",
            "termtype": "OnDemand",
            "capacitystatus": "Used",
            "tenancy": "Shared",
        }
        if self.ami and self.ami.usage_operation:
            query["operation"] = self.ami.usage_operation
        else:
            query["operation"] = "RunInstances"
        return query
