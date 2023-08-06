from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.assays_set_active_json_body import AssaysSetActiveJsonBody
from ...models.assays_set_active_response_200 import AssaysSetActiveResponse200
from ...models.assays_set_active_response_400 import AssaysSetActiveResponse400
from ...models.assays_set_active_response_401 import AssaysSetActiveResponse401
from ...models.assays_set_active_response_500 import AssaysSetActiveResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: AssaysSetActiveJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/assays/set_active".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[AssaysSetActiveResponse200, AssaysSetActiveResponse400, AssaysSetActiveResponse401, AssaysSetActiveResponse500]]:
    if response.status_code == 500:
        response_500 = AssaysSetActiveResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = AssaysSetActiveResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = AssaysSetActiveResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        response_200 = AssaysSetActiveResponse200.from_dict(response.json())



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AssaysSetActiveResponse200, AssaysSetActiveResponse400, AssaysSetActiveResponse401, AssaysSetActiveResponse500]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: AssaysSetActiveJsonBody,

) -> Response[Union[AssaysSetActiveResponse200, AssaysSetActiveResponse400, AssaysSetActiveResponse401, AssaysSetActiveResponse500]]:
    """Activate or deactivate assay

     Activates or deactivates an assay.

    Args:
        json_body (AssaysSetActiveJsonBody):  Request to activate or deactivate an assay.

    Returns:
        Response[Union[AssaysSetActiveResponse200, AssaysSetActiveResponse400, AssaysSetActiveResponse401, AssaysSetActiveResponse500]]
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
    json_body: AssaysSetActiveJsonBody,

) -> Optional[Union[AssaysSetActiveResponse200, AssaysSetActiveResponse400, AssaysSetActiveResponse401, AssaysSetActiveResponse500]]:
    """Activate or deactivate assay

     Activates or deactivates an assay.

    Args:
        json_body (AssaysSetActiveJsonBody):  Request to activate or deactivate an assay.

    Returns:
        Response[Union[AssaysSetActiveResponse200, AssaysSetActiveResponse400, AssaysSetActiveResponse401, AssaysSetActiveResponse500]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: AssaysSetActiveJsonBody,

) -> Response[Union[AssaysSetActiveResponse200, AssaysSetActiveResponse400, AssaysSetActiveResponse401, AssaysSetActiveResponse500]]:
    """Activate or deactivate assay

     Activates or deactivates an assay.

    Args:
        json_body (AssaysSetActiveJsonBody):  Request to activate or deactivate an assay.

    Returns:
        Response[Union[AssaysSetActiveResponse200, AssaysSetActiveResponse400, AssaysSetActiveResponse401, AssaysSetActiveResponse500]]
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
    json_body: AssaysSetActiveJsonBody,

) -> Optional[Union[AssaysSetActiveResponse200, AssaysSetActiveResponse400, AssaysSetActiveResponse401, AssaysSetActiveResponse500]]:
    """Activate or deactivate assay

     Activates or deactivates an assay.

    Args:
        json_body (AssaysSetActiveJsonBody):  Request to activate or deactivate an assay.

    Returns:
        Response[Union[AssaysSetActiveResponse200, AssaysSetActiveResponse400, AssaysSetActiveResponse401, AssaysSetActiveResponse500]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
