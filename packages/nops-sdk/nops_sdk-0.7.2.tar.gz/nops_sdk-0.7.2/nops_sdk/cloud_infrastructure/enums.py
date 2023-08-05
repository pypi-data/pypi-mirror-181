from __future__ import annotations

from decimal import Decimal
from enum import Enum
from enum import EnumMeta
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nops_sdk.cloud_infrastructure import Resource


class _MetaEnum(EnumMeta):
    """Enables '...in Enum' style lookups."""

    def __contains__(cls, obj) -> bool:
        try:
            cls(obj)
        except ValueError:
            return False
        return True


class Periodicity(str, Enum):
    """Options for cost effect estimation period."""

    HOURLY = "hourly"
    DAILY = "daily"
    MONTHLY = "monthly"
    YEARLY = "yearly"

    @property
    def hourly_multiplicator(self) -> Decimal:
        return {
            Periodicity.HOURLY: Decimal("1"),
            Periodicity.DAILY: Decimal("24"),
            Periodicity.MONTHLY: Decimal(24 * 30),
            Periodicity.YEARLY: Decimal(24 * 365),
        }[self]


class CloudOperationType(str, Enum):
    """Types of Cloud operations"""

    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class AWSRegion(str, Enum):
    """AWS regions"""

    US_EAST_1 = "us-east-1"
    US_EAST_2 = "us-east-2"
    US_WEST_1 = "us-west-1"
    US_WEST_2 = "us-west-2"
    AF_SOUTH_1 = "af-south-1"
    AP_EAST_1 = "ap-east-1"
    AP_SOUTH_1 = "ap-south-1"
    AP_SOUTHEAST_1 = "ap-southeast-1"
    AP_SOUTHEAST_2 = "ap-southeast-2"
    AP_SOUTHEAST_3 = "ap-southeast-3"
    AP_NORTHEAST_1 = "ap-northeast-1"
    AP_NORTHEAST_2 = "ap-northeast-2"
    AP_NORTHEAST_3 = "ap-northeast-3"
    EU_WEST_1 = "eu-west-1"
    EU_WEST_2 = "eu-west-2"
    EU_WEST_3 = "eu-west-3"
    EU_SOUTH_1 = "eu-south-1"
    EU_NORTH_1 = "eu-north-1"
    EU_CENTRAL_1 = "eu-central-1"
    ME_SOUTH_1 = "me-south-1"
    SA_EAST_1 = "sa-east-1"
    CA_CENTRAL_1 = "ca-central-1"


class AWSProductFamily(str, Enum, metaclass=_MetaEnum):
    """Supported AWS producted families"""

    EC2 = "ec2"
    RDS = "rds"
    EKS = "aws_eks_cluster"
    EKS_NODE_GROUP = "aws_eks_node_group"

    @property
    def resource_class(self) -> Resource:
        from nops_sdk.cloud_infrastructure import EKSCluster
        from nops_sdk.cloud_infrastructure import EKSNodeGroup
        from nops_sdk.cloud_infrastructure import Instance
        from nops_sdk.cloud_infrastructure import RDSInstance

        return {
            AWSProductFamily.EC2: Instance,
            AWSProductFamily.RDS: RDSInstance,
            AWSProductFamily.EKS: EKSCluster,
            AWSProductFamily.EKS_NODE_GROUP: EKSNodeGroup,
        }[self]
