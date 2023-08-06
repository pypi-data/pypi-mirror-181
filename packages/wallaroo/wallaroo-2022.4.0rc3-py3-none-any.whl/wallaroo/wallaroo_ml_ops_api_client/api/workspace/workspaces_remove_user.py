from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.workspaces_remove_user_json_body import \
    WorkspacesRemoveUserJsonBody
from ...models.workspaces_remove_user_response_200 import \
    WorkspacesRemoveUserResponse200
from ...models.workspaces_remove_user_response_400 import \
    WorkspacesRemoveUserResponse400
from ...models.workspaces_remove_user_response_401 import \
    WorkspacesRemoveUserResponse401
from ...models.workspaces_remove_user_response_500 import \
    WorkspacesRemoveUserResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: WorkspacesRemoveUserJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/workspaces/remove_user".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[WorkspacesRemoveUserResponse200, WorkspacesRemoveUserResponse400, WorkspacesRemoveUserResponse401, WorkspacesRemoveUserResponse500]]:
    if response.status_code == 500:
        response_500 = WorkspacesRemoveUserResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = WorkspacesRemoveUserResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = WorkspacesRemoveUserResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = WorkspacesRemoveUserResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[WorkspacesRemoveUserResponse200, WorkspacesRemoveUserResponse400, WorkspacesRemoveUserResponse401, WorkspacesRemoveUserResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: WorkspacesRemoveUserJsonBody,

) -> Response[Union[WorkspacesRemoveUserResponse200, WorkspacesRemoveUserResponse400, WorkspacesRemoveUserResponse401, WorkspacesRemoveUserResponse500]]:
    """Removes a user from a workspace

     Remove a User from a given Workspace

    Args:
        json_body (WorkspacesRemoveUserJsonBody):  Request to remove a User from a Workspace

    Returns:
        Response[Union[WorkspacesRemoveUserResponse200, WorkspacesRemoveUserResponse400, WorkspacesRemoveUserResponse401, WorkspacesRemoveUserResponse500]]
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
    json_body: WorkspacesRemoveUserJsonBody,

) -> Optional[Union[WorkspacesRemoveUserResponse200, WorkspacesRemoveUserResponse400, WorkspacesRemoveUserResponse401, WorkspacesRemoveUserResponse500]]:
    """Removes a user from a workspace

     Remove a User from a given Workspace

    Args:
        json_body (WorkspacesRemoveUserJsonBody):  Request to remove a User from a Workspace

    Returns:
        Response[Union[WorkspacesRemoveUserResponse200, WorkspacesRemoveUserResponse400, WorkspacesRemoveUserResponse401, WorkspacesRemoveUserResponse500]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: WorkspacesRemoveUserJsonBody,

) -> Response[Union[WorkspacesRemoveUserResponse200, WorkspacesRemoveUserResponse400, WorkspacesRemoveUserResponse401, WorkspacesRemoveUserResponse500]]:
    """Removes a user from a workspace

     Remove a User from a given Workspace

    Args:
        json_body (WorkspacesRemoveUserJsonBody):  Request to remove a User from a Workspace

    Returns:
        Response[Union[WorkspacesRemoveUserResponse200, WorkspacesRemoveUserResponse400, WorkspacesRemoveUserResponse401, WorkspacesRemoveUserResponse500]]
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
    json_body: WorkspacesRemoveUserJsonBody,

) -> Optional[Union[WorkspacesRemoveUserResponse200, WorkspacesRemoveUserResponse400, WorkspacesRemoveUserResponse401, WorkspacesRemoveUserResponse500]]:
    """Removes a user from a workspace

     Remove a User from a given Workspace

    Args:
        json_body (WorkspacesRemoveUserJsonBody):  Request to remove a User from a Workspace

    Returns:
        Response[Union[WorkspacesRemoveUserResponse200, WorkspacesRemoveUserResponse400, WorkspacesRemoveUserResponse401, WorkspacesRemoveUserResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
