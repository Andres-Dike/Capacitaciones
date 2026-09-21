QUe es solid? SOLID es un acrónimo que representa cinco principios fundamentales del diseño y la arquitectura de software. Su objetivo es ayudar a escribir código más limpio, escalable, flexible y fácil de mantener a lo largo del tiempo. Significado del acrónimo

Cada letra hace referencia a un principio de diseño específico:

S (Single Responsibility Principle - Principio de Responsabilidad Única): Una clase debe tener una sola razón para cambiar, lo que significa que solo debe realizar una única tarea o función.

O (Open/Closed Principle - Principio de Abierto/Cerrado): Las entidades de software (clases, módulos, funciones) deben estar abiertas para la extensión, pero cerradas para la modificación.

L (Liskov Substitution Principle - Principio de Sustitución de Liskov): Las clases derivadas deben ser sustituibles por sus clases base sin alterar el comportamiento correcto del programa.

I (Interface Segregation Principle - Principio de Segregación de Interfaces): Es preferible contar con varias interfaces específicas y pequeñas que con una sola interfaz grande y multipropósito.

D (Dependency Inversion Principle - Principio de Inversión de Dependencias): Se debe depender de abstracciones (interfaces o clases abstractas) y no de implementaciones concretas.

Origen y popularización

La formulación inicial de estos principios fue realizada por Robert C. Martin (conocido como "Uncle Bob") a finales de la década de 1990. Sin embargo, el acrónimo SOLID fue acuñado e introducido posteriormente por Michael Feathers alrededor del año 2004 para agrupar y recordar fácilmente estos cinco conceptos.

Problema planteado

Fueron desarrollados para combatir los síntomas de un mal diseño de software, a menudo denominado "código rancio" (code smells), caracterizado por:

Rigidez: El código es difícil de cambiar porque un pequeño cambio afecta a muchas otras partes del sistema.

Fragilidad: Al modificar un módulo, se rompen partes inesperadas e inconexas del software.

Inmovilidad: Es complicado reutilizar componentes en otros proyectos debido a su alto acoplamiento con el sistema actual.

Relación con los conceptos clave

Programación Orientada a Objetos (POO): SOLID guía la aplicación práctica de los pilares de la POO (Encapsulamiento, Herencia, Polimorfismo y Abstracción). Evita abusos comunes, como la herencia inadecuada o la creación de clases gigantes ("God Objects"), asegurando que la estructura orientada a objetos sea sólida.

Mantenibilidad: Reduce drásticamente la complejidad operativa. Al estar cada responsabilidad aislada y bien definida, localizar y corregir un error (o adaptar una regla de negocio) requiere modificar solo el componente específico sin riesgo de alterar el resto del sistema.

Extensibilidad: Facilita la incorporación de nuevas funcionalidades sin reescribir código existente. Mediante el uso de abstracciones e interfaces (principios O y D), se pueden añadir nuevos comportamientos simplemente implementando nuevas clases.

Refactorización: Proporciona la meta y la guía clara al reestructurar código existente. Cuando se refactoriza un sistema para mejorar su diseño interno sin cambiar su comportamiento externo, SOLID sirve como el estándar hacia el cual debe evolucionar esa arquitectura.

¿Qué problema intenta solucionar SOLID? SOLID intenta solucionar el deterioro del código a lo largo del tiempo, un fenómeno en el desarrollo de software donde el código fuente se vuelve cada vez más difícil de modificar, probar y mantener a medida que el proyecto crece.Los problemas clave que combateRobert C. Martin ("Uncle Bob") definió estos síntomas principales de un software con mal diseño:Rigidez: El sistema es difícil de cambiar porque una modificación simple en un lugar requiere un efecto dominó de cambios en muchos otros módulos.Fragilidad: Cada vez que realizas un cambio o corriges un error, se rompen inesperadamente otras partes del código que no tenían relación evidente con la modificación.Inmovilidad (Dificultad de reutilización): Es imposible extraer una parte del sistema para usarla en otro módulo o proyecto porque está fuertemente acoplada (pegada) a dependencias concretas que no se pueden separar.Viscosidad: Hacer las cosas "bien" (respetando la arquitectura) es tan difícil o lento que los desarrolladores terminan recurriendo a parches o hacks rápidos, lo que degrada la calidad del código aún más rápido.Complejidad innecesaria: Presencia de estructuras sobrediseñadas o clases gigantes ("God Objects") que intentan hacer de todo, lo que dificulta comprender cómo funciona el sistema.El objetivo finalSOLID busca transformar ese código rígido en un sistema con bajo acoplamiento y alta cohesión. Al aplicar estos principios, se consigue que el software responda al cambio de forma ágil, reduciendo el costo de mantenimiento y el riesgo de introducir nuevos errores.

Single responsabilitie-Principle. Una clase debe hacer solo una cosa