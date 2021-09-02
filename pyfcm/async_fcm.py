import asyncio
import aiohttp
import json

async def fetch_tasks(end_point,headers,payloads,timeout):
    """

    :param end_point (str) : FCM endpoint
    :param headers (dict) : FCM Request Headers
    :param payloads (list) : payloads contains bytes after self.parse_payload
    :param timeout (int) : FCM timeout
    :return:
    """
    fetches = [asyncio.Task(send_request(end_point=end_point,headers=headers,payload=payload,timeout=timeout)) for payload in payloads]
    return await asyncio.gather(*fetches)


async def send_request(end_point,headers,payload,timeout=5):
    """

    :param end_point (str) : FCM endpoint
    :param headers (dict) : FCM Request Headers
    :param payloads (list) : payloads contains bytes after self.parse_payload
    :param timeout (int) : FCM timeout
    :return:
    """
    timeout = aiohttp.ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(headers=headers,timeout=timeout) as session:

        async with session.post(end_point,data=payload) as res:
            result = await res.text()
            result = json.loads(result)
            return result
