"""
main.py - Miniaplicacion: Detector de duplicidad de prestaciones en cuentas medicas.

Que hace mi aplicacion:
1. Tomo una cuenta medica (lista de prestaciones) de ejemplo.
2. Le pido a Gemini que detecte posibles prestaciones duplicadas.
3. Muestro el resultado en pantalla en formato ordenado.

Reutilizo las funciones de mi modulo consumir_gemini.py sin modificarlo.
"""

import consumir_gemini

# ----------------------------------------------------------------------
# 1. CONFIGURACION: modelo que uso
# ----------------------------------------------------------------------
# Elijo gemini-3.6-flash porque fue el mas estable y disponible en mis pruebas durante el curso.
MODELO = "gemini-3.6-flash"

# ----------------------------------------------------------------------
# 2. INSTRUCCION DE SISTEMA (el rol y las reglas del modelo).
#    La mantengo separada del mensaje del usuario.
# ----------------------------------------------------------------------
SYSTEM_INSTRUCTION = (
    "Eres un auditor de cuentas medicas. Tu tarea es revisar una lista de "
    "prestaciones de una cuenta y detectar posibles DUPLICIDADES: prestaciones "
    "que se cobran mas de una vez, ya sea con el mismo nombre o con nombres "
    "distintos que se refieren a lo mismo. "
    "Para cada posible duplicado, entrega los numeros de los items involucrados, "
    "un motivo breve, y un nivel de riesgo de devolucion de cuenta: 'alto', 'medio' o 'bajo'. "
    "Si no encuentras duplicados, devuelve una lista vacia. "
    "Responde SOLO con los datos solicitados, sin explicaciones adicionales."
)

# ----------------------------------------------------------------------
# 3. RESPUESTA (response_schema).
#    Defino la forma exacta del JSON que quiero recibir, asi la respuesta
#    siempre llega ordenada y la puedo leer de forma mas simple.
# ----------------------------------------------------------------------
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "duplicados": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {"type": "number"}
                    },
                    "motivo": {"type": "string"},
                    "nivel": {"type": "string"}
                },
                "required": ["items", "motivo", "nivel"]
            }
        }
    },
    "required": ["duplicados"]
}

# ----------------------------------------------------------------------
# 4. CUENTA DE EJEMPLO (el mensaje del usuario).
#    Por ahora la escribo aqui. Mas adelante la leere desde un archivo txt, csv o copiare y pegare el texto.
# ----------------------------------------------------------------------
CUENTA_EJEMPLO = """Revisa esta cuenta medica y detecta prestaciones duplicadas:
1. Radiografia de torax - cantidad 1
2. Rx torax - cantidad 1
3. Suero fisiologico 500ml - cantidad 2
4. Suero fisiologico 500ml - cantidad 1
5. Consulta medica general - cantidad 1
6. Hemograma completo - cantidad 1
"""

def analizar_cuenta(texto_cuenta):
    """
    Envio la cuenta a Gemini y devuelvo el resultado ya convertido a datos
    de Python (un diccionario con la lista de duplicados).
    """
    # Armo la peticion reutilizando mi modulo.
    url, body = consumir_gemini.armar_peticion(
        MODELO,
        texto_cuenta,
        SYSTEM_INSTRUCTION,
        RESPONSE_SCHEMA
    )

    # Envio la peticion a Gemini.
    datos = consumir_gemini.enviar_peticion(url, body)

    # Extraigo el texto que devolvio el modelo.
    texto = consumir_gemini.extraer_texto(datos)

    # Convierto ese texto en datos ordenados (JSON validado).
    resultado = consumir_gemini.parsear_respuesta_json(texto, ["duplicados"])

    return resultado

def mostrar_resultado(resultado):
    """Imprimo el resultado en pantalla."""
    duplicados = resultado["duplicados"]

    print("\n" + "=" * 60)
    print(" RESULTADO DEL ANALISIS DE DUPLICIDAD")
    print("=" * 60)

    if len(duplicados) == 0:
        print("No se detectaron prestaciones duplicadas.")
        return

    print(f"Se detectaron {len(duplicados)} posible(s) duplicado(s):\n")

    # Uso un contador manual para numerar cada duplicado.
    numero = 1
    for dup in duplicados:
        items = dup["items"]
        motivo = dup["motivo"]
        nivel = dup["nivel"]
        print(f"{numero}. Items {items} | Nivel: {nivel}")
        print(f"   Motivo: {motivo}\n")
        numero = numero + 1

# ----------------------------------------------------------------------
# 5. PUNTO DE ENTRADA: esto se ejecuta solo si corro este archivo directo.
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        resultado = analizar_cuenta(CUENTA_EJEMPLO)
        mostrar_resultado(resultado)
        print("Proceso terminado sin errores.")
    except (ValueError, RuntimeError) as error:
        print("No se pudo completar el analisis:", error)
