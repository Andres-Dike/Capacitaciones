import json

from use_cases.MarcarTask import MarcarTask
from use_cases.ListTask import ListTask
from use_cases.CreateTask import CreateTask
from infrastructure.InMemoryTaskRepository import InMemoryTaskRepository


repository = InMemoryTaskRepository()

create_task = CreateTask(repository)
list_task = ListTask(repository)
marcar_task = MarcarTask(repository)


def lambda_handler(event, context):

    http_method = event.get("httpMethod")

    # POST - Crear tarea
    if http_method == "POST":

        try:
            body = json.loads(event.get("body") or "{}")
        except (ValueError, TypeError):
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "mensaje": "El cuerpo de la petición no es un JSON válido"
                })
            }

        nombre = body.get("nombre")

        tarea = create_task.agregar_tarea(nombre)

        if tarea is None:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "mensaje": "El nombre de la tarea no puede estar vacío"
                })
            }

        return {
            "statusCode": 201,
            "body": json.dumps({
                "mensaje": "Tarea registrada correctamente",
                "tarea": {
                    "nombre": tarea.nombre,
                    "completada": tarea.completada
                }
            })
        }

    # GET - Listar tareas
    if http_method == "GET":

        if list_task.lista_esta_vacia():
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "mensaje": "La lista de tareas está vacía"
                })
            }

        tareas = list_task.listar_tareas()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "tareas": [
                    {
                        "nombre": tarea.nombre,
                        "completada": tarea.completada
                    }
                    for tarea in tareas
                ]
            })
        }

    # PUT - Marcar tarea como completada
    if http_method == "PUT":

        nombre = (event.get("queryStringParameters") or {}).get("nombre")

        resultado = marcar_task.marcar_completada(nombre)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "mensaje": resultado
            })
        }

    return {
        "statusCode": 405,
        "body": json.dumps({
            "mensaje": "Método HTTP no permitido"
        })
    }