# 🤝 Guía de Contribución — Microservicio de Tareas

Gracias por contribuir a este proyecto. A continuación se describen las reglas y convenciones que seguimos.

---

## 🌿 Estrategia de Branching (GitFlow)

Usamos **GitFlow** con las siguientes ramas:

| Rama | Origen | Destino | Propósito |
|---|---|---|---|
| `main` | — | — | Código en producción, estable |
| `develop` | `main` | `main` | Integración de nuevas funcionalidades |
| `feature/<nombre>` | `develop` | `develop` | Desarrollo de una nueva funcionalidad |
| `hotfix/<nombre>` | `main` | `main` + `develop` | Corrección urgente en producción |

### Crear una rama feature
```bash
git checkout develop
git pull origin develop
git checkout -b feature/nombre-descriptivo
```

### Crear una rama hotfix
```bash
git checkout main
git pull origin main
git checkout -b hotfix/descripcion-del-fix
```

---

## 📝 Convenciones de Commits

Usamos **Conventional Commits** para mantener un historial claro y generable:

```
<tipo>: <descripción breve>
```

### Tipos permitidos

| Tipo | Uso |
|---|---|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de un bug |
| `docs` | Cambios en documentación |
| `refactor` | Refactorización sin cambio de funcionalidad |
| `test` | Añadir o modificar tests |
| `chore` | Tareas de mantenimiento (CI, dependencias) |
| `ci` | Cambios en la configuración de CI/CD |

### Ejemplos buenos ✅
```
feat: agregar endpoint DELETE para eliminar tareas
fix: corregir asignación de ID duplicado en tareas concurrentes
docs: actualizar README con instrucciones de Docker
ci: agregar SonarCloud al pipeline de CI/CD
test: agregar tests para el endpoint PUT /tareas/<id>
```

### Ejemplos malos ❌
```
fix
cambios
update
arreglos varios
```

---

## 🔀 Reglas de Pull Request

### Para abrir un PR:
1. La rama debe estar actualizada con su rama base (`develop` o `main`).
2. Todos los tests deben pasar localmente antes de abrir el PR.
3. El título del PR debe seguir la convención de commits.
4. Incluir una descripción de **qué** cambia y **por qué**.

### Para aprobar un PR:
- Se requiere **al menos 1 revisión aprobatoria** de otro integrante.
- El pipeline de CI/CD debe pasar exitosamente (tests + SonarCloud).
- El Quality Gate de SonarCloud no debe tener errores críticos.
- No se permiten pushes directos a `main` (branch protection activa).

### Proceso de merge:
1. Abrir PR con descripción clara.
2. Esperar revisión del compañero.
3. Resolver comentarios si los hay.
4. Merge una vez aprobado y pipeline verde.
5. Eliminar la rama después del merge.

---

## 🧪 Tests

Antes de abrir un PR, ejecutar los tests localmente:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest test_app.py -v

# Ejecutar tests con cobertura
pytest test_app.py -v --cov=app --cov-report=term-missing
```

---

## 🐳 Desarrollo con Docker

```bash
# Construir imagen
docker build -t microservicio-tareas .

# Levantar todos los servicios
docker compose up -d

# Ver logs
docker compose logs -f

# Detener servicios
docker compose down
```
