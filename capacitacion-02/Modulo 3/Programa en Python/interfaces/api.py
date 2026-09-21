# Adaptador de entrada: API REST con FastAPI.
from fastapi import FastAPI
from use_cases.CreateTask import CreateTask
from use_cases.ListTask import ListTask
from infrastructure.InMemoryTaskRepository import InMemoryTaskRepository

app = FastAPI()

# Composicion / inyeccion de dependencias.
repository = InMemoryTaskRepository()
create_task = CreateTask(repository)
list_task = ListTask(repository)


@app.get("/tareas")
def registrar_tarea(nombre: str):
    resultado = create_task.agregar_tarea(nombre)
    return {"mensaje": resultado}


@app.get("/tareas/listar")
def listar_tareas():
    tareas = list_task.listar_tareas()
    return {
        "tareas": [
            {"nombre": t.nombre, "completada": t.completada}
            for t in tareas
        ]
    }
