from typing import Annotated

from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: str = Field(min_length=1, max_length=120)
    precio: float = Field(gt=0, le=999999)
    activo: bool = True

    @field_validator("nombre")
    @classmethod
    def nombre_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("El nombre es obligatorio")
        return value

    @classmethod
    def as_form(
        cls,
        nombre: Annotated[str, Form(min_length=1, max_length=120)],
        precio: Annotated[float, Form(gt=0, le=999999)],
        activo: Annotated[bool, Form()] = True,
    ) -> "ProductCreate":
        return cls(nombre=nombre, precio=precio, activo=activo)


class ProductUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    precio: float | None = Field(default=None, gt=0, le=999999)
    imagen: str | None = Field(default=None, max_length=255)
    activo: bool | None = None

    @field_validator("nombre")
    @classmethod
    def nombre_not_blank(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("El nombre es obligatorio")
        return value


class ProductResponse(BaseModel):
    _id: str
    nombre: str
    precio: float
    imagen: str | None = None
    activo: bool = True
