from os import environ
from dotenv import load_dotenv
from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.middleware.gzip import GZipMiddleware

from backend.auth.jwt_bearer import get_current_user
from backend.auth.router import router as auth_router
from backend.http_client import IMEICheckClient
from backend.models import IMEI
from db.user import User


load_dotenv()
IMEI_API_TOKEN = environ.get("IMEI_API_TOKEN")

imei_api = IMEICheckClient(
    base_url="https://api.imeicheck.net",
    api_key=IMEI_API_TOKEN
)

app = FastAPI(
    title="test-Hatiko-API",
    license_info={
        "name": "MIT",
        "url": "https://github.com/Haenes/test-Hatiko/blob/main/LICENSE"
    },
)

app.add_middleware(GZipMiddleware, compresslevel=6)
app.include_router(auth_router)


@app.post("/check-imei")
async def check_imei(
    imei: IMEI,
    current_user: Annotated[User, Depends(get_current_user)]
) -> dict:
    results = await imei_api.check(imei.imei)
    return results
