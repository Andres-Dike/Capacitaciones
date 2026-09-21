#esta clase tiene laresponsabilidad de manejar la interacción con el usuario, 
# y delega la responsabilidad de manejar las tareas a la clase TaskService.
from TaskService import TaskService
class Main:
    def __init__(self, taskService):
        self.taskService = taskService

    def run(self):
        while True:
            print("1. Agregar tarea")
            print("2. Listar tareas")
            print("3. Marcar tarea como completada")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre = input("Ingrese el nombre de la tarea: ")
                resultado = self.taskService.agregar_tarea(nombre)
                print(resultado)
            elif opcion == "2":
                tareas = self.taskService.listar_tareas()
                for i, tarea in enumerate(tareas):
                    estado = "Completada" if tarea.completada else "Pendiente"
                    print(f"{i + 1}. {tarea.nombre} - {estado}")
            elif opcion == "3":
                nombre = input("Ingrese el nombre de la tarea a marcar como completada: ")
                resultado = self.taskService.marcar_completada(nombre.strip().lower())
                print(resultado)
            elif opcion == "4":
                break
            else:
                print("Opción inválida. Intente nuevamente.")
taskService = TaskService()
app = Main(taskService)
app.run()