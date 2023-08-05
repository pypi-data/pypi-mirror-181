from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Optional


@dataclass
class Ami:
    "Represents an AWS AMI"
    aws_id: str
    usage_operation: Optional[str] = field(default_factory=str)
