# Memoria de uso de Inteligencia Artificial

Este documento recoge el uso de IA durante el desarrollo y refactorización de la Práctica 2. El objetivo no ha sido copiar código sin revisión, sino utilizar la IA como apoyo para migrar el backend, detectar errores, mejorar arquitectura y documentar las decisiones técnicas.

## 1. Contexto de uso

La práctica pedía sustituir el backend original por un backend desarrollado en Python, manteniendo el frontend Svelte 5 y el contrato de API existente. La IA se usó como asistente para:

- Analizar los requisitos del PDF de la práctica.
- Identificar los endpoints que el frontend necesitaba conservar.
- Crear una primera versión mínima con FastAPI.
- Revisar si los requisitos mínimos estaban cubiertos.
- Ajustar la protección de rutas privadas.
- Añadir funcionalidades avanzadas de backend.
- Documentar la ejecución, checklist y uso de IA.

## 2. Prompts clave utilizados

### Prompt 1: adaptación inicial a requisitos mínimos

```text
Necesito hacer cambios en la práctica adjunta teniendo en cuenta los requisitos presentados en el PDF adjunto, centrémonos en primera instancia en los requisitos mínimos para el proyecto.
```

### Resultado esperado

Se pidió una versión mínima que cumpliera:

- Backend en Python con Flask o FastAPI.
- Separación por capas.
- JWT.
- Mismos endpoints principales que consumía el frontend Svelte.

### Refinamiento aplicado

Tras la primera versión se revisó el cumplimiento de requisitos mínimos y se detectó que `GET /api/productos` estaba público. Aunque el frontend podía funcionar así, el requisito de producto protegido por roles podía interpretarse de forma más estricta. Se decidió corregirlo para exigir autenticación también en el listado.

---

### Prompt 2: revisión de requisitos mínimos

```text
Revisa los requisitos mínimos dados.
```

### Resultado esperado

Se buscaba comprobar que la solución no solo arrancaba, sino que cumplía realmente el enunciado.

### Corrección derivada

Se ajustó la ruta:

```text
GET /api/productos
```

para que requiriera token JWT. Las acciones de crear, editar y borrar productos quedaron limitadas a rol `admin`.

---

### Prompt 3: funcionalidades avanzadas

```text
Continuemos ahora con las funcionalidades avanzadas del backend.
```

### Resultado esperado

Se pidió ampliar el backend para cubrir:

- Validación estricta.
- Manejo global de excepciones.
- Persistencia real con base de datos y patrón repositorio.

### Refinamiento aplicado

La primera versión ya tenía una organización por capas y validaciones básicas. Para reforzar el bloque avanzado se migró el acceso a datos hacia SQLAlchemy ORM, dejando el acceso encapsulado en repositorios.

---

### Prompt 4: documentación y ejecución

```text
Dado el último zip que has generado, realiza una checklist de todo y un README general para la ejecución del proyecto.
```

### Resultado esperado

Se pidió documentación clara para entregar y ejecutar el proyecto en Windows/VS Code, incluyendo backend, frontend, usuarios, endpoints y comprobaciones finales.

## 3. Error o alucinación detectada en la IA

### Error detectado

En una fase inicial, la IA propuso comandos de Linux o PowerShell sin tener en cuenta que algunos se estaban ejecutando realmente en CMD de Windows. Por ejemplo:

```bash
cat .gitignore
ls
```

En CMD esos comandos no funcionan. También ocurrió con comandos como `Expand-Archive`, que pertenecen a PowerShell, no a CMD.

### Por qué era incorrecto

La práctica se estaba ejecutando en Windows desde terminal integrada de Visual Studio Code. En Windows pueden usarse distintos shells:

- CMD.
- PowerShell.
- Git Bash.

Cada uno tiene comandos distintos. Usar comandos del shell equivocado bloquea la ejecución aunque el proyecto esté bien.

### Corrección manual aplicada

Se diferenciaron comandos para CMD y PowerShell. Finalmente, se usó PowerShell en VS Code y se documentaron comandos correctos como:

```powershell
Copy-Item .env.example .env -Force
Remove-Item -Recurse -Force .venv
Expand-Archive archivo.zip -DestinationPath destino -Force
```

Para CMD se usaron equivalentes como:

```cmd
type .gitignore
dir
```

## 4. Error técnico detectado durante el desarrollo

### Error detectado

El frontend fallaba al ejecutar `npm install` por conflicto de dependencias:

```text
Found: vite@6.x
Could not resolve dependency:
peer vite@^5.0.0 from @sveltejs/vite-plugin-svelte@4.x
```

### Por qué era incorrecto

El plugin `@sveltejs/vite-plugin-svelte@4.x` esperaba Vite 5, pero el proyecto tenía configurado Vite 6. Esto impedía instalar dependencias y después `npm run dev` fallaba porque `vite` no existía en `node_modules`.

### Corrección aplicada

Se ajustó la dependencia del frontend a:

```json
"vite": "^5.0.0"
```

Después se regeneró `package-lock.json` con `npm install`.

## 5. Decisiones revisadas manualmente

### Elección de FastAPI

Se eligió FastAPI porque facilita:

- Definir endpoints REST.
- Validar datos con Pydantic.
- Generar documentación automática en `/docs`.
- Usar dependencias para autenticación y autorización.

### Separación por capas

La IA sugirió una estructura modular. Se revisó y se mantuvo esta arquitectura:

```text
routers -> controllers -> services -> repositories -> models/database
```

Esto evita que `main.py` o los routers contengan toda la lógica.

### JWT y roles

Se comprobó que el token incluyera los campos necesarios para el frontend:

```json
{
  "id": "1",
  "username": "admin",
  "role": "admin"
}
```

También se revisó que las rutas privadas usaran:

```text
Authorization: Bearer <token>
```

### Persistencia

La primera aproximación podía usar SQLite de forma directa. Para cumplir mejor el requisito avanzado, se migró a SQLAlchemy ORM y se encapsuló el acceso a datos en repositorios.

### Seguridad básica

Se mantuvo el hash de contraseñas en backend y se evitó subir a GitHub:

- `.env`.
- `.venv`.
- `backend/data/app.db`.
- `node_modules`.
- Imágenes locales de `backend/uploads`.

## 6. Conclusión crítica

La IA fue útil para acelerar tareas de refactorización, documentación y revisión de requisitos. Sin embargo, sus respuestas necesitaron revisión manual, especialmente en:

- Comandos dependientes del sistema operativo.
- Compatibilidad de dependencias npm.
- Interpretación estricta de rutas protegidas.
- Separación real de responsabilidades.
- Persistencia mediante ORM en lugar de soluciones más simples.

El código final no se aceptó automáticamente: se revisó, se ejecutó, se corrigió y se documentaron las decisiones técnicas.
