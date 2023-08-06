from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.plateau_get_topic_name_json_body import \
    PlateauGetTopicNameJsonBody
from ...models.plateau_get_topic_name_response_200 import \
    PlateauGetTopicNameResponse200
from ...models.plateau_get_topic_name_response_400 import \
    PlateauGetTopicNameResponse400
from ...models.plateau_get_topic_name_response_401 import \
    PlateauGetTopicNameResponse401
from ...models.plateau_get_topic_name_response_500 import \
    PlateauGetTopicNameResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: PlateauGetTopicNameJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/plateau/get_topic_name".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[PlateauGetTopicNameResponse200, PlateauGetTopicNameResponse400, PlateauGetTopicNameResponse401, PlateauGetTopicNameResponse500]]:
    if response.status_code == 500:
        response_500 = PlateauGetTopicNameResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = PlateauGetTopicNameResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = PlateauGetTopicNameResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = PlateauGetTopicNameResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PlateauGetTopicNameResponse200, PlateauGetTopicNameResponse400, PlateauGetTopicNameResponse401, PlateauGetTopicNameResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: PlateauGetTopicNameJsonBody,

) -> Response[Union[PlateauGetTopicNameResponse200, PlateauGetTopicNameResponse400, PlateauGetTopicNameResponse401, PlateauGetTopicNameResponse500]]:
    """Get topic name

     Returns the topic name for the given pipeline.

    Args:
        json_body (PlateauGetTopicNameJsonBody):  Request for topic name.

    Returns:
        Response[Union[PlateauGetTopicNameResponse200, PlateauGetTopicNameResponse400, PlateauGetTopicNameResponse401, PlateauGetTopicNameResponse500]]
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
    json_body: PlateauGetTopicNameJsonBody,

) -> Optional[Union[PlateauGetTopicNameResponse200, PlateauGetTopicNameResponse400, PlateauGetTopicNameResponse401, PlateauGetTopicNameResponse500]]:
    """Get topic name

     Returns the topic name for the given pipeline.

    Args:
        json_body (PlateauGetTopicNameJsonBody):  Request for topic name.

    Returns:
        Response[Union[PlateauGetTopicNameResponse200, PlateauGetTopicNameResponse400, PlateauGetTopicNameResponse401, PlateauGetTopicNameResponse500]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: PlateauGetTopicNameJsonBody,

) -> Response[Union[PlateauGetTopicNameResponse200, PlateauGetTopicNameResponse400, PlateauGetTopicNameResponse401, PlateauGetTopicNameResponse500]]:
    """Get topic name

     Returns the topic name for the given pipeline.

    Args:
        json_body (PlateauGetTopicNameJsonBody):  Request for topic name.

    Returns:
        Response[Union[PlateauGetTopicNameResponse200, PlateauGetTopicNameResponse400, PlateauGetTopicNameResponse401, PlateauGetTopicNameResponse500]]
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
    json_body: PlateauGetTopicNameJsonBody,

) -> Optional[Union[PlateauGetTopicNameResponse200, PlateauGetTopicNameResponse400, PlateauGetTopicNameResponse401, PlateauGetTopicNameResponse500]]:
    """Get topic name

     Returns the topic name for the given pipeline.

    Args:
        json_body (PlateauGetTopicNameJsonBody):  Request for topic name.

    Returns:
        Response[Union[PlateauGetTopicNameResponse200, PlateauGetTopicNameResponse400, PlateauGetTopicNameResponse401, PlateauGetTopicNameResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
