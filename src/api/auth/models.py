from pydantic import BaseModel


class User(BaseModel):
    username: int


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: int
