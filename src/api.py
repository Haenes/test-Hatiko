from typing import Annotated

from fastapi import FastAPI, Depends
from fastapi.middleware.gzip import GZipMiddleware

from api.auth.jwt_bearer import get_current_user
from api.auth.router import router as auth_router
from api.http_client import IMEICheckClient
from api.models import IMEI
from db.user import User
from settings import Settings


imei_api = IMEICheckClient(
    base_url="https://api.imeicheck.net",
    api_key=Settings.IMEI_API_TOKEN
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
) -> dict[str, str | dict]:
    results = await imei_api.check(imei.imei)
    return results
