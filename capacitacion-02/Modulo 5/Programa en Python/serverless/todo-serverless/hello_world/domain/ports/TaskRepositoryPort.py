from abc import ABC, abstractmethod
from domain.Task import Task

# PUERTO DE SALIDA (Output Port).
# El dominio define este contrato; la infraestructura lo implementa.
# Los casos de uso dependen de esta abstraccion, NO de una implementacion concreta.
# Esto permite cambiar la implementacion (memoria -> DynamoDB) sin tocar el dominio.
class TaskRepositoryPort(ABC):

    @abstractmethod
    def agregar_tarea(self, tarea: Task):
        ...

    @abstractmethod
    def listar_tareas(self):
        ...

    @abstractmethod
    def marcar_completada(self, nombre: str):
        ...
