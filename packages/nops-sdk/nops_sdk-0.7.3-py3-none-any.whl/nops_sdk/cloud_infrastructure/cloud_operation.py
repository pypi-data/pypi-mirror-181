from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from decimal import Decimal
from typing import Optional

from nops_sdk.cloud_infrastructure._resource import Resource
from nops_sdk.cloud_infrastructure.enums import AWSProductFamily
from nops_sdk.cloud_infrastructure.enums import CloudOperationType
from nops_sdk.cloud_infrastructure.enums import Periodicity


@dataclass
class CloudOperation:
    """An operation in AWS (such as create EC2 with Terraform)

    Args:
        type: an instance of CloudOperationType specifying the action taken
        created_resource: the AWS resource which is created with this operation
        deleted_resource: the AWS resource which is deleted with this operation
        _cost_effect: cost effect of the action on the AWS bill
        _report: a formatted report of the cost effect of this operation
    """

    type: CloudOperationType
    created_resource: Optional[Resource] = None
    deleted_resource: Optional[Resource] = None
    _cost_effect: Decimal = field(default=Decimal("0"), init=False)
    _report: str = field(default="", init=False)

    @classmethod
    def from_raw_input(cls, spec_item: dict[str, str]):
        """Build a CloudOperation from raw user input (e.g. terraform changeset input)."""
        operation = cls(type=CloudOperationType(spec_item["operation_type"]))
        ResourceClass = AWSProductFamily(spec_item["resource_type"]).resource_class

        if old_data := spec_item.get("old_data"):
            operation.deleted_resource = ResourceClass.from_raw_input(old_data)
        if new_data := spec_item.get("new_data"):
            operation.created_resource = ResourceClass.from_raw_input(new_data)
        return operation

    def resources(self) -> dict:
        """Produce a `{domain_id: Resource}` dict of this operation's resources."""
        resources = {}
        if self.created_resource:
            resources[self.created_resource.domain_id] = self.created_resource
        if self.deleted_resource:
            resources[self.deleted_resource.domain_id] = self.deleted_resource
        return resources

    @property
    def cost_effect(self):
        return self._cost_effect

    @property
    def report(self):
        return self._report

    def compute_cost_effect(self, period: Periodicity) -> Decimal:
        """Compute the price effect of the operation for the provided period.

        Args:
            period: length of the period
        Returns:
            cost_change: the cost effect of the operation in the given period
        Raises:
            PricingException
        """
        cost_effect = Decimal("0")
        if self.created_resource and self.created_resource.unit_of_price == "Hrs":
            cost_effect += self.created_resource.price_per_unit * period.hourly_multiplicator
        if self.deleted_resource and self.deleted_resource.unit_of_price == "Hrs":
            cost_effect -= self.deleted_resource.price_per_unit * period.hourly_multiplicator
        self._cost_effect = cost_effect
        self._set_report(period)
        return cost_effect

    def _set_report(self, period: Periodicity):
        """A human readable report of the cost impact of this operation"""
        if self.type == CloudOperationType.CREATE:
            base_report = f"Create {self.created_resource}"
        elif self.type == CloudOperationType.DELETE:
            base_report = f"Delete {self.deleted_resource}"
        elif self.type == CloudOperationType.UPDATE:
            base_report = f"Update {self.deleted_resource} to {self.created_resource}"
        self._report = " ".join([base_report, f"with a {period.value} cost impact of {self.cost_effect:.2f}"])
