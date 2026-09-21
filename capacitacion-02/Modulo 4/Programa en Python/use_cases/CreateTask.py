from domain.Task import Task
from domain.ports.TaskRepositoryPort import TaskRepositoryPort

# Caso de uso: crear una tarea. Cumple SRP.
# Depende del PUERTO (abstraccion), no de la implementacion concreta.
class CreateTask:
    def __init__(self, repository: TaskRepositoryPort):
        self.repository = repository

    def agregar_tarea(self, nombre):
        if not nombre.strip():
            return "La tarea no puede estar vacía"
        nombre = nombre.strip().lower()
        tarea = Task(nombre)
        self.repository.agregar_tarea(tarea)
        return tarea
