from Task import Task

#esta clase service aplica el principio SPR, ya que tiene una sola responsabilidad,
#  que es manejar las tareas, 
# y delega la responsabilidad de representar una tarea a la clase Task.
class TaskService:
    def __init__(self):
        self.tareas = [] 

    def agregar_tarea(self, nombre):
        if not nombre.strip():
            return "La tarea no puede estar vacía"
        nombre = nombre.strip().lower()
        tarea = Task(nombre)
        self.tareas.append(tarea)
        return "Tarea agregada correctamente"
    # Esta función lista las tareas
    def listar_tareas(self):
            return self.tareas
    
        # Esta función marca la tarea como completada
    def marcar_completada(self, nombre):
          
           nombre = nombre.strip().lower()
           for tarea in self.tareas:
            if tarea.nombre == nombre:
                      tarea.completada = True
                      return "Tarea marcada como completada"
            return "Tarea no encontrada"
