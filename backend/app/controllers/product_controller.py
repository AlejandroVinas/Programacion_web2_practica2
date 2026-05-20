import shutil
import sqlite3
import time
from pathlib import Path

from fastapi import Depends, File, Form, Query, UploadFile

from app.core.config import get_settings
from app.database import db_session
from app.dependencies.auth import get_current_user, require_admin
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductUpdate
from app.services.product_service import ProductService


def _service(conn: sqlite3.Connection = Depends(db_session)) -> ProductService:
    return ProductService(ProductRepository(conn))


def get_products(
    name: str | None = Query(default=None),
    _current_user: dict = Depends(get_current_user),
    service: ProductService = Depends(_service),
) -> list[dict]:
    return service.get_all_products(name)


def create_product(
    nombre: str = Form(...),
    precio: float = Form(...),
    activo: bool = Form(True),
    imagen: UploadFile | None = File(default=None),
    _admin: dict = Depends(require_admin),
    service: ProductService = Depends(_service),
) -> dict:
    filename = _save_upload(imagen) if imagen and imagen.filename else None
    return service.create_product(
        {
            "nombre": nombre,
            "precio": precio,
            "activo": activo,
            "imagen": filename,
        }
    )


def update_product(
    product_id: str,
    payload: ProductUpdate,
    _admin: dict = Depends(require_admin),
    service: ProductService = Depends(_service),
) -> dict:
    return service.update_product(product_id, payload.model_dump(exclude_unset=True))


def delete_product(
    product_id: str,
    _admin: dict = Depends(require_admin),
    service: ProductService = Depends(_service),
) -> dict:
    service.delete_product(product_id)
    return {"message": "Producto eliminado"}


def _save_upload(file: UploadFile) -> str:
    upload_dir: Path = get_settings().upload_path
    upload_dir.mkdir(parents=True, exist_ok=True)
    safe_suffix = Path(file.filename or "").suffix.lower()
    filename = f"{int(time.time() * 1000)}{safe_suffix}"
    target = upload_dir / filename
    with target.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return filename
