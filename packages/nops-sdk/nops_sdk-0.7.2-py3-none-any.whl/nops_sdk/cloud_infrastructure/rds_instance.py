from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from decimal import Decimal
from typing import Any
from typing import Literal
from typing import Optional

from nops_sdk.cloud_infrastructure import AWSRegion
from nops_sdk.cloud_infrastructure._resource import Resource

UsageOperationLookup = {
    # look up key is made of engine + license type
    "mysql": "CreateDBInstance:0002",  # MySQL
    "oracle-se1 + byol": "CreateDBInstance:0003",  # Oracle SE1 (BYOL)
    "oracle-se + byol": "CreateDBInstance:0004",  # Oracle SE (BYOL)
    "oracle-ee + byol": "CreateDBInstance:0005",  # Oracle EE (BYOL)
    "oracle-se1 + aws": "CreateDBInstance:0006",  # Oracle SE1 (LI)
    "sqlserver-se + byol": "CreateDBInstance:0008",  # SQL Server SE (BYOL)
    "sqlserver-ee + byol": "CreateDBInstance:0009",  # SQL Server EE (BYOL)
    "sqlserver-ex + aws": "CreateDBInstance:0010",  # SQL Server Exp (LI)
    "sqlserver-web + aws": "CreateDBInstance:0011",  # SQL Server Web (LI)
    "sqlserver-se + aws": "CreateDBInstance:0012",  # SQL Server SE (LI)
    "postgresql": "CreateDBInstance:0014",  # PostgreSQL
    "sqlserver-ee + aws": "CreateDBInstance:0015",  # SQL Server EE (LI)
    "aurora": "CreateDBInstance:0016",  # Aurora MySQL
    "mariadb": "CreateDBInstance:0018",  # MariaDB
    "oracle-se2 + byol": "CreateDBInstance:0019",  # Oracle SE2 (BYOL)
    "oracle-se2 + aws": "CreateDBInstance:0020",  # Oracle SE2 (LI)
    "aurora-postgresql": "CreateDBInstance:0021",  # Aurora PostgreSQL
    "neptune": "CreateDBInstance:0022",  # Neptune
}

License = Literal["general-public-license", "bring-your-own-license", "amazon-license"]


@dataclass
class RDSInstance(Resource):
    """
    Designates an AWS RDS instance

    Args:
        instance_class: an identifier of resource instance (e.g. db.t2.micro)
        unit_of_price: the unit of measurement for price (e.g. Hr in $1/Hr)
        price_per_unit: price of the resource for the specified unit
    """

    instance_class: Optional[str] = ""
    engine: Optional[str] = ""
    multi_az: Optional[bool] = False
    license: Optional[License] = "general-public-license"
    unit_of_price: Optional[str] = ""
    price_per_unit: Optional[Decimal] = Decimal("0")
    usage_operation: Optional[str] = ""
    related_resources: Optional[dict[str, Resource]] = field(default_factory=lambda: {})

    def __str__(self) -> str:
        return f"{self.instance_class} RDS instance"

    @property
    def multi_az_str(self):
        return "Multi-AZ" if self.multi_az else "Single-AZ"

    @classmethod
    def from_raw_input(cls, spec_item: dict[str, Any]) -> "RDSInstance":
        """Build a class instance from raw input.

        Args:
            spec_item
        Returns:
            rds_instance
        """
        rds_instance = cls(
            instance_class=spec_item["instance_class"],
            engine=spec_item["engine"],
            multi_az=spec_item.get("multi_az", False),
            license=spec_item.get("license_model", ""),
        )
        short_license = {"general-public-license": "", "bring-your-own-license": "byol", "amazon-license": "aws"}.get(
            rds_instance.license, ""
        )
        lookup_key = rds_instance.engine
        if short_license:
            lookup_key = f"{rds_instance.engine} + {short_license}"
        rds_instance.usage_operation = UsageOperationLookup[lookup_key]
        return rds_instance

    def to_db_query(self, region: AWSRegion) -> dict[str, Any]:
        return {
            "region_code": region.value,
            "service_code": "AmazonRDS",
            "operation": self.usage_operation,
            "instance_type": self.instance_class,
            "termtype": "OnDemand",  # a reasonable assumption
            "deployment_option": self.multi_az_str,
            "unit": "Hrs",
        }
