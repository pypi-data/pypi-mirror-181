from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.models_upload_stream_response_200 import \
    ModelsUploadStreamResponse200
from ...models.models_upload_stream_response_400 import \
    ModelsUploadStreamResponse400
from ...models.models_upload_stream_response_401 import \
    ModelsUploadStreamResponse401
from ...models.models_upload_stream_response_500 import \
    ModelsUploadStreamResponse500
from ...models.models_upload_stream_visibility import \
    ModelsUploadStreamVisibility
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    name: str,
    filename: str,
    visibility: ModelsUploadStreamVisibility,
    workspace_id: int,

) -> Dict[str, Any]:
    url = "{}/v1/api/models/upload_stream".format(
        client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    params: Dict[str, Any] = {}
    params["name"] = name


    params["filename"] = filename


    json_visibility = visibility.value

    params["visibility"] = json_visibility


    params["workspace_id"] = workspace_id



    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    

    

    return {
	    "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ModelsUploadStreamResponse200, ModelsUploadStreamResponse400, ModelsUploadStreamResponse401, ModelsUploadStreamResponse500]]:
    if response.status_code == 500:
        response_500 = ModelsUploadStreamResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = ModelsUploadStreamResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = ModelsUploadStreamResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = ModelsUploadStreamResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ModelsUploadStreamResponse200, ModelsUploadStreamResponse400, ModelsUploadStreamResponse401, ModelsUploadStreamResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    name: str,
    filename: str,
    visibility: ModelsUploadStreamVisibility,
    workspace_id: int,

) -> Response[Union[ModelsUploadStreamResponse200, ModelsUploadStreamResponse400, ModelsUploadStreamResponse401, ModelsUploadStreamResponse500]]:
    """Stream a large model directly into storage

     Streams a potentially large model directly into storage.

    Args:
        name (str):  Name of the model in the workspace.
        filename (str):  Model filename.
        visibility (ModelsUploadStreamVisibility):  Desired model visibility.
        workspace_id (int):  Workspace identifier.

    Returns:
        Response[Union[ModelsUploadStreamResponse200, ModelsUploadStreamResponse400, ModelsUploadStreamResponse401, ModelsUploadStreamResponse500]]
    """


    kwargs = _get_kwargs(
        client=client,
name=name,
filename=filename,
visibility=visibility,
workspace_id=workspace_id,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    name: str,
    filename: str,
    visibility: ModelsUploadStreamVisibility,
    workspace_id: int,

) -> Optional[Union[ModelsUploadStreamResponse200, ModelsUploadStreamResponse400, ModelsUploadStreamResponse401, ModelsUploadStreamResponse500]]:
    """Stream a large model directly into storage

     Streams a potentially large model directly into storage.

    Args:
        name (str):  Name of the model in the workspace.
        filename (str):  Model filename.
        visibility (ModelsUploadStreamVisibility):  Desired model visibility.
        workspace_id (int):  Workspace identifier.

    Returns:
        Response[Union[ModelsUploadStreamResponse200, ModelsUploadStreamResponse400, ModelsUploadStreamResponse401, ModelsUploadStreamResponse500]]
    """


    return sync_detailed(
        client=client,
name=name,
filename=filename,
visibility=visibility,
workspace_id=workspace_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    name: str,
    filename: str,
    visibility: ModelsUploadStreamVisibility,
    workspace_id: int,

) -> Response[Union[ModelsUploadStreamResponse200, ModelsUploadStreamResponse400, ModelsUploadStreamResponse401, ModelsUploadStreamResponse500]]:
    """Stream a large model directly into storage

     Streams a potentially large model directly into storage.

    Args:
        name (str):  Name of the model in the workspace.
        filename (str):  Model filename.
        visibility (ModelsUploadStreamVisibility):  Desired model visibility.
        workspace_id (int):  Workspace identifier.

    Returns:
        Response[Union[ModelsUploadStreamResponse200, ModelsUploadStreamResponse400, ModelsUploadStreamResponse401, ModelsUploadStreamResponse500]]
    """


    kwargs = _get_kwargs(
        client=client,
name=name,
filename=filename,
visibility=visibility,
workspace_id=workspace_id,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    name: str,
    filename: str,
    visibility: ModelsUploadStreamVisibility,
    workspace_id: int,

) -> Optional[Union[ModelsUploadStreamResponse200, ModelsUploadStreamResponse400, ModelsUploadStreamResponse401, ModelsUploadStreamResponse500]]:
    """Stream a large model directly into storage

     Streams a potentially large model directly into storage.

    Args:
        name (str):  Name of the model in the workspace.
        filename (str):  Model filename.
        visibility (ModelsUploadStreamVisibility):  Desired model visibility.
        workspace_id (int):  Workspace identifier.

    Returns:
        Response[Union[ModelsUploadStreamResponse200, ModelsUploadStreamResponse400, ModelsUploadStreamResponse401, ModelsUploadStreamResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
name=name,
filename=filename,
visibility=visibility,
workspace_id=workspace_id,

    )).parsed
