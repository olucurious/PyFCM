import asyncio
import niquests


async def fetch_tasks(end_point, headers, payloads, timeout):
    """

    :param end_point (str) : FCM endpoint
    :param headers (dict) : FCM Request Headers
    :param payloads (list) : payloads contains bytes after self.parse_payload
    :param timeout (int) : FCM timeout
    :return:
    """
    return await asyncio.gather(
        *[
            send_request(
                end_point=end_point, headers=headers, payload=payload, timeout=timeout
            )
            for payload in payloads
        ]
    )


async def send_request(end_point, headers, payload, timeout=5):
    """

    :param end_point (str) : FCM endpoint
    :param headers (dict) : FCM Request Headers
    :param payloads (list) : payloads contains bytes after self.parse_payload
    :param timeout (int) : FCM timeout
    :return:
    """
    async with niquests.AsyncSession() as session:
        response = await session.post(
            end_point, data=payload, headers=headers, timeout=timeout
        )
        return response.json()
