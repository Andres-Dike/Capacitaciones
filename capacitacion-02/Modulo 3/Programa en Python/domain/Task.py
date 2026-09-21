# Entidad del dominio: representa una tarea.
# Tiene una sola responsabilidad: almacenar el nombre de la tarea y su estado.
# Vive en el dominio y NO depende de ninguna capa externa (regla de dependencias hexagonal).
class Task:
    def __init__(self, nombre):
        self.nombre = nombre
        self.completada = False
