# SumarioCommit - Punto de entrada principal
# -*- coding: utf-8 -*-

import os
import sys
from dotenv import load_dotenv

# Importar componentes necesarios del paquete
# Usar imports relativos si main.py estuviera dentro de un paquete,
# pero como es el script principal, usamos imports normales.
from sumario_commit import cli
from sumario_commit import util_debug
from sumario_commit import constantes # Necesario para constantes.CODIFICACION_ARCHIVOS, etc

# --- NUEVA FUNCIÓN ---
def verificar_y_crear_env_si_no_existe():
    """
    Verifica si el archivo .env existe en la carpeta actual.
    Si no existe, lo crea con contenido predeterminado y avisa al usuario.
    """
    nombre_archivo_env = ".env"
    if not os.path.exists(nombre_archivo_env):
        print(f"Advertencia: El archivo de configuración '{nombre_archivo_env}' no existe.")
        print(f"Creando '{nombre_archivo_env}' con valores predeterminados...")
        contenido_predeterminado = f"""# Por favor, reemplaza "TU_API_KEY_AQUI" con tu clave API real de Google Gemini.
# Obtén una clave en https://aistudio.google.com/
{constantes.VAR_ENTORNO_API_KEY}="TU_API_KEY_AQUI"

# Opcional: Cambia a "1" para activar los mensajes de depuración detallados.
{constantes.VAR_ENTORNO_DEBUG}="0"
"""
        try:
            with open(nombre_archivo_env, 'w', encoding=constantes.CODIFICACION_ARCHIVOS) as f:
                f.write(contenido_predeterminado)
            print(f"Archivo '{nombre_archivo_env}' creado exitosamente.")
            print("\n¡ACCIÓN REQUERIDA! Debes editar este archivo '.env' ahora:")
            print(f"  1. Abre el archivo '{nombre_archivo_env}' con un editor de texto.")
            print(f"  2. Reemplaza 'TU_API_KEY_AQUI' en la línea '{constantes.VAR_ENTORNO_API_KEY}=' con tu clave API real.")
            print("  3. Guarda los cambios en el archivo.")
            print("\nLa aplicación necesita esta clave para generar los resúmenes.")
            # Pausar para dar tiempo a editar o al menos leer el mensaje crítico
            input("Presiona Enter para continuar (después de editar '.env' si es posible)... ")
        except IOError as e:
            print(f"\nError Crítico: No se pudo crear el archivo '{nombre_archivo_env}': {e}")
            print("Por favor, crea el archivo '.env' manualmente en esta carpeta con el contenido:")
            print(f'{constantes.VAR_ENTORNO_API_KEY}="TU_API_KEY_AQUI"')
            print(f'{constantes.VAR_ENTORNO_DEBUG}="0"')
            print("\nY reemplaza TU_API_KEY_AQUI con tu clave real.")
            sys.exit(1) # Salir si no se puede crear el archivo esencial

# --- FIN NUEVA FUNCIÓN ---


def ejecutar_aplicacion():
    """Función principal que inicia la aplicación CLI."""
    util_debug.registrar_depuracion("Inicio de la aplicación SumarioCommit.")

    # Llama a la función principal de la interfaz CLI
    cli.iniciar_cli()

    util_debug.registrar_depuracion("Fin de la aplicación.")


if __name__ == "__main__":
    # --- LLAMADA A LA NUEVA FUNCIÓN ---
    # Se ejecuta ANTES de intentar cargar las variables
    verificar_y_crear_env_si_no_existe()
    # --- FIN LLAMADA ---

    # Cargar variables de entorno desde .env al inicio
    # load_dotenv buscará el archivo .env (que ahora sabemos que existe)
    load_dotenv()
    util_debug.configurar_depuracion() # Leer variable de entorno SUMARIOCOMMIT_DEBUG

    try:
        ejecutar_aplicacion()
    except KeyboardInterrupt:
        # Captura Ctrl+C globalmente si no se hizo en el bucle CLI
        print("\n\nSalida forzada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError fatal no recuperado: {e}")
        util_debug.registrar_depuracion(f"Excepción fatal en __main__: {e}")
        sys.exit(1)