import aiohttp
from typing import Union


async def send_request(url: str, request_type: str, json_convert: bool = True) -> Union[dict, str]:
    """
    Wrapper for aiohttp requests
    :param url: url for request
    :param request_type: http method (post, get, delete, patch)
    :param json_convert: apply json to response text
    :return: answer as json
    """
    async with aiohttp.ClientSession() as session:
        async with getattr(session, request_type)(url) as resp:
            return resp.json() if json_convert else resp.text()
