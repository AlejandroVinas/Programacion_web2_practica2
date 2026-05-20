# Frontend Svelte 5 - Práctica 2 PW2

Frontend SPA construido con **Svelte 5 + Vite**. Consume el backend Python/FastAPI de la Práctica 2 en `http://localhost:3000`.

## Requisitos previos

- Node.js 18 o superior.
- Backend funcionando en `http://localhost:3000`.

## Instalación y ejecución

Desde la raíz del proyecto:

```powershell
cd frontend-svelte
npm install
npm run dev
```

Abrir la URL indicada por Vite, normalmente:

```text
http://localhost:5173
```

## Backend necesario

Antes de iniciar sesión, debe estar arrancado el backend:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env -Force
python seed.py
python run.py
```

Documentación de la API:

```text
http://localhost:3000/docs
```

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `admin123` | admin |
| `user` | `user123` | user |

## Estructura del frontend

```text
src/
├── components/
│   ├── ProductCard.svelte
│   ├── ProductDetail.svelte
│   ├── ProductForm.svelte
│   ├── Toast.svelte
│   └── UserRow.svelte
├── pages/
│   ├── Login.svelte
│   ├── Products.svelte
│   ├── Profile.svelte
│   ├── Register.svelte
│   └── Users.svelte
├── services/
│   └── api.js
├── stores/
│   └── auth.svelte.js
├── App.svelte
└── main.js
```

## Endpoints consumidos

| Método | Ruta | Acceso |
|---|---|---|
| `POST` | `/api/login` | Público |
| `POST` | `/api/register` | Público |
| `GET` | `/api/productos` | Usuario autenticado |
| `POST` | `/api/productos` | Admin |
| `PUT` | `/api/productos/{id}` | Admin |
| `DELETE` | `/api/productos/{id}` | Admin |
| `GET` | `/api/users` | Admin |
| `POST` | `/api/users` | Admin |
| `PUT` | `/api/users/{id}` | Admin |
| `DELETE` | `/api/users/{id}` | Admin |

## Funcionalidades principales

- Login y registro.
- Almacenamiento del token JWT.
- Navegación SPA.
- Listado de productos.
- CRUD de productos para admin.
- Gestión de usuarios para admin.
- Vista de perfil.
- Mensajes de éxito/error mediante toast.

## Dependencias importantes

La versión de Vite se mantiene en `^5.0.0` porque es compatible con `@sveltejs/vite-plugin-svelte ^4.0.0`.
