from aiohttp import ClientSession


class HTTPClient:
    def __init__(self, base_url: str, api_key: str):
        self._session = ClientSession(
            base_url=base_url,
            headers={
                "Authorization": "Bearer " + api_key,
                "Content-Type": "application/json"
            }
        )


class IMEICheckClient(HTTPClient):
    async def check(self, imei: str):
        async with self._session.post(
            url="/v1/checks",
            json={"deviceId": imei, "serviceId": 12}
        ) as response:
            results = await response.json()

            return {
                "status": results["status"],
                "properties": results["properties"]
            }
