1. Clean Architecture

La Clean Architecture fue propuesta por Robert C. Martin como una forma de organizar sistemas alrededor de sus reglas de negocio, manteniendo esas reglas independientes de frameworks, bases de datos, interfaces y otros detalles externos.

Martin señala que diferentes enfoques como Hexagonal Architecture, Onion Architecture, BCE y Clean Architecture persiguen esencialmente el mismo objetivo: separar las responsabilidades y mantener las reglas de negocio independientes de las interfaces y tecnologías externas.

La idea fundamental puede resumirse así:

                 ┌───────────────────────┐
                 │      Frameworks       │
                 │      Database         │
                 │       Web/UI          │
                 ├───────────────────────┤
                 │   Interface Adapters  │
                 ├───────────────────────┤
                 │      Use Cases        │
                 ├───────────────────────┤
                 │       Entities        │
                 └───────────────────────┘

Pero lo importante no son los círculos.

Lo importante es la:

Dependency Rule

Las dependencias del código deben apuntar hacia adentro. El núcleo de negocio no debe conocer los detalles externos.

Por ejemplo, esto sería malo:

public class ClienteService {

    private MySQLConnection database;

    public ClienteService() {
        database = new MySQLConnection();
    }
}

Porque ClienteService, que contiene lógica de aplicación, conoce directamente:

MySQL

Si mañana cambiamos:

MySQL
   ↓
PostgreSQL

la lógica tiene que modificarse.

2. ¿Qué busca Clean Architecture?

Busca que podamos cambiar cosas externas sin destruir el núcleo del sistema.

Por ejemplo:

                 CAMBIAR
                   ↓
        ┌────────────────────┐
        │      Frontend      │
        └────────────────────┘

        ┌────────────────────┐
        │     PostgreSQL     │
        └────────────────────┘

        ┌────────────────────┐
        │       AWS          │
        └────────────────────┘

        ┌────────────────────┐
        │      OpenAI        │
        └────────────────────┘

                 ↓

          SIN MODIFICAR

        ┌────────────────────┐
        │   REGLAS DEL       │
        │     NEGOCIO        │
        └────────────────────┘

Ese es uno de los objetivos principales.

3. Las cuatro zonas de Clean Architecture

Una forma común de visualizarla es:

┌──────────────────────────────────────────────┐
│              FRAMEWORKS / DRIVERS             │
│                                              │
│  Spring │ PostgreSQL │ REST │ AWS │ React   │
│                                              │
│   ┌──────────────────────────────────────┐   │
│   │       INTERFACE ADAPTERS             │   │
│   │                                      │   │
│   │ Controllers │ Repositories │ DTOs   │   │
│   │                                      │   │
│   │   ┌──────────────────────────────┐   │   │
│   │   │          USE CASES           │   │   │
│   │   │                              │   │   │
│   │   │ CrearCliente                 │   │   │
│   │   │ CrearOportunidad             │   │   │
│   │   │ RegistrarVenta               │   │   │
│   │   │                              │   │   │
│   │   │   ┌──────────────────────┐   │   │   │
│   │   │   │      ENTITIES       │   │   │   │
│   │   │   │                      │   │   │   │
│   │   │   │ Cliente              │   │   │   │
│   │   │   │ Empresa              │   │   │   │
│   │   │   │ Oportunidad          │   │   │   │
│   │   │   └──────────────────────┘   │   │   │
│   │   └──────────────────────────────┘   │   │
│   └──────────────────────────────────────┘   │
└──────────────────────────────────────────────┘
4. Entities

Las Entities representan las reglas de negocio más importantes.

Para una CRM B2B podríamos tener:

Empresa
Contacto
Oportunidad
Actividad
Usuario
Producto
Cotización
Venta

Por ejemplo:

public class Empresa {

    private String id;
    private String nombre;
    private String ruc;
    private EstadoEmpresa estado;

}

Pero una Entity no debería ser simplemente una clase con getters y setters.

Puede contener reglas propias del negocio.

Por ejemplo:

public class Oportunidad {

    private double monto;
    private EstadoOportunidad estado;

    public void cerrarGanada() {

        if (estado != EstadoOportunidad.EN_NEGOCIACION) {
            throw new IllegalStateException(
                "La oportunidad no puede cerrarse"
            );
        }

        estado = EstadoOportunidad.GANADA;
    }
}

La regla:

Una oportunidad solo puede cerrarse
si está en negociación

es una regla de negocio.

Por eso pertenece al dominio.

5. Use Cases

Los casos de uso representan las acciones que el sistema permite realizar.

En una CRM B2B:

Crear empresa
Registrar contacto
Crear oportunidad
Asignar vendedor
Cambiar etapa
Crear actividad
Registrar llamada
Crear cotización
Cerrar oportunidad
Registrar venta

Podríamos tener:

public class CrearEmpresaUseCase {

    public Empresa ejecutar(CrearEmpresaRequest request) {

        // validar reglas
        // crear empresa
        // guardar empresa

    }
}

El Use Case no debería saber:

HTTP
SQL
React
PostgreSQL
Spring Controller

Su trabajo es ejecutar una acción del negocio.

6. Interface Adapters

Aquí convertimos información del mundo exterior al formato que necesita nuestra aplicación.

Ejemplo:

HTTP
 ↓
Controller
 ↓
Request DTO
 ↓
Use Case

El controller podría recibir:

{
    "nombre": "Empresa XYZ",
    "ruc": "0999999999001"
}

y convertirlo en:

CrearEmpresaRequest

El controller no debería contener toda la lógica de creación de empresas.

Su responsabilidad es adaptar:

HTTP → aplicación
7. Frameworks y Drivers

Aquí viven los detalles técnicos:

Spring Boot
PostgreSQL
JPA
AWS
Redis
Kafka
REST
React

Son detalles externos.

La aplicación debería poder cambiar:

PostgreSQL → MongoDB

sin tener que cambiar:

Reglas de negocio
8. ¿Qué tiene que ver esto con Arquitectura Hexagonal?

Muchísimo.

Alistair Cockburn propuso originalmente Hexagonal Architecture, también conocida como Ports and Adapters, con el objetivo de permitir que una aplicación funcione sin depender directamente de una interfaz de usuario o una base de datos, facilitando las pruebas y el reemplazo de tecnologías externas.

AWS también describe Hexagonal Architecture como un patrón para desacoplar la lógica de negocio de bases de datos, interfaces y APIs externas mediante puertos y adaptadores.

Por eso puedes pensar:

Clean Architecture
       +
Hexagonal Architecture
       ↓
Aplicación desacoplada

No son conceptos enemigos.

De hecho, comparten la idea fundamental:

      DEPENDENCIAS
           ↓
       HACIA EL
         CORE
9. Arquitectura Hexagonal

La arquitectura sería conceptualmente:

                   ┌───────────────┐
                   │    React      │
                   └───────┬───────┘
                           │
                      Adaptador
                           │
                           ▼
                    ┌─────────────┐
                    │   PUERTO    │
                    │   ENTRADA   │
                    └──────┬──────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │                         │
              │       APLICACIÓN        │
              │                         │
              │       DOMINIO           │
              │                         │
              │ Empresas                │
              │ Contactos               │
              │ Oportunidades           │
              │ Ventas                  │
              │                         │
              └────────────┬────────────┘
                           │
                    Puerto de salida
                           │
                           ▼
                    ┌─────────────┐
                    │  Adaptador  │
                    │ PostgreSQL  │
                    └─────────────┘

El hexágono no significa que necesariamente haya seis componentes.

Cockburn utiliza la forma para representar diferentes lados de interacción con el exterior. Lo importante son los puertos y adaptadores.

10. ¿Qué es un puerto?

Un puerto es una interfaz que define cómo la aplicación se comunica con el exterior.

Por ejemplo:

public interface EmpresaRepository {

    Empresa guardar(Empresa empresa);

    Optional<Empresa> buscarPorId(String id);

    List<Empresa> buscarTodas();
}

Esto es un puerto.

La aplicación dice:

"Necesito una forma de guardar y consultar empresas."

Pero no dice:

"Necesito PostgreSQL."

Eso es fundamental.

11. ¿Qué es un adaptador?

El adaptador implementa ese puerto utilizando una tecnología concreta.

Por ejemplo:

public class EmpresaRepositoryPostgres
        implements EmpresaRepository {

    @Override
    public Empresa guardar(Empresa empresa) {
        // guardar en PostgreSQL
    }

    @Override
    public Optional<Empresa> buscarPorId(String id) {
        // consultar PostgreSQL
    }

    @Override
    public List<Empresa> buscarTodas() {
        // SELECT ...
    }
}

Entonces:

Aplicación
     │
     │ EmpresaRepository
     ▼
PostgreSQL Adapter
     │
     ▼
PostgreSQL

La aplicación conoce:

EmpresaRepository

pero no necesita conocer:

PostgreSQL
12. Puertos de entrada y salida

Aquí hay una distinción que te conviene aprender.

Puertos de entrada

Permiten que algo externo le pida algo a nuestra aplicación.

Ejemplo:

public interface CrearEmpresaUseCase {

    EmpresaResponse ejecutar(
        CrearEmpresaRequest request
    );
}

El controller utiliza ese puerto.

React
  ↓
REST Controller
  ↓
CrearEmpresaUseCase
  ↓
Aplicación
Puertos de salida

Permiten que nuestra aplicación solicite algo al exterior.

Por ejemplo:

public interface EmpresaRepository {

    Empresa guardar(Empresa empresa);

}

La aplicación utiliza el puerto:

Use Case
   ↓
EmpresaRepository
   ↓
Adapter
   ↓
PostgreSQL

Esta separación es central en Ports & Adapters. Los adaptadores de entrada conducen la aplicación y los adaptadores de salida implementan los puertos que la aplicación necesita para interactuar con sistemas externos.

13. Ahora sí: CRM B2B

Vamos a diseñar una CRM B2B.

CRM significa:

Customer Relationship Management.

Pero B2B cambia bastante la estructura.

No estamos administrando únicamente:

Personas

sino:

Empresas
   ↓
Contactos
   ↓
Oportunidades
   ↓
Negociaciones
   ↓
Cotizaciones
   ↓
Ventas
14. Funcionalidades del CRM

Propongo estos módulos:

CRM B2B
│
├── Empresas
├── Contactos
├── Oportunidades
├── Actividades
├── Productos
├── Cotizaciones
├── Ventas
├── Usuarios
├── Tareas
└── Reportes
15. Flujo principal

El flujo comercial sería:

EMPRESA
   │
   ▼
CONTACTO
   │
   ▼
OPORTUNIDAD
   │
   ▼
CALIFICACIÓN
   │
   ▼
NEGOCIACIÓN
   │
   ▼
COTIZACIÓN
   │
   ▼
NEGOCIACIÓN
   │
   ▼
GANADA / PERDIDA
   │
   ▼
VENTA

Por ejemplo:

Empresa ABC
     ↓
Juan Pérez
     ↓
Compra de software
     ↓
$25.000
     ↓
Cotización
     ↓
Negociación
     ↓
Venta
16. Arquitectura general

La arquitectura propuesta sería:

                         CRM B2B
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
     REST API          Webhooks            Tests
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐       ┌──────────┐       ┌──────────┐
   │ Adapter │       │ Adapter  │       │ Adapter  │
   └────┬────┘       └────┬─────┘       └────┬─────┘
        │                 │                  │
        └─────────────────┼──────────────────┘
                          ▼
                ┌───────────────────┐
                │   INPUT PORTS     │
                └─────────┬─────────┘
                          │
                          ▼
        ┌───────────────────────────────────┐
        │                                   │
        │          APPLICATION              │
        │                                   │
        │  CrearEmpresa                     │
        │  CrearContacto                    │
        │  CrearOportunidad                 │
        │  CrearCotizacion                  │
        │  RegistrarVenta                   │
        │                                   │
        └────────────────┬──────────────────┘
                         │
                         ▼
                ┌───────────────────┐
                │      DOMAIN       │
                │                   │
                │ Empresa           │
                │ Contacto          │
                │ Oportunidad       │
                │ Cotizacion        │
                │ Venta             │
                └─────────┬─────────┘
                          │
                    OUTPUT PORTS
                          │
           ┌──────────────┼───────────────┐
           ▼              ▼               ▼
       PostgreSQL       Email           CRM externo
        Adapter         Adapter           Adapter
           │              │                │
           ▼              ▼                ▼
       PostgreSQL       SMTP/API        Salesforce
17. Estructura de proyecto

Si lo implementáramos con Java + Spring Boot, no recomiendo hacer esto:

controller/
service/
repository/
model/

para absolutamente todo el sistema.

Porque cuando el sistema crece puedes terminar con:

controller/
   EmpresaController
   ContactoController
   VentaController
   ...

service/
   EmpresaService
   ContactoService
   VentaService
   ...

repository/
   EmpresaRepository
   ContactoRepository
   VentaRepository

y toda la lógica del negocio queda distribuida sin una estructura clara.

Para una arquitectura hexagonal, prefiero organizarlo por dominio/módulo:

src/main/java/com/crm/

├── empresa/
│   ├── domain/
│   │   ├── Empresa.java
│   │   └── EmpresaRepository.java
│   │
│   ├── application/
│   │   ├── CrearEmpresaUseCase.java
│   │   └── CrearEmpresaService.java
│   │
│   └── infrastructure/
│       ├── EmpresaController.java
│       └── EmpresaRepositoryPostgres.java
│
├── contacto/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
│
├── oportunidad/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
│
├── cotizacion/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
│
├── venta/
│   ├── domain/
│   ├── application/
│   └── infrastructure/
│
└── shared/

Esto hace que la arquitectura "grite" el negocio y no el framework.

18. Módulo Empresa

La entidad:

public class Empresa {

    private String id;
    private String nombre;
    private String ruc;
    private String industria;
    private EstadoEmpresa estado;

}

El dominio no debería necesitar:

@Entity
@Table
@Autowired
@RestController

para representar la lógica de negocio.

Esas son preocupaciones externas.

19. Puerto de entrada
public interface CrearEmpresaUseCase {

    Empresa ejecutar(
        CrearEmpresaRequest request
    );
}

Este es un puerto de entrada.

20. Implementación del caso de uso
public class CrearEmpresaService
        implements CrearEmpresaUseCase {

    private final EmpresaRepository repository;

    public CrearEmpresaService(
            EmpresaRepository repository) {

        this.repository = repository;
    }

    @Override
    public Empresa ejecutar(
            CrearEmpresaRequest request) {

        Empresa empresa = new Empresa(
            request.nombre(),
            request.ruc(),
            request.industria()
        );

        return repository.guardar(empresa);
    }
}

Fíjate en algo importante:

EmpresaRepository

es una interfaz.

El Use Case no sabe si detrás hay:

PostgreSQL
MongoDB
API
memoria
21. Puerto de salida
public interface EmpresaRepository {

    Empresa guardar(Empresa empresa);

    Optional<Empresa> buscarPorId(String id);

    List<Empresa> buscarTodas();
}

Este puerto pertenece al lado interno de la aplicación.

22. Adaptador PostgreSQL
@Repository
public class EmpresaRepositoryPostgres
        implements EmpresaRepository {

    private final EmpresaJpaRepository repository;

    public EmpresaRepositoryPostgres(
            EmpresaJpaRepository repository) {

        this.repository = repository;
    }

    @Override
    public Empresa guardar(Empresa empresa) {

        // conversión
        // persistencia
        // PostgreSQL

        return empresa;
    }
}

Ahora tenemos:

             APPLICATION
                  │
                  │
                  ▼
       EmpresaRepository
              interface
                  ▲
                  │
                  │ implements
                  │
     EmpresaRepositoryPostgres
                  │
                  ▼
             PostgreSQL
23. REST Controller

El controller es un adaptador de entrada.

@RestController
@RequestMapping("/empresas")
public class EmpresaController {

    private final CrearEmpresaUseCase crearEmpresa;

    public EmpresaController(
            CrearEmpresaUseCase crearEmpresa) {

        this.crearEmpresa = crearEmpresa;
    }

    @PostMapping
    public EmpresaResponse crear(
            @RequestBody CrearEmpresaRequest request) {

        return crearEmpresa.ejecutar(request);
    }
}

El controller no contiene:

Reglas de negocio
SQL
cálculos
validaciones complejas

Su función principal es adaptar HTTP al caso de uso.

24. Flujo completo

Cuando llega:

POST /empresas

con:

{
    "nombre": "ABC Software",
    "ruc": "0999999999001",
    "industria": "Tecnología"
}

ocurre:

HTTP
 │
 ▼
EmpresaController
 │
 ▼
CrearEmpresaUseCase
 │
 ▼
CrearEmpresaService
 │
 ▼
EmpresaRepository
 │
 ▼
EmpresaRepositoryPostgres
 │
 ▼
PostgreSQL

La dirección de las dependencias sigue siendo hacia el núcleo.

25. Módulo Oportunidades

Este será uno de los módulos más importantes de una CRM B2B.

Una oportunidad podría tener:

id
empresa
contacto
vendedor
nombre
monto
etapa
probabilidad
fecha_cierre_estimada

Por ejemplo:

public class Oportunidad {

    private String id;
    private String empresaId;
    private String contactoId;

    private double monto;

    private EtapaOportunidad etapa;

    private double probabilidad;

}
26. Etapas

Podríamos definir:

PROSPECTO
    ↓
CALIFICADA
    ↓
REUNIÓN
    ↓
PROPUESTA
    ↓
NEGOCIACIÓN
    ↓
GANADA

o:

PERDIDA
27. Regla de negocio

Aquí es donde Clean Architecture realmente comienza a tener sentido.

Por ejemplo:

Una oportunidad no puede pasar directamente
de PROSPECTO a GANADA.

La regla podría estar en el dominio:

public void avanzarA(EtapaOportunidad nuevaEtapa) {

    if (!etapa.puedeAvanzarA(nuevaEtapa)) {
        throw new IllegalStateException(
            "Transición de etapa no permitida"
        );
    }

    this.etapa = nuevaEtapa;
}

No queremos esta regla dentro del controller:

@PostMapping
public ...

porque entonces la regla estaría atada a HTTP.

28. Caso de uso

Podríamos tener:

public interface AvanzarOportunidadUseCase {

    void ejecutar(
        String oportunidadId,
        EtapaOportunidad nuevaEtapa
    );
}

Y:

public class AvanzarOportunidadService
        implements AvanzarOportunidadUseCase {

    private final OportunidadRepository repository;

    @Override
    public void ejecutar(
            String id,
            EtapaOportunidad nuevaEtapa) {

        Oportunidad oportunidad =
            repository.buscarPorId(id);

        oportunidad.avanzarA(nuevaEtapa);

        repository.guardar(oportunidad);
    }
}

La regla sigue estando en:

Dominio

y el caso de uso coordina:

buscar
 ↓
aplicar regla
 ↓
guardar
29. Cotizaciones

Una oportunidad puede generar una cotización.

Oportunidad
      │
      ▼
Cotización
      │
      ├── Producto A
      ├── Producto B
      └── Producto C

Por ejemplo:

Cotización #COT-001

Empresa:
ABC Software

Producto:
Sistema ERP

Cantidad:
20

Precio:
$1.000

Total:
$20.000

El sistema podría calcular:

subtotal
descuento
impuestos
total

La lógica de cálculo no debería vivir en el controller.

30. Venta

Cuando la oportunidad se gana:

Oportunidad
     │
     ▼
GANADA
     │
     ▼
Venta

El caso de uso:

CerrarOportunidad

podría:

validar oportunidad
       ↓
marcar como GANADA
       ↓
crear venta
       ↓
registrar actividad
       ↓
notificar vendedor

Aquí puede aparecer otro puerto:

public interface NotificationPort {

    void enviar(
        String destinatario,
        String mensaje
    );
}

La aplicación no sabe si la notificación se envía mediante:

Email
WhatsApp
SMS
AWS SNS
31. Adaptador de correo
public class EmailNotificationAdapter
        implements NotificationPort {

    @Override
    public void enviar(
            String destinatario,
            String mensaje) {

        // SMTP / proveedor externo
    }
}

Podemos cambiarlo:

NotificationPort
       ▲
       │
       ├── EmailAdapter
       ├── SMSAdapter
       └── WhatsAppAdapter

sin modificar la regla de negocio.

32. Arquitectura completa del CRM

Una representación más profesional sería:

                         EXTERIOR
────────────────────────────────────────────────────────────

   React              Mobile              External Systems
     │                   │                       │
     ▼                   ▼                       ▼
 REST Adapter       API Adapter            Webhook Adapter
     │                   │                       │
     └───────────────────┼───────────────────────┘
                         │
                         ▼
                  INBOUND PORTS
                         │
                         ▼
┌────────────────────────────────────────────────────────────┐
│                                                            │
│                    APPLICATION CORE                        │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                     USE CASES                        │  │
│  │                                                      │  │
│  │ CrearEmpresa                                        │  │
│  │ CrearContacto                                       │  │
│  │ CrearOportunidad                                    │  │
│  │ AvanzarOportunidad                                  │  │
│  │ CrearCotizacion                                    │  │
│  │ CerrarOportunidad                                  │  │
│  │ RegistrarVenta                                     │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                  │
│  ┌──────────────────────▼───────────────────────────────┐  │
│  │                       DOMAIN                         │  │
│  │                                                      │  │
│  │ Empresa                                             │  │
│  │ Contacto                                            │  │
│  │ Oportunidad                                         │  │
│  │ Cotización                                          │  │
│  │ Venta                                               │  │
│  │ Reglas comerciales                                  │  │
│  └──────────────────────┬───────────────────────────────┘  │
│                         │                                  │
│                     OUTBOUND PORTS                         │
└─────────────────────────┼──────────────────────────────────┘
                          │
              ┌───────────┼─────────────┐
              ▼           ▼             ▼
        PostgreSQL      Email       External CRM
          Adapter      Adapter        Adapter
              │           │             │
              ▼           ▼             ▼
        PostgreSQL       SMTP       Salesforce/etc.
33. ¿Dónde está Clean Architecture aquí?

La arquitectura hexagonal que diseñamos cumple los principios de Clean Architecture:

                  CORE
                   │
          ┌────────┴────────┐
          │                 │
       DOMAIN           USE CASES
          │                 │
          └────────┬────────┘
                   │
                PORTS
                   │
          ┌────────┴────────┐
          │                 │
      ADAPTERS          ADAPTERS
          │                 │
       REST             DATABASE
          │                 │
       React          PostgreSQL

La tecnología está fuera.

El negocio está dentro.

34. Ejemplo de cambio de tecnología

Supongamos que hoy usamos:

PostgreSQL

Mañana la empresa decide utilizar:

MongoDB

Con una arquitectura tradicional podríamos tener:

Service
 ↓
JPA
 ↓
PostgreSQL

y tendríamos que modificar bastante código.

Con Hexagonal:

                EmpresaRepository
                       ▲
                       │
             ┌─────────┴─────────┐
             │                   │
       PostgreSQL            MongoDB
        Adapter              Adapter

La aplicación sigue utilizando:

EmpresaRepository

El cambio está principalmente en el adaptador.

Eso es exactamente el tipo de desacoplamiento que busca Hexagonal Architecture. AWS destaca que este enfoque facilita cambiar tecnologías de almacenamiento o interfaces con poco o ningún impacto sobre la lógica de negocio.

35. Pruebas

Esta arquitectura también facilita muchísimo las pruebas.

Podemos crear un adaptador falso:

public class EmpresaRepositoryInMemory
        implements EmpresaRepository {

    private List<Empresa> empresas =
        new ArrayList<>();
}

Ahora podemos probar:

CrearEmpresaService

sin:

PostgreSQL
Spring
Internet
API

Simplemente:

Use Case
   ↓
Fake Repository
   ↓
Memoria

Esto está alineado con el objetivo original de Cockburn: que la aplicación pueda probarse sin depender de la base de datos o de la interfaz externa.

36. Ejemplo de prueba
@Test
void deberiaCrearEmpresa() {

    EmpresaRepository repository =
        new EmpresaRepositoryInMemory();

    CrearEmpresaUseCase useCase =
        new CrearEmpresaService(repository);

    CrearEmpresaRequest request =
        new CrearEmpresaRequest(
            "ABC",
            "0999999999001",
            "Tecnologia"
        );

    Empresa empresa =
        useCase.ejecutar(request);

    assertEquals(
        "ABC",
        empresa.getNombre()
    );
}

No necesitamos levantar:

PostgreSQL

ni:

Servidor HTTP

para probar la regla.

37. Algo importante: no confundir abstracción con interfaces por todas partes

Una mala interpretación sería:

"Como es Clean Architecture, todo tiene que ser una interfaz."

No.

No necesitamos crear:

EmpresaServiceInterface
EmpresaServiceImpl
EmpresaFactoryInterface
EmpresaFactoryImpl
...

para absolutamente todo.

Las interfaces son útiles principalmente en los límites donde queremos desacoplar la aplicación de algo externo o definir contratos importantes.

Por ejemplo:

EmpresaRepository
NotificationPort
PaymentPort

tiene mucho sentido.

Crear interfaces innecesarias solo agrega complejidad.

38. Arquitectura recomendada para este CRM

Si fuera un proyecto real para implementar, yo usaría:

Frontend
React
   │
   ▼
REST API
Spring Boot
   │
   ▼
Hexagonal Architecture
   │
   ├── Domain
   │
   ├── Application
   │
   ├── Ports
   │
   └── Adapters
   │
   ▼
PostgreSQL

Y los módulos:

CRM
│
├── Empresa
├── Contacto
├── Oportunidad
├── Actividad
├── Producto
├── Cotización
├── Venta
└── Usuario
39. Arquitectura final resumida visualmente
                         CRM B2B
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
       WEB                MOBILE           EXTERNO
         │                  │                  │
         ▼                  ▼                  ▼
    REST Adapter       REST Adapter       Webhook Adapter
         │                  │                  │
         └──────────────────┼──────────────────┘
                            ▼
                     INPUT PORTS
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                                                        │
│                    APPLICATION                         │
│                                                        │
│  Empresa      Contacto      Oportunidad               │
│  Cotización   Venta         Actividades               │
│                                                        │
│                    USE CASES                            │
│                                                        │
│  CrearEmpresa                                          │
│  CrearContacto                                         │
│  CrearOportunidad                                      │
│  AvanzarOportunidad                                    │
│  CrearCotización                                       │
│  CerrarVenta                                           │
│                                                        │
│                       DOMAIN                           │
│                                                        │
│  Reglas comerciales                                    │
│  Validaciones                                          │
│  Estados                                               │
│  Entidades                                             │
│                                                        │
└────────────────────────┬───────────────────────────────┘
                         │
                    OUTPUT PORTS
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
       ▼                 ▼                 ▼
 PostgreSQL           Email          External APIs
 Adapter              Adapter             Adapter
       │                 │                 │
       ▼                 ▼                 ▼
 PostgreSQL             SMTP        ERP / Payments
La idea que debes aprenderte

Si mañana te preguntan “¿qué es Clean Architecture?”, no memorices los cuatro círculos.

Quédate con esto:

Clean Architecture busca que las reglas de negocio sean independientes de los detalles externos. Las dependencias deben apuntar hacia el núcleo.

Y si te preguntan “¿qué es Arquitectura Hexagonal?”:

Es una arquitectura de Ports & Adapters donde la aplicación se comunica con el exterior mediante puertos, y los adaptadores conectan esos puertos con tecnologías concretas como REST, PostgreSQL, correo o APIs externas.

Y para tu CRM B2B:

React
  ↓
Adapter
  ↓
Puerto de entrada
  ↓
Use Case
  ↓
Dominio
  ↓
Puerto de salida
  ↓
Adapter
  ↓
PostgreSQL

Esa es la esencia. El CRM sabe de empresas, contactos, oportunidades y ventas; no debería saber si está hablando con PostgreSQL, React, AWS o un servicio de correo.

Fuentes principales consultadas:

Alistair Cockburn, artículo original sobre Hexagonal / Ports & Adapters Architecture.
Robert C. Martin, The Clean Architecture Dependency Rule, sobre separación de responsabilidades y regla de dependencias.
AWS Prescriptive Guidance, Hexagonal Architecture Pattern, sobre desacoplamiento de lógica de negocio, UI y almacenamiento.
arc42 Quality Model, explicación de puertos de entrada/salida, adaptadores y dirección de dependencias.
Alistair Cockburn / Juan Manuel Garrido de Paz, recursos y evolución del concepto Ports & Adapters.