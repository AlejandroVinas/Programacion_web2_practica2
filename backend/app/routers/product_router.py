from fastapi import APIRouter, status

from app.controllers import product_controller

router = APIRouter(prefix="/productos", tags=["Productos"])

router.get("")(product_controller.get_products)
router.get("/")(product_controller.get_products)
router.post("", status_code=status.HTTP_201_CREATED)(product_controller.create_product)
router.post("/", status_code=status.HTTP_201_CREATED)(product_controller.create_product)
router.put("/{product_id}")(product_controller.update_product)
router.delete("/{product_id}")(product_controller.delete_product)
