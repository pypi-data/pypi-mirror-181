from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...models.service_content_response import ServiceContentResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: AuthenticatedClient,
    ref: str,
    oblivious_user_id: str,
    repo_id: str,
    account_type: Union[Unset, None, str] = "github",
    ref_type: Union[Unset, None, str] = "branch",
) -> Dict[str, Any]:
    url = "{}/repo/service/yaml".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ref"] = ref

    params["oblivious_user_id"] = oblivious_user_id

    params["repo_id"] = repo_id

    params["account_type"] = account_type

    params["ref_type"] = ref_type

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
) -> Optional[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]:
    if response.status_code == 200:
        response_200 = ServiceContentResponse.from_dict(response.json())

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
) -> Response[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]:
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
    account_type: Union[Unset, None, str] = "github",
    ref_type: Union[Unset, None, str] = "branch",
) -> Response[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]:
    """Get Repo Service Yaml

     API to fetch the service.yaml content as object for the given service.

    Args:
        ref (str):
        oblivious_user_id (str):
        repo_id (str):
        account_type (Union[Unset, None, str]):  Default: 'github'.
        ref_type (Union[Unset, None, str]):  Default: 'branch'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        ref=ref,
        oblivious_user_id=oblivious_user_id,
        repo_id=repo_id,
        account_type=account_type,
        ref_type=ref_type,
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
    account_type: Union[Unset, None, str] = "github",
    ref_type: Union[Unset, None, str] = "branch",
) -> Optional[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]:
    """Get Repo Service Yaml

     API to fetch the service.yaml content as object for the given service.

    Args:
        ref (str):
        oblivious_user_id (str):
        repo_id (str):
        account_type (Union[Unset, None, str]):  Default: 'github'.
        ref_type (Union[Unset, None, str]):  Default: 'branch'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]
    """

    return sync_detailed(
        client=client,
        ref=ref,
        oblivious_user_id=oblivious_user_id,
        repo_id=repo_id,
        account_type=account_type,
        ref_type=ref_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    ref: str,
    oblivious_user_id: str,
    repo_id: str,
    account_type: Union[Unset, None, str] = "github",
    ref_type: Union[Unset, None, str] = "branch",
) -> Response[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]:
    """Get Repo Service Yaml

     API to fetch the service.yaml content as object for the given service.

    Args:
        ref (str):
        oblivious_user_id (str):
        repo_id (str):
        account_type (Union[Unset, None, str]):  Default: 'github'.
        ref_type (Union[Unset, None, str]):  Default: 'branch'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]
    """

    kwargs = _get_kwargs(
        client=client,
        ref=ref,
        oblivious_user_id=oblivious_user_id,
        repo_id=repo_id,
        account_type=account_type,
        ref_type=ref_type,
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
    account_type: Union[Unset, None, str] = "github",
    ref_type: Union[Unset, None, str] = "branch",
) -> Optional[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]:
    """Get Repo Service Yaml

     API to fetch the service.yaml content as object for the given service.

    Args:
        ref (str):
        oblivious_user_id (str):
        repo_id (str):
        account_type (Union[Unset, None, str]):  Default: 'github'.
        ref_type (Union[Unset, None, str]):  Default: 'branch'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, ServiceContentResponse]]
    """

    return (
        await asyncio_detailed(
            client=client,
            ref=ref,
            oblivious_user_id=oblivious_user_id,
            repo_id=repo_id,
            account_type=account_type,
            ref_type=ref_type,
        )
    ).parsed
