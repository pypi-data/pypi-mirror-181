from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.models_list_json_body import ModelsListJsonBody
from ...models.models_list_response_200 import ModelsListResponse200
from ...models.models_list_response_400 import ModelsListResponse400
from ...models.models_list_response_401 import ModelsListResponse401
from ...models.models_list_response_500 import ModelsListResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: ModelsListJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/models/list".format(
        client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    json_json_body = json_body.to_dict()



    

    return {
	    "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]:
    if response.status_code == 500:
        response_500 = ModelsListResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = ModelsListResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = ModelsListResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = ModelsListResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: ModelsListJsonBody,

) -> Response[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]:
    """Retrieve models

     Returns models in the given workspace.

    Args:
        json_body (ModelsListJsonBody):  Workspace model retrieval request.

    Returns:
        Response[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]
    """


    kwargs = _get_kwargs(
        client=client,
json_body=json_body,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    json_body: ModelsListJsonBody,

) -> Optional[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]:
    """Retrieve models

     Returns models in the given workspace.

    Args:
        json_body (ModelsListJsonBody):  Workspace model retrieval request.

    Returns:
        Response[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: ModelsListJsonBody,

) -> Response[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]:
    """Retrieve models

     Returns models in the given workspace.

    Args:
        json_body (ModelsListJsonBody):  Workspace model retrieval request.

    Returns:
        Response[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]
    """


    kwargs = _get_kwargs(
        client=client,
json_body=json_body,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    json_body: ModelsListJsonBody,

) -> Optional[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]:
    """Retrieve models

     Returns models in the given workspace.

    Args:
        json_body (ModelsListJsonBody):  Workspace model retrieval request.

    Returns:
        Response[Union[ModelsListResponse200, ModelsListResponse400, ModelsListResponse401, ModelsListResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
