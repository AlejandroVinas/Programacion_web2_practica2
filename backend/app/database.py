from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.core.security import hash_password
from app.models import Base, ProductModel, UserModel


def _build_sqlalchemy_url(raw_database_url: str) -> str:
    """Acepta tanto rutas sencillas como URLs SQLAlchemy completas."""
    if "://" in raw_database_url:
        if raw_database_url.startswith("sqlite:///"):
            db_path = Path(raw_database_url.replace("sqlite:///", "", 1))
            db_path.parent.mkdir(parents=True, exist_ok=True)
        return raw_database_url

    db_path = Path(raw_database_url)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{db_path.as_posix()}"


settings = get_settings()
SQLALCHEMY_DATABASE_URL = _build_sqlalchemy_url(settings.database_url)

engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {},
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def init_db() -> None:
    """Crea las tablas ORM y carga datos mínimos si la BD está vacía."""
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        users_count = session.scalar(select(UserModel).limit(1))
        if users_count is None:
            session.add_all(
                [
                    UserModel(username="admin", password_hash=hash_password("admin123"), role="admin"),
                    UserModel(username="user", password_hash=hash_password("user123"), role="user"),
                ]
            )

        products_count = session.scalar(select(ProductModel).limit(1))
        if products_count is None:
            session.add_all(
                [
                    ProductModel(nombre="Camiseta básica", precio=19.99, imagen=None, activo=True),
                    ProductModel(nombre="Sudadera PW2", precio=39.99, imagen=None, activo=True),
                    ProductModel(nombre="Producto inactivo de ejemplo", precio=9.99, imagen=None, activo=False),
                ]
            )

        session.commit()


def db_session() -> Iterator[Session]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
