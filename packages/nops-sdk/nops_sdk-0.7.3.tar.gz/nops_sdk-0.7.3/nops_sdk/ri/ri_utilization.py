from __future__ import annotations

from dataclasses import asdict
from typing import Literal

from nops_sdk.api._api_request import APIRequest
from nops_sdk.api._api_request import RequestMethods
from nops_sdk.ri.query import RIQueryParams
from nops_sdk.ri.schemas import EC2DetailSchema
from nops_sdk.ri.schemas import RIDetailSchema
from nops_sdk.ri.schemas import RIOverviewSchema
from nops_sdk.ri.schemas import TimeseriesSchema

Period = (Literal["0.5", "1", "7", "30"])

class RIUtilization:
    """Get insights about your Reserve Instance Utilization from the nOps API!

    Example:
        >>> from nops_sdk.ri.ri_utilization import RIUtilization
        >>> ri_util = RIUtilization()
        We start by querying for an overview to get a general picture of RI utilization as well as
        available permutations of AWS region and instance family, tenancy and platforms.
        >>> overview = ri_util.overview()
        >>> overview
        [
            RIOverviewSchema(
                instance_region='us-east-1',
                instance_family='t2', instance_platform='linux',
                instance_tenancy='default',
                coverage=0,
                unused_units=0,
                accounts=['202279780353'],
                reserved_units=0,
                running_units=1.0
            ),
            RIOverviewSchema(
                instance_region='us-west-2',
                instance_family='t3', instance_platform='linux',
                instance_tenancy='default',
                coverage=0, unused_units=0,
                accounts=['202279780353'],
                reserved_units=0,
                running_units=16
            )
        ],
        After taking a glance, we pick the us-east-1/t2/linux/default permutation to delve further into and select it like so:
        >>> query_params = overview[0].query_params
        >>> query_params
        RIQueryParams(region='us-east-1', family='t2', tenancy='default', platform='linux')
        -------------------------
        Now, we use the query params to get a more detailed overview of EC2 instances in that
        region, family, tenancy and platform.
        >>> ri_util.ec2_detail(query_params)
        [
            EC2DetailSchema(
                size_count=2,
                account=['202279780353'],
                instance_size='micro'
            ),
            EC2DetailSchema(
                size_count=14,
                account=['202279780353'],
                instance_size='medium'
            )
        ]
    """

    def overview(self) -> list[RIOverviewSchema]:
        """Get an overview of your Reserve Instance utilization.  For each permutation of
        AWS region and instance family, tenancy and platform, returns the number of running and reserved normalized units.

        Returns:
            list of :class:`RIOverviewSchema`
        """
        api_request = APIRequest(method=RequestMethods.GET, endpoint="/svc/nops_ri_calc/v4/ri/ri_overview")
        rsp = api_request.send().json()
        return [RIOverviewSchema.from_raw(it) for it in rsp]

    def ri_detail(self, query_params: RIQueryParams) -> list[RIDetailSchema]:
        """
        Given a permutations of AWS region and instance family, tenancy and platform, get detailed information about matching reserved instances.

        Args:
            query_params: an instance of :class:`RIQueryParams` specifying a permutation of interest
        Returns:
            list of :class:`RIDetailSchema`
        """
        api_request = APIRequest(
            method=RequestMethods.GET, endpoint="/svc/nops_ri_calc/v4/ri/ri_detail", params=asdict(query_params)
        )
        rsp = api_request.send().json()
        return [RIDetailSchema.from_raw(it) for it in rsp]

    def ec2_detail(self, query_params: RIQueryParams) -> list[EC2DetailSchema]:
        """
        Given a permutations of AWS region and instance family, tenancy and platform, get detailed information about matching ec2 instances.

        Args:
            query_params: an instance of :class:`RIQueryParams` specifying a permutation of interest
        Returns:
            list of :class:`EC2DetailSchema`
        """
        api_request = APIRequest(
            method=RequestMethods.GET, endpoint="/svc/nops_ri_calc/v4/ri/ec2_detail", params=asdict(query_params)
        )
        rsp = api_request.send().json()
        return [EC2DetailSchema.from_raw(it) for it in rsp]
    
    def timeseries(self, query_params: RIQueryParams,  period: Period) -> list[TimeseriesSchema]:
        """
        Given a permutations of AWS region and instance family, tenancy and platform, get timeseries data.

        Args:
            query_params: an instance of :class:`RIQueryParams` specifying a permutation of interest
        Returns:
            list of :class:`Timeseries`
        """
        api_request = APIRequest(
            method=RequestMethods.GET, endpoint="/svc/nops_ri_calc/v4ri/timeseries", params={**asdict(query_params), **{"period": period}}
        )
        rsp = api_request.send().json()
        return [TimeseriesSchema.from_raw(it) for it in rsp]


