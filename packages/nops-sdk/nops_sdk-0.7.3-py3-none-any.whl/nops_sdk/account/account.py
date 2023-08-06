from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from nops_sdk.client import Client
from nops_sdk.cloud_infrastructure import VPC
from nops_sdk.cloud_infrastructure import SecurityGroup
from nops_sdk.cloud_infrastructure import SubNet
from nops_sdk.cloud_infrastructure._resource import Resource
from nops_sdk.cloud_infrastructure.enums import AWSProductFamily


@dataclass
class Account:
    """Designates a cloud account

    Args:
        id: the id of an account as assigned by nOps
        name: name of the account
        client: the client to which this account belongs
    """

    id: str
    name: Optional[str] = ""
    client: Optional[Client] = None

    @classmethod
    def from_raw(cls, api_response: dict) -> "Account":
        """
        Build an Account object from raw API response

        Args:
            api_response (dict)
        Returns:
            Account
        """
        return Account(
            id=api_response["id"],
            name=api_response["name"],
            client=Client(id=api_response["client"]),
        )

    def get_related_resources(self, resource_id: str) -> Resource:
        """Get related Resource of a given AWS Resource

        Args:
            resource_id: The AWS id of the resource

        Returns:
            Resource: an instance of :class:`Resource` with populated ``related_resources``
        Examples:
            >>> from nops_sdk.account import Account
            note: you'll need to provide your own account and resource ids.
            >>> account = Account(id="10963")
            >>> resource_with_relations = account.get_related_resources(resource_id="i-07f6c6d7441264685")
            >>> resource_with_relations.related_resources
            {'vpc': VPC (aws_id=vpc-f4f4288d), 'security_groups': [SecurityGroup (aws_id=sg-d02aaba2)], 'subnets': [SubNet (aws_id=subnet-8c4db8e8)]}
        """
        from nops_sdk.api._api_request import APIRequest
        from nops_sdk.api._api_request import RequestMethods

        request = APIRequest(
            endpoint="c/sdk/impact_graph/related_resources/",
            method=RequestMethods.GET,
            params={"project_id": self.id, "resource_id": resource_id},
        )
        response = request.send().json()
        ResourceClass = AWSProductFamily(response["resource_type"].lower()).resource_class
        raw_related_resources = response["related_resources"]
        related_resources = {}
        for key in response["related_resources"]:
            if key == "vpc":
                related_resources[key] = VPC(aws_id=raw_related_resources[key])
            if key == "security_groups":
                related_resources[key] = [SecurityGroup(aws_id=sg_id) for sg_id in raw_related_resources[key]]
            if key == "subnets":
                related_resources[key] = [SubNet(aws_id=sn_id) for sn_id in raw_related_resources[key]]
        return ResourceClass(aws_id=response["response_id"], related_resources=related_resources)
