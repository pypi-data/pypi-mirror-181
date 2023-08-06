"""
This module exposes the :class:`APIClient`, which is the main entry point to the nOps SDK.

Example usage:
    >>> from nops_sdk.api import APIClient
    >>> client = APIClient()
    >>> client.get_accounts()
    [Account(id=1, name='my test account', client=Client(id=14428))]

"""
from nops_sdk.api.api_client import APIClient

__all__ = ["APIClient"]
