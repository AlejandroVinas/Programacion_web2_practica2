# Checklist de entrega completa - Práctica 2

Checklist global para revisar la entrega antes de subirla o presentarla en el Campus.

## 1. Entrega y repositorio

| Requisito | Estado | Evidencia |
|---|---:|---|
| Código en repositorio público | ✅ | GitHub: `AlejandroVinas/Programacion_web2_practica2` |
| Rama de mínimos conservada | ✅ | `main` + etiqueta `v1` |
| Rama de avanzados creada | ✅ | `v2-avanzado-backend` |
| Etiqueta de versión avanzada | ✅ | `v2` |
| README general de ejecución | ✅ | `README.md` |
| Documentación técnica del backend avanzado | ✅ | `DOCUMENTACION_AVANZADOS_BACKEND.md` |
| Checklist de mínimos | ✅ | `CHECKLIST_REQUISITOS_MINIMOS.md` |
| Checklist de avanzados | ✅ | `CHECKLIST_FUNCIONALIDADES_AVANZADAS.md` |
| Memoria de uso de IA | ✅ | `MEMORIA_USO_IA.md` |
| `.env` no subido | ✅ | Ignorado por `.gitignore` |
| Base de datos local no subida | ✅ | `backend/data/*.db` ignorado |
| Entorno virtual no subido | ✅ | `.venv/` ignorado |
| `node_modules` no subido | ✅ | Ignorado por `.gitignore` |

## 2. Requisitos mínimos del backend

| Requisito mínimo | Estado | Archivo / evidencia |
|---|---:|---|
| Backend creado con Python | ✅ | `backend/` |
| Framework Flask o FastAPI | ✅ | FastAPI en `backend/app/main.py` |
| Separación de responsabilidades | ✅ | `routers`, `controllers`, `services`, `repositories`, `schemas`, `dependencies`, `core` |
| No centralizar lógica en un único archivo | ✅ | `main.py` solo configura app, CORS, errores y rutas |
| Login con JWT | ✅ | `backend/app/services/auth_service.py`, `backend/app/core/security.py` |
| Validación de JWT en rutas privadas | ✅ | `backend/app/dependencies/auth.py` |
| Gestión de errores `401` | ✅ | Falta de token / usuario no encontrado |
| Gestión de errores `403` | ✅ | Token inválido/expirado o rol insuficiente |
| Roles `admin` y `user` | ✅ | `backend/app/schemas/user_schema.py` y dependencias de autorización |
| CRUD de productos | ✅ | `product_router.py`, `product_controller.py`, `product_service.py`, `product_repository.py` |
| CRUD de usuarios | ✅ | `user_router.py`, `user_controller.py`, `user_service.py`, `user_repository.py` |
| Mismos endpoints principales | ✅ | `/api/login`, `/api/register`, `/api/productos`, `/api/users` |
| JSON compatible con Svelte | ✅ | Respuestas con `_id`, `username`, `role`, `nombre`, `precio`, `imagen`, `activo` |

## 3. Endpoints y permisos

| Método | Endpoint | Estado | Acceso |
|---|---|---:|---|
| `POST` | `/api/login` | ✅ | Público |
| `POST` | `/api/register` | ✅ | Público |
| `GET` | `/api/productos` | ✅ | Usuario autenticado |
| `POST` | `/api/productos` | ✅ | Admin |
| `PUT` | `/api/productos/{id}` | ✅ | Admin |
| `DELETE` | `/api/productos/{id}` | ✅ | Admin |
| `GET` | `/api/users` | ✅ | Admin |
| `POST` | `/api/users` | ✅ | Admin |
| `PUT` | `/api/users/{id}` | ✅ | Admin |
| `DELETE` | `/api/users/{id}` | ✅ | Admin |
| `GET` | `/health` | ✅ | Público |
| `GET` | `/docs` | ✅ | Documentación FastAPI |

## 4. Funcionalidades avanzadas de backend

| Requisito avanzado | Estado | Archivo / evidencia |
|---|---:|---|
| Validación estricta de datos | ✅ | `backend/app/schemas/*.py` |
| Uso de Pydantic / FastAPI | ✅ | `ProductCreate`, `ProductUpdate`, `UserCreate`, `UserUpdate`, `LoginRequest`, `RegisterRequest` |
| Validación de longitudes | ✅ | `Field(min_length=..., max_length=...)` |
| Validación de rangos numéricos | ✅ | `precio > 0` y `precio <= 999999` |
| Validación de roles | ✅ | `Literal["admin", "user"]` |
| Validación de usuario | ✅ | Patrón `^[a-zA-Z0-9_.-]+$` |
| Rechazo de campos extra | ✅ | `ConfigDict(extra="forbid")` |
| Respuestas `422` estructuradas | ✅ | Handler `RequestValidationError` en `main.py` |
| Manejo global de excepciones | ✅ | Handlers en `backend/app/main.py` |
| Excepciones de negocio controladas | ✅ | `backend/app/core/exceptions.py` |
| Errores de base de datos controlados | ✅ | Handler `SQLAlchemyError` |
| Persistencia real | ✅ | SQLite local en `backend/data/app.db` |
| Uso de ORM estándar | ✅ | SQLAlchemy en `backend/app/models.py` y `database.py` |
| Patrón repositorio | ✅ | `UserRepository` y `ProductRepository` |
| Servicios separados de repositorios | ✅ | `backend/app/services/*.py` |
| Controladores sin SQL directo | ✅ | `backend/app/controllers/*.py` |
| Carga de datos iniciales | ✅ | `backend/seed.py` e inicialización en `database.py` |

## 5. Uso de IA en el desarrollo

| Requisito de IA | Estado | Evidencia |
|---|---:|---|
| Documento Markdown con prompts clave | ✅ | `MEMORIA_USO_IA.md` |
| Explicación de iteraciones | ✅ | Sección de iteraciones en `MEMORIA_USO_IA.md` |
| Error o alucinación documentada | ✅ | Sección de errores detectados y corrección manual |
| Análisis crítico del código generado | ✅ | Justificación de seguridad, capas y compatibilidad |
| Correcciones manuales explicadas | ✅ | JWT, rutas protegidas, SQLAlchemy, Vite y `.gitignore` |

## 6. Frontend

| Requisito / comprobación | Estado | Evidencia |
|---|---:|---|
| Frontend Svelte 5 conservado | ✅ | `frontend-svelte/` |
| API centralizada | ✅ | `frontend-svelte/src/services/api.js` |
| Login con JWT | ✅ | `Login.svelte`, `auth.svelte.js` |
| Navegación SPA | ✅ | `App.svelte` |
| Páginas de productos | ✅ | `Products.svelte`, componentes de producto |
| Página de usuarios | ✅ | `Users.svelte`, `UserRow.svelte` |
| Dependencias frontend compatibles | ✅ | `vite ^5.0.0`, `@sveltejs/vite-plugin-svelte ^4.0.0` |
| Build/ejecución con Vite | ✅ | `npm install`, `npm run dev` |

## 7. Ejecución local

| Comprobación | Estado | Comando |
|---|---:|---|
| Instalar backend | ✅ | `pip install -r requirements.txt` dentro de `backend` |
| Crear `.env` | ✅ | `Copy-Item .env.example .env -Force` |
| Crear datos iniciales | ✅ | `python seed.py` |
| Ejecutar backend | ✅ | `python run.py` |
| Abrir Swagger | ✅ | `http://localhost:3000/docs` |
| Instalar frontend | ✅ | `npm install` dentro de `frontend-svelte` |
| Ejecutar frontend | ✅ | `npm run dev` |
| Abrir app | ✅ | `http://localhost:5173` |

## 8. Usuarios de prueba

| Usuario | Contraseña | Rol | Estado |
|---|---|---|---:|
| `admin` | `admin123` | admin | ✅ |
| `user` | `user123` | user | ✅ |

## 9. Pruebas recomendadas antes de entregar

- [ ] Arrancar backend con `python run.py`.
- [ ] Abrir `http://localhost:3000/docs`.
- [ ] Arrancar frontend con `npm run dev`.
- [ ] Abrir `http://localhost:5173`.
- [ ] Iniciar sesión como `admin/admin123`.
- [ ] Crear un producto.
- [ ] Editar un producto.
- [ ] Borrar un producto.
- [ ] Entrar en la gestión de usuarios como admin.
- [ ] Iniciar sesión como `user/user123`.
- [ ] Comprobar que el usuario normal no puede acceder a acciones admin.
- [ ] Probar un dato inválido y comprobar error `422`.
- [ ] Confirmar que no hay `.env`, `.venv`, `node_modules`, `dist`, `app.db` ni imágenes locales preparadas para commit.

## 10. Estado final

La versión `v2-avanzado-backend` cubre:

- Requisitos mínimos del backend.
- Funcionalidades avanzadas de backend.
- Documentación de ejecución.
- Documentación del uso de IA.
- Compatibilidad con el frontend Svelte 5.
