#esta clase no aplica el principio SPR, ya que tiene varias responsabilidades,
#  como agregar tareas, listar tareas y marcar tareas como completadas.
class ToDo:

    def __init__(self):
        self.tareas = []

    # Esta función registra la tarea y valida que no esté vacía
    def agregar_tarea(self, nombre):
        if not nombre.strip():
            return "La tarea no puede estar vacía"

        tarea = {
            "nombre": nombre,
            "completada": False
        }

        self.tareas.append(tarea)
        return "Tarea agregada correctamente"

    # Esta función lista las tareas
    def listar_tareas(self):
        return self.tareas

    # Esta función marca la tarea como completada
    def marcar_completada(self, nombre):
        for tarea in self.tareas:
            if tarea["nombre"] == nombre:
                tarea["completada"] = True
                return "Tarea marcada como completada"

        return "Tarea no encontrada"
todo=ToDo()
print(todo.agregar_tarea("Comprar leche"))
print(todo.agregar_tarea("Hacer ejercicio"))
print(todo.agregar_tarea("Comprar leche"))
print(todo.agregar_tarea("Hacer ejercicio"))
print(todo.agregar_tarea(""))
print(todo.marcar_completada("Comprar leche"))
print(todo.marcar_completada("Hacer ejercicio"))
print(todo.listar_tareas())
       