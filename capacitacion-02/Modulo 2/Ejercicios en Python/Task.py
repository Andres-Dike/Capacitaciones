#esta clase se encarga de representar una tarea, y tiene una sola responsabilidad, que es almacenar el nombre de la tarea y su estado de completada o no.
class Task:
    def __init__(self, nombre):
        self.nombre = nombre
        self.completada = False
    