from fastapi import APIRouter, status

from app.controllers import auth_controller

router = APIRouter(tags=["Auth"])

router.post("/login")(auth_controller.login)
router.post("/register", status_code=status.HTTP_201_CREATED)(auth_controller.register)
