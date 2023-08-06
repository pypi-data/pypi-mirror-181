from dataclasses import dataclass

from nops_sdk.cloud_infrastructure._resource import Resource


@dataclass
class VPC(Resource):
    """Designates an AWS VPC."""

    def __repr__(self) -> str:
        return f"VPC (aws_id={self.aws_id})"
