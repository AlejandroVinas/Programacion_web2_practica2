from pydantic import BaseModel, Field


class ProductUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    precio: float | None = Field(default=None, gt=0)
    imagen: str | None = None
    activo: bool | None = None


class ProductResponse(BaseModel):
    _id: str
    nombre: str
    precio: float
    imagen: str | None = None
    activo: bool = True
