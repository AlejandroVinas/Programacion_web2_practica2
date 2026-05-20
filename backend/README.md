# Backend Python - Práctica 2 PW2

Backend nuevo desarrollado con **FastAPI** para sustituir al backend original de Node/Express manteniendo el contrato que ya consume el frontend Svelte 5.

## Requisitos

- Python 3.11 o superior
- pip

## Instalación

```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
python run.py
```

El backend queda disponible en `http://localhost:3000` y la documentación automática en `http://localhost:3000/docs`.

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | admin123 | admin |
| user | user123 | user |

## Endpoints mantenidos para el frontend

Todos los endpoints principales se mantienen bajo `/api`, igual que en la práctica anterior:

| Método | Endpoint | Acceso | Uso |
|---|---|---|---|
| POST | `/api/login` | Público | Devuelve `{ token }` con JWT |
| POST | `/api/register` | Público | Registra usuario con rol `user` |
| GET | `/api/productos` | Usuario autenticado | Lista productos. Soporta `?name=` |
| POST | `/api/productos` | Admin | Crea producto con `multipart/form-data` |
| PUT | `/api/productos/{id}` | Admin | Edita producto |
| DELETE | `/api/productos/{id}` | Admin | Elimina producto |
| GET | `/api/users` | Admin | Lista usuarios |
| POST | `/api/users` | Admin | Crea usuario |
| PUT | `/api/users/{id}` | Admin | Edita usuario/rol |
| DELETE | `/api/users/{id}` | Admin | Elimina usuario |

## Estructura por capas

```text
backend/
├── app/
│   ├── main.py                 # Configuración FastAPI, CORS, rutas y errores globales
│   ├── database.py             # Conexión e inicialización SQLite
│   ├── core/                   # Configuración, seguridad JWT y excepciones
│   ├── dependencies/           # Dependencias de autenticación y rol admin
│   ├── routers/                # Definición de rutas HTTP
│   ├── controllers/            # Manejo de petición/respuesta
│   ├── services/               # Lógica de negocio
│   ├── repositories/           # Acceso a datos SQLite
│   └── schemas/                # Esquemas Pydantic de entrada/salida
├── uploads/                    # Imágenes subidas
├── data/                       # Base de datos SQLite generada localmente
├── requirements.txt
├── seed.py
└── run.py
```

## JWT y roles

- El login genera un JWT firmado con `id`, `username` y `role`, que es justo lo que decodifica el frontend.
- Las rutas privadas leen `Authorization: Bearer <token>`.
- Si no hay token se responde `401`.
- Si el token es inválido/expirado o el usuario no es admin se responde `403`.

## Base de datos

Se usa SQLite mediante SQLAlchemy ORM para evitar depender de MongoDB/Redis y facilitar la ejecución local. La capa de repositorios encapsula el acceso a datos con SQLAlchemy, así que controladores y servicios no acceden directamente a la base de datos.

## Funcionalidades avanzadas

### Validación estricta

Los esquemas Pydantic de `app/schemas` validan longitudes, formatos, rangos numéricos y roles permitidos. En productos, la creación con `multipart/form-data` también valida `nombre`, `precio`, `activo` e imagen. Los errores se devuelven como `422 Unprocessable Entity` con una estructura JSON uniforme.

### Manejo global de errores

`app/main.py` define manejadores para `AppError`, `RequestValidationError`, `SQLAlchemyError` y errores HTTP generales. Así, los errores de lógica de negocio, validación y base de datos no llegan al frontend como trazas internas, sino como respuestas HTTP limpias.

### ORM y patrón repositorio

`app/models.py` contiene los modelos ORM `UserModel` y `ProductModel`. `app/database.py` crea el motor, sesiones y tablas. Los repositorios `UserRepository` y `ProductRepository` son la única capa que trabaja con SQLAlchemy.

