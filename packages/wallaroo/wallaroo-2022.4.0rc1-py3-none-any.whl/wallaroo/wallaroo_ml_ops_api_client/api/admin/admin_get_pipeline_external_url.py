from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.admin_get_pipeline_external_url_json_body import \
    AdminGetPipelineExternalUrlJsonBody
from ...models.admin_get_pipeline_external_url_response_200 import \
    AdminGetPipelineExternalUrlResponse200
from ...models.admin_get_pipeline_external_url_response_400 import \
    AdminGetPipelineExternalUrlResponse400
from ...models.admin_get_pipeline_external_url_response_401 import \
    AdminGetPipelineExternalUrlResponse401
from ...models.admin_get_pipeline_external_url_response_500 import \
    AdminGetPipelineExternalUrlResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: AdminGetPipelineExternalUrlJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/admin/get_pipeline_external_url".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[AdminGetPipelineExternalUrlResponse200, AdminGetPipelineExternalUrlResponse400, AdminGetPipelineExternalUrlResponse401, AdminGetPipelineExternalUrlResponse500]]:
    if response.status_code == 500:
        response_500 = AdminGetPipelineExternalUrlResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = AdminGetPipelineExternalUrlResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = AdminGetPipelineExternalUrlResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = AdminGetPipelineExternalUrlResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AdminGetPipelineExternalUrlResponse200, AdminGetPipelineExternalUrlResponse400, AdminGetPipelineExternalUrlResponse401, AdminGetPipelineExternalUrlResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: AdminGetPipelineExternalUrlJsonBody,

) -> Response[Union[AdminGetPipelineExternalUrlResponse200, AdminGetPipelineExternalUrlResponse400, AdminGetPipelineExternalUrlResponse401, AdminGetPipelineExternalUrlResponse500]]:
    """Returns the URL for the given pipeline that clients may send inferences to from outside of the
    cluster.

     Returns the external inference URL for a given pipeline.

    Args:
        json_body (AdminGetPipelineExternalUrlJsonBody):  Request for pipeline URL-related
            operations.

    Returns:
        Response[Union[AdminGetPipelineExternalUrlResponse200, AdminGetPipelineExternalUrlResponse400, AdminGetPipelineExternalUrlResponse401, AdminGetPipelineExternalUrlResponse500]]
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
    json_body: AdminGetPipelineExternalUrlJsonBody,

) -> Optional[Union[AdminGetPipelineExternalUrlResponse200, AdminGetPipelineExternalUrlResponse400, AdminGetPipelineExternalUrlResponse401, AdminGetPipelineExternalUrlResponse500]]:
    """Returns the URL for the given pipeline that clients may send inferences to from outside of the
    cluster.

     Returns the external inference URL for a given pipeline.

    Args:
        json_body (AdminGetPipelineExternalUrlJsonBody):  Request for pipeline URL-related
            operations.

    Returns:
        Response[Union[AdminGetPipelineExternalUrlResponse200, AdminGetPipelineExternalUrlResponse400, AdminGetPipelineExternalUrlResponse401, AdminGetPipelineExternalUrlResponse500]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: AdminGetPipelineExternalUrlJsonBody,

) -> Response[Union[AdminGetPipelineExternalUrlResponse200, AdminGetPipelineExternalUrlResponse400, AdminGetPipelineExternalUrlResponse401, AdminGetPipelineExternalUrlResponse500]]:
    """Returns the URL for the given pipeline that clients may send inferences to from outside of the
    cluster.

     Returns the external inference URL for a given pipeline.

    Args:
        json_body (AdminGetPipelineExternalUrlJsonBody):  Request for pipeline URL-related
            operations.

    Returns:
        Response[Union[AdminGetPipelineExternalUrlResponse200, AdminGetPipelineExternalUrlResponse400, AdminGetPipelineExternalUrlResponse401, AdminGetPipelineExternalUrlResponse500]]
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
    json_body: AdminGetPipelineExternalUrlJsonBody,

) -> Optional[Union[AdminGetPipelineExternalUrlResponse200, AdminGetPipelineExternalUrlResponse400, AdminGetPipelineExternalUrlResponse401, AdminGetPipelineExternalUrlResponse500]]:
    """Returns the URL for the given pipeline that clients may send inferences to from outside of the
    cluster.

     Returns the external inference URL for a given pipeline.

    Args:
        json_body (AdminGetPipelineExternalUrlJsonBody):  Request for pipeline URL-related
            operations.

    Returns:
        Response[Union[AdminGetPipelineExternalUrlResponse200, AdminGetPipelineExternalUrlResponse400, AdminGetPipelineExternalUrlResponse401, AdminGetPipelineExternalUrlResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
