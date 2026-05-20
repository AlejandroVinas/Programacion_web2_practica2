import sqlite3

from app.core.exceptions import AppError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, username: str, password: str) -> dict:
        if self.user_repository.find_by_username(username):
            raise AppError("El usuario ya existe", 400)
        try:
            user = self.user_repository.create(username, hash_password(password), "user")
        except sqlite3.IntegrityError:
            raise AppError("El usuario ya existe", 400)
        return {"_id": user["_id"], "username": user["username"], "role": user["role"]}

    def login(self, username: str, password: str) -> str:
        user = self.user_repository.find_by_username(username)
        if not user or not verify_password(password, user["password_hash"]):
            raise UnauthorizedError("Credenciales inválidas")

        return create_access_token(
            {
                "id": user["_id"],
                "username": user["username"],
                "role": user["role"],
            }
        )
