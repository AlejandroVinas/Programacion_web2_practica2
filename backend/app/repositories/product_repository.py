from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ProductModel


def _parse_id(product_id: str | int) -> int | None:
    try:
        return int(product_id)
    except (TypeError, ValueError):
        return None


def _to_product(product: ProductModel | None) -> dict[str, Any] | None:
    if product is None:
        return None
    return {
        "_id": str(product.id),
        "id": product.id,
        "nombre": product.nombre,
        "precio": float(product.precio),
        "imagen": product.imagen,
        "activo": bool(product.activo),
    }


class ProductRepository:
    """Repositorio ORM: todo el acceso a datos de productos queda encapsulado aquí."""

    def __init__(self, session: Session):
        self.session = session

    def find_all(self, name_filter: str | None = None) -> list[dict[str, Any]]:
        query = select(ProductModel)
        if name_filter:
            query = query.where(ProductModel.nombre.ilike(f"%{name_filter.strip()}%"))
        query = query.order_by(ProductModel.id.desc())
        products = self.session.scalars(query).all()
        return [_to_product(product) for product in products if product]

    def find_by_id(self, product_id: str | int) -> dict[str, Any] | None:
        parsed_id = _parse_id(product_id)
        if parsed_id is None:
            return None
        product = self.session.get(ProductModel, parsed_id)
        return _to_product(product)

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        product = ProductModel(
            nombre=data["nombre"],
            precio=float(data["precio"]),
            imagen=data.get("imagen"),
            activo=bool(data.get("activo", True)),
        )
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return _to_product(product)

    def update(self, product_id: str, data: dict[str, Any]) -> dict[str, Any] | None:
        parsed_id = _parse_id(product_id)
        if parsed_id is None:
            return None
        product = self.session.get(ProductModel, parsed_id)
        if product is None:
            return None

        for key in ["nombre", "precio", "imagen", "activo"]:
            if key in data and data[key] is not None:
                setattr(product, key, bool(data[key]) if key == "activo" else data[key])

        self.session.commit()
        self.session.refresh(product)
        return _to_product(product)

    def delete(self, product_id: str) -> None:
        parsed_id = _parse_id(product_id)
        if parsed_id is None:
            return
        product = self.session.get(ProductModel, parsed_id)
        if product is not None:
            self.session.delete(product)
            self.session.commit()
