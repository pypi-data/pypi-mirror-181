from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from decimal import Decimal
from typing import Any
from typing import Optional

from nops_sdk.cloud_infrastructure._resource import Resource
from nops_sdk.cloud_infrastructure.enums import AWSRegion


@dataclass
class EKSNodeGroup(Resource):
    """
    Designates an AWS EKS Node Group

    Args:
        name: name of the EKS Node group
        cluster_name: name of the associated EKS cluster
        min_size: minimum number of instances required in the node
        max_size: maximum number of instances required in the node
        desired_size: target number of instances required in the node
        instances_types: type of instances (e.g. m6i.large)
    """

    name: str = ""
    cluster_name: str = ""
    min_size: int = 0
    max_size: int = 0
    desired_size: int = 0
    instance_types: list[str] = field(default_factory=list)
    _price_per_unit: Optional[Decimal] = None

    def __str__(self):
        return f"AWS EKS NodeGroup cluster {self.name} on cluster {self.cluster_name}"

    @property
    def price_per_unit(self):
        """
        Price_per_unit is understood as the price of this node group assuming
        a desired number of instances are running."""
        return self._price_per_instance * self.desired_size

    @property
    def min_price(self):
        return self._price_per_instance * self.min_size

    @property
    def max_price(self):
        return self._price_per_instance * self.max_price

    @price_per_unit.setter
    def price_per_unit(self, value: Decimal):
        self._price_per_instance = value

    @classmethod
    def from_raw_input(cls, spec_item: dict[str, Any]) -> "EKSNodeGroup":
        """Build a class instance from raw input.

        Args:
            spec_item
        Returns:
            an instance of EKSNodeGroup
        """
        return cls(
            name=spec_item["node_group_name"],
            cluster_name=spec_item["cluster_name"],
            min_size=spec_item["scaling_config"][0]["min_size"],
            max_size=spec_item["scaling_config"][0]["max_size"],
            desired_size=spec_item["scaling_config"][0]["desired_size"],
            instance_types=spec_item["instance_types"],
        )

    def to_db_query(self, region: AWSRegion) -> dict[str, str]:
        # Node groups are thought of as a bunch of EC2 Instances
        return {
            "region_code": region.value,
            "service_code": "AmazonEC2",
            "instance_type": self.instance_types[0],
            "unit": "Hrs",
            "termtype": "OnDemand",
            "capacitystatus": "Used",
            "tenancy": "Shared",
            "operation": "RunInstances",
        }


@dataclass
class EKSCluster(Resource):
    """
    Designates an AWS EKS cluster

    Args:
        name: name of the AWS EKS cluster
        price_per_unit: price of the resource for the specified unit

    price_per_unit: Optional[Decimal] = Decimal("0")
    """

    name: str = ""

    def __str__(self):
        return f"AWS EKS cluster {self.name}"

    @classmethod
    def from_raw_input(cls, spec_item: dict[str, Any]) -> "EKSCluster":
        """Build a class instance from raw input.

        Args:
            spec_item
        Returns:
            eks_cluster
        """
        return cls(name=spec_item["name"])

    def to_db_query(self, region: AWSRegion) -> dict[str, Any]:
        return {
            "region_code": region.value,
            "operation": "CreateOperation",
            "service_code": "AmazonEKS",
        }
