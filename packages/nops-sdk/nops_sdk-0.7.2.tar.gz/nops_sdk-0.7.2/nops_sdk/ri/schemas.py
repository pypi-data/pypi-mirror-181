"""This module contains schemas - dataclasses that deserialize raw API 
responses and usually correspond to 1 nOps API endpoint - for the Reserved Instances module."""
from __future__ import annotations

from dataclasses import dataclass
from dataclasses import fields
from decimal import Decimal
from typing import Optional

from nops_sdk.ri.query import RIQueryParams


@dataclass
class _BaseSchema:
    """A base schema dataclass mixin."""

    @classmethod
    def from_raw(cls, api_response: dict):
        """Build an instance of this class from api response. Requires that the field names of the class
        and keys in the api_response correspond.

        Args:
            api_response: api response
        """
        return cls(**{f: api_response[f] for f in [f.name for f in fields(cls)]})


@dataclass
class RIDetailSchema(_BaseSchema):
    instance_type: str
    account: str
    offering_class: str
    platform: str
    terms: str
    expiration_date: str


@dataclass
class EC2DetailSchema(_BaseSchema):
    size_count: int
    account: list[str]
    instance_size: str


@dataclass
class RIOverviewSchema(_BaseSchema):
    instance_region: str
    instance_family: str
    instance_platform: str
    instance_tenancy: str
    coverage: float
    unused_units: float
    accounts: Optional[set[str]]
    reserved_units: Optional[Decimal]
    running_units: Optional[Decimal]

    @property
    def query_params(self) -> RIQueryParams:
        """Query params corresponding to this overview item."""
        return RIQueryParams(
            region=self.instance_region,
            family=self.instance_family,
            tenancy=self.instance_tenancy,
            platform=self.instance_platform,
        )
