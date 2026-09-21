from abc import ABC, abstractmethod
from domain.Task import Task

# PUERTO DE SALIDA (Output Port).
# El dominio/aplicacion define este contrato; la infraestructura lo implementa.
# Asi los casos de uso dependen de esta abstraccion y NO de una implementacion concreta.
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
