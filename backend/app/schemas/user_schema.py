from pydantic import BaseModel, Field
from typing import Literal


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=4, max_length=100)
    role: Literal["admin", "user"] = "user"


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=50)
    password: str | None = Field(default=None, min_length=4, max_length=100)
    role: Literal["admin", "user"] | None = None


class UserResponse(BaseModel):
    _id: str
    username: str
    role: Literal["admin", "user"]
