from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.explainability_list_configs_by_pipeline_json_body import \
    ExplainabilityListConfigsByPipelineJsonBody
from ...models.explainability_list_configs_by_pipeline_response_200_item import \
    ExplainabilityListConfigsByPipelineResponse200Item
from ...models.explainability_list_configs_by_pipeline_response_400 import \
    ExplainabilityListConfigsByPipelineResponse400
from ...models.explainability_list_configs_by_pipeline_response_401 import \
    ExplainabilityListConfigsByPipelineResponse401
from ...models.explainability_list_configs_by_pipeline_response_500 import \
    ExplainabilityListConfigsByPipelineResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: ExplainabilityListConfigsByPipelineJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/explainability/list_configs_by_pipeline".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[ExplainabilityListConfigsByPipelineResponse400, ExplainabilityListConfigsByPipelineResponse401, ExplainabilityListConfigsByPipelineResponse500, List[Optional[ExplainabilityListConfigsByPipelineResponse200Item]]]]:
    if response.status_code == 500:
        response_500 = ExplainabilityListConfigsByPipelineResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = ExplainabilityListConfigsByPipelineResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = ExplainabilityListConfigsByPipelineResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            _response_200_item = response_200_item_data
            response_200_item: Optional[ExplainabilityListConfigsByPipelineResponse200Item]
            if _response_200_item is None:
                response_200_item = None
            else:
                response_200_item = ExplainabilityListConfigsByPipelineResponse200Item.from_dict(_response_200_item)



            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ExplainabilityListConfigsByPipelineResponse400, ExplainabilityListConfigsByPipelineResponse401, ExplainabilityListConfigsByPipelineResponse500, List[Optional[ExplainabilityListConfigsByPipelineResponse200Item]]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: ExplainabilityListConfigsByPipelineJsonBody,

) -> Response[Union[ExplainabilityListConfigsByPipelineResponse400, ExplainabilityListConfigsByPipelineResponse401, ExplainabilityListConfigsByPipelineResponse500, List[Optional[ExplainabilityListConfigsByPipelineResponse200Item]]]]:
    """List explainability configs for a given pipeline

     Returns a list of explainability configs for the specified pipeline.

    Args:
        json_body (ExplainabilityListConfigsByPipelineJsonBody):

    Returns:
        Response[Union[ExplainabilityListConfigsByPipelineResponse400, ExplainabilityListConfigsByPipelineResponse401, ExplainabilityListConfigsByPipelineResponse500, List[Optional[ExplainabilityListConfigsByPipelineResponse200Item]]]]
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
    json_body: ExplainabilityListConfigsByPipelineJsonBody,

) -> Optional[Union[ExplainabilityListConfigsByPipelineResponse400, ExplainabilityListConfigsByPipelineResponse401, ExplainabilityListConfigsByPipelineResponse500, List[Optional[ExplainabilityListConfigsByPipelineResponse200Item]]]]:
    """List explainability configs for a given pipeline

     Returns a list of explainability configs for the specified pipeline.

    Args:
        json_body (ExplainabilityListConfigsByPipelineJsonBody):

    Returns:
        Response[Union[ExplainabilityListConfigsByPipelineResponse400, ExplainabilityListConfigsByPipelineResponse401, ExplainabilityListConfigsByPipelineResponse500, List[Optional[ExplainabilityListConfigsByPipelineResponse200Item]]]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: ExplainabilityListConfigsByPipelineJsonBody,

) -> Response[Union[ExplainabilityListConfigsByPipelineResponse400, ExplainabilityListConfigsByPipelineResponse401, ExplainabilityListConfigsByPipelineResponse500, List[Optional[ExplainabilityListConfigsByPipelineResponse200Item]]]]:
    """List explainability configs for a given pipeline

     Returns a list of explainability configs for the specified pipeline.

    Args:
        json_body (ExplainabilityListConfigsByPipelineJsonBody):

    Returns:
        Response[Union[ExplainabilityListConfigsByPipelineResponse400, ExplainabilityListConfigsByPipelineResponse401, ExplainabilityListConfigsByPipelineResponse500, List[Optional[ExplainabilityListConfigsByPipelineResponse200Item]]]]
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
    json_body: ExplainabilityListConfigsByPipelineJsonBody,

) -> Optional[Union[ExplainabilityListConfigsByPipelineResponse400, ExplainabilityListConfigsByPipelineResponse401, ExplainabilityListConfigsByPipelineResponse500, List[Optional[ExplainabilityListConfigsByPipelineResponse200Item]]]]:
    """List explainability configs for a given pipeline

     Returns a list of explainability configs for the specified pipeline.

    Args:
        json_body (ExplainabilityListConfigsByPipelineJsonBody):

    Returns:
        Response[Union[ExplainabilityListConfigsByPipelineResponse400, ExplainabilityListConfigsByPipelineResponse401, ExplainabilityListConfigsByPipelineResponse500, List[Optional[ExplainabilityListConfigsByPipelineResponse200Item]]]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
