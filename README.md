# 🛠️ Microservicio de Gestión de Tareas

[![CI/CD Pipeline](https://github.com/gferrufino/MicroservicioColaborativo/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/gferrufino/MicroservicioColaborativo/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=gferrufino_MicroservicioColaborativo&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=gferrufino_MicroservicioColaborativo)

Microservicio desarrollado en **Python (Flask)** como parte del pipeline DevOps de la asignatura **Ingeniería DevOps (DOY0101)**.

**Docente:** Cristian Bugueño Pantoja

---

## 📌 Descripción del Proyecto

API REST de gestión de tareas que permite crear, listar, completar y eliminar tareas. El proyecto implementa un pipeline CI/CD completo con:

- **Control de versiones** con GitFlow
- **Contenerización** con Docker y Docker Compose
- **Integración continua** con GitHub Actions
- **Análisis de calidad** con SonarCloud
- **Escaneo de dependencias** con Dependabot
- **Despliegue automático** a AWS EC2
- **Monitoreo** con AWS CloudWatch

### Endpoints disponibles

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Health check del servicio |
| `GET` | `/tareas` | Listar todas las tareas |
| `POST` | `/tareas` | Crear nueva tarea (body: `{"titulo": "..."}`) |
| `GET` | `/tareas/<id>` | Obtener tarea por ID |
| `PUT` | `/tareas/<id>` | Marcar tarea como completada |
| `DELETE` | `/tareas/<id>` | Eliminar tarea |

---

## 🏗️ Arquitectura del Proyecto

```
                    ┌─────────────────────────────────────────────┐
                    │              GitHub Repository               │
                    │                                              │
                    │  push/PR ──► GitHub Actions (CI/CD Pipeline) │
                    │               │                              │
                    │               ├── 🧪 Tests (pytest)         │
                    │               ├── 🔍 SonarCloud Analysis    │
                    │               ├── 🐳 Docker Build & Push    │
                    │               └── 🚀 Deploy to EC2          │
                    └──────────────────────┬──────────────────────┘
                                           │
                                           ▼
                    ┌─────────────────────────────────────────────┐
                    │              AWS EC2 Instance                 │
                    │                                              │
                    │  ┌─────────────────────────────────────┐    │
                    │  │        Docker Compose                │    │
                    │  │                                      │    │
                    │  │  ┌──────────────┐  ┌─────────────┐  │    │
                    │  │  │  Flask API   │  │    Redis     │  │    │
                    │  │  │  (puerto     │──│  (cache,     │  │    │
                    │  │  │   5000)      │  │   puerto     │  │    │
                    │  │  │              │  │   6379)      │  │    │
                    │  │  └──────────────┘  └─────────────┘  │    │
                    │  │       tareas-network                 │    │
                    │  └─────────────────────────────────────┘    │
                    │                                              │
                    │  CloudWatch Agent ──► Métricas & Logs        │
                    └─────────────────────────────────────────────┘
```

---

## 📁 Estructura del Proyecto

```
microservicio-tareas/
├── app.py                        # API Flask — lógica del microservicio
├── test_app.py                   # Tests unitarios con pytest
├── requirements.txt              # Dependencias Python
├── Dockerfile                    # Imagen Docker multi-stage
├── docker-compose.yml            # Orquestación: app + Redis
├── .dockerignore                 # Exclusiones del build Docker
├── sonar-project.properties      # Configuración de SonarCloud
├── CONTRIBUTING.md               # Guía de contribución y reglas de PR
├── README.md                     # Este archivo
└── .github/
    ├── dependabot.yml            # Escaneo automático de dependencias
    └── workflows/
        └── ci-cd.yml             # Pipeline CI/CD completo
```

---

## 🌿 Estrategia de Ramificación: GitFlow

Se eligió **GitFlow** como estrategia de ramificación por las siguientes razones:

- Permite separar claramente el código en producción (`main`) del código en desarrollo (`develop`).
- Facilita el trabajo en equipo mediante ramas específicas para cada funcionalidad (`feature/`) y correcciones urgentes (`hotfix/`).
- Es ideal para proyectos con ciclos de entrega definidos, como este proyecto académico.
- Proporciona mayor trazabilidad del código, cumpliendo con los estándares de CI/CD.

### Comparación con Trunk-Based Development

| Característica | GitFlow | Trunk-Based |
|---|---|---|
| Ramas principales | `main` + `develop` | Solo `main` |
| Ideal para | Equipos medianos, releases programados | Equipos grandes, despliegue continuo |
| Complejidad | Media | Baja |
| Trazabilidad | Alta | Media |

### Estructura de Ramas

| Rama | Origen | Propósito |
|---|---|---|
| `main` | — | Código en producción, estable |
| `develop` | `main` | Integración de nuevas funcionalidades |
| `feature/<nombre>` | `develop` | Desarrollo de una nueva funcionalidad |
| `hotfix/<nombre>` | `main` | Correcciones urgentes en producción |

> Para más detalles sobre convenciones de commits, reglas de PR y flujo de merge, ver [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 🐳 Docker — Contenerización

### Dockerfile (multi-stage build)

El `Dockerfile` implementa buenas prácticas:

- **Imagen base liviana:** `python:3.10-slim` (~50 MB vs ~900 MB de la imagen full)
- **Multi-stage build:** Separa la instalación de dependencias (builder) de la imagen final (production)
- **Usuario no-root:** Se ejecuta como `appuser` por seguridad
- **Health check integrado:** Docker verifica automáticamente que la app responde
- **Cache de capas:** `requirements.txt` se copia antes que el código para aprovechar el cache

### Docker Compose — Orquestación

Se orquestan **2 servicios**:

| Servicio | Imagen | Puerto | Propósito |
|---|---|---|---|
| `app` | Build local | 5000 | API Flask (microservicio principal) |
| `redis` | `redis:7-alpine` | 6379 | Cache y persistencia de datos |

Características:
- **Health checks** en ambos servicios
- **Dependencia ordenada:** `app` espera a que `redis` esté healthy
- **Red compartida:** `tareas-network` (bridge)
- **Volumen persistente:** `redis-data` para no perder datos entre reinicios
- **Restart policy:** `unless-stopped`

### Levantar el entorno localmente

```bash
# Clonar el repositorio
git clone https://github.com/gferrufino/MicroservicioColaborativo.git
cd MicroservicioColaborativo

# Opción 1: Con Docker Compose (recomendado)
docker compose up -d
# La API estará disponible en http://localhost:5000

# Opción 2: Sin Docker
pip install -r requirements.txt
python app.py
# La API estará disponible en http://localhost:5000

# Verificar que funciona
curl http://localhost:5000/health

# Probar los endpoints
curl -X POST http://localhost:5000/tareas -H "Content-Type: application/json" -d '{"titulo": "Mi primera tarea"}'
curl http://localhost:5000/tareas
```

---

## ⚙️ Pipeline CI/CD — GitHub Actions

El pipeline se ejecuta automáticamente en:
- Cada **push** a `develop` o `main`
- Cada **Pull Request** hacia `main`

### Flujo completo (4 jobs)

```
commit → push/PR
    │
    ▼
┌──────────────────┐
│  🧪 Test         │  Ejecuta pytest con cobertura
│  (ubuntu-latest) │  Si falla → pipeline se detiene
└────────┬─────────┘
         │ ✅
         ▼
┌──────────────────┐
│  🔍 SonarCloud   │  Análisis de calidad y seguridad
│  Quality Gate    │  Si falla → pipeline se detiene
└────────┬─────────┘
         │ ✅
         ▼
┌──────────────────┐
│  🐳 Docker       │  Build imagen + push a Docker Hub
│  Build & Push    │  Solo en push (no en PRs)
└────────┬─────────┘
         │ ✅
         ▼
┌──────────────────┐
│  🚀 Deploy       │  SSH a EC2 + docker compose up
│  to EC2          │  Solo en push a main
└──────────────────┘
```

### Trazabilidad

Cada commit se puede seguir en toda la cadena:
1. **Commit** → visible en el historial de Git
2. **Build** → visible en la pestaña Actions de GitHub
3. **Test** → resultados de pytest en los logs del workflow
4. **Quality** → dashboard de SonarCloud
5. **Deploy** → imagen etiquetada con el SHA del commit en Docker Hub

### Secrets necesarios en GitHub

| Secret | Descripción |
|---|---|
| `DOCKER_USERNAME` | Usuario de Docker Hub |
| `DOCKER_PASSWORD` | Password/token de Docker Hub |
| `SONAR_TOKEN` | Token de autenticación de SonarCloud |
| `EC2_HOST` | IP o hostname de la instancia EC2 |
| `EC2_USERNAME` | Usuario SSH de EC2 (ej. `ec2-user`) |
| `EC2_SSH_KEY` | Clave privada SSH para EC2 |

---

## 🔍 Calidad y Seguridad

### SonarCloud
- **Integrado en el pipeline:** se ejecuta en cada PR hacia `main`
- **Quality Gate configurado:** bloquea el merge si hay errores críticos
- **Métricas:** bugs, vulnerabilidades, code smells, cobertura de código
- **Dashboard:** [Ver en SonarCloud](https://sonarcloud.io/summary/new_code?id=gferrufino_MicroservicioColaborativo)

### Dependabot
- **Escaneo semanal** de dependencias Python, GitHub Actions y Docker
- **PRs automáticos** cuando se detectan vulnerabilidades
- **Labels automáticos:** `dependencies`, `security`

### Branch Protection
- Push directo a `main` está **bloqueado**
- Se requiere al menos **1 aprobación** en el PR
- El pipeline CI/CD debe pasar antes del merge
- Los secretos están protegidos como **GitHub Secrets** (nunca en el código)

---

## 📊 Monitoreo y Logging (CloudWatch)

### Logging en la aplicación
- Se usa el módulo `logging` de Python con formato estructurado
- Niveles: `INFO` para operaciones normales, `WARNING` para errores de validación
- Gunicorn envía access logs a stdout → CloudWatch los captura

### Dashboards de CloudWatch

Se configuraron dashboards con las siguientes métricas:

| Métrica | Descripción | Por qué importa |
|---|---|---|
| **CPU Utilization** | Uso de CPU de la instancia EC2 | Detectar sobrecarga del servicio |
| **Memory Usage** | Uso de memoria RAM | Prevenir OOM (Out of Memory) |
| **Network In/Out** | Tráfico de red | Monitorear volumen de requests |
| **Container Health** | Estado de los contenedores Docker | Detectar caídas del servicio |
| **HTTP 5xx Errors** | Errores del servidor | Alertar sobre fallos en la API |
| **Request Latency** | Tiempo de respuesta | Garantizar SLA de rendimiento |

### Alertas configuradas
- **CPU > 80%** durante 5 minutos → Notificación
- **Container unhealthy** → Alerta crítica
- **5xx errors > 10/min** → Alerta crítica

---

## 🧪 Tests

Ejecutar los tests localmente:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
pytest test_app.py -v

# Ejecutar tests con reporte de cobertura
pytest test_app.py -v --cov=app --cov-report=term-missing
```

### Tests implementados

| Clase | Tests | Qué valida |
|---|---|---|
| `TestHealthCheck` | 2 | Endpoint `/health` responde con status y versión |
| `TestAgregarTarea` | 4 | Crear tareas válidas e inválidas (sin título, vacío, sin JSON) |
| `TestListarTareas` | 2 | Lista vacía y con datos |
| `TestObtenerTarea` | 2 | Obtener por ID existente e inexistente |
| `TestCompletarTarea` | 2 | Completar tarea existente e inexistente |
| `TestEliminarTarea` | 2 | Eliminar tarea existente e inexistente |

---

## 🤖 Herramientas de IA Utilizadas

En el desarrollo de este proyecto se utilizaron las siguientes herramientas de IA:

| Herramienta | Uso | Alcance |
|---|---|---|
| **GitHub Copilot / Gemini** | Asistencia en la escritura de código y documentación | Generación de boilerplate, estructura de archivos |
| **ChatGPT / Gemini** | Consultas técnicas sobre Docker, CI/CD, AWS | Resolución de dudas de configuración |

**Nota:** Todas las decisiones de arquitectura, estrategia de branching y diseño del pipeline fueron tomadas por los integrantes del equipo. Las herramientas de IA se usaron como apoyo, no como generador del trabajo final.

---

## 💭 Reflexiones Individuales

### Gabriel Ferrufino
<!-- 
⚠️ IMPORTANTE: Esta sección debe ser escrita por Gabriel de forma genuina, 
sin apoyo de herramientas de IA. Incluir:
- Qué aprendí durante el semestre sobre DevOps
- Cuál fue mi contribución principal al proyecto
- Qué desafíos enfrenté y cómo los resolví
- Qué haría diferente si empezara de nuevo
-->
*[Pendiente — escribir reflexión personal sin uso de IA]*

### Matias Pulgar
<!-- 
⚠️ IMPORTANTE: Esta sección debe ser escrita por Matias de forma genuina, 
sin apoyo de herramientas de IA. Incluir:
- Qué aprendí durante el semestre sobre DevOps
- Cuál fue mi contribución principal al proyecto
- Qué desafíos enfrenté y cómo los resolví
- Qué haría diferente si empezara de nuevo
-->
*[Pendiente — escribir reflexión personal sin uso de IA]*

---

## 👥 Integrantes

- **Gabriel Ferrufino**
- **Matias Pulgar**

---

## 📚 Referencias

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [SonarCloud Documentation](https://docs.sonarcloud.io/)
- [AWS CloudWatch Documentation](https://docs.aws.amazon.com/cloudwatch/)
