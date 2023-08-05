from __future__ import annotations

import json
from functools import wraps
from json import JSONDecodeError
from typing import Callable

from requests import Response

from nops_sdk.exceptions import APIException


def handle_api_exceptions(f: Callable) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.status_code == 500:
            return _handle_server_500()

        if response.status_code not in [200, 201, 202, 203, 204]:
            return _handle_api_exception(response)

        if "text/html" in response.headers["Content-Type"]:
            return _handle_html_response()

        response = _handle_api_validation_exception(response)
        return response

    return wrapper


def _handle_server_500():
    raise APIException("Code 500: the nOps API encountered an unexpected error.")


def _handle_api_exception(response: Response):
    try:
        json_content = response.json()
    except JSONDecodeError:
        json_content = None
    base_message = f"The nOps API returned an error (code {response.status_code})."
    if json_content:
        base_message = "\n".join([base_message, "API Message:", json.dumps(json_content)])
    raise APIException(base_message)


def _handle_api_validation_exception(response: Response):
    try:
        json_content = response.json()
    except JSONDecodeError:
        raise APIException("Error encountered at response content decoding.")

    if isinstance(json_content, dict) and json_content.get("errors"):
        raise APIException(json_content["errors"])
    return response


def _handle_html_response():
    raise APIException("Uh oh - we received text/html when we werent expecting to. Is your key valid?")
