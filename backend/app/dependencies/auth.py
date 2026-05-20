import sqlite3
from typing import Annotated

import jwt
from fastapi import Depends, Header

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.database import db_session
from app.repositories.user_repository import UserRepository


def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    conn: sqlite3.Connection = Depends(db_session),
) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedError("Token requerido")

    token = authorization.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise ForbiddenError("Token expirado")
    except jwt.PyJWTError:
        raise ForbiddenError("Token inválido")

    user_id = payload.get("id")
    if not user_id:
        raise ForbiddenError("Token inválido")

    user = UserRepository(conn).find_by_id(user_id)
    if not user:
        raise UnauthorizedError("Usuario no encontrado")
    return user


def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    if current_user.get("role") != "admin":
        raise ForbiddenError("Solo admin")
    return current_user
