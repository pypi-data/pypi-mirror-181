from __future__ import annotations

from logging import getLogger
from typing import Optional
from typing import Union

from nops_sdk.cloud_infrastructure._cloud_operation_group import CloudOperationGroup
from nops_sdk.cloud_infrastructure.cloud_operation import CloudOperation
from nops_sdk.cloud_infrastructure.cloud_operation import Periodicity
from nops_sdk.cloud_infrastructure.enums import AWSProductFamily
from nops_sdk.cloud_infrastructure.enums import AWSRegion

logger = getLogger(__name__)


class CloudCost:
    """Compute AWS Infrastructure cost change from changes to Infrastructure as Code files!

    Currently only Terraform is supported.
    Supported AWS resources are specified in :class:`cloud_infrastructure.enums.AWSProductFamily`

    Args:
        aws_region: The AWS region where resources are.
        spec: a list of operations
    Examples:
        >>> from nops_sdk.pricing import CloudCost
        >>> from nops_sdk.cloud_infrastructure.enums import AWSRegion
        >>> from nops_sdk.cloud_infrastructure.cloud_operation import Periodicity
        >>> spec = [
                {
                    "new_data": {"instance_type": "t2.micro"},
                    "old_data": None,
                    "operation_type": "create",
                    "resource_type": "ec2",
                    "ami": "ami-0269f532"
                },
                {
                    "new_data": None,
                    "old_data": {
                        "instance_class": "db.t2.micro",
                        "engine": "oracle-ee",
                        "license_model": "bring-your-own-license",
                        "multi_az": True
                    },
                    "operation_type": "delete",
                    "resource_type": "rds",
                },
                {
                    "new_data": {"instance_type": "t2.nano", "ami": "ami-00bb6f60"},
                    "old_data": {"instance_type": "t2.micro", "ami": "ami-0269f532"},
                    "operation_type": "update",
                    "resource_type": "ec2"
                },
                {
                    'id': None,
                    'resource_type': 'aws_eks_cluster',
                    'operation_type': 'create',
                    'old_data': None,
                    'new_data': {
                        'name': 'devopsthehardway-cluster',
                    }
                },
                {
                    'id': None,
                    'resource_type': 'aws_eks_node_group',
                    'operation_type': 'create',
                    'old_data': None,
                    'new_data': {
                        'cluster_name': 'devopsthehardway-cluster',
                        'instance_types': ['t3.xlarge'],
                        'node_group_name': 'devopsthehardway-workernodes',
                        'scaling_config': [
                            {
                            'desired_size': 1,
                            'max_size': 1,
                            'min_size': 1
                            }
                        ],
                    }
                }
            ]
        >>> cloud_cost = CloudCost(aws_region=AWSRegion('us-west-2'), spec=spec)
        >>> cloud_cost.load_prices()
        After you load the prices, you can compute and output prices for any supported `Peridocity` at no significant cost.
        >>> cloud_cost.compute_cost_effects(period=Periodicity('monthly'))
        >>> cloud_cost.output_report()
        Create t2.micro EC2 instance with a monthly cost impact of 8.35
        Delete db.t2.micro RDS instance with a monthly cost impact of -9.79
        Update t2.micro EC2 instance to t2.nano EC2 instance with a monthly cost impact of -4.18
        Create AWS EKS cluster devopsthehardway-cluster with a monthly cost impact of 72.00
        Create AWS EKS NodeGroup cluster devopsthehardway-workernodes on cluster devopsthehardway-cluster with a monthly cost impact of 119.81
    """

    def __init__(self, aws_region: Union[str, AWSRegion], spec: list[dict[str, str]]) -> None:
        if isinstance(aws_region, str):
            aws_region = AWSRegion(aws_region)
        self.aws_region = aws_region
        self.spec = spec
        self.operation_group: Optional[CloudOperationGroup] = None

    def load_prices(self):
        """Load price data from AWS and nOps API and populate cost fields in Resources."""
        # parse raw input into an `CloudOperationGroup` object.
        self.operation_group = self._parse_to_cloudoperation_group()
        # Get and populate cost related fields of the `Resource` instances in operations involved.
        self._populate_cost_fields()

    def compute_cost_effects(self, period: Periodicity = Periodicity.MONTHLY):
        """Given a period, compute the cost effect. Makes sense only after prices have been
        loaded via :py:attr:`CloudCost.load_prices`.

        Args:
            period: defaults to monthly
        Returns:
            None
        """
        for op in self.operation_group.operations:
            op.compute_cost_effect(Periodicity(period))

    def output_report(self):
        """Print out the reports of the operations."""
        for op in self.operation_group.operations:
            print(op.report)

    def _parse_to_cloudoperation_group(self) -> CloudOperationGroup:
        operations = []
        for action in self.spec:
            if not action["resource_type"] in AWSProductFamily:
                continue
            operations.append(CloudOperation.from_raw_input(action))
        return CloudOperationGroup(operations)

    def _populate_cost_fields(self):
        self.operation_group.populate_ami_usage_operation(self.aws_region)
        request = self.operation_group.api_request(self.aws_region)
        api_response = request.send().json()
        self.operation_group.populate_cost_from_api_response(api_response)
