from domain.ports.TaskRepositoryPort import TaskRepositoryPort

# Caso de uso: listar tareas. Depende del PUERTO.
class ListTask:
    def __init__(self, repository: TaskRepositoryPort):
        self.repository = repository

    def listar_tareas(self):
        if not self.lista_esta_vacia():
            return self.repository.listar_tareas()

    def lista_esta_vacia(self):
        return len(self.repository.listar_tareas()) == 0
