import os
import requests
from dotenv import load_dotenv

load_dotenv()

#Constantes
MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")
    
#Función para crear solicitud

def armar_peticion(pregunta): #pregunta = "Confirma la conexión"
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía.")
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"  #"https://generativelanguage.googleapis.com/v1beta/models/"
    body = {
        "contents": 
            [{"parts": [{"text": pregunta}]}]
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
        raise RuntimeError(f"Error en la petición. Status Code: {respuesta.status_code}")

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
    url, body = armar_peticion(pregunta) #obtenemos url y body para la petición
    #url = resultado de armar_peticion
    #body = resultado de armar_peticion
    datos = enviar_peticion(url, body)
    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"Costo de la petición: ${costo:.6f} USD")
    return extraer_texto(datos)

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
    tokens_razonamiento = uso["thoughtsTokenCount"] #revisar si existe o no, si no existe colocarlo como 0
    costo = (tokens_entrada * precio_entrada) + ((tokens_salida + tokens_razonamiento) * precio_salida)
    return costo
    
try:
    print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexión funciona"))
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación: ", error)