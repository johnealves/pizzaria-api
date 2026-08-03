from pydantic import BaseModel


class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: bool | None = True
    admin: bool | None = False

    class Config:
        from_attributes = True
