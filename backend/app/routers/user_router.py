from fastapi import APIRouter, status

from app.controllers import user_controller

router = APIRouter(prefix="/users", tags=["Usuarios"])

router.get("")(user_controller.get_users)
router.get("/")(user_controller.get_users)
router.post("", status_code=status.HTTP_201_CREATED)(user_controller.create_user)
router.post("/", status_code=status.HTTP_201_CREATED)(user_controller.create_user)
router.put("/{user_id}")(user_controller.update_user)
router.delete("/{user_id}")(user_controller.delete_user)
