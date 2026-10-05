# Evidencias LOGISTPULSE

## Ejecución verificada

- Fecha: 05 de octubre de 2026, 14:44 (America/Guayaquil).
- Commit probado: `370b8dd90a637546400304ba63161fbbc0b85d4b`.
- Comando: `python scripts/value-recovery-smoke.py --project LOGISTPULSE`.
- Resultado: `PASS` real sobre Docker; no se usaron simulaciones.
- Pedido de prueba: `ORD-656EE9`.
- Salud: `GET /health/fulfillment` devolvió HTTP 200 y `UP`.
- Creación: `POST /api/fulfillment/orders` devolvió HTTP 201, el id anterior y `WAITING`.
- Consulta: `GET /api/fulfillment/orders` devolvió HTTP 200 e incluyó el pedido.
- Evento: el mismo id fue observado en `WAITING`, `PREPARING` y `READY` mediante Redpanda y `fulfillment-worker`.
- Persistencia: después de `docker compose down` y `docker compose up -d --wait`, el API y PostgreSQL conservaron `ORD-656EE9` en `READY`.

La salida íntegra y estructurada está en `evidencias/sprint1.json`; la comprobación del entorno y de persistencia está en `evidencias/verificacion-entorno.json`. El repositorio de entrega es https://github.com/martinendara-Dev/LOGISTPULSE-MartinEndara y el PR es https://github.com/martinendara-Dev/LOGISTPULSE-MartinEndara/pull/1. La revisión de Antonio Muñoz o Marco Bonilla y la fusión permanecen pendientes; no se atribuye una revisión no realizada.
