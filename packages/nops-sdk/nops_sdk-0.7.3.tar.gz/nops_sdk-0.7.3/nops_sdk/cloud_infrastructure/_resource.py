from __future__ import annotations

import uuid
from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Optional

from nops_sdk.cloud_infrastructure import enums


@dataclass
class Resource(ABC):
    """
    A Base class designating an cloud resource, for example, an AWS EC2 instance.
    """

    aws_id: Optional[str] = ""
    domain_id: str = field(init=False)

    def __post_init__(self):
        # an SDK specific default ID used in cases where we don't have actual
        # AWS ID but still need some ref key
        self.domain_id = str(uuid.uuid4())

    @classmethod
    def from_raw_input(cls) -> "Resource":
        """Build Resource from raw input"""
        raise NotImplementedError

    @classmethod
    def to_db_query(cls, aws_region: enums.AWSRegion) -> dict[str, Any]:
        """Export parameters in the format of a Db query"""
        raise NotImplementedError
