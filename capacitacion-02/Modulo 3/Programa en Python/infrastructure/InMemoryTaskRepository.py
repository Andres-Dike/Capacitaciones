from domain.ports.TaskRepositoryPort import TaskRepositoryPort

# ADAPTADOR DE SALIDA (infraestructura).
# Implementa el puerto TaskRepositoryPort usando una lista en memoria.
# Se puede sustituir por otra implementacion (BD, archivo, etc.) sin tocar el dominio.
class InMemoryTaskRepository(TaskRepositoryPort):
    def __init__(self):
        self.tareas = []  # Lista para almacenar las tareas

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def listar_tareas(self):
        return self.tareas

    def marcar_completada(self, nombre):
        for tarea in self.tareas:
            if tarea.nombre == nombre:
                tarea.completada = True
                return "Tarea marcada como completada"
        return "Tarea no encontrada"
