import sqlite3
from typing import Any


def _to_product(row: sqlite3.Row | None) -> dict[str, Any] | None:
    if row is None:
        return None
    return {
        "_id": str(row["id"]),
        "id": row["id"],
        "nombre": row["nombre"],
        "precio": float(row["precio"]),
        "imagen": row["imagen"],
        "activo": bool(row["activo"]),
    }


class ProductRepository:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def find_all(self, name_filter: str | None = None) -> list[dict[str, Any]]:
        if name_filter:
            rows = self.conn.execute(
                "SELECT id, nombre, precio, imagen, activo FROM products WHERE LOWER(nombre) LIKE ? ORDER BY id DESC",
                (f"%{name_filter.lower()}%",),
            ).fetchall()
        else:
            rows = self.conn.execute(
                "SELECT id, nombre, precio, imagen, activo FROM products ORDER BY id DESC"
            ).fetchall()
        return [_to_product(row) for row in rows if row]

    def find_by_id(self, product_id: str | int) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT id, nombre, precio, imagen, activo FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        return _to_product(row)

    def create(self, data: dict[str, Any]) -> dict[str, Any]:
        cursor = self.conn.execute(
            "INSERT INTO products (nombre, precio, imagen, activo) VALUES (?, ?, ?, ?)",
            (
                data["nombre"],
                data["precio"],
                data.get("imagen"),
                1 if data.get("activo", True) else 0,
            ),
        )
        self.conn.commit()
        return self.find_by_id(cursor.lastrowid)

    def update(self, product_id: str, data: dict[str, Any]) -> dict[str, Any] | None:
        fields = []
        values = []
        for key in ["nombre", "precio", "imagen", "activo"]:
            if key in data and data[key] is not None:
                fields.append(f"{key} = ?")
                values.append(1 if key == "activo" and data[key] else 0 if key == "activo" else data[key])
        if not fields:
            return self.find_by_id(product_id)
        values.append(product_id)
        self.conn.execute(f"UPDATE products SET {', '.join(fields)} WHERE id = ?", values)
        self.conn.commit()
        return self.find_by_id(product_id)

    def delete(self, product_id: str) -> None:
        self.conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.conn.commit()
