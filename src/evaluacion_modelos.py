import consumir_gemini
import time

def evaluar_modelo(nombre_modelo, pregunta, precio_entrada, precio_salida, repeticiones=4):
    """
    Ejecuta 'repeticiones' veces la misma peticion para un modelo especifico.
    Calcula e imprime Latencia, Costo y Respuesta de cada intento,
    ademas del promedio de latencia al final.
    """
    system_instruction = "Eres un auditor de cuentas medicas que detecta prestaciones duplicadas y responde de forma breve."
    print("=" * 70)
    print(f" EVALUANDO MODELO: {nombre_modelo}")
    print("=" * 70)
    
    latencias = []
    costos = []

    for i in range(1, repeticiones + 1):
        print(f"\n--- Intento {i} de {repeticiones} ({nombre_modelo}) ---")
        
        # 1. Armar petición (puedes pasar el modelo si tu función lo requiere)
        url, body = consumir_gemini.armar_peticion(nombre_modelo, pregunta, system_instruction) 

        # 2. Medir latencia
        inicio = time.perf_counter()
        datos = consumir_gemini.enviar_peticion(url, body)
        fin = time.perf_counter()
        
        latencia = fin - inicio
        latencias.append(latencia)
        
        # 3. Calcular costo
        costo = consumir_gemini.calcular_costo(datos, precio_entrada, precio_salida)
        costos.append(costo)
        
        # 4. Extraer respuesta
        respuesta = consumir_gemini.extraer_texto(datos)
        
        # 5. Imprimir resultados de la petición actual
        print(f"Latencia:  {latencia:.2f} segundos")
        print(f"Costo:     ${costo:.6f} USD")
        print(f"Respuesta: {respuesta}")

    # Resumen acumulado del modelo
    latencia_promedio = sum(latencias) / len(latencias)
    costo_total = sum(costos)
    
    print("\n" + "-" * 40)
    print(f" RESUMEN {nombre_modelo}:")
    print(f" Latencia promedio: {latencia_promedio:.2f} segundos")
    print(f" Costo acumulado ({repeticiones} peticiones): ${costo_total:.6f} USD")
    print("-" * 40 + "\n")


pregunta_prueba = "Revisa esta cuenta y di si hay prestaciones duplicadas: 1. Radiografia de torax, 2. Rx torax, 3. Hemograma. Responde en una frase breve."
modelos = [
    {
        "nombre": "gemini-3.6-flash",
        "precio_entrada": 0.00000075,
        "precio_salida": 0.00000375
    },
    {
        "nombre": "gemini-3.1-flash-lite",
        "precio_entrada": 0.00000025,
        "precio_salida": 0.00000150
    },
    {
        "nombre": "gemini-3.8-flash",
        "precio_entrada": 0.00000075,
        "precio_salida": 0.00000375
    }
]

# Procesar los 3 modelos consecutivamente
for config in modelos:
    try:
        evaluar_modelo(
            nombre_modelo=config["nombre"],
            pregunta=pregunta_prueba,
            precio_entrada=config["precio_entrada"],
            precio_salida=config["precio_salida"],
            repeticiones=2
        )
    except (ValueError, RuntimeError) as error:
        print(f"No se pudo evaluar el modelo {config['nombre']}: {error}")
#Ejecute solo 2 repeticiones por modelo, por limitación de la capa gratuita de Gemini.
#Envolví la evaluación de cada modelo en un try/except por que me daba mucho error 503, asi al menos guardo ese resultado.