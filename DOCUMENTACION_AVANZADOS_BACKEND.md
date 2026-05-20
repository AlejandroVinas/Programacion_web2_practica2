# Funcionalidades avanzadas de backend

Este documento resume las mejoras añadidas sobre la v1 de requisitos mínimos para cubrir el bloque avanzado de la práctica.

## 1. Validación estricta de datos

Se han reforzado los esquemas de validación con Pydantic y validaciones nativas de FastAPI:

- `app/schemas/auth_schema.py`
  - `LoginRequest`
  - `RegisterRequest`
- `app/schemas/user_schema.py`
  - `UserCreate`
  - `UserUpdate`
- `app/schemas/product_schema.py`
  - `ProductCreate`
  - `ProductUpdate`

Validaciones aplicadas:

- `username` entre 3 y 50 caracteres para registro/usuarios.
- `username` restringido a letras, números, guiones, guion bajo y punto.
- `password` entre 4 y 100 caracteres.
- `role` limitado a `admin` o `user`.
- `nombre` de producto obligatorio, entre 1 y 120 caracteres y sin espacios vacíos.
- `precio` obligatorio, mayor que 0 y menor o igual que 999999.
- `activo` booleano.
- `imagen` opcional, solo extensiones `.jpg`, `.jpeg`, `.png`, `.gif` y `.webp`, con tamaño máximo de 2 MB.

Cuando los datos no cumplen las reglas, FastAPI devuelve automáticamente `422 Unprocessable Entity` con detalles estructurados.

## 2. Manejo global de excepciones

En `app/main.py` se centralizan los errores mediante manejadores globales:

- `AppError`: errores controlados de lógica de negocio.
- `RequestValidationError`: errores de validación de entrada, con respuesta `422`.
- `SQLAlchemyError`: errores de base de datos traducidos a una respuesta HTTP limpia.
- `StarletteHTTPException`: errores HTTP generales en formato JSON unificado.

Formato de respuesta usado:

```json
{
  "error": "Mensaje resumido",
  "message": "Mensaje compatible con el frontend",
  "details": []
}
```

`details` solo aparece cuando hay errores de validación.

## 3. Persistencia real con ORM y patrón repositorio

La persistencia se ha migrado a SQLite mediante SQLAlchemy ORM.

Archivos principales:

- `app/models.py`: modelos ORM `UserModel` y `ProductModel`.
- `app/database.py`: motor SQLAlchemy, `SessionLocal`, creación de tablas e inicialización de datos.
- `app/repositories/user_repository.py`: acceso a datos de usuarios.
- `app/repositories/product_repository.py`: acceso a datos de productos.

La arquitectura queda separada así:

```text
routers -> controllers -> services -> repositories -> models/database
```

Los controladores y servicios no ejecutan SQL directamente. Todo el acceso a base de datos está encapsulado en repositorios.

## 4. Compatibilidad mantenida con el frontend

Se mantienen los endpoints principales de la v1:

| Método | Endpoint | Permiso |
|---|---|---|
| POST | `/api/login` | Público |
| POST | `/api/register` | Público |
| GET | `/api/productos` | Usuario autenticado |
| POST | `/api/productos` | Admin |
| PUT | `/api/productos/{id}` | Admin |
| DELETE | `/api/productos/{id}` | Admin |
| GET | `/api/users` | Admin |
| POST | `/api/users` | Admin |
| PUT | `/api/users/{id}` | Admin |
| DELETE | `/api/users/{id}` | Admin |

También se conserva el formato JSON que espera Svelte:

- Productos: `_id`, `nombre`, `precio`, `imagen`, `activo`.
- Usuarios: `_id`, `username`, `role`.
- Login: `{ "token": "..." }`.

## 5. Pruebas realizadas

Se han comprobado los siguientes casos con `FastAPI TestClient`:

- `GET /health` devuelve `200`.
- `POST /api/login` con admin y user devuelve token.
- `GET /api/productos` sin token devuelve `401`.
- `GET /api/productos` con token de usuario devuelve `200`.
- `GET /api/users` sin token devuelve `401`.
- `GET /api/users` con usuario normal devuelve `403`.
- `GET /api/users` con admin devuelve `200`.
- `POST /api/productos` con admin devuelve `201`.
- `PUT /api/productos/{id}` con precio inválido devuelve `422`.
- `DELETE /api/productos/{id}` con admin devuelve `200`.
- `POST /api/users` con admin devuelve `201`.
- `PUT /api/users/{id}` con rol inválido devuelve `422`.
- `DELETE /api/users/{id}` con admin devuelve `200`.

## 6. Nota sobre dependencias del frontend

Se ha ajustado `frontend-svelte/package.json` para usar `vite ^5.0.0`, compatible con `@sveltejs/vite-plugin-svelte ^4.0.0`, evitando el conflicto de dependencias que aparecía al ejecutar `npm install`.
