from __future__ import annotations

from nops_sdk.account import Account
from nops_sdk.api._api_request import APIRequest
from nops_sdk.api._api_request import RequestMethods


class APIClient:
    def get_accounts(self) -> "list[Account]":
        """Get a list of all accessible accounts.

        Returns:
            list[Account]
        """
        request = APIRequest(endpoint="/c/admin/projectaws/", method=RequestMethods.GET)
        response = request.send()
        accounts = [Account.from_raw(account) for account in response.json()]
        return accounts
