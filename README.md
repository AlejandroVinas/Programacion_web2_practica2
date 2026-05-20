# Programación Web 2 - Práctica 2

Proyecto completo de la Práctica 2: **frontend Svelte 5** conectado a un nuevo **backend Python con FastAPI**, manteniendo el contrato de API de la práctica anterior y añadiendo funcionalidades avanzadas de backend.

## 1. Tecnologías utilizadas

| Parte | Tecnología |
|---|---|
| Frontend | Svelte 5 + Vite |
| Backend | Python 3.11+ + FastAPI |
| Autenticación | JWT |
| Base de datos | SQLite |
| ORM | SQLAlchemy |
| Validación | Pydantic / FastAPI |
| Documentación API | Swagger automático de FastAPI |

## 2. Estructura general

```text
Programacion_web2_practica2/
├── backend/
│   ├── app/
│   │   ├── controllers/      # Reciben la petición HTTP y llaman a servicios
│   │   ├── core/             # Configuración, seguridad JWT y excepciones
│   │   ├── dependencies/     # Dependencias de autenticación y permisos
│   │   ├── repositories/     # Acceso a datos con SQLAlchemy
│   │   ├── routers/          # Definición de rutas FastAPI
│   │   ├── schemas/          # Validaciones Pydantic
│   │   ├── services/         # Lógica de negocio
│   │   ├── database.py       # Motor, sesiones e inicialización de BD
│   │   ├── main.py           # App FastAPI, CORS, rutas y errores globales
│   │   └── models.py         # Modelos ORM
│   ├── data/                 # SQLite local generado en ejecución
│   ├── uploads/              # Imágenes locales subidas por usuarios
│   ├── .env.example          # Variables de entorno de ejemplo
│   ├── requirements.txt      # Dependencias Python
│   ├── run.py                # Arranque del servidor
│   └── seed.py               # Inicialización de datos de prueba
├── frontend-svelte/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── stores/
│   │   ├── App.svelte
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── CHECKLIST_ENTREGA_COMPLETA.md
├── CHECKLIST_REQUISITOS_MINIMOS.md
├── CHECKLIST_FUNCIONALIDADES_AVANZADAS.md
├── DOCUMENTACION_AVANZADOS_BACKEND.md
├── MEMORIA_USO_IA.md
└── README.md
```

## 3. Requisitos previos

Antes de ejecutar el proyecto necesitas tener instalado:

- **Python 3.11 o superior**.
- **Node.js 18 o superior**.
- **Git**.
- **Visual Studio Code**, recomendado para abrir dos terminales integradas.

Para comprobar versiones:

```powershell
python --version
node --version
npm --version
git --version
```

## 4. Ejecución del backend

Abre una terminal en Visual Studio Code desde la raíz del proyecto.

### 4.1. Entrar en la rama avanzada

```powershell
git switch v2-avanzado-backend
```

### 4.2. Entrar en la carpeta backend

```powershell
cd backend
```

### 4.3. Crear entorno virtual

Solo es necesario la primera vez:

```powershell
python -m venv .venv
```

### 4.4. Activar entorno virtual en PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

Cuando esté activado aparecerá `(.venv)` al inicio de la terminal.

### 4.5. Instalar dependencias Python

```powershell
pip install -r requirements.txt
```

### 4.6. Crear archivo `.env`

```powershell
Copy-Item .env.example .env -Force
```

El archivo `.env.example` incluido contiene valores válidos para desarrollo local:

```env
PORT=3000
JWT_SECRET=cambia_este_secreto_en_produccion_minimo_32_bytes
JWT_EXPIRES_MINUTES=60
DATABASE_URL=data/app.db
UPLOAD_DIR=uploads
FRONTEND_ORIGIN=http://localhost:5173
```

### 4.7. Crear base de datos y datos iniciales

```powershell
python seed.py
```

También se inicializan tablas automáticamente al arrancar el backend.

### 4.8. Arrancar backend

```powershell
python run.py
```

Si todo va bien, se verá algo parecido a:

```text
Uvicorn running on http://0.0.0.0:3000
```

Abrir en navegador:

```text
http://localhost:3000/docs
```

La URL `/docs` muestra la documentación interactiva de FastAPI.

## 5. Ejecución del frontend

Deja el backend abierto en una terminal. Abre una **segunda terminal** en Visual Studio Code.

### 5.1. Entrar en la carpeta frontend

```powershell
cd "C:\Users\aleja\OneDrive\Escritorio\Nueva carpeta\Programacion_web2_practica2\frontend-svelte"
```

O, si ya estás en la raíz del proyecto:

```powershell
cd frontend-svelte
```

### 5.2. Instalar dependencias Node

```powershell
npm install
```

### 5.3. Arrancar frontend

```powershell
npm run dev
```

Abrir en navegador la URL que indique Vite, normalmente:

```text
http://localhost:5173
```

## 6. Usuarios de prueba

| Usuario | Contraseña | Rol | Permisos |
|---|---|---|---|
| `admin` | `admin123` | admin | CRUD completo de productos y usuarios |
| `user` | `user123` | user | Puede iniciar sesión y consultar productos |

## 7. URLs principales

| Servicio | URL |
|---|---|
| Frontend | `http://localhost:5173` |
| Backend | `http://localhost:3000` |
| Swagger/FastAPI docs | `http://localhost:3000/docs` |
| Healthcheck | `http://localhost:3000/health` |
| Imágenes subidas | `http://localhost:3000/uploads/<archivo>` |

## 8. Endpoints principales

| Método | Endpoint | Acceso | Descripción |
|---|---|---|---|
| `POST` | `/api/login` | Público | Iniciar sesión y obtener JWT |
| `POST` | `/api/register` | Público | Registrar usuario con rol `user` |
| `GET` | `/api/productos` | Usuario autenticado | Listar productos; permite filtro `?name=` |
| `POST` | `/api/productos` | Admin | Crear producto con `multipart/form-data` |
| `PUT` | `/api/productos/{id}` | Admin | Editar producto |
| `DELETE` | `/api/productos/{id}` | Admin | Eliminar producto |
| `GET` | `/api/users` | Admin | Listar usuarios |
| `POST` | `/api/users` | Admin | Crear usuario |
| `PUT` | `/api/users/{id}` | Admin | Editar usuario |
| `DELETE` | `/api/users/{id}` | Admin | Eliminar usuario |

## 9. Compatibilidad con el frontend

El backend conserva los formatos que espera Svelte:

### Login

```json
{
  "token": "jwt_generado"
}
```

### Producto

```json
{
  "_id": "1",
  "nombre": "Camiseta básica",
  "precio": 19.99,
  "imagen": null,
  "activo": true
}
```

### Usuario

```json
{
  "_id": "1",
  "username": "admin",
  "role": "admin"
}
```

## 10. Funcionalidades implementadas

### Requisitos mínimos

- Backend nuevo en Python con FastAPI.
- Separación por capas: routers, controllers, services, repositories, schemas, dependencies y core.
- JWT para login y rutas privadas.
- Roles `admin` y `user`.
- Endpoints compatibles con el frontend Svelte.
- Rutas privadas con errores `401` y `403`.

### Funcionalidades avanzadas

- Validación estricta con Pydantic.
- Errores `422` estructurados.
- Manejo global de excepciones.
- Persistencia real con SQLite.
- ORM SQLAlchemy.
- Patrón repositorio aplicado.
- Validación de imágenes subidas por extensión, tipo y tamaño.

## 11. Comandos rápidos

### Backend

```powershell
cd "C:\Users\aleja\OneDrive\Escritorio\Nueva carpeta\Programacion_web2_practica2"
git switch v2-avanzado-backend
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env -Force
python seed.py
python run.py
```

### Frontend

```powershell
cd "C:\Users\aleja\OneDrive\Escritorio\Nueva carpeta\Programacion_web2_practica2\frontend-svelte"
npm install
npm run dev
```

## 12. Problemas frecuentes

### `Could not open requirements file`

Significa que estás en la carpeta equivocada. Debes estar dentro de `backend`:

```powershell
cd backend
pip install -r requirements.txt
```

### `vite no se reconoce como comando`

Normalmente pasa si `npm install` no se ejecutó correctamente. Solución:

```powershell
cd frontend-svelte
npm install
npm run dev
```

### Error de permisos al activar `.venv`

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### `0.0.0.0:3000` no abre en navegador

En navegador usa:

```text
http://localhost:3000/docs
```

No uses `http://0.0.0.0:3000`.

### Rehacer base de datos local

Si quieres reiniciar datos locales:

```powershell
cd backend
Remove-Item -Force data\app.db -ErrorAction SilentlyContinue
python seed.py
python run.py
```

## 13. Archivos que no se deben subir a GitHub

El `.gitignore` evita subir archivos generados localmente:

```text
backend/.venv/
backend/.env
backend/data/*.db
backend/uploads/*
frontend-svelte/node_modules/
frontend-svelte/dist/
__pycache__/
```

Se mantienen las carpetas `backend/data/` y `backend/uploads/` gracias a sus archivos `.gitkeep`.

## 14. Entrega recomendada

Para entregar la versión avanzada, indicar:

```text
Repositorio: https://github.com/AlejandroVinas/Programacion_web2_practica2
Rama: v2-avanzado-backend
Etiqueta: v2
```

Documentos incluidos:

- `README.md`: ejecución general del proyecto.
- `CHECKLIST_ENTREGA_COMPLETA.md`: checklist global de requisitos.
- `CHECKLIST_REQUISITOS_MINIMOS.md`: checklist del bloque mínimo.
- `CHECKLIST_FUNCIONALIDADES_AVANZADAS.md`: checklist del bloque avanzado.
- `DOCUMENTACION_AVANZADOS_BACKEND.md`: explicación técnica del backend avanzado.
- `MEMORIA_USO_IA.md`: memoria del uso de IA durante el desarrollo.
