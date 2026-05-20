# Checklist de requisitos mínimos - Práctica 2

## 1. Estructura y separación de responsabilidades

- Backend creado con **FastAPI** (`backend/app/main.py`).
- Código separado por capas:
  - `routers/`: endpoints y agrupación de rutas.
  - `controllers/`: entrada/salida HTTP.
  - `services/`: lógica de negocio.
  - `repositories/`: acceso a SQLite.
  - `schemas/`: validación de datos con Pydantic.
  - `dependencies/`: autenticación JWT y autorización admin.
  - `core/`: configuración, seguridad y excepciones.
- El archivo principal no concentra la lógica de negocio.

## 2. Autenticación básica con JWT

- `/api/login` genera un JWT con `id`, `username` y `role`.
- Las rutas privadas leen `Authorization: Bearer <token>`.
- El listado de productos (`GET /api/productos`) requiere usuario autenticado; crear, editar y borrar productos requiere rol `admin`.
- Se devuelven errores `401` cuando falta el token y `403` cuando el token no es válido o el rol no permite la acción.
- Usuarios iniciales:
  - `admin/admin123` con rol `admin`.
  - `user/user123` con rol `user`.

## 3. Migración del API y contrato con Svelte

Se mantienen los endpoints que consume `frontend-svelte/src/services/api.js`:

- `POST /api/login`
- `POST /api/register`
- `GET /api/productos`
- `POST /api/productos`
- `PUT /api/productos/{id}`
- `DELETE /api/productos/{id}`
- `GET /api/users`
- `POST /api/users`
- `PUT /api/users/{id}`
- `DELETE /api/users/{id}`

Las respuestas conservan los campos esperados por el frontend:

- Producto: `_id`, `nombre`, `precio`, `imagen`, `activo`.
- Usuario: `_id`, `username`, `role`.
- Login: `{ "token": "..." }`.
