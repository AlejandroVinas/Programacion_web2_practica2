import sqlite3
from typing import Any


def _to_user(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "_id": str(row["id"]),
        "id": row["id"],
        "username": row["username"],
        "password_hash": row["password_hash"],
        "role": row["role"],
    }


class UserRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def find_all(self) -> list[dict[str, Any]]:
        rows = self.conn.execute("SELECT id, username, password_hash, role FROM users ORDER BY id").fetchall()
        return [_to_user(row) for row in rows if row]

    def find_by_id(self, user_id: str | int) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT id, username, password_hash, role FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return _to_user(row)

    def find_by_username(self, username: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT id, username, password_hash, role FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        return _to_user(row)

    def create(self, username: str, password_hash: str, role: str = "user") -> dict[str, Any]:
        cursor = self.conn.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
            (username, password_hash, role),
        )
        self.conn.commit()
        return self.find_by_id(cursor.lastrowid)

    def update(self, user_id: str, data: dict[str, Any]) -> dict[str, Any] | None:
        fields = []
        values = []
        for key in ["username", "password_hash", "role"]:
            if key in data and data[key] is not None:
                fields.append(f"{key} = ?")
                values.append(data[key])
        if not fields:
            return self.find_by_id(user_id)
        values.append(user_id)
        self.conn.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ?", values)
        self.conn.commit()
        return self.find_by_id(user_id)

    def delete(self, user_id: str) -> None:
        self.conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
