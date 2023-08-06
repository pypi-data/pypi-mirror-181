from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from typing import Any
from typing import Callable
from typing import Optional

import requests
from requests import Response
from requests.compat import urljoin

from nops_sdk._settings import NOPS_API_URL
from nops_sdk.api._decorators import handle_api_exceptions
from nops_sdk.exceptions import ImproperlyConfigured
from nops_sdk.pkg_version import _get_version

logger = logging.getLogger(__name__)


class RequestMethods(str, Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    PATCH = "patch"
    DELETE = "delete"
    OPTIONS = "options"


@dataclass
class APIRequest:
    endpoint: str
    method: RequestMethods
    payload: Optional[dict] = field(default_factory=lambda: {})
    params: Optional[dict] = field(default_factory=lambda: {})

    def __post_init__(self):
        """Set API Key to request query parameters."""
        if not (api_key := os.getenv("NOPS_API_KEY")):
            raise ImproperlyConfigured("NOPS_API_KEY is not set")
        self.params["api_key"] = api_key
        self._url = urljoin(NOPS_API_URL, self.endpoint)

    @handle_api_exceptions
    def send(self) -> Response:
        """Send a request to nOps API and return the response"""
        kwargs = {"params": self.params, "headers": self._headers}
        if self.method in [RequestMethods.POST, RequestMethods.PUT, RequestMethods.PATCH]:
            kwargs["json"] = self.payload
        logging.info(f"Sending {self.method} request to {self._url} with params {self.params} and payload {self.payload}")
        return self._request_function(self._url, **kwargs)

    @property
    def _request_function(self) -> Callable[[Any], Response]:
        return getattr(requests, self.method)

    @property
    def _headers(self) -> "dict[str, str]":
        return {"Accept": "application/json", "Content-Type": "application/json", "Sdk-Version": _get_version()}
