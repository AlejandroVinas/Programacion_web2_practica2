from app.core.exceptions import NotFoundError
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository

    def get_all_products(self, name: str | None = None) -> list[dict]:
        normalized_name = name.strip() if name else None
        return [self._public_product(product) for product in self.product_repository.find_all(normalized_name)]

    def create_product(self, data: dict) -> dict:
        product = self.product_repository.create(data)
        return self._public_product(product)

    def update_product(self, product_id: str, data: dict) -> dict:
        if not self.product_repository.find_by_id(product_id):
            raise NotFoundError("Producto no encontrado")
        product = self.product_repository.update(product_id, data)
        return self._public_product(product)

    def delete_product(self, product_id: str) -> None:
        if not self.product_repository.find_by_id(product_id):
            raise NotFoundError("Producto no encontrado")
        self.product_repository.delete(product_id)

    @staticmethod
    def _public_product(product: dict) -> dict:
        return {
            "_id": product["_id"],
            "nombre": product["nombre"],
            "precio": float(product["precio"]),
            "imagen": product.get("imagen"),
            "activo": bool(product.get("activo", True)),
        }
