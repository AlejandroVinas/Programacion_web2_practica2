# Backend FastAPI - Práctica 2 PW2

Backend desarrollado en **Python + FastAPI** para sustituir al backend original y mantener la compatibilidad con el frontend Svelte 5.

## Requisitos

- Python 3.11 o superior.
- pip.

## Instalación en Windows / PowerShell

Desde la raíz del proyecto:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env -Force
python seed.py
python run.py
```

Si PowerShell bloquea la activación del entorno:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Servidor:

```text
http://localhost:3000
```

Documentación automática:

```text
http://localhost:3000/docs
```

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | admin |
| `user` | `user123` | user |

## Variables de entorno

Archivo `.env.example`:

```env
PORT=3000
JWT_SECRET=cambia_este_secreto_en_produccion_minimo_32_bytes
JWT_EXPIRES_MINUTES=60
DATABASE_URL=data/app.db
UPLOAD_DIR=uploads
FRONTEND_ORIGIN=http://localhost:5173
```

Para desarrollo local basta con copiarlo a `.env`.

## Endpoints

| Método | Endpoint | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/api/login` | Público | Devuelve JWT |
| `POST` | `/api/register` | Público | Registra usuario normal |
| `GET` | `/api/productos` | Usuario autenticado | Lista productos |
| `POST` | `/api/productos` | Admin | Crea producto |
| `PUT` | `/api/productos/{id}` | Admin | Edita producto |
| `DELETE` | `/api/productos/{id}` | Admin | Elimina producto |
| `GET` | `/api/users` | Admin | Lista usuarios |
| `POST` | `/api/users` | Admin | Crea usuario |
| `PUT` | `/api/users/{id}` | Admin | Edita usuario |
| `DELETE` | `/api/users/{id}` | Admin | Elimina usuario |
| `GET` | `/health` | Público | Comprueba que la API está activa |

## Arquitectura

```text
routers -> controllers -> services -> repositories -> models/database
```

- `routers/`: rutas HTTP.
- `controllers/`: adaptación HTTP y dependencias.
- `services/`: lógica de negocio.
- `repositories/`: consultas y persistencia con SQLAlchemy.
- `schemas/`: validaciones Pydantic.
- `dependencies/`: autenticación y autorización.
- `core/`: configuración, seguridad y excepciones.

## Funcionalidades avanzadas

- Validación estricta con Pydantic.
- Errores `422` estructurados.
- Manejo global de excepciones.
- SQLite real como persistencia local.
- SQLAlchemy ORM.
- Patrón repositorio.
- Validación de imágenes subidas.

## Base de datos

La base de datos se genera localmente en:

```text
backend/data/app.db
```

No debe subirse a GitHub. Está ignorada en `.gitignore`.

Para reiniciarla:

```powershell
Remove-Item -Force data\app.db -ErrorAction SilentlyContinue
python seed.py
python run.py
```
