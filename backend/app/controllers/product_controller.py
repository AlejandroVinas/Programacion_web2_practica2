import shutil
import time
from pathlib import Path
from typing import Annotated

from fastapi import Depends, File, Query, UploadFile
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.exceptions import AppError
from app.database import db_session
from app.dependencies.auth import get_current_user, require_admin
from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.services.product_service import ProductService

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_IMAGE_BYTES = 2 * 1024 * 1024


def _service(session: Session = Depends(db_session)) -> ProductService:
    return ProductService(ProductRepository(session))


def get_products(
    name: str | None = Query(default=None, max_length=120),
    _current_user: dict = Depends(get_current_user),
    service: ProductService = Depends(_service),
) -> list[dict]:
    return service.get_all_products(name)


def create_product(
    payload: Annotated[ProductCreate, Depends(ProductCreate.as_form)],
    imagen: UploadFile | None = File(default=None),
    _admin: dict = Depends(require_admin),
    service: ProductService = Depends(_service),
) -> dict:
    data = payload.model_dump()
    data["imagen"] = _save_upload(imagen) if imagen and imagen.filename else None
    return service.create_product(data)


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

    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in ALLOWED_IMAGE_EXTENSIONS:
        raise AppError("Formato de imagen no permitido", 422)

    content_type = file.content_type or ""
    if content_type and not content_type.startswith("image/"):
        raise AppError("El archivo subido debe ser una imagen", 422)

    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > MAX_IMAGE_BYTES:
        raise AppError("La imagen no puede superar 2 MB", 422)

    filename = f"{int(time.time() * 1000)}{suffix}"
    target = upload_dir / filename
    with target.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return filename
