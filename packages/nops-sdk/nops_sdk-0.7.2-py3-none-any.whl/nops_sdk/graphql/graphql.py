from __future__ import annotations

from typing import Any


class GraphQL:
    """
    Designates a GraphQL query handler
    """

    def __init__(self, query):
        """
        Args:
            query: the graphql query to be executed on the nOps database
        """
        self.query = query

    def get_query_result(self) -> dict[str, Any]:
        """Get results for a given query

        Returns:
            Raw object response of the executed query
        Examples:
            >>> from nops_sdk.graphql import GraphQL
            >>> query = "query MyS3Buckets { s3_buckets(limit: 2) { name } }"
            >>> graphql = GraphQL(query=query)
            >>> result = graphql.get_query_result()
            {
                's3_buckets': [
                    {'name': 'x-client-009-account'},
                    {'name': 'x-client-009-account-001'}
                ]
            }
        """
        from nops_sdk.api._api_request import APIRequest
        from nops_sdk.api._api_request import RequestMethods

        request = APIRequest(
            endpoint="svc/hasura/v1/graphql",
            method=RequestMethods.POST,
            payload={"query": self.query},
        )
        response = request.send()
        return response.json()["data"]
