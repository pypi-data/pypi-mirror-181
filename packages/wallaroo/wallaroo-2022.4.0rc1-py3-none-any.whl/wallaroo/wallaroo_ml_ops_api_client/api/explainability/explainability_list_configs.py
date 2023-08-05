from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.explainability_list_configs_response_200_item import \
    ExplainabilityListConfigsResponse200Item
from ...models.explainability_list_configs_response_400 import \
    ExplainabilityListConfigsResponse400
from ...models.explainability_list_configs_response_401 import \
    ExplainabilityListConfigsResponse401
from ...models.explainability_list_configs_response_500 import \
    ExplainabilityListConfigsResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,

) -> Dict[str, Any]:
    url = "{}/v1/api/explainability/list_configs".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ExplainabilityListConfigsResponse400, ExplainabilityListConfigsResponse401, ExplainabilityListConfigsResponse500, List[Optional[ExplainabilityListConfigsResponse200Item]]]]:
    if response.status_code == 500:
        response_500 = ExplainabilityListConfigsResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = ExplainabilityListConfigsResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = ExplainabilityListConfigsResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            _response_200_item = response_200_item_data
            response_200_item: Optional[ExplainabilityListConfigsResponse200Item]
            if _response_200_item is None:
                response_200_item = None
            else:
                response_200_item = ExplainabilityListConfigsResponse200Item.from_dict(_response_200_item)



            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ExplainabilityListConfigsResponse400, ExplainabilityListConfigsResponse401, ExplainabilityListConfigsResponse500, List[Optional[ExplainabilityListConfigsResponse200Item]]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,

) -> Response[Union[ExplainabilityListConfigsResponse400, ExplainabilityListConfigsResponse401, ExplainabilityListConfigsResponse500, List[Optional[ExplainabilityListConfigsResponse200Item]]]]:
    """List explainability configs

     Returns a list of explainability configs.

    Returns:
        Response[Union[ExplainabilityListConfigsResponse400, ExplainabilityListConfigsResponse401, ExplainabilityListConfigsResponse500, List[Optional[ExplainabilityListConfigsResponse200Item]]]]
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

) -> Optional[Union[ExplainabilityListConfigsResponse400, ExplainabilityListConfigsResponse401, ExplainabilityListConfigsResponse500, List[Optional[ExplainabilityListConfigsResponse200Item]]]]:
    """List explainability configs

     Returns a list of explainability configs.

    Returns:
        Response[Union[ExplainabilityListConfigsResponse400, ExplainabilityListConfigsResponse401, ExplainabilityListConfigsResponse500, List[Optional[ExplainabilityListConfigsResponse200Item]]]]
    """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,

) -> Response[Union[ExplainabilityListConfigsResponse400, ExplainabilityListConfigsResponse401, ExplainabilityListConfigsResponse500, List[Optional[ExplainabilityListConfigsResponse200Item]]]]:
    """List explainability configs

     Returns a list of explainability configs.

    Returns:
        Response[Union[ExplainabilityListConfigsResponse400, ExplainabilityListConfigsResponse401, ExplainabilityListConfigsResponse500, List[Optional[ExplainabilityListConfigsResponse200Item]]]]
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

) -> Optional[Union[ExplainabilityListConfigsResponse400, ExplainabilityListConfigsResponse401, ExplainabilityListConfigsResponse500, List[Optional[ExplainabilityListConfigsResponse200Item]]]]:
    """List explainability configs

     Returns a list of explainability configs.

    Returns:
        Response[Union[ExplainabilityListConfigsResponse400, ExplainabilityListConfigsResponse401, ExplainabilityListConfigsResponse500, List[Optional[ExplainabilityListConfigsResponse200Item]]]]
    """


    return (await asyncio_detailed(
        client=client,

    )).parsed
