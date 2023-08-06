from enum import Enum

from nops_sdk.api._api_request import APIRequest
from nops_sdk.api._api_request import RequestMethods


class K8SPeriodicity(Enum):
    """Denotes the choices of periodicity for K8S recommendations."""

    TWENTY_FOUR_HOURS = 1
    SEVEN_DAYS = 7
    THIRTY_DAYS = 30


class K8SRecommendations:
    """Get K8S pod request and limit configuration recommendations.

    Args:
        cluster_id: id of the concerned cluster

    Example:
        >>> from nops_sdk.k8s.pod_recommendations import K8SRecommendations
        >>> recommendations = K8SRecommendations(cluster_id="my_clust_id")
        >>> recommendations.overview(period=K8SPeriodicity.TWENTY_FOUR_HOURS)
        [
            {
                "base_name": "pod_name1",
                "recommendations": 1
            },
            {
                "base_name": "pod_name2",
                "recommendations": 1
            }
            ...
        ]
        >>> recommedantions.by_pod(base_name="pod_name2", period=K8SPeriodicity.TWENTY_FOUR_HOURS)
        [{
            'name': 'pod_name2',
            'cost': 4.725176576592933,
            'ram_usage': 140937142.27470765,
            'cpu_usage': 0.0022271234666475024,
            'ram_request': 1000000000.0,
            'cpu_request': None,
            'ram_limit': 1000000000.0,
            'cpu_limit': None,
            'container': 'pod_name2',
            'recommended_ram_request': 105702856.70603073,
            'recommended_ram_limit': 158554285.0590461,
            'recommended_cpu_request': 0.0022271234666475024,
            'recommended_cpu_limit': 0.0033406851999712535,
            'savings': 2.1128559570033185
        }]
    """

    def __init__(self, cluster_id: str) -> None:
        self.cluster_id = cluster_id

    def overview(self, period: K8SPeriodicity) -> dict:
        """Get an overview of recommendations containing a count of recommendations
        per pod.

        Args:
            period: concerned time period
        Returns:
            list of pod names with a count of recommendations associated with them
        """
        api_request = APIRequest(
            method=RequestMethods.GET,
            endpoint="/svc/k8s_cost/recommendations_overview",
            params={"cluster_id": self.cluster_id, "period": period.value},
        )
        return api_request.send().json()

    def by_pod(self, base_name: str, period: K8SPeriodicity):
        """Get recommendations for a specific pod.

        Args:
            base_name: name of the pod
            period: concerned time period
        """
        api_request = APIRequest(
            method=RequestMethods.GET,
            endpoint="/svc/k8s_cost/pod_recommendations",
            params={"cluster_id": self.cluster_id, "base_name": base_name, "period": period.value},
        )
        return api_request.send().json()
