from domain.ports.TaskRepositoryPort import TaskRepositoryPort


# Caso de uso: marcar tarea como completada. Depende del PUERTO.
class MarcarTask:
    def __init__(self, repository: TaskRepositoryPort):
        self.repository = repository

    def marcar_completada(self, nombre):
        if not nombre or not nombre.strip():
            return "La tarea no puede estar vacía"

        nombre = nombre.strip().lower()

        if not self.existe_tarea(nombre):
            return "La tarea no existe"

        return self.repository.marcar_completada(nombre)

    def existe_tarea(self, nombre):
        for tarea in self.repository.listar_tareas():
            if tarea.nombre == nombre:
                return True
        return False
