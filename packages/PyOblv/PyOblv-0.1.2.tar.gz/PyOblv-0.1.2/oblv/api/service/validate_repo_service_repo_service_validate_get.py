from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...models.service_validation_response import ServiceValidationResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    ref: str,
    oblivious_user_id: str,
    repo_id: str,
    ref_type: Union[Unset, None, str] = "branch",
    account_type: Union[Unset, None, str] = "github",
) -> Dict[str, Any]:
    url = "{}/repo/service/validate".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ref"] = ref

    params["oblivious_user_id"] = oblivious_user_id

    params["repo_id"] = repo_id

    params["ref_type"] = ref_type

    params["account_type"] = account_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    if response.status_code == 200:
        response_200 = ServiceValidationResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400_message = response.json()["message"]
        raise BadRequestError(message=response_400_message)
    if response.status_code == 500:
        response_500_request_id = response.headers["apigw-requestid"]
        raise HTTPClientError(request_id=response_500_request_id)
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())
        if response_422.detail[0].type.__contains__("regex"):
            report = "Invalid " + response_422.detail[0].loc[-1] + " provided"
        report = "Invalid " + response_422.detail[0].loc[-1] + " provided"
        raise ParamValidationError(report=report)
    if response.status_code == 403:
        raise UnauthorizedTokenError()
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    ref: str,
    oblivious_user_id: str,
    repo_id: str,
    ref_type: Union[Unset, None, str] = "branch",
    account_type: Union[Unset, None, str] = "github",
) -> Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    """Validate Repo Service

     API to validate a service with supported service schema. The checks include

    - Presence of service.yaml in ./oblivious folder.
    - Presence of Dockerfile in ./oblivious folder.
    - Content of service.yaml must be valid with respect to supported service schema.

    Args:
        ref (str):
        oblivious_user_id (str):
        repo_id (str):
        ref_type (Union[Unset, None, str]):  Default: 'branch'.
        account_type (Union[Unset, None, str]):  Default: 'github'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        ref=ref,
        oblivious_user_id=oblivious_user_id,
        repo_id=repo_id,
        ref_type=ref_type,
        account_type=account_type,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
    ref: str,
    oblivious_user_id: str,
    repo_id: str,
    ref_type: Union[Unset, None, str] = "branch",
    account_type: Union[Unset, None, str] = "github",
) -> Optional[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    """Validate Repo Service

     API to validate a service with supported service schema. The checks include

    - Presence of service.yaml in ./oblivious folder.
    - Presence of Dockerfile in ./oblivious folder.
    - Content of service.yaml must be valid with respect to supported service schema.

    Args:
        ref (str):
        oblivious_user_id (str):
        repo_id (str):
        ref_type (Union[Unset, None, str]):  Default: 'branch'.
        account_type (Union[Unset, None, str]):  Default: 'github'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]
    """

    return sync_detailed(
        client=client,
        ref=ref,
        oblivious_user_id=oblivious_user_id,
        repo_id=repo_id,
        ref_type=ref_type,
        account_type=account_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    ref: str,
    oblivious_user_id: str,
    repo_id: str,
    ref_type: Union[Unset, None, str] = "branch",
    account_type: Union[Unset, None, str] = "github",
) -> Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    """Validate Repo Service

     API to validate a service with supported service schema. The checks include

    - Presence of service.yaml in ./oblivious folder.
    - Presence of Dockerfile in ./oblivious folder.
    - Content of service.yaml must be valid with respect to supported service schema.

    Args:
        ref (str):
        oblivious_user_id (str):
        repo_id (str):
        ref_type (Union[Unset, None, str]):  Default: 'branch'.
        account_type (Union[Unset, None, str]):  Default: 'github'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        ref=ref,
        oblivious_user_id=oblivious_user_id,
        repo_id=repo_id,
        ref_type=ref_type,
        account_type=account_type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    ref: str,
    oblivious_user_id: str,
    repo_id: str,
    ref_type: Union[Unset, None, str] = "branch",
    account_type: Union[Unset, None, str] = "github",
) -> Optional[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]:
    """Validate Repo Service

     API to validate a service with supported service schema. The checks include

    - Presence of service.yaml in ./oblivious folder.
    - Presence of Dockerfile in ./oblivious folder.
    - Content of service.yaml must be valid with respect to supported service schema.

    Args:
        ref (str):
        oblivious_user_id (str):
        repo_id (str):
        ref_type (Union[Unset, None, str]):  Default: 'branch'.
        account_type (Union[Unset, None, str]):  Default: 'github'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceValidationResponse]]
    """

    return (
        await asyncio_detailed(
            client=client,
            ref=ref,
            oblivious_user_id=oblivious_user_id,
            repo_id=repo_id,
            ref_type=ref_type,
            account_type=account_type,
        )
    ).parsed
