# -*- coding: utf-8 -*-
# Utilidades para interactuar con el modelo de lenguaje (IA - Gemini)
import google.generativeai as genai
from sumario_commit import util_config
from sumario_commit import constantes
from sumario_commit import util_debug

# Variable global para el modelo inicializado
modelo_ia = None

def configurar_ia() -> bool:
    """Configura el cliente de la API de Google AI."""
    global modelo_ia
    api_key = util_config.obtener_api_key()
    if not api_key:
        return False

    try:
        util_debug.registrar_depuracion("Configurando API de Google AI.")
        genai.configure(api_key=api_key)
        # Crear el modelo una vez
        modelo_ia = genai.GenerativeModel(constantes.NOMBRE_MODELO_IA)
        util_debug.registrar_depuracion(f"Modelo IA '{constantes.NOMBRE_MODELO_IA}' listo.")
        return True
    except Exception as e:
        print(f"Error al configurar la API de Google AI: {e}")
        util_debug.registrar_depuracion(f"Excepción al configurar GenAI: {e}")
        modelo_ia = None
        return False

def construir_prompt(diff_content: str) -> str:
    """Construye el prompt completo para enviar a la IA."""
    prompt_sistema = f"""
Eres un asistente experto en análisis de código y commits de Git. Tu tarea es analizar el siguiente patch de Git (diff) y extraer *exclusivamente* dos puntos clave: las tareas concretas que se realizaron y cualquier aprendizaje, descubrimiento o dificultad encontrada durante la implementación de esos cambios.

Basándote *únicamente* en el contenido del patch proporcionado, responde de forma concisa y estructurada en castellano y en primera persona. No añadas introducciones, conclusiones ni ningún otro texto fuera de la estructura solicitada.

Formato estricto de la respuesta:

**Tareas Realizadas:**
- [Descripción breve de la tarea 1 basada en el diff]
- [Descripción breve de la tarea 2 basada en el diff]
- ...

**Aprendizajes:**
- [Descripción breve del aprendizaje 1, si se infiere del diff o comentarios]
- [Descripción breve de la dificultad o descubrimiento 2, si se infiere]
- ...

**Resumen General de Tareas:**
[Un resumen muy breve (2-3 líneas máximo) describiendo en general qué tipo de trabajo se realizó en este commit.]
- ...
**Resumen General de Aprendizaje:**
[Un resumen muy breve (2-3 líneas máximo) sobre los aprendizajes, descubrimientos o dificultades clave encontradas, si se pueden inferir.]
- ...

Si no puedes inferir claramente alguna de las secciones (especialmente Aprendizajes) a partir del patch, deja esa sección vacía o indica "No se infieren aprendizajes directos del patch". No inventes información. Si no hay tareas claras, indícalo también.

Aquí está el patch:
```diff
{diff_content}
```"""
    util_debug.registrar_depuracion("Prompt construido para la IA.")
    return prompt_sistema

def generar_resumen_con_ia(patch_contenido: str) -> str | None:
    """Envía el patch a la IA y devuelve el resumen generado."""
    global modelo_ia

    if modelo_ia is None:
        print("Error: El modelo de IA no está configurado. Intenta configurar la API Key.")
        util_debug.registrar_depuracion("Intento de generar resumen sin modelo IA configurado.")
        if not configurar_ia():  # Intenta configurar de nuevo
            return None

    if not patch_contenido:
        util_debug.registrar_depuracion("Contenido del patch vacío, no se llama a la IA.")
        return "Error: Contenido del patch vacío."

    prompt = construir_prompt(patch_contenido)
    util_debug.registrar_depuracion(f"Enviando prompt a la IA (modelo {constantes.NOMBRE_MODELO_IA})...")

    try:
        # Configuración para asegurar respuesta de texto
        generation_config = genai.types.GenerationConfig(
            #candidate_count=1,  # Solo necesitamos una respuesta
            response_mime_type="text/plain"  # Asegurar texto plano
        )
        respuesta = modelo_ia.generate_content(prompt, generation_config=generation_config)

        # Acceder al texto de la respuesta de forma segura
        if respuesta.parts:
            resumen = respuesta.text  # Acceso directo si parts existe y tiene contenido
            util_debug.registrar_depuracion("Respuesta recibida de la IA.")
            return resumen
        else:
            # Manejar el caso donde no hay 'parts' o están vacías (podría indicar bloqueo, etc.)
            print("Error: La IA no devolvió contenido válido.")
            util_debug.registrar_depuracion(f"Respuesta IA sin 'parts' válidas. Prompt Safety?: {respuesta.prompt_feedback}")
            return None

    except Exception as e:
        print(f"Error al interactuar con la API de Gemini: {e}")
        util_debug.registrar_depuracion(f"Excepción durante llamada a generate_content: {e}")
        return None