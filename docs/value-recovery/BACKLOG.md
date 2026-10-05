# Product Backlog LOGISTPULSE

INC-LP-01: incepción 2.1 del PDF inicial. TEC-LP-01/02/03: análisis documental, escenarios y prototipado de sus secciones 2.2/2.3/2.4. Los hallazgos BP/LP mantienen los IDs del documento del equipo.

MoSCoW: Must obligatorio, Should importante, Could ampliación. Puntos relativos: 1 simple, 2 varios casos, 3 integración/recuperación. No equivalen a horas. Código base existente significa revisión estática, no prueba ejecutada.

## HU-LP-01
Como operador, quiero crear un pedido, para iniciar su preparación.

Aceptación: POST /api/fulfillment/orders con storeId, channel y total: 201, orderId y estado inicial WAITING.
Origen: LP-01 / LP-02; prioridad Must; 2 puntos; depende de —. Estado: Verificada en Docker, `T-LP-01 PASS`.

## HU-LP-02
Como operador, quiero consultar pedidos recientes, para identificar el que registré.

Aceptación: GET /api/fulfillment/orders: 200; máximo 20 pedidos, del más reciente al más antiguo; contiene el orderId creado.
Origen: LP-03; prioridad Must; 1 punto; depende de 01. Estado: Verificada en Docker, `T-LP-02 PASS`.

## HU-LP-03
Como responsable de cocina, quiero recibir pedidos nuevos, para iniciar su procesamiento.

Aceptación: Con broker y worker disponibles, ORDER_CREATED se publica en logistpulse.orders y el worker actualiza el mismo orderId a PREPARING.
Origen: LP-04; prioridad Must; 2 puntos; depende de 01. Estado: Verificada en Docker, `T-LP-03 PASS`.

## HU-LP-04
Como operador, quiero observar el avance del pedido, para saber cuándo está listo.

Aceptación: En laboratorio sin cola previa, el mismo id pasa WAITING → PREPARING → READY en ≤ 60 s; cada consulta refleja su estado guardado.
Origen: LP-05; prioridad Must; 2 puntos; depende de 02,03. Estado: Verificada en Docker, `T-LP-04 PASS`.

## HU-LP-05
Como operador, quiero rechazar totales negativos, para evitar pedidos incorrectos.

Aceptación: Total negativo: respuesta 422 o 400 explicando el error y ningún pedido nuevo.
Origen: LP-08; prioridad Should; 1 puntos; depende de 01. Estado: Pendiente; el modelo base no valida positividad.

## HU-LP-06
Como operador, quiero una confirmación con id, para reconocer el pedido creado.

Aceptación: Después de crear, la pantalla muestra el orderId y una confirmación del estado inicial.
Origen: LP-07; prioridad Should; 1 puntos; depende de 01. Estado: Propuesto; la Vista debe ampliarse.

## HU-LP-07
Como operador, quiero etiquetas claras de estado, para entender el avance sin depender del color.

Aceptación: WAITING, PREPARING y READY se presentan como En espera, En preparación y Listo, siempre con texto.
Origen: LP-09 / LP-15; prioridad Should; 1 puntos; depende de 02. Estado: Propuesto; la Vista usa etiquetas técnicas.

## HU-LP-08
Como operador, quiero actualizar el listado y reconocer errores, para consultar información vigente.

Aceptación: Actualizar muestra hora de consulta; una lista vacía y una falla presentan mensajes distintos.
Origen: LP-10 / LP-12 / LP-14; prioridad Should; 2 puntos; depende de 02. Estado: Propuesto; prueba UI pendiente.

## HU-LP-09
Como supervisor, quiero recuperar pedidos sin procesar, para evitar que queden olvidados.

Aceptación: Si la publicación falla, el pedido sigue consultable y un mecanismo de recuperación lo procesa sin crear otro id.
Origen: LP-11; prioridad Could; 3 puntos; depende de 01,03. Estado: Pendiente; no existe recuperación garantizada.

## HU-LP-10
Como operador, quiero bloquear el botón mientras envío, para evitar solicitudes repetidas.

Aceptación: Mientras hay una creación pendiente, el botón no permite otro envío; ante respuesta perdida advierte consultar antes de repetir.
Origen: LP-16 / LP-17; prioridad Could; 1 puntos; depende de 01. Estado: Propuesto; no hay idempotencia de pedidos.

## SPR-LP-01
Crear un pedido ficticio, consultarlo y demostrar su procesamiento automático hasta READY.
Historias: HU-LP-01, HU-LP-02, HU-LP-03, HU-LP-04; 7 puntos. Duración: una semana. Capacidad propuesta para LOGISTPULSE: 18 horas de trabajo total; tres integrantes con 6 horas disponibles cada uno. Confirmar disponibilidad.
Roles propuestos: PO Martín Endara; SM Antonio Muñoz; desarrollo Martín, Antonio y Marco Bonilla.
Definition of Done: criterios verificados en el stack original, evidencia guardada, README y matriz actualizados, PR revisado/comentado por otro integrante y fusionado, sin secretos. El código heredado se distingue del aporte nuevo. Estado al cierre técnico: aceptación, evidencia y documentación completas; revisión humana y fusión pendientes.

## Tareas técnicas
- HU-01: identificar contrato y probar creación; Marco, 2 h.
- HU-02: comprobar validaciones (BP) o consulta (LP); Marco, 2 h.
- HU-03: probar reintento (BP) o llegada al worker (LP); Marco y Antonio, 3 h.
- HU-04: comprobar consulta (BP) o secuencia del mismo id (LP); Antonio, 3 h.
- Backlog, MVC y matriz; Martín, 4 h.
- README, PR, revisión cruzada y evidencia; Martín y Antonio, 3 h.
- Ensayo del flujo; los tres, 1 h de trabajo total.

Total para LOGISTPULSE: 18 horas. En las tareas compartidas las horas son esfuerzo combinado, no se multiplican por persona. Se propone una semana, del 05 al 11 de octubre de 2026. Estos responsables son una propuesta de planificación.
