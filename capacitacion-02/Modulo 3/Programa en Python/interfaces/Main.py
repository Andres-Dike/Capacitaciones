# Adaptador de entrada: interfaz de linea de comandos (CLI).
# Delega la logica a los casos de uso; no conoce la infraestructura concreta.
from use_cases.CreateTask import CreateTask
from use_cases.ListTask import ListTask
from use_cases.MarcarTask import MarcarTask
from infrastructure.InMemoryTaskRepository import InMemoryTaskRepository


class Main:
    def __init__(self, createTask, listTask, marcarTask):
        self.CreateTask = createTask
        self.ListTask = listTask
        self.MarcarTask = marcarTask

    def run(self):
        while True:
            print("1. Agregar tarea")
            print("2. Listar tareas")
            print("3. Marcar tarea como completada")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                nombre = input("Ingrese el nombre de la tarea: ")
                resultado = self.CreateTask.agregar_tarea(nombre)
                print(resultado)
            elif opcion == "2":
                tareas = self.ListTask.listar_tareas()
                for i, tarea in enumerate(tareas):
                    estado = "Completada" if tarea.completada else "Pendiente"
                    print(f"{i + 1}. {tarea.nombre} - {estado}")
            elif opcion == "3":
                nombre = input("Ingrese el nombre de la tarea a marcar como completada: ")
                resultado = self.MarcarTask.marcar_completada(nombre.strip().lower())
                print(resultado)
            elif opcion == "4":
                break
            else:
                print("Opción inválida. Intente nuevamente.")


# Composicion / inyeccion de dependencias:
# aqui se elige el adaptador concreto y se inyecta en los casos de uso.
repository = InMemoryTaskRepository()
createTask = CreateTask(repository)
listTask = ListTask(repository)
marcarTask = MarcarTask(repository)

app = Main(createTask, listTask, marcarTask)
app.run()
