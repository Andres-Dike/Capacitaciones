1er clase
la clase task se encarga de la entidad del sistema, registrado el nombre de la tarea y su esta completada o no

2da clase
la clase main, se encarga de imprimir los mensajes de salida, metodos y registrar los datos que ingresan los usuarios

3ra
La clase TaskService sí respeta el principio de Responsabilidad Única (SRP, el
primero), porque su única responsabilidad es gestionar tareas. Sin embargo, no 
cumple del todo el principio Abierto/Cerrado (el segundo), ya que para agregar 
una nueva funcionalidad como 'eliminar tarea' tendría que modificar la clase 
existente en vez de extenderla.