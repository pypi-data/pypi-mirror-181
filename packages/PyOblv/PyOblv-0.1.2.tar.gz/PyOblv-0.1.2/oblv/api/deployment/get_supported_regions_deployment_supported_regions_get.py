from typing import Any, Dict, Optional, Union

import httpx

from ...client import AuthenticatedClient
from ...exceptions import UnauthorizedTokenError
from ...models.message_model import MessageModel
from ...models.supported_regions import SupportedRegions
from ...types import Response


def _get_kwargs(
    *,
    client: AuthenticatedClient,
) -> Dict[str, Any]:
    url = "{}/deployment/supported_regions".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, SupportedRegions, MessageModel]]:
    if response.status_code == 200:
        response_200 = SupportedRegions.from_dict(response.json())

        return response_200
		
    if response.status_code == 500:
        response_500 = response.json()

        return response_500
		
    if response.status_code == 403:
        raise UnauthorizedTokenError()
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, SupportedRegions, MessageModel]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, SupportedRegions, MessageModel]]:
    """Deployment Supported Regions

     API to fetch a deployment's details.

    Returns:
        Response[Union[Any, SupportedRegions, MessageModel]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, SupportedRegions, MessageModel]]:
    """Deployment Supported Regions

     API to fetch a deployment's details.

    Returns:
        Response[Union[Any, SupportedRegions, MessageModel]]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[Union[Any, SupportedRegions, MessageModel]]:
    """Deployment Supported Regions

     API to fetch a deployment's details.

    Returns:
        Response[Union[Any, SupportedRegions, MessageModel]]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[Union[Any, SupportedRegions, MessageModel]]:
    """Deployment Supported Regions

     API to fetch a deployment's details.

    Returns:
        Response[Union[Any, SupportedRegions, MessageModel]]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
