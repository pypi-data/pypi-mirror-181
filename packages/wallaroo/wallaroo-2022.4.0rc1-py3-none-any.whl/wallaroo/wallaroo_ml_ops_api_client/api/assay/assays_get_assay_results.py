from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.assays_get_assay_results_json_body import \
    AssaysGetAssayResultsJsonBody
from ...models.assays_get_assay_results_response_200_item import \
    AssaysGetAssayResultsResponse200Item
from ...models.assays_get_assay_results_response_500 import \
    AssaysGetAssayResultsResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: AssaysGetAssayResultsJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/assays/get_assay_results".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[AssaysGetAssayResultsResponse500, List[AssaysGetAssayResultsResponse200Item]]]:
    if response.status_code == 500:
        response_500 = AssaysGetAssayResultsResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = AssaysGetAssayResultsResponse200Item.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AssaysGetAssayResultsResponse500, List[AssaysGetAssayResultsResponse200Item]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: AssaysGetAssayResultsJsonBody,

) -> Response[Union[AssaysGetAssayResultsResponse500, List[AssaysGetAssayResultsResponse200Item]]]:
    """Temporary mockup to get get assay results by assay_id.

     Returns assay results.

    Args:
        json_body (AssaysGetAssayResultsJsonBody):  Request to return assay results.

    Returns:
        Response[Union[AssaysGetAssayResultsResponse500, List[AssaysGetAssayResultsResponse200Item]]]
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
    json_body: AssaysGetAssayResultsJsonBody,

) -> Optional[Union[AssaysGetAssayResultsResponse500, List[AssaysGetAssayResultsResponse200Item]]]:
    """Temporary mockup to get get assay results by assay_id.

     Returns assay results.

    Args:
        json_body (AssaysGetAssayResultsJsonBody):  Request to return assay results.

    Returns:
        Response[Union[AssaysGetAssayResultsResponse500, List[AssaysGetAssayResultsResponse200Item]]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: AssaysGetAssayResultsJsonBody,

) -> Response[Union[AssaysGetAssayResultsResponse500, List[AssaysGetAssayResultsResponse200Item]]]:
    """Temporary mockup to get get assay results by assay_id.

     Returns assay results.

    Args:
        json_body (AssaysGetAssayResultsJsonBody):  Request to return assay results.

    Returns:
        Response[Union[AssaysGetAssayResultsResponse500, List[AssaysGetAssayResultsResponse200Item]]]
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
    json_body: AssaysGetAssayResultsJsonBody,

) -> Optional[Union[AssaysGetAssayResultsResponse500, List[AssaysGetAssayResultsResponse200Item]]]:
    """Temporary mockup to get get assay results by assay_id.

     Returns assay results.

    Args:
        json_body (AssaysGetAssayResultsJsonBody):  Request to return assay results.

    Returns:
        Response[Union[AssaysGetAssayResultsResponse500, List[AssaysGetAssayResultsResponse200Item]]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
