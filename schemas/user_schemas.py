from pydantic import BaseModel


class UserInfo(BaseModel):
    name: str
    email: str


class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: bool | None = True
    admin: bool | None = False

    class Config:
        from_attributes = True


class UserActionResponse(BaseModel):
    message: str
    user: UserInfo
