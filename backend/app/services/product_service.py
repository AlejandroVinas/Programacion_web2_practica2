from app.core.exceptions import AppError, NotFoundError
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get_all_products(self, name: str | None = None) -> list[dict]:
        return [self._public_product(product) for product in self.product_repository.find_all(name)]

    def create_product(self, data: dict) -> dict:
        self._validate_product_data(data, partial=False)
        product = self.product_repository.create(data)
        return self._public_product(product)

    def update_product(self, product_id: str, data: dict) -> dict:
        if not self.product_repository.find_by_id(product_id):
            raise NotFoundError("Producto no encontrado")
        self._validate_product_data(data, partial=True)
        product = self.product_repository.update(product_id, data)
        return self._public_product(product)

    def delete_product(self, product_id: str) -> None:
        if not self.product_repository.find_by_id(product_id):
            raise NotFoundError("Producto no encontrado")
        self.product_repository.delete(product_id)

    @staticmethod
    def _validate_product_data(data: dict, partial: bool) -> None:
        if not partial and not data.get("nombre"):
            raise AppError("El nombre es obligatorio", 400)
        if not partial and data.get("precio") is None:
            raise AppError("El precio es obligatorio", 400)
        if "nombre" in data and data["nombre"] is not None and not str(data["nombre"]).strip():
            raise AppError("El nombre es obligatorio", 400)
        if "precio" in data and data["precio"] is not None and float(data["precio"]) <= 0:
            raise AppError("El precio debe ser mayor que 0", 400)

    @staticmethod
    def _public_product(product: dict) -> dict:
        return {
            "_id": product["_id"],
            "nombre": product["nombre"],
            "precio": float(product["precio"]),
            "imagen": product.get("imagen"),
            "activo": bool(product.get("activo", True)),
        }
