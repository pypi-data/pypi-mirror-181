from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.v1_task_get_by_status_json_body import V1TaskGetByStatusJsonBody
from ...models.v1_task_get_by_status_response_200 import \
    V1TaskGetByStatusResponse200
from ...models.v1_task_get_by_status_response_400 import \
    V1TaskGetByStatusResponse400
from ...models.v1_task_get_by_status_response_401 import \
    V1TaskGetByStatusResponse401
from ...models.v1_task_get_by_status_response_500 import \
    V1TaskGetByStatusResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: V1TaskGetByStatusJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/tasks/get_by_status".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[V1TaskGetByStatusResponse200, V1TaskGetByStatusResponse400, V1TaskGetByStatusResponse401, V1TaskGetByStatusResponse500]]:
    if response.status_code == 500:
        response_500 = V1TaskGetByStatusResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = V1TaskGetByStatusResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = V1TaskGetByStatusResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = V1TaskGetByStatusResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[V1TaskGetByStatusResponse200, V1TaskGetByStatusResponse400, V1TaskGetByStatusResponse401, V1TaskGetByStatusResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: V1TaskGetByStatusJsonBody,

) -> Response[Union[V1TaskGetByStatusResponse200, V1TaskGetByStatusResponse400, V1TaskGetByStatusResponse401, V1TaskGetByStatusResponse500]]:
    """Get task by status.

     Retrieve list of tasks by their status.

    Args:
        json_body (V1TaskGetByStatusJsonBody):  Body for request to /tasks/get_by_status

    Returns:
        Response[Union[V1TaskGetByStatusResponse200, V1TaskGetByStatusResponse400, V1TaskGetByStatusResponse401, V1TaskGetByStatusResponse500]]
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
    json_body: V1TaskGetByStatusJsonBody,

) -> Optional[Union[V1TaskGetByStatusResponse200, V1TaskGetByStatusResponse400, V1TaskGetByStatusResponse401, V1TaskGetByStatusResponse500]]:
    """Get task by status.

     Retrieve list of tasks by their status.

    Args:
        json_body (V1TaskGetByStatusJsonBody):  Body for request to /tasks/get_by_status

    Returns:
        Response[Union[V1TaskGetByStatusResponse200, V1TaskGetByStatusResponse400, V1TaskGetByStatusResponse401, V1TaskGetByStatusResponse500]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: V1TaskGetByStatusJsonBody,

) -> Response[Union[V1TaskGetByStatusResponse200, V1TaskGetByStatusResponse400, V1TaskGetByStatusResponse401, V1TaskGetByStatusResponse500]]:
    """Get task by status.

     Retrieve list of tasks by their status.

    Args:
        json_body (V1TaskGetByStatusJsonBody):  Body for request to /tasks/get_by_status

    Returns:
        Response[Union[V1TaskGetByStatusResponse200, V1TaskGetByStatusResponse400, V1TaskGetByStatusResponse401, V1TaskGetByStatusResponse500]]
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
    json_body: V1TaskGetByStatusJsonBody,

) -> Optional[Union[V1TaskGetByStatusResponse200, V1TaskGetByStatusResponse400, V1TaskGetByStatusResponse401, V1TaskGetByStatusResponse500]]:
    """Get task by status.

     Retrieve list of tasks by their status.

    Args:
        json_body (V1TaskGetByStatusJsonBody):  Body for request to /tasks/get_by_status

    Returns:
        Response[Union[V1TaskGetByStatusResponse200, V1TaskGetByStatusResponse400, V1TaskGetByStatusResponse401, V1TaskGetByStatusResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
