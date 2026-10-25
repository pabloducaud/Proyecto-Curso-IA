import json
import time
from prompts.banco import BANCO_DE_PROMPT
from consumir_gemini import armar_peticion, enviar_peticion, extraer_texto, parsear_respuesta_json

#Es generico, se usa para recorrer mi banco de prompt que son los propios de mi miniaplicación.

registro = {}

try:

    for prompt in BANCO_DE_PROMPT:
        exitos = 0
        intentos = 2
        for intento in range(intentos):
            try:
                url, body = armar_peticion("gemini-3.6-flash", prompt["ejemplo_usuario"], prompt["system_instruction"], prompt["response_schema"])
                respuesta = enviar_peticion(url, body)
                text = extraer_texto(respuesta)
                datos = parsear_respuesta_json(text, prompt["claves_esperadas"])
                exitos += 1
                print(f"Respuesta: {datos}")
            except (ValueError, RuntimeError) as error:
                print(f"Intento {intento + 1} de {prompt['nombre']} fallo: {error}")
            time.sleep(1)  # Pausa de 1 segundo entre intentos
        print(f"{prompt['nombre']}: {exitos}/{intentos} respuestas exitosas")
        registro[prompt["nombre"]] = {"exitos": exitos, "intentos": intentos}
    #Tengo el try diferente al del curso para envolver toda la petición (armar, enviar, extraer y parsear) y atrapar tanto ValueError como RuntimeError, por el error 503 que me daba y no guardaba resultados.
    with open("prompts/registro_resultados.json", "w", encoding="utf-8") as archivo:
        json.dump(registro, archivo, indent=2, ensure_ascii=False)

except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación:", error)