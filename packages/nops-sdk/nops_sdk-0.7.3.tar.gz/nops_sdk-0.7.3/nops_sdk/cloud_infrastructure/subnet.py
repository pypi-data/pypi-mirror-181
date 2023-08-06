from dataclasses import dataclass

from nops_sdk.cloud_infrastructure._resource import Resource


@dataclass
class SubNet(Resource):
    """Designates an AWS SubNet."""

    def __repr__(self) -> str:
        return f"SubNet (aws_id={self.aws_id})"
