from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.pipelines_undeploy_json_body import PipelinesUndeployJsonBody
from ...models.pipelines_undeploy_response_200 import \
    PipelinesUndeployResponse200
from ...models.pipelines_undeploy_response_400 import \
    PipelinesUndeployResponse400
from ...models.pipelines_undeploy_response_401 import \
    PipelinesUndeployResponse401
from ...models.pipelines_undeploy_response_500 import \
    PipelinesUndeployResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: PipelinesUndeployJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/pipelines/undeploy".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Optional[PipelinesUndeployResponse200], PipelinesUndeployResponse400, PipelinesUndeployResponse401, PipelinesUndeployResponse500]]:
    if response.status_code == 500:
        response_500 = PipelinesUndeployResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = PipelinesUndeployResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = PipelinesUndeployResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: Optional[PipelinesUndeployResponse200]
        if _response_200 is None:
            response_200 = None
        else:
            response_200 = PipelinesUndeployResponse200.from_dict(_response_200)



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Optional[PipelinesUndeployResponse200], PipelinesUndeployResponse400, PipelinesUndeployResponse401, PipelinesUndeployResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: PipelinesUndeployJsonBody,

) -> Response[Union[Optional[PipelinesUndeployResponse200], PipelinesUndeployResponse400, PipelinesUndeployResponse401, PipelinesUndeployResponse500]]:
    """Undeploy pipeline

     Undeploys a previously deployed pipeline.

    Args:
        json_body (PipelinesUndeployJsonBody):  Request to undeploy a pipeline by either its own
            identifier,  or the deployment identifier.

    Returns:
        Response[Union[Optional[PipelinesUndeployResponse200], PipelinesUndeployResponse400, PipelinesUndeployResponse401, PipelinesUndeployResponse500]]
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
    json_body: PipelinesUndeployJsonBody,

) -> Optional[Union[Optional[PipelinesUndeployResponse200], PipelinesUndeployResponse400, PipelinesUndeployResponse401, PipelinesUndeployResponse500]]:
    """Undeploy pipeline

     Undeploys a previously deployed pipeline.

    Args:
        json_body (PipelinesUndeployJsonBody):  Request to undeploy a pipeline by either its own
            identifier,  or the deployment identifier.

    Returns:
        Response[Union[Optional[PipelinesUndeployResponse200], PipelinesUndeployResponse400, PipelinesUndeployResponse401, PipelinesUndeployResponse500]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: PipelinesUndeployJsonBody,

) -> Response[Union[Optional[PipelinesUndeployResponse200], PipelinesUndeployResponse400, PipelinesUndeployResponse401, PipelinesUndeployResponse500]]:
    """Undeploy pipeline

     Undeploys a previously deployed pipeline.

    Args:
        json_body (PipelinesUndeployJsonBody):  Request to undeploy a pipeline by either its own
            identifier,  or the deployment identifier.

    Returns:
        Response[Union[Optional[PipelinesUndeployResponse200], PipelinesUndeployResponse400, PipelinesUndeployResponse401, PipelinesUndeployResponse500]]
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
    json_body: PipelinesUndeployJsonBody,

) -> Optional[Union[Optional[PipelinesUndeployResponse200], PipelinesUndeployResponse400, PipelinesUndeployResponse401, PipelinesUndeployResponse500]]:
    """Undeploy pipeline

     Undeploys a previously deployed pipeline.

    Args:
        json_body (PipelinesUndeployJsonBody):  Request to undeploy a pipeline by either its own
            identifier,  or the deployment identifier.

    Returns:
        Response[Union[Optional[PipelinesUndeployResponse200], PipelinesUndeployResponse400, PipelinesUndeployResponse401, PipelinesUndeployResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
