# Adaptador de entrada: API REST con FastAPI.
from fastapi import FastAPI
from domain.Task import Task
from use_cases.CreateTask import CreateTask
from use_cases.ListTask import ListTask
from use_cases.MarcarTask import MarcarTask
from infrastructure.InMemoryTaskRepository import InMemoryTaskRepository

app = FastAPI()

# Composicion / inyeccion de dependencias.
repository = InMemoryTaskRepository()
create_task = CreateTask(repository)
list_task = ListTask(repository)
marcar_task = MarcarTask(repository)


@app.post("/tareas")
def registrar_tarea(nombre: str):
    tarea = create_task.agregar_tarea(nombre)

    # Si el nombre es invalido, el caso de uso devuelve un mensaje (str).
    if not isinstance(tarea, Task):
        return {"mensaje": tarea}

    return {
        "mensaje": "Tarea registrada correctamente",
        "tarea": {
            "nombre": tarea.nombre,
            "completada": tarea.completada
        }
    }


@app.get("/tareas")
def listar_tareas():
    if list_task.lista_esta_vacia():
        return {
            "mensaje": "No hay tareas registradas"
        }

    tareas = list_task.listar_tareas()

    return {
        "tareas": [
            {
                "nombre": tarea.nombre,
                "completada": tarea.completada
            }
            for tarea in tareas
        ]
    }


@app.put("/tareas/completar")
def marcar_tarea_completada(nombre: str):
    resultado = marcar_task.marcar_completada(nombre)
    return {
        "mensaje": resultado
    }
