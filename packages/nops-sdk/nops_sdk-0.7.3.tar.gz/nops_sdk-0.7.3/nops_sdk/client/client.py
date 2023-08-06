from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Client:
    """
    Designates a Client of nOps.

    Args:
        id: the client id provided by nOps
    """

    id: str

    @classmethod
    def from_raw(cls, api_response: dict) -> "Client":
        """
        Build a Client object from raw API response

        Args:
            api_response (dict)
        Returns:
            Client
        """
        return Client(id=api_response["id"])
