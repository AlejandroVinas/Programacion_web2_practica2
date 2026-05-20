from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str = Field(min_length=4, max_length=100)
    role: Literal["admin", "user"] = "user"

    @field_validator("username")
    @classmethod
    def normalize_username(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El usuario no puede estar vacío")
        return value


class UserUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str | None = Field(default=None, min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_.-]+$")
    password: str | None = Field(default=None, min_length=4, max_length=100)
    role: Literal["admin", "user"] | None = None

    @field_validator("username")
    @classmethod
    def normalize_username(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("El usuario no puede estar vacío")
        return value


class UserResponse(BaseModel):
    _id: str
    username: str
    role: Literal["admin", "user"]
