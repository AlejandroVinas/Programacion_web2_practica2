# Checklist de funcionalidades avanzadas

| Requisito avanzado | Estado | Implementación |
|---|---:|---|
| Validación estricta de datos | Cumple | Pydantic/FastAPI en `app/schemas`, constraints de longitud, patrón, rangos y roles. |
| Errores de validación estructurados | Cumple | `RequestValidationError` devuelve `422` con `error`, `message` y `details`. |
| Manejo global de excepciones | Cumple | Manejadores en `app/main.py` para negocio, validación, HTTP y base de datos. |
| Persistencia real | Cumple | SQLite real en `backend/data/app.db`, generado localmente. |
| ORM estándar | Cumple | SQLAlchemy ORM en `app/models.py` y `app/database.py`. |
| Patrón repositorio | Cumple | `UserRepository` y `ProductRepository` encapsulan todo el acceso a datos. |
| Compatibilidad frontend | Cumple | Se mantienen endpoints, métodos y JSON de la v1. |
| Dependencias frontend compatibles | Cumple | `vite` fijado a `^5.0.0` para evitar conflicto con `@sveltejs/vite-plugin-svelte`. |
