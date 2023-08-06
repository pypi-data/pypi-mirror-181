from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import BadRequestError, HTTPClientError, ParamValidationError, UnauthorizedTokenError
from ...models.http_validation_error import HTTPValidationError
from ...models.message_model import MessageModel
from ...models.repo_services import RepoServices
from ...types import UNSET, Response, Unset


def _get_kwargs(
    repo_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    account_type: Union[Unset, None, str] = "github",
) -> Dict[str, Any]:
    url = "{}/repo/{repo_id}".format(client.base_url, repo_id=repo_id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["oblivious_user_id"] = oblivious_user_id

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
) -> Optional[Union[Any, HTTPValidationError, MessageModel, RepoServices]]:
    if response.status_code == 200:
        response_200 = RepoServices.from_dict(response.json())

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
) -> Response[Union[Any, HTTPValidationError, MessageModel, RepoServices]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    repo_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    account_type: Union[Unset, None, str] = "github",
) -> Response[Union[Any, HTTPValidationError, MessageModel, RepoServices]]:
    """Get User Repos with Services

     API to fetch user's repo with services created for every repo.

    Args:
        repo_id (str):
        oblivious_user_id (str):
        account_type (Union[Unset, None, str]):  Default: 'github'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, RepoServices]]
    """

    kwargs = _get_kwargs(
        repo_id=repo_id,
        client=client,
        oblivious_user_id=oblivious_user_id,
        account_type=account_type,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    repo_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    account_type: Union[Unset, None, str] = "github",
) -> Optional[Union[Any, HTTPValidationError, MessageModel, RepoServices]]:
    """Get User Repos with Services

     API to fetch user's repo with services created for every repo.

    Args:
        repo_id (str):
        oblivious_user_id (str):
        account_type (Union[Unset, None, str]):  Default: 'github'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, RepoServices]]
    """

    return sync_detailed(
        repo_id=repo_id,
        client=client,
        oblivious_user_id=oblivious_user_id,
        account_type=account_type,
    ).parsed


async def asyncio_detailed(
    repo_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    account_type: Union[Unset, None, str] = "github",
) -> Response[Union[Any, HTTPValidationError, MessageModel, RepoServices]]:
    """Get User Repos with Services

     API to fetch user's repo with services created for every repo.

    Args:
        repo_id (str):
        oblivious_user_id (str):
        account_type (Union[Unset, None, str]):  Default: 'github'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, RepoServices]]
    """

    kwargs = _get_kwargs(
        repo_id=repo_id,
        client=client,
        oblivious_user_id=oblivious_user_id,
        account_type=account_type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    repo_id: str,
    *,
    client: AuthenticatedClient,
    oblivious_user_id: str,
    account_type: Union[Unset, None, str] = "github",
) -> Optional[Union[Any, HTTPValidationError, MessageModel, RepoServices]]:
    """Get User Repos with Services

     API to fetch user's repo with services created for every repo.

    Args:
        repo_id (str):
        oblivious_user_id (str):
        account_type (Union[Unset, None, str]):  Default: 'github'.

    Returns:
        Response[Union[Any, HTTPValidationError, MessageModel, RepoServices]]
    """

    return (
        await asyncio_detailed(
            repo_id=repo_id,
            client=client,
            oblivious_user_id=oblivious_user_id,
            account_type=account_type,
        )
    ).parsed
