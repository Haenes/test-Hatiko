import os
from aiohttp import ClientSession
from dotenv import load_dotenv


load_dotenv()
API_BASE_URL = os.environ.get("API_BASE_URL")


async def register(
    session: ClientSession,
    email: str,
    password: str
) -> dict[str, str] | str:
    data = {"username": email, "password": password}

    async with session.post("/auth/register", data=data) as r:
        if r.status != 200:
            return {"error": "Возникла ошибка!"}
        res = await r.json()

        if "access_token" in res:
            return res["access_token"]


async def get_token(
    session: ClientSession,
    email: str,
    password: str
) -> dict[str, str] | str:
    data = {"username": email, "password": password}

    async with session.post("/auth/token", data=data) as r:
        if r.status == 401:
            return {"error": "Неверный юзернейм или пароль"}
        res = await r.json()

        if "access_token" in res:
            return res["access_token"]


async def check_imei(
    session: ClientSession,
    api_token: str,
    imei: str,
) -> dict[str, str]:

    async with session.post(
        url="/check-imei",
        json={"imei": imei},
        headers={"Authorization": f"Bearer {api_token}"}
    ) as r:
        res = await r.json()
        return res
