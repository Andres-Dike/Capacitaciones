1\. Variables y tipos de datos

Las variables permiten almacenar valores en la memoria durante la ejecución de un programa. El valor de una variable puede cambiar durante la ejecución.

Los tipos de datos determinan qué tipo de valor puede almacenar una variable. Algunos ejemplos en Python son:

```
nombre = "Andrés"
edad = 20
salario = 500.50
activo = True
```

En este caso, `nombre` es una cadena de texto, `edad` es un entero, `salario` es un número decimal y `activo` es un valor booleano.

## 2\. Condicionales

Los condicionales permiten que un programa tome decisiones dependiendo de si se cumple o no una condición.

```
if edad >= 18:
    print("Mayor de edad")
else:
    print("Menor de edad")
```

## 3\. Bucles

Los bucles permiten repetir un bloque de código varias veces. Los más utilizados en Python son `for` y `while`.

```
for numero in range(5):
    print(numero)
```

## 4\. Funciones

Una función es un bloque de código que realiza una tarea específica y puede reutilizarse varias veces.

```
def saludar(nombre):
    print("Hola", nombre)
```

Las funciones ayudan a organizar y reutilizar el código.

## 5\. Listas

Las listas permiten almacenar varios valores dentro de una misma estructura. Sus elementos pueden modificarse.

```
frutas = ["manzana", "pera", "uva"]
```

Se pueden agregar, eliminar o modificar elementos de una lista.

## 6\. Diccionarios

Los diccionarios almacenan información mediante pares de clave y valor.

```
usuario = {
    "nombre": "Andrés",
    "edad": 20
}
```

Esto permite acceder a los datos utilizando sus respectivas claves.

## 7\. Manejo básico de errores

El manejo de errores permite controlar situaciones que pueden provocar que el programa falle durante su ejecución. En Python se puede utilizar `try` y `except`.

```
try:
    numero = int(input("Ingrese un número: "))
except ValueError:
    print("Debe ingresar un número válido")
```

## 8\. Clases simples

Una clase es una estructura que permite definir objetos con datos y comportamientos. Es uno de los conceptos fundamentales de la programación orientada a objetos.

```
class Persona:
    def __init__(self, nombre):
        self.nombre = nombre
```

A partir de esta clase se pueden crear objetos `Persona`.

## 9\. Lectura de errores en consola

Los errores mostrados en la consola proporcionan información sobre los problemas encontrados durante la ejecución del programa.

Es importante revisar:

-   El tipo de error.
-   El archivo donde ocurrió.
-   La línea en la que ocurrió.
-   El mensaje que describe el problema.

Leer correctamente estos mensajes permite identificar con mayor rapidez la causa del error.

## 10\. Ejecución de scripts Python

Un script de Python es un archivo que contiene instrucciones escritas en Python, normalmente con extensión `.py`.

Puede ejecutarse desde una terminal utilizando:

```
python archivo.py
```

La ejecución permite comprobar el comportamiento del programa y detectar posibles errores.

## 11\. Diferencia entre escribir código y entender código

**Escribir código** consiste en crear instrucciones para que el programa realice una tarea.

**Entender código** consiste en comprender qué hace, cómo funciona, qué datos utiliza y por qué está construido de determinada manera.

En un proyecto de software es importante desarrollar ambas capacidades. No basta con escribir código que funcione; también es necesario poder leer y comprender código existente para modificarlo, corregir errores y trabajar con código desarrollado por otros integrantes del equipo.