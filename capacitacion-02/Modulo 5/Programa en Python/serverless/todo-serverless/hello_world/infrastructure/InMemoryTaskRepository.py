from domain.ports.TaskRepositoryPort import TaskRepositoryPort

# ADAPTADOR DE SALIDA (infraestructura).
# Implementa el puerto usando una lista en memoria.
# NOTA: en Lambda la memoria NO persiste entre invocaciones; para persistencia
# real se puede crear otro adaptador (ej. DynamoDBTaskRepository) que implemente
# el mismo puerto, sin cambiar los casos de uso ni el dominio.
class InMemoryTaskRepository(TaskRepositoryPort):
    def __init__(self):
        self.tareas = []

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
