import os
import requests
from dotenv import load_dotenv

import  time

import json
import re

load_dotenv()

#Constantes
MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")
    
#Función para crear solicitud

def armar_peticion(MODELO, pregunta, system_instruction, response_schema=None): #pregunta = "Confirma la conexión"
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía.")
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"  #"https://generativelanguage.googleapis.com/v1beta/models/"
    body = {
            "systemInstruction": {
                "parts": [{"text": system_instruction}]
            },
            "contents": 
                [{"parts": [{"text": pregunta}]}]
        }

    if response_schema is not None:
        body["generationConfig"] = {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }

    return url, body

#Armar_peticion_Gemini -> url,body  

#Función envía la petición

def enviar_peticion(url, body):

    try:
       respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.ConnectionError:
       raise RuntimeError("No se pudo conectar con el servicio. Intenta nuevamente más tarde.")
    except requests.exceptions.Timeout:
       raise RuntimeError("La solicitud ha excedido el tiempo de espera. Intenta nuevamente más tarde.")

    if respuesta.status_code != 200:
        raise RuntimeError(
            f"Error en la petición. Status Code: {respuesta.status_code}" 
            #f"\nDetalle: {respuesta.text}"
        )

    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no llegó en el formato esperado.")

#Función procesa y extrae datos

def extraer_texto(datos): #Gemini
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("La respuesta no recibe el texto generado en el lugar definido.")

def obtener_dato_de_prueba(pregunta): #pregunta = "Confirma la conexión"

    response_schema = {
        "type": "object",
        "properties": {
            "categoria": {"type": "string"},
            "nivel": {"type": "number"}
        },
        "required": ["categoria", "nivel"]
    }
   
    system_instruction = "Eres un asistente amigable y respondes en máximo 2 palabras."
    url, body = armar_peticion(MODELO, pregunta, system_instruction, response_schema) #obtenemos url y body para la petición
    
    inicio = time.perf_counter() #Empezar el contador

    #url = resultado de armar_peticion
    #body = resultado de armar_peticion
    datos = enviar_peticion(url, body)

    fin = time.perf_counter() #Terminar el contador
    latencia = fin - inicio
    print(f"Latencia: {latencia:.2f} segundos")

    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo de la petición: ${costo:.6f} USD")
    texto = extraer_texto(datos)
    datos_formateados = parsear_respuesta_json(texto, ["categoria", "nivel"])
    return datos_formateados

#def calcular_costo(datos: dict, precio_entrada: float, precio_salida: float) -> float:
def calcular_costo(datos, precio_entrada, precio_salida):
    #datos = {dict... "usageMetadata"}
    uso = datos["usageMetadata"]
    '''
    uso = {
        "promptTokenCount": 10,
        "candidatesTokenCount": 471,
        "totalTokenCount": 1377,
        "promptTokensDetails": [
            {
                "modality": "TEXT",
                "tokenCount": 10
            }
        ],
        "thoughtsTokenCount": 896,
        "serviceTier": "standard"
    }
    '''
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso.get("thoughtsTokenCount", 0) #revisar si existe o no, si no existe colocarlo como 0
    costo = (tokens_entrada * precio_entrada) + ((tokens_salida + tokens_razonamiento) * precio_salida)
    return costo

def parsear_respuesta_json(texto, claves_requeridas=None):
    """
    claves_requeridas = ["categoria", "nivel"]
    """
    texto_limpio = texto.strip() #Eliminar espacios en blanco
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)
    try:
        datos = json.loads(texto_limpio) #Lanza una excepción si el texto no es un JSON válido
    except json.JSONDecodeError:
        raise ValueError("La respuesta del modelo no es un JSON válido.")

    if claves_requeridas:
        faltantes = [clave for clave in claves_requeridas if clave not in datos]
        if faltantes:
            raise ValueError(f"La respuesta no tiene la estructura esperada.")
    return datos

if __name__ == "__main__": #Solamente ejecútalo si el archivo en el que estoy está siendo directamente ejecutado. NO LO EJECUTA EN IMPORTS
    try:
        print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexión funciona"))
    except (ValueError, RuntimeError) as error:
        print("No se pudo completar la operación: ", error)

'''
Ejecutar 4 veces la MISMA petición con 1 modelo y ante cada petición se calcule e imprima: Latencia, Costo, Respuesta
Vuelver a hacer lo mismo con un modelo distinto (3 modelos a comparar)
OBJETIVO: Elegir el mejor modelo para mi proyecto
Usar un prompt relacionado con mi proyecto.
'''

"""
NOTA PARA MI PD (que es generico y que es de mi proyecto):

GENERICO (motor reutilizable, sirve para cualquier proyecto con Gemini):
- armar_peticion, enviar_peticion, extraer_texto, parsear_respuesta_json, calcular_costo.
  Estas funciones no saben de cuentas medicas, las uso desde main.py y consistencia.py.

NO ES GENERICO (quedo de la plantilla, es solo una prueba de conexion):
- obtener_dato_de_prueba y el bloque if __name__ == "__main__" del final.
  Usan el ejemplo "categoria/nivel", que no es de mi proyecto de duplicidad.
  Solo se ejecuta si corro este archivo directo (python consumir_gemini.py);
  cuando lo importo desde otros archivos, ese bloque NO se ejecuta.

LO ESPECIFICO DE MI PROYECTO VIVE EN OTROS ARCHIVOS:
- banco.py       -> mis 2 prompts (deteccion_duplicidad y clasificacion_riesgo_cuenta).
- main.py        -> mi miniaplicacion principal (usa el prompt de duplicidad).
- registro_resultados.json -> el resultado de mi prueba de consistencia (se genera solo).
"""