from dataclasses import dataclass

from nops_sdk.cloud_infrastructure._resource import Resource


@dataclass
class SecurityGroup(Resource):
    """Designates an AWS SecurityGroup."""

    def __repr__(self) -> str:
        return f"SecurityGroup (aws_id={self.aws_id})"
