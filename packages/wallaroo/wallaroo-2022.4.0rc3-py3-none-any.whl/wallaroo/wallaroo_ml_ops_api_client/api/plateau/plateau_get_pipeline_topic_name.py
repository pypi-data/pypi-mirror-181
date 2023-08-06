from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.plateau_get_pipeline_topic_name_json_body import \
    PlateauGetPipelineTopicNameJsonBody
from ...models.plateau_get_pipeline_topic_name_response_200 import \
    PlateauGetPipelineTopicNameResponse200
from ...models.plateau_get_pipeline_topic_name_response_400 import \
    PlateauGetPipelineTopicNameResponse400
from ...models.plateau_get_pipeline_topic_name_response_401 import \
    PlateauGetPipelineTopicNameResponse401
from ...models.plateau_get_pipeline_topic_name_response_500 import \
    PlateauGetPipelineTopicNameResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: PlateauGetPipelineTopicNameJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/plateau/get_pipeline_topic_name".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[PlateauGetPipelineTopicNameResponse200, PlateauGetPipelineTopicNameResponse400, PlateauGetPipelineTopicNameResponse401, PlateauGetPipelineTopicNameResponse500]]:
    if response.status_code == 500:
        response_500 = PlateauGetPipelineTopicNameResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = PlateauGetPipelineTopicNameResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = PlateauGetPipelineTopicNameResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = PlateauGetPipelineTopicNameResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[PlateauGetPipelineTopicNameResponse200, PlateauGetPipelineTopicNameResponse400, PlateauGetPipelineTopicNameResponse401, PlateauGetPipelineTopicNameResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: PlateauGetPipelineTopicNameJsonBody,

) -> Response[Union[PlateauGetPipelineTopicNameResponse200, PlateauGetPipelineTopicNameResponse400, PlateauGetPipelineTopicNameResponse401, PlateauGetPipelineTopicNameResponse500]]:
    """Get pipeline topic name

     Returns the given pipeline's topic name.

    Args:
        json_body (PlateauGetPipelineTopicNameJsonBody):  Request for pipeline topic name.

    Returns:
        Response[Union[PlateauGetPipelineTopicNameResponse200, PlateauGetPipelineTopicNameResponse400, PlateauGetPipelineTopicNameResponse401, PlateauGetPipelineTopicNameResponse500]]
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
    json_body: PlateauGetPipelineTopicNameJsonBody,

) -> Optional[Union[PlateauGetPipelineTopicNameResponse200, PlateauGetPipelineTopicNameResponse400, PlateauGetPipelineTopicNameResponse401, PlateauGetPipelineTopicNameResponse500]]:
    """Get pipeline topic name

     Returns the given pipeline's topic name.

    Args:
        json_body (PlateauGetPipelineTopicNameJsonBody):  Request for pipeline topic name.

    Returns:
        Response[Union[PlateauGetPipelineTopicNameResponse200, PlateauGetPipelineTopicNameResponse400, PlateauGetPipelineTopicNameResponse401, PlateauGetPipelineTopicNameResponse500]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: PlateauGetPipelineTopicNameJsonBody,

) -> Response[Union[PlateauGetPipelineTopicNameResponse200, PlateauGetPipelineTopicNameResponse400, PlateauGetPipelineTopicNameResponse401, PlateauGetPipelineTopicNameResponse500]]:
    """Get pipeline topic name

     Returns the given pipeline's topic name.

    Args:
        json_body (PlateauGetPipelineTopicNameJsonBody):  Request for pipeline topic name.

    Returns:
        Response[Union[PlateauGetPipelineTopicNameResponse200, PlateauGetPipelineTopicNameResponse400, PlateauGetPipelineTopicNameResponse401, PlateauGetPipelineTopicNameResponse500]]
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
    json_body: PlateauGetPipelineTopicNameJsonBody,

) -> Optional[Union[PlateauGetPipelineTopicNameResponse200, PlateauGetPipelineTopicNameResponse400, PlateauGetPipelineTopicNameResponse401, PlateauGetPipelineTopicNameResponse500]]:
    """Get pipeline topic name

     Returns the given pipeline's topic name.

    Args:
        json_body (PlateauGetPipelineTopicNameJsonBody):  Request for pipeline topic name.

    Returns:
        Response[Union[PlateauGetPipelineTopicNameResponse200, PlateauGetPipelineTopicNameResponse400, PlateauGetPipelineTopicNameResponse401, PlateauGetPipelineTopicNameResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
