from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import db_session
from app.dependencies.auth import require_admin
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate
from app.services.user_service import UserService


def _service(session: Session = Depends(db_session)) -> UserService:
    return UserService(UserRepository(session))


def get_users(
    _admin: dict = Depends(require_admin),
    service: UserService = Depends(_service),
) -> list[dict]:
    return service.get_all_users()


def create_user(
    payload: UserCreate,
    _admin: dict = Depends(require_admin),
    service: UserService = Depends(_service),
) -> dict:
    user = service.create_user(payload.model_dump())
    return {"message": "Usuario creado con éxito", "user": user}


def update_user(
    user_id: str,
    payload: UserUpdate,
    _admin: dict = Depends(require_admin),
    service: UserService = Depends(_service),
) -> dict:
    return service.update_user(user_id, payload.model_dump(exclude_unset=True))


def delete_user(
    user_id: str,
    _admin: dict = Depends(require_admin),
    service: UserService = Depends(_service),
) -> dict:
    service.delete_user(user_id)
    return {"message": "Usuario eliminado"}
