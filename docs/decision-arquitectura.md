# Decisión de arquitectura: elección de modelo

Fecha de la comparación: Martes 20 de Octubre del 2026
Nombre de la miniaplicación: Análisis de cuentas médicas con IA
Objetivo: Analizar cuentas médicas antes del envío a aseguradoras para disminuir devoluciones por inconsistencias, empezando por la detección de duplicidad de prestaciones.

## Modelo elegido

Elegí el modelo: gemini-3.6-flash

Mi miniaplicación sirve para: detectar prestaciones duplicadas en una cuenta médica (por ejemplo, un mismo examen cobrado dos veces con nombres distintos, o cargados a la misma hora y fecha) antes de enviarla a la aseguradora, clasificando cada hallazgo por nivel de riesgo de devolución.

Los requisitos que necesito cumplir son:

* Usar la API gratuita de Gemini sin exceder la cuota (entradas y salidas cortas, pocas llamadas).
* Entregar la respuesta en formato JSON estructurado y validado.
* Que el modelo detecte duplicados no obvios (mismo servicio con distinto nombre), y de no existir detecte coincidencias exactas.

## Diagrama de arquitectura

[Diagrama de Arquitectura] - (docs/diagrama_arquitectura_PD.png)

## Comparación de candidatos

- Estas son las preguntas y condiciones con las cuales se midieron los modelos:

* Preguntas y/o condiciones:

1. Se usó la misma petición para los tres modelos: una cuenta médica corta con una duplicidad evidente (Radiografía de tórax / Rx tórax) y un ítem no duplicado (Hemograma).
2. Se ejecutaron 2 repeticiones por modelo, midiendo latencia y costo en cada una (2 repeticiones para no agotar la cuota gratuita).
3. Se evaluó la calidad de la respuesta para mi caso: que identifique correctamente la duplicidad y responda de forma breve.

| Criterio | gemini-3.6-flash | gemini-3.1-flash-lite | gemini-3.8-flash |
|---|---|---|---|
| Tarifa de entrada en USD por millón de tokens | 0.75 | 0.25 | 0.75 |
| Tarifa de salida en USD por millón de tokens | 3.75 | 1.50 | 3.75 |
| Latencias observadas en segundos | 5.08 y 4.32 | 6.04 y 5.11 | No medida (timeout) |
| Latencia promedio en segundos | 4.70 | 5.57 | No medida (timeout) |
| Costo acumulado 2 peticiones (USD) | 0.002835 | 0.000105 | No medido (timeout) |
| Calidad para mi miniaplicación | Alta: detecta la duplicidad y la explica con precisión | Media: detecta la duplicidad pero con respuestas más simples | No evaluada (timeout) |

Fuente de las tarifas:
- Página oficial de precios de Gemini: ai.google.dev/gemini-api/docs/pricing (consultada en octubre 2026). Precios de la tarifa estándar vigentes hasta el 31 de diciembre de 2026.

Observación sobre las pruebas:
El modelo gemini-3.8-flash no pudo medirse porque la solicitud excedió el tiempo de espera (timeout de 30 segundos) en la prueba. Esto se registró gracias a que el código continúa con los demás modelos aunque uno falle. La evidencia completa de la corrida está en docs/evidencia_evaluacion_modelos.txt.

## Justificación

Elegí el modelo gemini-3.6-flash porque para mi aplicación entregó las respuestas más precisas y completas al detectar la duplicidad, con una latencia promedio buena (4.70 s) y fue el modelo más estable y disponible durante mis pruebas y en las sesiones del curso en el Gate 1.
Lo que observé en las pruebas fue que gemini-3.1-flash-lite es muchísimo más barato (unas 27 veces menos costo), pero sus respuestas son más simples; y que gemini-3.8-flash no respondió a tiempo (timeout).
El criterio más relevante para mi decisión fue la combinación de calidad de la respuesta y estabilidad/disponibilidad del modelo.
Una limitación que encontré en mi elección fue que gemini-3.6-flash es más caro que el flash-lite, lo que importa si en el futuro el volumen de cuentas crece.

## Alternativa descartada y por qué

Descarté gemini-3.8-flash porque no pude obtener datos de latencia ni costo (la solicitud excedió el tiempo de espera en la prueba), lo que lo hace poco confiable para mi caso en este momento.
Dejé gemini-3.1-flash-lite como alternativa a considerar a futuro: es la opción más económica y podría usarse para una primera revisión masiva de cuentas, reservando gemini-3.6-flash para el análisis detallado.