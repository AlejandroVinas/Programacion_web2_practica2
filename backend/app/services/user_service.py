from sqlalchemy.exc import IntegrityError

from app.core.exceptions import AppError, NotFoundError
from app.core.security import hash_password
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self) -> list[dict]:
        users = self.user_repository.find_all()
        return [self._public_user(user) for user in users]

    def create_user(self, data: dict) -> dict:
        if self.user_repository.find_by_username(data["username"]):
            raise AppError("El usuario ya existe", 409)
        try:
            user = self.user_repository.create(
                data["username"],
                hash_password(data["password"]),
                data.get("role", "user"),
            )
        except IntegrityError:
            raise AppError("El usuario ya existe", 409)
        return self._public_user(user)

    def update_user(self, user_id: str, data: dict) -> dict:
        current_user = self.user_repository.find_by_id(user_id)
        if not current_user:
            raise NotFoundError("Usuario no encontrado")

        update_data = {k: v for k, v in data.items() if v is not None}
        if "username" in update_data and update_data["username"] != current_user["username"]:
            if self.user_repository.find_by_username(update_data["username"]):
                raise AppError("Ese nombre de usuario ya está en uso", 409)
        if "password" in update_data:
            update_data["password_hash"] = hash_password(update_data.pop("password"))

        try:
            user = self.user_repository.update(user_id, update_data)
        except IntegrityError:
            raise AppError("Ese nombre de usuario ya está en uso", 409)
        return self._public_user(user)

    def delete_user(self, user_id: str) -> None:
        if not self.user_repository.find_by_id(user_id):
            raise NotFoundError("Usuario no encontrado")
        self.user_repository.delete(user_id)

    @staticmethod
    def _public_user(user: dict) -> dict:
        return {"_id": user["_id"], "username": user["username"], "role": user["role"]}
