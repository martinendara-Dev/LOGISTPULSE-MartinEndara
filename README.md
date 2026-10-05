# LOGISTPULSE-GOLDEN V1.0

**Independent LOGISTdragon universe — Operations, Logistics, IoT and Platform Engineering laboratory.**

LOGISTPULSE simulates a national restaurant/retail operation with 300 stores, distribution centers, fleet telemetry, kitchen equipment and event-driven order fulfillment. It is intentionally independent from BANKdragon/BANKPULSE.

## Product domains

- **Smart Inventory** — stock, forecast and stockout risk.
- **Supply & Distribution** — trucks, ETA and cold chain.
- **Smart Operations** — MQTT equipment telemetry and operational state.
- **Order Fulfillment** — event-driven kitchen queue using Kafka-compatible Redpanda.

## Architecture

```text
Browser / Operations Console :8080
          |
       Nginx Edge
          |
  +-------+---------+-----------+
  |       |         |           |
Inventory Distribution Operations Fulfillment
  |       |         |           |
Postgres Postgres  MongoDB    Postgres
                    ^           |
                    |           v
                  MQTT       Redpanda
                    ^           |
              Telemetry      Worker
              Simulator

Prometheus + Grafana + cAdvisor observe the runtime.
```

## Start

```bash
cp .env.example .env
docker compose up -d --build
docker compose ps
bash scripts/smoke.sh
```

Open Codespaces port **8080**.

## Observability

```bash
docker compose -f observability/compose.yaml up -d
```

- Grafana `3000` — `admin / logistpulse_demo`
- Prometheus `9090`
- cAdvisor `8088`

## Git/CI model

Work through feature branches and Pull Requests. `.github/workflows/ci.yml` validates the architecture contract, Compose configuration, builds the distributed stack and runs smoke tests before merge.

## Academic ownership

Design of Systems teams own frontend/backend product evolution. Software Development teams act as DevOps/Platform teams: Codespaces, CI/CD, containerization, integration readiness, observability and later DevSecOps security gates.

See `docs/` for C4, data ownership, missions and incident runbooks.

## Entrega de Diseño de Sistemas

### Alcance y autoría

El equipo está formado por Martín Endara, Antonio Muñoz y Marco Bonilla. La base heredada corresponde a `randUSFQ/LOGISTPULSE-GOLDEN`, commit `74fe4cdbedb32c55a7848b35195229adc58578b6`. El aporte del equipo está en la rama `docs/value-recovery-lp` y comprende el backlog, el Sprint 1, el diagrama MVC, la matriz de trazabilidad, la prueba de extremo a extremo y estas instrucciones. BANKPULSE no forma parte de esta entrega.

Repositorio del equipo: https://github.com/martinendara-Dev/LOGISTPULSE-MartinEndara. PR de HU-LP-01 a HU-LP-04: https://github.com/martinendara-Dev/LOGISTPULSE-MartinEndara/pull/1. El PR queda abierto hasta una revisión real de Antonio Muñoz o Marco Bonilla.

El Sprint 1 cubre HU-LP-01 a HU-LP-04: crear un pedido, consultarlo y comprobar que el mismo `orderId` avanza de `WAITING` a `PREPARING` y `READY` mediante Redpanda y `fulfillment-worker`.

- [Backlog y Sprint 1](docs/value-recovery/BACKLOG.md)
- [Diagrama y justificación MVC](docs/value-recovery/MVC.md)
- [Matriz de trazabilidad](docs/value-recovery/TRAZABILIDAD.csv)
- [Evidencia de ejecución](docs/value-recovery/EVIDENCIAS.md)

### Requisitos

- Docker Desktop con Docker Compose v2.
- Git 2.x.
- Python 3 para ejecutar la prueba de aceptación desde el host.
- Puertos disponibles: `8080` para la consola. PostgreSQL, MongoDB, MQTT y Redpanda permanecen dentro de la red `logistpulse-net`.

### Variables de entorno

Copiar `.env.example` a `.env`. El archivo `.env` está ignorado por Git y no debe publicarse. Las credenciales incluidas son exclusivamente de laboratorio.

| Variable | Uso | Valor de laboratorio |
| --- | --- | --- |
| `POSTGRES_USER` | Usuario de PostgreSQL | `logist` |
| `POSTGRES_PASSWORD` | Clave local de PostgreSQL | Configurar solo en `.env`; no publicar |
| `POSTGRES_HOST` | Host interno de PostgreSQL | `postgres` |
| `POSTGRES_PORT` | Puerto interno de PostgreSQL | `5432` |
| `MONGO_URI` | Conexión interna a MongoDB | `mongodb://mongo:27017` |
| `MQTT_HOST` / `MQTT_PORT` | Broker MQTT interno | `mosquitto` / `1883` |
| `KAFKA_BOOTSTRAP` | Broker Kafka compatible | `redpanda:9092` |
| `GF_SECURITY_ADMIN_USER` | Usuario local de Grafana | `admin` |
| `GF_SECURITY_ADMIN_PASSWORD` | Clave local de Grafana | Configurar solo en `.env`; no publicar |

### Estructura relevante

```text
frontend/                         Vista web y Nginx
services/fulfillment-api/         Controlador FastAPI y acceso SQL
services/fulfillment-worker/      Consumidor de eventos y cambio de estados
infra/postgres/init/              Creación de bases de datos
docs/value-recovery/              Entregables del equipo
scripts/value-recovery-smoke.py   Prueba real de HU-LP-01 a HU-LP-04
compose.yaml                      Servicios, red y volúmenes
```

### Inicio y comprobaciones

En PowerShell:

```powershell
Copy-Item .env.example .env
docker compose config --quiet
docker compose up --build -d --wait
docker compose ps
python scripts/value-recovery-smoke.py --project LOGISTPULSE
```

En Linux o macOS, sustituir la primera línea por `cp .env.example .env`. La consola queda disponible en `http://localhost:8080`. Las rutas de aceptación son:

- `GET /health/fulfillment`
- `POST /api/fulfillment/orders`
- `GET /api/fulfillment/orders`

La prueba escribe `evidencias/sprint1.json`. El resultado solo se considera aprobado cuando el archivo registra `PASS`, un `POST` con HTTP 201 y la secuencia del mismo identificador `WAITING`, `PREPARING`, `READY`.

La ejecución verificada del 05 de octubre de 2026 sobre el commit `370b8dd90a637546400304ba63161fbbc0b85d4b` produjo el pedido `ORD-656EE9` y terminó en `PASS`. Tras recrear los contenedores sin borrar volúmenes, el API y PostgreSQL conservaron ese pedido en `READY`.

Para revisar fallos:

```powershell
docker compose logs --no-color postgres redpanda fulfillment-api fulfillment-worker console
docker compose ps
```

`pg_data` conserva los pedidos al reiniciar los contenedores. `docker compose down` conserva el volumen; `docker compose down -v` lo elimina y no debe usarse durante la comprobación de persistencia.

### Modelo MVC del módulo

La separación MVC es lógica. `frontend/index.html` y `frontend/app.js` son la Vista. Las rutas `create()`, `orders()` y `health()` de `services/fulfillment-api/app.py` actúan como Controlador. `NewOrder`, la tabla `orders`, el SQL y `fulfillment-worker` componen el Modelo y el procesamiento de dominio. Redpanda comunica la creación con el worker sin reemplazar PostgreSQL como fuente persistente del estado.

### Limitaciones conocidas

El código heredado no rechaza totales negativos, no implementa idempotencia y no garantiza recuperar un pedido si la publicación del evento falla después de guardar en PostgreSQL. Estas mejoras corresponden a historias posteriores y no se presentan como terminadas en el Sprint 1.

