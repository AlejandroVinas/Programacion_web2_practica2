from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import db_session
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import LoginRequest, RegisterRequest
from app.services.auth_service import AuthService


def _service(session: Session = Depends(db_session)) -> AuthService:
    return AuthService(UserRepository(session))


def login(payload: LoginRequest, service: AuthService = Depends(_service)) -> dict:
    token = service.login(payload.username, payload.password)
    return {"token": token}


def register(payload: RegisterRequest, service: AuthService = Depends(_service)) -> dict:
    service.register(payload.username, payload.password)
    return {"message": "Usuario registrado con éxito"}
