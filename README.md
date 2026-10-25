# Detector de duplicidad de prestaciones en cuentas médicas

Miniaplicación del curso de Especialización en Desarrollo con IA Generativa. (Accenture)
Usa la API de Gemini para revisar una cuenta médica (lista de prestaciones) y detectar posibles **duplicidades**: prestaciones cobradas más de una vez, ya sea con el mismo nombre o con nombres distintos que se refieren a lo mismo. El objetivo es reducir las devoluciones de las aseguradoras antes de enviar la cuenta.

Para cada posible duplicado, la aplicación entrega los ítems involucrados, un motivo breve y un nivel de riesgo de devolución (alto, medio o bajo), en formato JSON.

## Requisitos previos

- Python 3.10 o superior.
- Una API key de Gemini (se obtiene en Google AI Studio).

## Instalación

1. Clona o descarga este repositorio y entra a la carpeta del proyecto.

2. Crea y activa un entorno virtual:

   En Windows (PowerShell):
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

   En macOS / Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instala las dependencias:
   ```powershell
   pip install -r requirements.txt
   ```

4. Configura tus credenciales:
   - Copia el archivo `.env.example` y renómbralo como `.env`.
   - Abre el `.env` y coloca tu API key real:
     ```
     GEMINI_API_KEY=tu_llave_aqui
     ```
   - El archivo `.env` nunca se sube al repositorio (ya está excluido en `.gitignore`).

## Cómo ejecutar

Todos los scripts se ejecutan desde la carpeta `src`, con el entorno virtual activado.

**Aplicación principal** (detecta duplicidad en una cuenta de ejemplo):
```powershell
cd src
python main.py
```

Verás en pantalla los duplicados detectados (ítems, motivo y nivel de riesgo) y, al final, el mensaje "Proceso terminado sin errores."

## Otros scripts

- **Prueba de consistencia del banco de prompts:**
  ```powershell
  python consistencia.py
  ```
  Ejecuta cada prompt del banco varias veces y guarda cuántas respuestas vinieron bien formadas en `prompts/registro_resultados.json`.

- **Evaluación y comparación de modelos:**
  ```powershell
  python evaluacion_modelos.py
  ```
  Mide latencia y costo de varios modelos de Gemini para una tarea de duplicidad. Sirvió para elegir el modelo documentado en `docs/decision-arquitectura.md`.

## Estructura del proyecto

- `src/main.py` : aplicación principal (detección de duplicidad).
- `src/consumir_gemini.py` : módulo genérico de conexión a la API de Gemini (armar, enviar y procesar peticiones).
- `src/evaluacion_modelos.py` : comparación de modelos por latencia y costo.
- `src/consistencia.py` : prueba de consistencia de los prompts.
- `src/prompts/banco.py` : banco de prompts del proyecto.
- `src/prompts/registro_resultados.json` : resultado de la prueba de consistencia.
- `docs/` : documentación (decisión de arquitectura, diagrama y evidencias).
- `requirements.txt` : dependencias de Python.
- `.env.example` : plantilla de variables de entorno (sin credenciales reales).

## Notas

- El modelo elegido para la aplicación es `gemini-3.6-flash`. La justificación y la comparación con otros modelos está en `docs/decision-arquitectura.md`.
- Ningún secreto (API key) va escrito en el código: todo se lee desde el archivo `.env`.
