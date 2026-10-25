def suma(a, b):
    resultado = a + b
    return resultado

#print(suma(5, 6))


estudiante = {
    "nombre": "Pablo",
    "edad": 39,
    "curso": {
        "nombre": "Python",
        "calificacion": 92
    },
    "tareas": [
        {
            "titulo": "Variables",
            "completada": True
        },
        {
            "titulo": "Consumo de APIs",
            "completada": False
        }
    ]
}

print ("El nombre del estudiante es:", estudiante["nombre"]) #El nombre de la estudiante
print ("La calificación del curso es:", estudiante["curso"]["calificacion"]) #La calificación del curso
print (estudiante["tareas"][1]["titulo"]) #El título de la segunda tarea
print (estudiante["tareas"][0]["completada"]) #El estado de la primera tarea
if estudiante["tareas"][0]["completada"]:
    print("La primera tarea esta completada")

#print("La primera tarea esta completada" if estudiante["tareas"][0]["completada"] else "No esta")
#console.log(condicion ? "Si se cumple" : "No se cumple")
#print(f'El nombre del estudiante es: {estudiante["nombre"]}')