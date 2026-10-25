"""
#Estructura de un prompt en el banco de prompts

BANCO_DE_PROMPT = [
    {
        "nombre": "x",
        "system_instruction": "y",
        "ejemplo_usuario": "z",
        "claves_esperadas": ["clave1", "clave2"],
        "response_schema": {
            "type": "object",
            "properties": {
                "categoria": {"type": "string"},
                "nivel": {"type": "number"}
            },
            "required": ["categoria", "nivel"]
        }
    }
]
"""

"""
Banco de prompts de mi miniaplicacion.

Prompt con su instruccion de sistema, ejemplo de mensaje de usuario, claves esperadas en la respuesta
y el response_schema del json a recibir siguiendo el formato visto en el curso.
"""

BANCO_DE_PROMPT = [
    {
        "nombre": "deteccion_duplicidad",
        "system_instruction": (
            "Eres un auditor de cuentas medicas. Tu tarea es revisar una lista de "
            "prestaciones de una cuenta y detectar posibles DUPLICIDADES: prestaciones "
            "que se cobran mas de una vez, ya sea con el mismo nombre o con nombres "
            "distintos que se refieren a lo mismo. "
            "Para cada posible duplicado, entrega los numeros de los items involucrados, "
            "un motivo breve, y un nivel de riesgo de devolucion de cuenta: 'alto', 'medio' o 'bajo'. "
            "Si no encuentras duplicados, devuelve una lista vacia. "
            "Responde SOLO con los datos solicitados, sin explicaciones adicionales."
        ),
        "ejemplo_usuario": (
            "Revisa esta cuenta medica y detecta prestaciones duplicadas:\n"
            "1. Radiografia de torax - cantidad 1\n"
            "2. Rx torax - cantidad 1\n"
            "3. Suero fisiologico 500ml - cantidad 2\n"
            "4. Suero fisiologico 500ml - cantidad 1\n"
            "5. Consulta medica general - cantidad 1\n"
            "6. Hemograma completo - cantidad 1"
        ),
        "claves_esperadas": ["duplicados"],
        "response_schema": {
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
    },
    {
        "nombre": "clasificacion_riesgo_cuenta",
        "system_instruction": (
            "Eres un auditor de cuentas medicas. Tu tarea es revisar una cuenta y "
            "clasificar el RIESGO GLOBAL de que la aseguradora la devuelva por "
            "inconsistencias. "
            "Devuelve un nivel de riesgo: 'alto', 'medio' o 'bajo', y un resumen "
            "breve (una sola frase) que justifique ese nivel. "
            "Responde SOLO con los datos solicitados, sin explicaciones adicionales."
        ),
        "ejemplo_usuario": (
            "Clasifica el riesgo de devolucion de esta cuenta medica:\n"
            "1. Radiografia de torax - cantidad 1\n"
            "2. Rx torax - cantidad 1\n"
            "3. Suero fisiologico 500ml - cantidad 2\n"
            "4. Suero fisiologico 500ml - cantidad 1\n"
            "5. Consulta medica general - cantidad 1\n"
            "6. Hemograma completo - cantidad 1"
        ),
        "claves_esperadas": ["nivel", "resumen"],
        "response_schema": {
            "type": "object",
            "properties": {
                "nivel": {"type": "string"},
                "resumen": {"type": "string"}
            },
            "required": ["nivel", "resumen"]
        }
    }
]

"""
Primer prompt es el prompt que representa la funcion principal de la miniaplicacion
y es el mismo que se encuentra en el main.py
El segundo prompt es complementario, y mas global, lo pense para que en caso de
mi prompt principal usar muchos tokens o llamadas a la api de gemini, este pueda hacer
una primera revision global a la cuenta y luego decidir si analizarla o no de acuerdo
a que tan riesgosa puede ser en cuanto a la devolucion de la aseguradora.
"""