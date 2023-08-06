from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.explainability_get_status_response_200 import \
    ExplainabilityGetStatusResponse200
from ...models.explainability_get_status_response_400 import \
    ExplainabilityGetStatusResponse400
from ...models.explainability_get_status_response_401 import \
    ExplainabilityGetStatusResponse401
from ...models.explainability_get_status_response_500 import \
    ExplainabilityGetStatusResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/v1/api/explainability/get_status".format(
        client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    

    return {
	    "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ExplainabilityGetStatusResponse200, ExplainabilityGetStatusResponse400, ExplainabilityGetStatusResponse401, ExplainabilityGetStatusResponse500]]:
    if response.status_code == 500:
        response_500 = ExplainabilityGetStatusResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = ExplainabilityGetStatusResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = ExplainabilityGetStatusResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = ExplainabilityGetStatusResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ExplainabilityGetStatusResponse200, ExplainabilityGetStatusResponse400, ExplainabilityGetStatusResponse401, ExplainabilityGetStatusResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,

) -> Response[Union[ExplainabilityGetStatusResponse200, ExplainabilityGetStatusResponse400, ExplainabilityGetStatusResponse401, ExplainabilityGetStatusResponse500]]:
    """Get explainability status

     Get the status of the explainability feature.

    Returns:
        Response[Union[ExplainabilityGetStatusResponse200, ExplainabilityGetStatusResponse400, ExplainabilityGetStatusResponse401, ExplainabilityGetStatusResponse500]]
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
    client: Client,

) -> Optional[Union[ExplainabilityGetStatusResponse200, ExplainabilityGetStatusResponse400, ExplainabilityGetStatusResponse401, ExplainabilityGetStatusResponse500]]:
    """Get explainability status

     Get the status of the explainability feature.

    Returns:
        Response[Union[ExplainabilityGetStatusResponse200, ExplainabilityGetStatusResponse400, ExplainabilityGetStatusResponse401, ExplainabilityGetStatusResponse500]]
    """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,

) -> Response[Union[ExplainabilityGetStatusResponse200, ExplainabilityGetStatusResponse400, ExplainabilityGetStatusResponse401, ExplainabilityGetStatusResponse500]]:
    """Get explainability status

     Get the status of the explainability feature.

    Returns:
        Response[Union[ExplainabilityGetStatusResponse200, ExplainabilityGetStatusResponse400, ExplainabilityGetStatusResponse401, ExplainabilityGetStatusResponse500]]
    """


    kwargs = _get_kwargs(
        client=client,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,

) -> Optional[Union[ExplainabilityGetStatusResponse200, ExplainabilityGetStatusResponse400, ExplainabilityGetStatusResponse401, ExplainabilityGetStatusResponse500]]:
    """Get explainability status

     Get the status of the explainability feature.

    Returns:
        Response[Union[ExplainabilityGetStatusResponse200, ExplainabilityGetStatusResponse400, ExplainabilityGetStatusResponse401, ExplainabilityGetStatusResponse500]]
    """


    return (await asyncio_detailed(
        client=client,

    )).parsed
