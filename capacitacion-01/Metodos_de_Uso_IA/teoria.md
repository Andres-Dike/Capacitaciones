1. Métodos de uso de IA
1.1 LLM con Structured Output

Un LLM normalmente recibe texto y devuelve texto. Por ejemplo:

Usuario:
Analiza este contrato y dime cuál es la fecha de vencimiento.

LLM:
El contrato vence el 15 de diciembre de 2027.

El problema aparece cuando nuestro sistema necesita utilizar esa respuesta automáticamente.

Si queremos guardar la información en una base de datos, podríamos necesitar:

{
  "fecha_vencimiento": "2027-12-15",
  "riesgo": "medio",
  "monto": 25000
}

Si el modelo responde de manera ligeramente diferente:

La fecha de vencimiento es el 15 de diciembre de 2027.
El riesgo parece medio.
El monto involucrado es de $25.000.

un programa tendría que interpretar nuevamente ese texto.

Aquí entra Structured Output.

¿Qué es?

Structured Output permite pedir al LLM que entregue su respuesta siguiendo un esquema estructurado definido por nosotros, normalmente mediante JSON Schema.

La documentación de OpenAI diferencia el antiguo JSON mode de Structured Outputs: con json_schema y strict se puede exigir que la salida siga el esquema proporcionado.

Por ejemplo, podemos definir:

{
  "type": "object",
  "properties": {
    "fecha_vencimiento": {
      "type": "string"
    },
    "riesgo": {
      "type": "string",
      "enum": ["bajo", "medio", "alto"]
    },
    "monto": {
      "type": "number"
    }
  },
  "required": [
    "fecha_vencimiento",
    "riesgo",
    "monto"
  ],
  "additionalProperties": false
}

Entonces el LLM debe producir algo como:

{
  "fecha_vencimiento": "2027-12-15",
  "riesgo": "medio",
  "monto": 25000
}

Esto es especialmente importante en un CLM porque los contratos contienen información que posteriormente debe ser utilizada por otros componentes del sistema.

Por ejemplo:

Contrato PDF
     ↓
LLM
     ↓
Structured Output
     ↓
JSON
     ↓
Base de datos
¿Para qué utilizaríamos Structured Output en el CLM?

Podríamos utilizarlo para extraer automáticamente:

- Número de contrato
- Partes involucradas
- Fecha de inicio
- Fecha de finalización
- Fecha de renovación
- Monto
- Moneda
- Tipo de contrato
- Obligaciones
- Penalizaciones
- Cláusulas de terminación
- Nivel de riesgo
- Jurisdicción

Por ejemplo:

{
  "contract_id": "CTR-2026-00452",
  "contract_type": "Proveedor",
  "parties": [
    "Empresa A",
    "Empresa B"
  ],
  "start_date": "2026-10-01",
  "end_date": "2027-10-01",
  "renewal": true,
  "currency": "USD",
  "amount": 50000,
  "risk_level": "medio"
}

El sistema puede tomar directamente esos datos y almacenarlos.

Ventaja

La ventaja fundamental es:

El LLM deja de ser únicamente un generador de texto y pasa a producir datos que el software puede consumir.

Esto permite conectar el LLM con:

LLM
 ↓
JSON estructurado
 ↓
Backend
 ↓
Base de datos
 ↓
Workflow
 ↓
Notificaciones
2. RAG — Retrieval-Augmented Generation
2.1 ¿Qué problema resuelve?

Un LLM tiene conocimiento general, pero un CLM necesita responder sobre información privada y específica de la empresa.

Por ejemplo:

Usuario:
¿Cuándo vence el contrato con Empresa XYZ?

El modelo por sí solo no debería inventar la respuesta.

El contrato podría estar almacenado en:

/contracts/empresa_xyz/contrato_2026.pdf

El LLM necesita recuperar ese documento antes de responder.

Ahí aparece RAG.

RAG significa:

Retrieval-Augmented Generation

o generación aumentada mediante recuperación.

La investigación original de Lewis et al. plantea precisamente combinar la memoria paramétrica del modelo con una memoria externa no paramétrica para tareas que requieren conocimiento específico.

3. ¿Cómo funciona RAG?

El proceso general es:

DOCUMENTOS
    ↓
Dividir en fragmentos
    ↓
Embeddings
    ↓
FAISS
    ↓
Índice vectorial

Cuando llega una pregunta:

"¿Cuándo vence el contrato de Empresa XYZ?"

se hace:

Pregunta
   ↓
Embedding
   ↓
FAISS
   ↓
Buscar fragmentos similares
   ↓
Fragmentos relevantes
   ↓
LLM
   ↓
Respuesta

La diferencia fundamental es que el LLM no tiene que "recordar" el contrato.

Lo consulta.

4. ¿Qué son los embeddings?

Un embedding transforma texto en una representación numérica.

Por ejemplo, conceptualmente:

"El contrato vence el 15 de diciembre de 2027"

se transforma en algo parecido a:

[0.13, -0.42, 0.87, 0.21, ...]

No significa que cada número tenga un significado humano directo.

Lo importante es que textos semánticamente similares producen vectores cercanos.

Por ejemplo:

"¿Cuándo termina el contrato?"

y

"La vigencia del acuerdo finaliza el 15 de diciembre de 2027."

pueden estar cerca en el espacio vectorial aunque no utilicen exactamente las mismas palabras.

5. ¿Qué es FAISS?

FAISS es una biblioteca desarrollada para realizar búsquedas eficientes por similitud entre vectores.

Su documentación oficial indica que permite realizar similarity search y clustering sobre vectores densos, incluyendo búsquedas de vecinos cercanos. También permite realizar búsquedas por lotes.

En nuestro sistema podríamos tener:

Contrato 1
   ↓
100 fragmentos
   ↓
100 embeddings

Contrato 2
   ↓
80 fragmentos
   ↓
80 embeddings

Contrato 3
   ↓
120 fragmentos
   ↓
120 embeddings

FAISS crea un índice:

FAISS INDEX
│
├── vector 1 → contrato1_chunk1
├── vector 2 → contrato1_chunk2
├── vector 3 → contrato1_chunk3
├── vector 4 → contrato2_chunk1
├── ...
└── vector 300 → contrato3_chunk120

Cuando preguntamos:

¿Qué penalización existe por terminar anticipadamente?

la pregunta también se convierte en vector.

FAISS busca los vectores más cercanos.

Por ejemplo:

Pregunta
   ↓
Vector Q
   ↓
FAISS
   ↓
Top 5 resultados

Y podría devolver:

Contrato 102 - página 8
Contrato 102 - página 9
Contrato 102 - página 15
Contrato 102 - página 16
Contrato 102 - página 22

Esos fragmentos se entregan al LLM.

6. Arquitectura RAG para el CLM

Para el CLM propondría separar el proceso de indexación del proceso de consulta.

Indexación

Cuando se carga un contrato:

                  CONTRATO PDF
                       │
                       ▼
                Extracción de texto
                       │
                       ▼
                 Chunking
                       │
                       ▼
                  Embeddings
                       │
                       ▼
                     FAISS
                       │
                       ▼
              Índice vectorial

Al mismo tiempo podemos guardar metadata:

{
  "contract_id": "CTR-001",
  "page": 12,
  "chunk_id": "CTR-001-012",
  "document_type": "contract",
  "version": 3
}

Esto es importante.

FAISS encuentra el vector, pero nuestro sistema necesita saber a qué contrato y página pertenece.

7. Procesamiento paralelo con OpenAI — Worker Pool

Este método es diferente de RAG.

RAG responde a:

¿Cómo recupero información relevante?

El procesamiento paralelo responde a:

¿Cómo proceso muchas tareas de IA de manera eficiente?

Imaginemos que una empresa carga:

500 contratos

Y queremos analizar cada uno.

Podríamos hacer:

Contrato 1 → OpenAI
esperar
Contrato 2 → OpenAI
esperar
Contrato 3 → OpenAI
esperar
...

Eso sería secuencial.

Es sencillo, pero puede ser lento.

8. Worker Pool

Un Worker Pool consiste en tener varios trabajadores procesando tareas simultáneamente.

Conceptualmente:

                    COLA DE TRABAJOS
                          │
          ┌───────────────┼───────────────┐
          ↓               ↓               ↓
      Worker 1        Worker 2        Worker 3
          ↓               ↓               ↓
       OpenAI           OpenAI           OpenAI
          ↓               ↓               ↓
      Resultado        Resultado        Resultado

Por ejemplo:

100 contratos
       ↓
     Queue
       ↓
┌──────┬──────┬──────┬──────┬──────┐
│ W1   │ W2   │ W3   │ W4   │ W5   │
└──────┴──────┴──────┴──────┴──────┘

Cada worker procesa contratos independientemente.

Pero hay un detalle muy importante:

No significa crear cientos de solicitudes simultáneas sin control.

La propia documentación/cookbook de OpenAI muestra un procesador paralelo que utiliza concurrencia, pero también controla solicitudes y tokens por minuto, aplica reintentos y registra errores.

Por ejemplo:

1000 tareas
      ↓
Queue
      ↓
10 workers
      ↓
OpenAI

Si un worker recibe un error de rate limit:

Worker
  ↓
429
  ↓
esperar
  ↓
retry

Esto permite aumentar el throughput sin simplemente saturar la API.

9. ¿Dónde utilizaríamos Worker Pool en el CLM?

Aquí tiene bastante sentido.

Supongamos que se suben:

100 contratos

El sistema necesita:

Extraer texto.
Identificar información.
Detectar fechas.
Identificar obligaciones.
Analizar riesgos.
Crear embeddings.
Indexar documentos.

No necesariamente tenemos que esperar a terminar completamente un contrato antes de empezar el siguiente.

Podemos hacer:

                 100 CONTRATOS
                       │
                       ▼
                    QUEUE
                       │
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
    Worker 1        Worker 2        Worker 3
       ↓               ↓               ↓
    OpenAI           OpenAI           OpenAI
       ↓               ↓               ↓
    análisis         análisis         análisis
       │               │               │
       └───────────────┼───────────────┘
                       ↓
                  Base de datos
                       +
                     FAISS
10. Los tres métodos no son independientes

Esta es la parte más importante del diseño.

No deberíamos implementar:

Structured Output
RAG
Worker Pool

como tres funcionalidades aisladas.

Lo interesante es combinarlas.

La arquitectura sería:

              ┌─────────────────────┐
              │       USUARIO       │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │      CHATBOT        │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   AI ORCHESTRATOR   │
              └───────┬─────┬───────┘
                      │     │
             ┌────────┘     └─────────┐
             ▼                        ▼
           RAG                 Structured Output
             │                        │
             ▼                        ▼
           FAISS                    JSON
             │                        │
             └──────────┬─────────────┘
                        ▼
                     LLM
                        │
                        ▼
                   Respuesta

Y el Worker Pool estaría principalmente en procesos masivos:

                    DOCUMENTOS
                        │
                        ▼
                      QUEUE
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
      Worker          Worker          Worker
        │               │               │
        └───────────────┼───────────────┘
                        ▼
                 OpenAI Processing
                        │
                        ▼
             Structured Output
                        │
                        ▼
                  Base de datos
                        +
                      FAISS
11. ¿Qué es un CLM?

CLM significa Contract Lifecycle Management.

Es un sistema que administra el ciclo completo de un contrato.

Un ciclo típico incluye:

Solicitud
   ↓
Creación
   ↓
Redacción
   ↓
Negociación
   ↓
Revisión
   ↓
Aprobación
   ↓
Firma
   ↓
Ejecución
   ↓
Monitoreo
   ↓
Renovación / Terminación

IBM describe el CLM como un proceso de extremo a extremo que cubre desde la creación y aprobación hasta el cumplimiento y la renovación o terminación. También señala funcionalidades como repositorio centralizado, control de versiones, workflows de aprobación, alertas de renovación y monitoreo de riesgos.

12. Arquitectura propuesta del CLM

Propongo una arquitectura basada en capas.

┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                            │
│                                                             │
│  Dashboard │ Contratos │ Documentos │ Aprobaciones │ Chat │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                         API / BACKEND                       │
│                                                             │
│ Auth │ Contracts │ Users │ Workflow │ Documents │ Chat API │
└───────────────┬──────────────────────┬──────────────────────┘
                │                      │
                │                      ▼
                │             ┌────────────────────┐
                │             │   AI ORCHESTRATOR  │
                │             └─────────┬──────────┘
                │                       │
                │          ┌────────────┼────────────┐
                │          ▼            ▼            ▼
                │       RAG Service   LLM Service   Worker Pool
                │          │            │            │
                │          ▼            ▼            ▼
                │        FAISS       OpenAI       OpenAI
                │                       │
                │                       ▼
                │                Structured Output
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│                         DATA LAYER                           │
│                                                             │
│ PostgreSQL │ Object Storage │ FAISS │ Audit Logs            │
└─────────────────────────────────────────────────────────────┘
13. Componentes del sistema
13.1 Frontend

Podría desarrollarse, por ejemplo, con:

React

Tendría módulos:

Dashboard
Contratos
Documentos
Negociaciones
Aprobaciones
Firmas
Obligaciones
Renovaciones
Reportes
Chatbot

El usuario podría abrir un contrato y tener el chatbot al lado.

Por ejemplo:

┌─────────────────────────────────────────────┐
│ Contrato #CTR-2026-00452                    │
├──────────────────────────┬──────────────────┤
│                          │                  │
│     DOCUMENTO PDF       │     CHATBOT      │
│                          │                  │
│  CLÁUSULA 1              │ ¿Qué obligaciones│
│  ...                     │ tiene el cliente?│
│                          │                  │
│  CLÁUSULA 2              │ El contrato      │
│  ...                     │ establece...     │
│                          │                  │
└──────────────────────────┴──────────────────┘
14. Backend

El backend sería responsable de:

Usuarios
Contratos
Documentos
Permisos
Workflows
Aprobaciones
Notificaciones
Chatbot
Integración con IA

Podría utilizar:

Java + Spring Boot

o:

Python + FastAPI

Para un proyecto académico, ambas son válidas.

Si se quiere mantener una arquitectura alineada con lo que ya has trabajado en Spring Boot, usaría:

React
   ↓
Spring Boot
   ↓
PostgreSQL

y un servicio de IA independiente:

Spring Boot
     ↓
AI Service
     ↓
OpenAI
15. Base de datos

Una posible estructura sería:

USERS
-----
id
name
email
role

CONTRACTS
---------
id
title
contract_type
status
start_date
end_date
created_by
risk_level

CONTRACT_PARTIES
----------------
id
contract_id
party_id
role

DOCUMENTS
---------
id
contract_id
file_name
version
storage_path
uploaded_at

CLAUSES
-------
id
contract_id
type
content

OBLIGATIONS
-----------
id
contract_id
description
due_date
responsible_user
status

APPROVALS
---------
id
contract_id
approver_id
status
approved_at

AUDIT_LOG
---------
id
user_id
action
contract_id
timestamp

Y además tendríamos un almacenamiento de documentos:

Object Storage
      │
      ├── contracts/
      ├── amendments/
      ├── attachments/
      └── templates/
16. ¿Dónde entra FAISS?

FAISS no debería reemplazar la base de datos tradicional.

Tendríamos:

PostgreSQL
    ↓
Datos estructurados

y:

FAISS
    ↓
Información vectorizada

Por ejemplo:

PostgreSQL

Contrato:
CTR-001
Empresa:
ABC
Fecha:
2027-12-15
Estado:
Activo

Mientras FAISS tendría:

Vector
 ↓
Chunk del contrato
 ↓
Metadata
 ↓
CTR-001 / página 8

Cada tecnología hace algo diferente.

17. Pipeline de carga de contrato

Supongamos que el usuario sube:

contrato_abc.pdf

El flujo sería:

Usuario
  │
  ▼
Frontend
  │
  ▼
Backend
  │
  ▼
Object Storage
  │
  ▼
Document Processing Queue
  │
  ▼
Worker Pool

Aquí empiezan los workers.

18. Worker 1 — extracción
PDF
 ↓
Extracción de texto
 ↓
Texto limpio

Resultado:

Contrato de prestación de servicios...

CLÁUSULA PRIMERA...
CLÁUSULA SEGUNDA...
...
19. Worker 2 — extracción estructurada

Se manda el texto al LLM.

Se define un esquema:

{
  "contract_type": "string",
  "start_date": "string",
  "end_date": "string",
  "amount": "number",
  "currency": "string",
  "renewable": "boolean",
  "risk_level": "string"
}

El LLM devuelve:

{
  "contract_type": "Servicios",
  "start_date": "2026-10-01",
  "end_date": "2027-10-01",
  "amount": 35000,
  "currency": "USD",
  "renewable": true,
  "risk_level": "medio"
}

El backend puede guardar directamente esa información.

Aquí estamos utilizando:

Structured Output.

20. Worker 3 — generación de embeddings

El contrato se divide en chunks:

Chunk 1
Chunk 2
Chunk 3
Chunk 4
...
Chunk 50

Cada chunk pasa por el modelo de embeddings:

Chunk 1 → vector
Chunk 2 → vector
Chunk 3 → vector
...

Luego:

vectors
   ↓
FAISS
21. Worker 4 — análisis de riesgo

Otro worker podría analizar:

- Penalizaciones
- Terminación anticipada
- Renovación automática
- Obligaciones
- Cláusulas fuera del estándar

Y devolver:

{
  "risk_level": "alto",
  "risks": [
    {
      "type": "termination",
      "severity": "high",
      "description": "Penalización elevada por terminación anticipada"
    },
    {
      "type": "renewal",
      "severity": "medium",
      "description": "Renovación automática"
    }
  ]
}

Otra vez:

Structured Output.

22. Chatbot inteligente

Ahora llegamos a la parte principal.

El usuario pregunta:

¿Qué penalización tengo si termino este contrato antes de tiempo?

El chatbot no debería simplemente preguntarle al LLM.

Debe hacer:

Usuario
   │
   ▼
Chatbot API
   │
   ▼
AI Orchestrator
   │
   ▼
¿Necesita información del contrato?
   │
   ▼
RAG
   │
   ▼
Embedding de pregunta
   │
   ▼
FAISS
   │
   ▼
Top-K chunks
   │
   ▼
LLM
   │
   ▼
Respuesta
23. Ejemplo real del RAG

Pregunta:

¿Qué penalización existe por terminar anticipadamente?

FAISS puede devolver:

Chunk 37:
"En caso de terminación anticipada..."

Chunk 38:
"El contratante deberá pagar..."

Chunk 39:
"La penalización será equivalente al..."

El sistema construye el contexto:

CONTEXTO RECUPERADO:

[Contrato CTR-001]
[Página 8]
En caso de terminación anticipada...

[Contrato CTR-001]
[Página 8]
El contratante deberá pagar...

[Contrato CTR-001]
[Página 9]
La penalización será equivalente...

Entonces:

LLM

Pregunta:
¿Qué penalización existe?

Contexto:
[fragmentos recuperados]

Genera una respuesta basada exclusivamente
en el contexto proporcionado.

El LLM responde.

24. Structured Output también puede utilizarse en el chatbot

El chatbot no necesariamente debería devolver solamente:

La penalización es del 20%.

Podemos definir:

{
  "answer": "La penalización corresponde al 20%...",
  "confidence": "high",
  "sources": [
    {
      "contract_id": "CTR-001",
      "page": 8
    }
  ],
  "requires_human_review": false
}

Entonces el frontend puede mostrar:

Respuesta

La penalización corresponde al 20%...

Fuente:
Contrato CTR-001
Página 8

Confianza:
Alta

Eso es muchísimo más útil para un CLM.

25. Preguntas que podría responder el chatbot

Por ejemplo:

Fechas
¿Cuándo vence este contrato?
Obligaciones
¿Qué obligaciones tiene el proveedor?
Riesgos
¿Qué cláusulas considero riesgosas?
Penalizaciones
¿Cuánto tendría que pagar si termino el contrato?
Renovación
¿Este contrato se renueva automáticamente?
Comparación
¿Qué cambió entre la versión 2 y la versión 3?
Cumplimiento
¿Qué obligaciones están próximas a vencer?
Búsqueda global
Muéstrame contratos que tengan renovación automática.

En este último caso podríamos combinar:

Base de datos
+
RAG
+
LLM
26. AI Orchestrator

Yo incluiría explícitamente un componente:

AI Orchestrator

Su función sería decidir qué proceso ejecutar.

Por ejemplo:

Usuario:
¿Cuándo vence mi contrato?

El orchestrator detecta:

Tipo:
Consulta contractual

Necesita:
RAG

Entonces:

AI Orchestrator
      ↓
RAG Service
      ↓
FAISS
      ↓
LLM

Pero si llega:

Analiza este contrato y extrae toda su información.

podría hacer:

AI Orchestrator
      ↓
Worker Pool
      ↓
Structured Output
      ↓
Database
27. Arquitectura completa

La arquitectura final quedaría aproximadamente así:

                         ┌───────────────────┐
                         │      USUARIO      │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │     REACT UI      │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   SPRING BOOT     │
                         │      API          │
                         └─────────┬─────────┘
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
      ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
      │  Contract   │       │   Workflow  │       │    Chat     │
      │   Service   │       │   Service   │       │    API      │
      └──────┬──────┘       └─────────────┘       └──────┬──────┘
             │                                            │
             │                                            ▼
             │                                  ┌─────────────────┐
             │                                  │ AI ORCHESTRATOR │
             │                                  └────────┬────────┘
             │                                           │
             │                         ┌─────────────────┼────────────────┐
             │                         │                 │                │
             │                         ▼                 ▼                ▼
             │                   ┌──────────┐     ┌──────────┐    ┌────────────┐
             │                   │   RAG    │     │   LLM    │    │   WORKER   │
             │                   │ SERVICE  │     │ SERVICE  │    │    POOL    │
             │                   └────┬─────┘     └────┬─────┘    └─────┬──────┘
             │                        │                │                │
             │                        ▼                │                ▼
             │                     ┌──────┐           │             OpenAI
             │                     │FAISS │           │
             │                     └──┬───┘           │
             │                        │                │
             │                        └────────┬───────┘
             │                                 │
             │                                 ▼
             │                         Structured Output
             │                                 │
             │                                 ▼
             │                               JSON
             │
             ▼
      ┌─────────────────┐
      │   PostgreSQL    │
      └─────────────────┘

             │
             ▼
      ┌─────────────────┐
      │  Object Storage │
      │ PDF / DOCX etc. │
      └─────────────────┘
28. Flujo completo de un contrato

Ahora podemos unir absolutamente todo.

Supongamos que el usuario carga:

Contrato_Proveedor_XYZ.pdf
Paso 1 — Upload
React
 ↓
Spring Boot
 ↓
Object Storage
Paso 2 — Crear tarea

El backend genera:

Task:
PROCESS_CONTRACT

y la coloca en:

Queue
Paso 3 — Worker Pool

Los workers comienzan a procesar.

                QUEUE
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
    Worker 1   Worker 2   Worker 3
Paso 4 — Extracción

Worker 1:

PDF
 ↓
Texto
Paso 5 — Structured Output

Worker 2:

Texto
 ↓
OpenAI
 ↓
Structured Output
 ↓
JSON

Resultado:

{
  "start_date": "2026-10-01",
  "end_date": "2027-10-01",
  "amount": 50000,
  "currency": "USD",
  "renewal": true,
  "risk_level": "medium"
}

Se guarda en PostgreSQL.

Paso 6 — Embeddings

Worker 3:

Texto
 ↓
Chunks
 ↓
Embeddings
 ↓
FAISS

Ahora el contrato puede ser consultado semánticamente.

29. Consulta del usuario

El usuario pregunta:

¿Este contrato se renueva automáticamente?

El sistema:

Pregunta
 ↓
Embedding
 ↓
FAISS
 ↓
Encontrar chunks relevantes
 ↓
Contexto
 ↓
OpenAI
 ↓
Respuesta

El chatbot podría responder:

Sí. El contrato establece una renovación automática
por períodos de 12 meses, salvo que alguna de las
partes comunique su intención de no renovarlo con
30 días de anticipación.

Fuente:
Contrato CTR-2026-00452
Página 12
30. ¿Dónde aparece cada método?

Esto debería quedar muy claro en la arquitectura:

Método	Uso dentro del CLM
Structured Output	Extraer información estructurada de contratos
RAG	Responder preguntas utilizando contratos reales
FAISS	Buscar semánticamente fragmentos relevantes
Worker Pool	Procesar muchos contratos/tareas simultáneamente
LLM	Analizar, interpretar y generar respuestas
PostgreSQL	Guardar información estructurada
Object Storage	Guardar documentos originales

La combinación sería:

                 ┌───────────────┐
                 │     LLM       │
                 └───────┬───────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
   Structured       RAG + FAISS    Worker Pool
    Output              │              │
          │             │              │
          ▼             ▼              ▼
      JSON          Contexto       Procesamiento
          │             │              │
          └─────────────┼──────────────┘
                        ▼
                    CLM INTELIGENTE
31. ¿Por qué esta arquitectura tiene sentido?

Porque cada tecnología resuelve un problema diferente.

Structured Output

Evita que el backend tenga que interpretar texto libre.

LLM → JSON
RAG + FAISS

Evita depender únicamente del conocimiento interno del LLM.

Pregunta
 ↓
Documentos reales
 ↓
Respuesta
Worker Pool

Evita procesar grandes cantidades de contratos uno por uno.

100 contratos
 ↓
Workers
 ↓
procesamiento concurrente
32. Una característica especialmente importante: trazabilidad

En un CLM no recomendaría que el chatbot responda únicamente:

La penalización es del 15%.

Debería responder:

La penalización es del 15%.

Fuente:
Contrato CTR-2026-00452
Página 18
Cláusula 7.2

Esto es importante porque el usuario debe poder verificar la respuesta contra el documento original.

El enfoque RAG también ayuda a proporcionar procedencia de la información recuperada; la investigación original sobre RAG señala precisamente la importancia de disponer de conocimiento externo y de poder actualizarlo.

33. Control de acceso

Hay otro punto crítico.

Imaginemos:

Contrato A → Empresa A
Contrato B → Empresa B

Un usuario de Empresa A no debería preguntarle al chatbot:

Muéstrame el contrato de Empresa B.

y obtener información privada.

Por eso el RAG debe incorporar metadata y filtros de autorización.

Por ejemplo:

{
  "contract_id": "CTR-001",
  "company_id": "COMP-01",
  "department_id": "LEGAL",
  "classification": "CONFIDENTIAL"
}

Cuando el usuario pregunta:

¿Cuándo vence mi contrato?

el sistema primero determina qué contratos puede consultar.

Entonces:

Usuario
 ↓
Authentication
 ↓
Authorization
 ↓
Contratos permitidos
 ↓
RAG
 ↓
FAISS

No debería ser:

Usuario
 ↓
FAISS global

porque eso podría filtrar información de otros contratos.

34. Worker Pool y seguridad

También hay que controlar qué documentos procesa cada worker.

Por ejemplo:

Queue
│
├── Contract A → Company A
├── Contract B → Company B
├── Contract C → Company C

Cada tarea debería tener metadata:

{
  "task_id": "TASK-001",
  "contract_id": "CTR-001",
  "company_id": "COMP-01",
  "operation": "ANALYZE_CONTRACT"
}

Así el resultado puede relacionarse correctamente con el contrato.

35. Arquitectura de producción

Si el sistema evolucionara de proyecto académico a sistema real, agregaría:

                   Load Balancer
                         │
                         ▼
                  API Gateway
                         │
                ┌────────┴────────┐
                ▼                 ▼
           Backend 1          Backend 2
                │                 │
                └────────┬────────┘
                         ▼
                       Queue
                         │
             ┌───────────┼───────────┐
             ▼           ▼           ▼
          Worker 1    Worker 2    Worker 3
             │           │           │
             └───────────┼───────────┘
                         ▼
                       OpenAI

Para trabajos masivos, la cola permite desacoplar el backend del procesamiento de IA.

36. Manejo de errores

El Worker Pool debe contemplar errores.

Por ejemplo:

Worker 1
   ↓
OpenAI
   ↓
Rate limit
   ↓
Retry

Si sigue fallando:

Retry 1
Retry 2
Retry 3
   ↓
Failed

La implementación de procesamiento paralelo publicada en el OpenAI Cookbook contempla precisamente concurrencia, control de solicitudes/tokens, reintentos y seguimiento de errores.

37. Ejemplo de Worker Pool conceptual

No es todavía una implementación completa, pero la lógica sería:

queue = [
    contrato1,
    contrato2,
    contrato3,
    contrato4
]

workers = 4

while queue:

    task = queue.pop()

    worker = get_available_worker()

    worker.process(task)

En una implementación real utilizaríamos concurrencia asíncrona, una cola y límites de concurrencia.

Por ejemplo:

Queue
 ↓
Semaphore(5)
 ↓
máximo 5 solicitudes simultáneas

Así no hacemos:

1000 requests → OpenAI

al mismo tiempo.

38. Ejemplo de Structured Output conceptual

Podríamos tener una clase:

class ContractData:
    contract_type: str
    start_date: str
    end_date: str
    amount: float
    currency: str
    renewal: bool
    risk_level: str

El objetivo es que el resultado del LLM pueda convertirse en:

{
    "contract_type": "Proveedor",
    "start_date": "2026-10-01",
    "end_date": "2027-10-01",
    "amount": 50000,
    "currency": "USD",
    "renewal": true,
    "risk_level": "medium"
}

Esto permite que posteriormente el backend haga:

contract.end_date = result["end_date"]
contract.amount = result["amount"]

en lugar de tener que interpretar:

"El contrato tiene un valor aproximado de cincuenta mil
dólares y finaliza el primero de octubre..."
39. Ejemplo conceptual de RAG
question = "¿Cuál es la penalización por terminar el contrato?"

question_embedding = embed(question)

results = faiss.search(
    question_embedding,
    k=5
)

context = get_chunks(results)

answer = llm(
    question=question,
    context=context
)

La lógica esencial es:

Pregunta
 ↓
Embedding
 ↓
FAISS
 ↓
Top K
 ↓
Contexto
 ↓
LLM
 ↓
Respuesta
40. Un chatbot más avanzado

El chatbot podría tener diferentes tipos de consultas:

                    CHATBOT
                       │
                       ▼
                AI ORCHESTRATOR
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
   CONSULTA         ACCIÓN          ANÁLISIS
       │               │                │
       ▼               ▼                ▼
      RAG          Backend API       Worker Pool
       │               │                │
       ▼               ▼                ▼
    FAISS          Contratos         OpenAI
       │
       ▼
      LLM

Por ejemplo:

Consulta
¿Cuándo vence el contrato 123?

→ RAG.

Acción
Crea una solicitud de renovación.

→ Backend/Workflow.

Análisis
Analiza todos mis contratos y dime cuáles
tienen alto riesgo.

→ Worker Pool + Structured Output.

Esta separación es mucho más potente que hacer que absolutamente todo pase por una sola llamada al LLM.

41. Flujo para analizar 1 contrato
                 PDF
                  │
                  ▼
          Extracción de texto
                  │
                  ▼
                Chunks
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
     Embeddings       LLM Analysis
          │                │
          ▼                ▼
        FAISS       Structured Output
                           │
                           ▼
                       PostgreSQL
42. Flujo para analizar 1000 contratos
                1000 CONTRATOS
                       │
                       ▼
                     QUEUE
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ▼               ▼               ▼
    Worker 1        Worker 2        Worker N
       │               │               │
       ▼               ▼               ▼
    OpenAI           OpenAI           OpenAI
       │               │               │
       ▼               ▼               ▼
 Structured        Structured       Structured
 Output            Output           Output
       │               │               │
       └───────────────┼───────────────┘
                       ▼
                  PostgreSQL
                       +
                     FAISS

Este es el escenario donde Worker Pool aporta más valor.

43. Ciclo completo del CLM con IA

Finalmente, el CLM podría quedar así:

                    SOLICITUD
                        │
                        ▼
                   CREACIÓN
                        │
                        ▼
                  REDACCIÓN
                        │
                        ▼
              ┌─────────────────┐
              │   AI ASSISTANT  │
              └────────┬────────┘
                       │
                       ▼
                  NEGOCIACIÓN
                       │
                       ▼
                   REVISIÓN
                       │
                       ▼
                  APROBACIÓN
                       │
                       ▼
                     FIRMA
                       │
                       ▼
                 CONTRATO ACTIVO
                       │
              ┌────────┴─────────┐
              │                  │
              ▼                  ▼
          MONITOREO           CHATBOT
              │                  │
              │                  ▼
              │             RAG + FAISS
              │                  │
              │                  ▼
              │                 LLM
              │                  │
              ▼                  ▼
        OBLIGACIONES          RESPUESTAS
        VENCIMIENTOS
        RIESGOS
              │
              ▼
          RENOVACIÓN
              │
              ▼
        TERMINACIÓN

Este modelo coincide con las funciones que normalmente se esperan de un CLM moderno: repositorio centralizado, creación y negociación, workflows de aprobación, firma, monitoreo, alertas de renovación y análisis.

44. Respuesta final que podrías dar si te preguntan cómo se integran los tres métodos

La idea central de la arquitectura es esta:

                 CONTRATOS
                     │
                     ▼
                WORKER POOL
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
    Extracción    Análisis     Embeddings
        │            │            │
        │            ▼            ▼
        │      STRUCTURED       FAISS
        │        OUTPUT           │
        │            │            │
        └────────────┼────────────┘
                     ▼
                 DATABASE
                     │
                     ▼
                  CHATBOT
                     │
                     ▼
               AI ORCHESTRATOR
                     │
                     ▼
                RAG + FAISS
                     │
                     ▼
                    LLM
                     │
                     ▼
             STRUCTURED OUTPUT
                     │
                     ▼
                  RESPUESTA

Por tanto:

Structured Output se utiliza para convertir las capacidades del LLM en datos estructurados que el sistema pueda procesar.

RAG con FAISS se utiliza para que el chatbot pueda consultar el contenido real de los contratos y responder basándose en información recuperada, en lugar de depender únicamente del conocimiento del modelo.

Worker Pool se utiliza para procesar múltiples contratos y tareas de IA de manera concurrente y controlada, respetando los límites de la API mediante throttling y reintentos.

La combinación de los tres permite construir un CLM en el que la IA no sea simplemente un chatbot que "conversa", sino una capa inteligente integrada con los documentos, la base de datos y los procesos del ciclo de vida contractual.

Fuentes principales
OpenAI API — Structured Outputs — documentación sobre JSON Schema, Structured Outputs y validación estricta.
OpenAI Cookbook — ejemplos y guías — colección oficial de ejemplos de integración con OpenAI.
OpenAI Cookbook — procesamiento paralelo de solicitudes — implementación de procesamiento concurrente con control de rate limits, tokens y reintentos.
FAISS Documentation — documentación oficial de búsqueda por similitud de vectores.
Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks — trabajo académico fundacional sobre RAG.
IBM — Contract Lifecycle Management — etapas y funcionalidades de un CLM moderno.
IBM — Contract Management Lifecycle — creación, negociación, ejecución, monitoreo y renovación/terminación.