from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.assays_run_interactive_baseline_json_body import \
    AssaysRunInteractiveBaselineJsonBody
from ...models.assays_run_interactive_baseline_response_200 import \
    AssaysRunInteractiveBaselineResponse200
from ...models.assays_run_interactive_baseline_response_400 import \
    AssaysRunInteractiveBaselineResponse400
from ...models.assays_run_interactive_baseline_response_401 import \
    AssaysRunInteractiveBaselineResponse401
from ...models.assays_run_interactive_baseline_response_500 import \
    AssaysRunInteractiveBaselineResponse500
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: AssaysRunInteractiveBaselineJsonBody,

) -> Dict[str, Any]:
    url = "{}/v1/api/assays/run_interactive_baseline".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[AssaysRunInteractiveBaselineResponse400, AssaysRunInteractiveBaselineResponse401, AssaysRunInteractiveBaselineResponse500, Optional[AssaysRunInteractiveBaselineResponse200]]]:
    if response.status_code == 500:
        response_500 = AssaysRunInteractiveBaselineResponse500.from_dict(response.json())



        return response_500
    if response.status_code == 400:
        response_400 = AssaysRunInteractiveBaselineResponse400.from_dict(response.json())



        return response_400
    if response.status_code == 401:
        response_401 = AssaysRunInteractiveBaselineResponse401.from_dict(response.json())



        return response_401
    if response.status_code == 200:
        _response_200 = response.json()
        response_200: Optional[AssaysRunInteractiveBaselineResponse200]
        if _response_200 is None:
            response_200 = None
        else:
            response_200 = AssaysRunInteractiveBaselineResponse200.from_dict(_response_200)



        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AssaysRunInteractiveBaselineResponse400, AssaysRunInteractiveBaselineResponse401, AssaysRunInteractiveBaselineResponse500, Optional[AssaysRunInteractiveBaselineResponse200]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: AssaysRunInteractiveBaselineJsonBody,

) -> Response[Union[AssaysRunInteractiveBaselineResponse400, AssaysRunInteractiveBaselineResponse401, AssaysRunInteractiveBaselineResponse500, Optional[AssaysRunInteractiveBaselineResponse200]]]:
    """Create interactive baseline

     Creates an interactive assay baseline.

    Args:
        json_body (AssaysRunInteractiveBaselineJsonBody):  Request for interactive assay baseline.

    Returns:
        Response[Union[AssaysRunInteractiveBaselineResponse400, AssaysRunInteractiveBaselineResponse401, AssaysRunInteractiveBaselineResponse500, Optional[AssaysRunInteractiveBaselineResponse200]]]
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
    json_body: AssaysRunInteractiveBaselineJsonBody,

) -> Optional[Union[AssaysRunInteractiveBaselineResponse400, AssaysRunInteractiveBaselineResponse401, AssaysRunInteractiveBaselineResponse500, Optional[AssaysRunInteractiveBaselineResponse200]]]:
    """Create interactive baseline

     Creates an interactive assay baseline.

    Args:
        json_body (AssaysRunInteractiveBaselineJsonBody):  Request for interactive assay baseline.

    Returns:
        Response[Union[AssaysRunInteractiveBaselineResponse400, AssaysRunInteractiveBaselineResponse401, AssaysRunInteractiveBaselineResponse500, Optional[AssaysRunInteractiveBaselineResponse200]]]
    """


    return sync_detailed(
        client=client,
json_body=json_body,

    ).parsed

async def asyncio_detailed(
    *,
    client: Client,
    json_body: AssaysRunInteractiveBaselineJsonBody,

) -> Response[Union[AssaysRunInteractiveBaselineResponse400, AssaysRunInteractiveBaselineResponse401, AssaysRunInteractiveBaselineResponse500, Optional[AssaysRunInteractiveBaselineResponse200]]]:
    """Create interactive baseline

     Creates an interactive assay baseline.

    Args:
        json_body (AssaysRunInteractiveBaselineJsonBody):  Request for interactive assay baseline.

    Returns:
        Response[Union[AssaysRunInteractiveBaselineResponse400, AssaysRunInteractiveBaselineResponse401, AssaysRunInteractiveBaselineResponse500, Optional[AssaysRunInteractiveBaselineResponse200]]]
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
    json_body: AssaysRunInteractiveBaselineJsonBody,

) -> Optional[Union[AssaysRunInteractiveBaselineResponse400, AssaysRunInteractiveBaselineResponse401, AssaysRunInteractiveBaselineResponse500, Optional[AssaysRunInteractiveBaselineResponse200]]]:
    """Create interactive baseline

     Creates an interactive assay baseline.

    Args:
        json_body (AssaysRunInteractiveBaselineJsonBody):  Request for interactive assay baseline.

    Returns:
        Response[Union[AssaysRunInteractiveBaselineResponse400, AssaysRunInteractiveBaselineResponse401, AssaysRunInteractiveBaselineResponse500, Optional[AssaysRunInteractiveBaselineResponse200]]]
    """


    return (await asyncio_detailed(
        client=client,
json_body=json_body,

    )).parsed
