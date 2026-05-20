import sqlite3
from pathlib import Path
from typing import Iterator
from app.core.config import get_settings


SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'user')) DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    imagen TEXT,
    activo INTEGER NOT NULL DEFAULT 1
);
"""


def get_connection() -> sqlite3.Connection:
    settings = get_settings()
    db_path: Path = settings.database_path
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Crea las tablas necesarias y carga datos mínimos si la BD está vacía."""
    from app.core.security import hash_password

    with get_connection() as conn:
        conn.executescript(SCHEMA)
        users_count = conn.execute("SELECT COUNT(*) AS total FROM users").fetchone()["total"]
        if users_count == 0:
            conn.executemany(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                [
                    ("admin", hash_password("admin123"), "admin"),
                    ("user", hash_password("user123"), "user"),
                ],
            )

        products_count = conn.execute("SELECT COUNT(*) AS total FROM products").fetchone()["total"]
        if products_count == 0:
            conn.executemany(
                "INSERT INTO products (nombre, precio, imagen, activo) VALUES (?, ?, ?, ?)",
                [
                    ("Camiseta básica", 19.99, None, 1),
                    ("Sudadera PW2", 39.99, None, 1),
                    ("Producto inactivo de ejemplo", 9.99, None, 0),
                ],
            )
        conn.commit()


def db_session() -> Iterator[sqlite3.Connection]:
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()
