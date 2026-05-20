# PW2 - Práctica 2: Backend Python + Frontend Svelte 5

Esta versión adapta la práctica anterior a los requisitos mínimos de la Práctica 2: se sustituye el backend Node/Express por un backend en **Python + FastAPI**, manteniendo el frontend en **Svelte 5** y los mismos endpoints principales.

## Arranque rápido

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
python run.py
```

Servidor: `http://localhost:3000`

### Frontend

En otra terminal:

```bash
cd frontend-svelte
npm install
npm run dev
```

Frontend: `http://localhost:5173`

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | admin123 | admin |
| user | user123 | user |

## Qué requisitos mínimos cubre

1. **Backend creado con Python/FastAPI.**
2. **Separación de responsabilidades:** routers, controllers, services, repositories, schemas, dependencies y core.
3. **JWT compatible con el frontend:** `/api/login` devuelve `{ token }` con payload `id`, `username` y `role`.
4. **Protección de rutas privadas:** `Authorization: Bearer <token>`, con respuestas 401/403.
5. **Contrato de API mantenido:** se conservan `/api/login`, `/api/register`, `/api/productos` y `/api/users` con métodos y JSON compatibles con Svelte.

## Endpoints principales

| Método | Endpoint | Rol necesario |
|---|---|---|
| POST | `/api/login` | público |
| POST | `/api/register` | público |
| GET | `/api/productos` | usuario autenticado |
| POST | `/api/productos` | admin |
| PUT | `/api/productos/{id}` | admin |
| DELETE | `/api/productos/{id}` | admin |
| GET | `/api/users` | admin |
| POST | `/api/users` | admin |
| PUT | `/api/users/{id}` | admin |
| DELETE | `/api/users/{id}` | admin |

La documentación automática de FastAPI está en `http://localhost:3000/docs`.

## Funcionalidades avanzadas incluidas en esta versión

Esta versión añade mejoras para el bloque avanzado del backend:

- Validación estricta con Pydantic/FastAPI en usuarios, login, registro y productos.
- Respuestas `422` estructuradas cuando los datos no cumplen formato, longitud o rango.
- Manejo global de excepciones para errores de negocio, validación, HTTP y base de datos.
- Persistencia real con SQLite mediante SQLAlchemy ORM.
- Patrón repositorio reforzado: los controladores y servicios no ejecutan SQL directamente.
- Documento `DOCUMENTACION_AVANZADOS_BACKEND.md` con el detalle de las mejoras y pruebas.
- Ajuste del frontend a `vite ^5.0.0` para resolver el conflicto de dependencias con el plugin de Svelte.

