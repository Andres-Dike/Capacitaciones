from domain.ports.TaskRepositoryPort import TaskRepositoryPort

# Caso de uso: marcar tarea como completada. Depende del PUERTO.
class MarcarTask:
    def __init__(self, repository: TaskRepositoryPort):
        self.repository = repository

    def marcar_completada(self, nombre):
        return self.repository.marcar_completada(nombre)
