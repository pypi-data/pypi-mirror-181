from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.models_upload_multipart_data import ModelsUploadMultipartData
from ...models.models_upload_response_200 import ModelsUploadResponse200
from ...models.models_upload_response_400 import ModelsUploadResponse400
from ...models.models_upload_response_401 import ModelsUploadResponse401
from ...models.models_upload_response_500 import ModelsUploadResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    multipart_data: ModelsUploadMultipartData,

) -> Dict[str, Any]:
    url = "{}/v1/api/models/upload".format(
        client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    

    

    

    

    multipart_multipart_data = multipart_data.to_multipart()




    return {
	    "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[ModelsUploadResponse200, ModelsUploadResponse400, ModelsUploadResponse401, ModelsUploadResponse500]]:
    if response.status_code == 500:
        response_500 = ModelsUploadResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = ModelsUploadResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = ModelsUploadResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = ModelsUploadResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[ModelsUploadResponse200, ModelsUploadResponse400, ModelsUploadResponse401, ModelsUploadResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    multipart_data: ModelsUploadMultipartData,

) -> Response[Union[ModelsUploadResponse200, ModelsUploadResponse400, ModelsUploadResponse401, ModelsUploadResponse500]]:
    """Uploads a model to storage

     Uploads a model to storage.

    Args:
        multipart_data (ModelsUploadMultipartData):  Model upload request.

    Returns:
        Response[Union[ModelsUploadResponse200, ModelsUploadResponse400, ModelsUploadResponse401, ModelsUploadResponse500]]
    """


    kwargs = _get_kwargs(
        client=client,
multipart_data=multipart_data,

    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)

def sync(
    *,
    client: Client,
    multipart_data: ModelsUploadMultipartData,

) -> Optional[Union[ModelsUploadResponse200, ModelsUploadResponse400, ModelsUploadResponse401, ModelsUploadResponse500]]:
    """Uploads a model to storage

     Uploads a model to storage.

    Args:
        multipart_data (ModelsUploadMultipartData):  Model upload request.

    Returns:
        Response[Union[ModelsUploadResponse200, ModelsUploadResponse400, ModelsUploadResponse401, ModelsUploadResponse500]]
    """


    return sync_detailed(
        client=client,
multipart_data=multipart_data,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: ModelsUploadMultipartData,

) -> Response[Union[ModelsUploadResponse200, ModelsUploadResponse400, ModelsUploadResponse401, ModelsUploadResponse500]]:
    """Uploads a model to storage

     Uploads a model to storage.

    Args:
        multipart_data (ModelsUploadMultipartData):  Model upload request.

    Returns:
        Response[Union[ModelsUploadResponse200, ModelsUploadResponse400, ModelsUploadResponse401, ModelsUploadResponse500]]
    """


    kwargs = _get_kwargs(
        client=client,
multipart_data=multipart_data,

    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(
            **kwargs
        )

    return _build_response(response=response)

async def asyncio(
    *,
    client: Client,
    multipart_data: ModelsUploadMultipartData,

) -> Optional[Union[ModelsUploadResponse200, ModelsUploadResponse400, ModelsUploadResponse401, ModelsUploadResponse500]]:
    """Uploads a model to storage

     Uploads a model to storage.

    Args:
        multipart_data (ModelsUploadMultipartData):  Model upload request.

    Returns:
        Response[Union[ModelsUploadResponse200, ModelsUploadResponse400, ModelsUploadResponse401, ModelsUploadResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
multipart_data=multipart_data,

    )).parsed
