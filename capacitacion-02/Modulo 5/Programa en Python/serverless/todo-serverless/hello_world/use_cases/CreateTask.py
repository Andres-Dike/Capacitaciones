from domain.Task import Task
from domain.ports.TaskRepositoryPort import TaskRepositoryPort


# Caso de uso: crear una tarea. Depende del PUERTO, no de la implementacion.
class CreateTask:
    def __init__(self, repository: TaskRepositoryPort):
        self.repository = repository

    def agregar_tarea(self, nombre):
        if not nombre or not nombre.strip():
            return None

        nombre = nombre.strip().lower()
        tarea = Task(nombre)

        self.repository.agregar_tarea(tarea)
        return tarea
