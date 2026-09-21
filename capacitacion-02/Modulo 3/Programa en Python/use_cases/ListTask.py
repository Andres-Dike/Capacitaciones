from domain.ports.TaskRepositoryPort import TaskRepositoryPort

# Caso de uso: listar tareas. Depende del PUERTO, no de la implementacion.
class ListTask:
    def __init__(self, repository: TaskRepositoryPort):
        self.repository = repository

    def listar_tareas(self):
        return self.repository.listar_tareas()
