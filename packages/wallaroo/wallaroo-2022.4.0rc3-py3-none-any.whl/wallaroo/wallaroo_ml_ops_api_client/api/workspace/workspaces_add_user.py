from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.workspaces_add_user_json_body import WorkspacesAddUserJsonBody
from ...models.workspaces_add_user_response_200 import \
    WorkspacesAddUserResponse200
from ...models.workspaces_add_user_response_400 import \
    WorkspacesAddUserResponse400
from ...models.workspaces_add_user_response_401 import \
    WorkspacesAddUserResponse401
from ...models.workspaces_add_user_response_500 import \
    WorkspacesAddUserResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: WorkspacesAddUserJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/workspaces/add_user".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[WorkspacesAddUserResponse200, WorkspacesAddUserResponse400, WorkspacesAddUserResponse401, WorkspacesAddUserResponse500]]:
    if response.status_code == 500:
        response_500 = WorkspacesAddUserResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = WorkspacesAddUserResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = WorkspacesAddUserResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = WorkspacesAddUserResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[WorkspacesAddUserResponse200, WorkspacesAddUserResponse400, WorkspacesAddUserResponse401, WorkspacesAddUserResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: WorkspacesAddUserJsonBody,

) -> Response[Union[WorkspacesAddUserResponse200, WorkspacesAddUserResponse400, WorkspacesAddUserResponse401, WorkspacesAddUserResponse500]]:
    """Add user to workspace

     Adds an existing user to the given workspace.

    Args:
        json_body (WorkspacesAddUserJsonBody):  Request for adding a user to workspace.

    Returns:
        Response[Union[WorkspacesAddUserResponse200, WorkspacesAddUserResponse400, WorkspacesAddUserResponse401, WorkspacesAddUserResponse500]]
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
    json_body: WorkspacesAddUserJsonBody,

) -> Optional[Union[WorkspacesAddUserResponse200, WorkspacesAddUserResponse400, WorkspacesAddUserResponse401, WorkspacesAddUserResponse500]]:
    """Add user to workspace

     Adds an existing user to the given workspace.

    Args:
        json_body (WorkspacesAddUserJsonBody):  Request for adding a user to workspace.

    Returns:
        Response[Union[WorkspacesAddUserResponse200, WorkspacesAddUserResponse400, WorkspacesAddUserResponse401, WorkspacesAddUserResponse500]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: WorkspacesAddUserJsonBody,

) -> Response[Union[WorkspacesAddUserResponse200, WorkspacesAddUserResponse400, WorkspacesAddUserResponse401, WorkspacesAddUserResponse500]]:
    """Add user to workspace

     Adds an existing user to the given workspace.

    Args:
        json_body (WorkspacesAddUserJsonBody):  Request for adding a user to workspace.

    Returns:
        Response[Union[WorkspacesAddUserResponse200, WorkspacesAddUserResponse400, WorkspacesAddUserResponse401, WorkspacesAddUserResponse500]]
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
    json_body: WorkspacesAddUserJsonBody,

) -> Optional[Union[WorkspacesAddUserResponse200, WorkspacesAddUserResponse400, WorkspacesAddUserResponse401, WorkspacesAddUserResponse500]]:
    """Add user to workspace

     Adds an existing user to the given workspace.

    Args:
        json_body (WorkspacesAddUserJsonBody):  Request for adding a user to workspace.

    Returns:
        Response[Union[WorkspacesAddUserResponse200, WorkspacesAddUserResponse400, WorkspacesAddUserResponse401, WorkspacesAddUserResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
