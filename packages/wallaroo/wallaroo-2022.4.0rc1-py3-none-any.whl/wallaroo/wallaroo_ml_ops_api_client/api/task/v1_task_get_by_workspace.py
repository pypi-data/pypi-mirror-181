from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.v1_task_get_by_workspace_json_body import \
    V1TaskGetByWorkspaceJsonBody
from ...models.v1_task_get_by_workspace_response_200 import \
    V1TaskGetByWorkspaceResponse200
from ...models.v1_task_get_by_workspace_response_400 import \
    V1TaskGetByWorkspaceResponse400
from ...models.v1_task_get_by_workspace_response_401 import \
    V1TaskGetByWorkspaceResponse401
from ...models.v1_task_get_by_workspace_response_500 import \
    V1TaskGetByWorkspaceResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: V1TaskGetByWorkspaceJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/tasks/get_by_workspace".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[V1TaskGetByWorkspaceResponse200, V1TaskGetByWorkspaceResponse400, V1TaskGetByWorkspaceResponse401, V1TaskGetByWorkspaceResponse500]]:
    if response.status_code == 500:
        response_500 = V1TaskGetByWorkspaceResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = V1TaskGetByWorkspaceResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = V1TaskGetByWorkspaceResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = V1TaskGetByWorkspaceResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[V1TaskGetByWorkspaceResponse200, V1TaskGetByWorkspaceResponse400, V1TaskGetByWorkspaceResponse401, V1TaskGetByWorkspaceResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: V1TaskGetByWorkspaceJsonBody,

) -> Response[Union[V1TaskGetByWorkspaceResponse200, V1TaskGetByWorkspaceResponse400, V1TaskGetByWorkspaceResponse401, V1TaskGetByWorkspaceResponse500]]:
    """Get task by workspace id.

     Retrieve a list of tasks owned by this workspace.

    Args:
        json_body (V1TaskGetByWorkspaceJsonBody):  Body for request to /tasks/get_by_workspace

    Returns:
        Response[Union[V1TaskGetByWorkspaceResponse200, V1TaskGetByWorkspaceResponse400, V1TaskGetByWorkspaceResponse401, V1TaskGetByWorkspaceResponse500]]
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
    json_body: V1TaskGetByWorkspaceJsonBody,

) -> Optional[Union[V1TaskGetByWorkspaceResponse200, V1TaskGetByWorkspaceResponse400, V1TaskGetByWorkspaceResponse401, V1TaskGetByWorkspaceResponse500]]:
    """Get task by workspace id.

     Retrieve a list of tasks owned by this workspace.

    Args:
        json_body (V1TaskGetByWorkspaceJsonBody):  Body for request to /tasks/get_by_workspace

    Returns:
        Response[Union[V1TaskGetByWorkspaceResponse200, V1TaskGetByWorkspaceResponse400, V1TaskGetByWorkspaceResponse401, V1TaskGetByWorkspaceResponse500]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: V1TaskGetByWorkspaceJsonBody,

) -> Response[Union[V1TaskGetByWorkspaceResponse200, V1TaskGetByWorkspaceResponse400, V1TaskGetByWorkspaceResponse401, V1TaskGetByWorkspaceResponse500]]:
    """Get task by workspace id.

     Retrieve a list of tasks owned by this workspace.

    Args:
        json_body (V1TaskGetByWorkspaceJsonBody):  Body for request to /tasks/get_by_workspace

    Returns:
        Response[Union[V1TaskGetByWorkspaceResponse200, V1TaskGetByWorkspaceResponse400, V1TaskGetByWorkspaceResponse401, V1TaskGetByWorkspaceResponse500]]
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
    json_body: V1TaskGetByWorkspaceJsonBody,

) -> Optional[Union[V1TaskGetByWorkspaceResponse200, V1TaskGetByWorkspaceResponse400, V1TaskGetByWorkspaceResponse401, V1TaskGetByWorkspaceResponse500]]:
    """Get task by workspace id.

     Retrieve a list of tasks owned by this workspace.

    Args:
        json_body (V1TaskGetByWorkspaceJsonBody):  Body for request to /tasks/get_by_workspace

    Returns:
        Response[Union[V1TaskGetByWorkspaceResponse200, V1TaskGetByWorkspaceResponse400, V1TaskGetByWorkspaceResponse401, V1TaskGetByWorkspaceResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
