from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import UserModel


def _parse_id(user_id: str | int) -> int | None:
    try:
        return int(user_id)
    except (TypeError, ValueError):
        return None


def _to_user(user: UserModel | None) -> dict[str, Any] | None:
    if user is None:
        return None
    return {
        "_id": str(user.id),
        "id": user.id,
        "username": user.username,
        "password_hash": user.password_hash,
        "role": user.role,
    }


class UserRepository:
    """Repositorio ORM: aísla SQLAlchemy de servicios y controladores."""

    def __init__(self, session: Session):
        self.session = session

    def find_all(self) -> list[dict[str, Any]]:
        users = self.session.scalars(select(UserModel).order_by(UserModel.id)).all()
        return [_to_user(user) for user in users if user]

    def find_by_id(self, user_id: str | int) -> dict[str, Any] | None:
        parsed_id = _parse_id(user_id)
        if parsed_id is None:
            return None
        user = self.session.get(UserModel, parsed_id)
        return _to_user(user)

    def find_by_username(self, username: str) -> dict[str, Any] | None:
        user = self.session.scalar(select(UserModel).where(UserModel.username == username))
        return _to_user(user)

    def create(self, username: str, password_hash: str, role: str = "user") -> dict[str, Any]:
        user = UserModel(username=username, password_hash=password_hash, role=role)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return _to_user(user)

    def update(self, user_id: str, data: dict[str, Any]) -> dict[str, Any] | None:
        parsed_id = _parse_id(user_id)
        if parsed_id is None:
            return None
        user = self.session.get(UserModel, parsed_id)
        if user is None:
            return None

        for key in ["username", "password_hash", "role"]:
            if key in data and data[key] is not None:
                setattr(user, key, data[key])

        self.session.commit()
        self.session.refresh(user)
        return _to_user(user)

    def delete(self, user_id: str) -> None:
        parsed_id = _parse_id(user_id)
        if parsed_id is None:
            return
        user = self.session.get(UserModel, parsed_id)
        if user is not None:
            self.session.delete(user)
            self.session.commit()
