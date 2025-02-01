from pydantic import BaseModel


class IMEI(BaseModel):
    imei: str
