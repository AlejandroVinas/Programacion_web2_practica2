# Práctica 2 - Desarrollo de Backend con Python, Arquitectura Limpia e Inteligencia Artificial

Repositorio de la Práctica 2 de Programación Web 2.

El objetivo principal de esta práctica es sustituir el backend original por un nuevo backend desarrollado en Python, manteniendo la compatibilidad con el frontend en Svelte 5 desarrollado previamente.

La versión actual del proyecto corresponde a la **v2 avanzada**, que incluye:

- Backend en Python con FastAPI.
- Arquitectura limpia separada por capas.
- Autenticación mediante JWT.
- Control de roles `user` y `admin`.
- CRUD completo de productos.
- CRUD completo de usuarios.
- Validación estricta de datos con Pydantic.
- Manejo global de excepciones.
- Persistencia real con SQLite y SQLAlchemy ORM.
- Patrón repositorio.
- Frontend en Svelte 5 conectado al nuevo backend.
- Documentación del uso de Inteligencia Artificial durante el desarrollo.

---

## Estructura general del proyecto

```text
Programacion_web2_practica2/
│
├── backend/
│   ├── app/
│   │   ├── controllers/
│   │   ├── core/
│   │   ├── dependencies/
│   │   ├── repositories/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── database.py
│   │   ├── main.py
│   │   └── models.py
│   │
│   ├── data/
│   │   └── .gitkeep
│   │
│   ├── uploads/
│   │   └── .gitkeep
│   │
│   ├── .env.example
│   ├── requirements.txt
│   ├── run.py
│   ├── seed.py
│   └── README.md
│
├── frontend-svelte/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── README.md
│
├── CHECKLIST_ENTREGA_COMPLETA.md
├── CHECKLIST_REQUISITOS_MINIMOS.md
├── CHECKLIST_FUNCIONALIDADES_AVANZADAS.md
├── DOCUMENTACION_AVANZADOS_BACKEND.md
├── MEMORIA_USO_IA.md
├── README.md
└── .gitignore
```

---

## Versiones del proyecto

El repositorio conserva dos versiones principales:

```text
v1-base              Versión mínima original.
v2-avanzado-backend  Rama de desarrollo de la versión avanzada.
main                 Versión final avanzada presentada.
```

Etiquetas disponibles:

```text
v1  Versión mínima.
v2  Versión avanzada final.
```

---

## Tecnologías utilizadas

### Backend

- Python 3.11
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite
- JWT con `python-jose`
- Passlib con bcrypt

### Frontend

- Svelte 5
- Vite
- JavaScript
- HTML/CSS

---

## Requisitos previos

Antes de ejecutar el proyecto hay que tener instalado:

- Python 3.11 o superior.
- Node.js.
- npm.
- Git.

Para comprobarlo:

```bash
python --version
node --version
npm --version
git --version
```

---

## Ejecución del backend

Abre una terminal en la raíz del proyecto:

```bash
cd "C:\Users\aleja\OneDrive\Escritorio\Nueva carpeta\Programacion_web2_practica2"
```

Entra en la carpeta del backend:

```bash
cd backend
```

Crea el entorno virtual:

```bash
python -m venv .venv
```

Activa el entorno virtual.

En PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

En CMD:

```cmd
.venv\Scripts\activate
```

Si PowerShell bloquea la ejecución de scripts, ejecutar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

Copia el archivo de variables de entorno.

En PowerShell:

```powershell
Copy-Item .env.example .env -Force
```

En CMD:

```cmd
copy .env.example .env
```

Carga datos iniciales:

```bash
python seed.py
```

Arranca el backend:

```bash
python run.py
```

El backend quedará disponible en:

```text
http://localhost:3000
```

La documentación automática de FastAPI estará en:

```text
http://localhost:3000/docs
```

---

## Ejecución del frontend

Abre una segunda terminal y entra en la carpeta del frontend:

```bash
cd "C:\Users\aleja\OneDrive\Escritorio\Nueva carpeta\Programacion_web2_practica2\frontend-svelte"
```

Instala dependencias:

```bash
npm install
```

Ejecuta el servidor de desarrollo:

```bash
npm run dev
```

El frontend quedará disponible normalmente en:

```text
http://localhost:5173
```

---

## Usuarios de prueba

El archivo `seed.py` crea usuarios iniciales para probar la aplicación.

### Usuario administrador

```text
Usuario: admin
Contraseña: admin123
Rol: admin
```

### Usuario normal

```text
Usuario: user
Contraseña: user123
Rol: user
```

---

## Endpoints principales del backend

### Autenticación

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/api/login` | Iniciar sesión y obtener token JWT |
| POST | `/api/register` | Registrar usuario |

### Productos

| Método | Endpoint | Permiso |
|---|---|---|
| GET | `/api/productos` | Usuario autenticado |
| GET | `/api/productos/{id}` | Usuario autenticado |
| POST | `/api/productos` | Admin |
| PUT | `/api/productos/{id}` | Admin |
| DELETE | `/api/productos/{id}` | Admin |

### Usuarios

| Método | Endpoint | Permiso |
|---|---|---|
| GET | `/api/users` | Admin |
| GET | `/api/users/{id}` | Admin |
| POST | `/api/users` | Admin |
| PUT | `/api/users/{id}` | Admin |
| DELETE | `/api/users/{id}` | Admin |

### Salud del backend

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/health` | Comprueba que el backend está activo |

---

## Autenticación y roles

El backend utiliza JWT para autenticar usuarios.

Al iniciar sesión correctamente en `/api/login`, el backend devuelve un token JWT con información del usuario:

```json
{
  "token": "jwt_generado"
}
```

El token incluye datos como:

```json
{
  "id": 1,
  "username": "admin",
  "role": "admin"
}
```

Las rutas protegidas comprueban:

- Si el token existe.
- Si el token es válido.
- Si el usuario tiene permisos suficientes.
- Si el rol es `admin` cuando la operación lo requiere.

Errores esperados:

```text
401 Unauthorized
403 Forbidden
422 Unprocessable Entity
404 Not Found
```

---

## Arquitectura del backend

El backend está dividido en capas para cumplir con una arquitectura limpia y evitar que toda la lógica esté concentrada en un único archivo.

### `routers`

Definen las rutas HTTP.

Ejemplo:

```text
backend/app/routers/product_router.py
```

### `controllers`

Reciben la petición, llaman a los servicios y devuelven la respuesta.

```text
backend/app/controllers/product_controller.py
```

### `services`

Contienen la lógica de negocio.

```text
backend/app/services/product_service.py
```

### `repositories`

Gestionan el acceso a la base de datos.

```text
backend/app/repositories/product_repository.py
```

### `schemas`

Definen validaciones y estructuras de entrada/salida con Pydantic.

```text
backend/app/schemas/product_schema.py
```

### `models`

Define los modelos ORM con SQLAlchemy.

```text
backend/app/models.py
```

### `dependencies`

Contiene dependencias reutilizables, como autenticación y autorización.

```text
backend/app/dependencies/auth.py
```

### `core`

Contiene configuración, seguridad y excepciones.

```text
backend/app/core/
```

---

## Base de datos

La aplicación utiliza SQLite como base de datos real mediante SQLAlchemy ORM.

La base de datos se genera localmente en:

```text
backend/data/app.db
```

Este archivo no se sube al repositorio porque está incluido en `.gitignore`.

Para recrearlo:

```bash
cd backend
python seed.py
```

---

## Validaciones avanzadas

La versión avanzada incluye validación estricta con Pydantic.

Ejemplos de validaciones:

- El nombre de producto es obligatorio.
- El precio debe ser mayor o igual que 0.
- El rol de usuario solo puede ser `user` o `admin`.
- El username no puede estar vacío.
- La contraseña debe cumplir una longitud mínima.
- Los datos inválidos devuelven error `422`.

Ejemplo de error:

```json
{
  "error": "Validation error",
  "message": "Los datos enviados no son válidos",
  "details": []
}
```

---

## Manejo global de excepciones

El backend centraliza los errores para devolver respuestas limpias y consistentes.

Se gestionan, entre otros:

- Errores HTTP.
- Errores de validación.
- Errores de lógica de negocio.
- Errores de base de datos.
- Errores inesperados.

Esto evita mostrar trazas internas al usuario y mejora la seguridad del backend.

---

## Documentación incluida

El proyecto incluye varios documentos de apoyo:

```text
CHECKLIST_ENTREGA_COMPLETA.md
```

Checklist general de la entrega.

```text
CHECKLIST_REQUISITOS_MINIMOS.md
```

Comprobación de requisitos mínimos.

```text
CHECKLIST_FUNCIONALIDADES_AVANZADAS.md
```

Comprobación de funcionalidades avanzadas.

```text
DOCUMENTACION_AVANZADOS_BACKEND.md
```

Explicación técnica de las mejoras avanzadas.

```text
MEMORIA_USO_IA.md
```

Memoria del uso de Inteligencia Artificial durante el desarrollo.

---

## Uso de Inteligencia Artificial

Durante el desarrollo se ha utilizado IA como apoyo para:

- Diseñar la arquitectura por capas.
- Refactorizar el backend hacia FastAPI.
- Implementar autenticación JWT.
- Mejorar validaciones con Pydantic.
- Revisar errores de compatibilidad con el frontend.
- Documentar decisiones técnicas.

El uso de IA está documentado en:

```text
MEMORIA_USO_IA.md
```

Este documento incluye:

- Prompts utilizados.
- Iteraciones realizadas.
- Errores o alucinaciones detectadas.
- Correcciones manuales aplicadas.

---

## Comprobación rápida

### Backend

```bash
cd backend
python run.py
```

Abrir:

```text
http://localhost:3000/docs
```

### Frontend

```bash
cd frontend-svelte
npm run dev
```

Abrir:

```text
http://localhost:5173
```

### Login de prueba

```text
admin / admin123
```

---

## Subida a GitHub

Para subir cambios:

```bash
git status
git add .
git commit -m "mensaje del cambio"
git push origin main
```

Para consultar ramas:

```bash
git branch
```

Para cambiar de rama:

```bash
git switch nombre-rama
```

---

## Archivos ignorados

El proyecto no sube al repositorio archivos generados localmente como:

```text
backend/.env
backend/.venv/
backend/data/app.db
backend/uploads/*
frontend-svelte/node_modules/
frontend-svelte/dist/
__pycache__/
```

Esto evita subir:

- Variables privadas.
- Bases de datos locales.
- Entornos virtuales.
- Dependencias instaladas.
- Archivos temporales.
- Imágenes subidas durante pruebas.

---

## Estado final del proyecto

La versión final presentada corresponde a:

```text
main
```

También se conserva:

```text
v1-base
```

como versión mínima original.

La versión avanzada también está disponible como:

```text
v2-avanzado-backend
```

y como etiqueta:

```text
v2
```

---

## Autor

Proyecto desarrollado para la asignatura de Programación Web 2.

Alumno: Alejandro Viñas
