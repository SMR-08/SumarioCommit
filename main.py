# SumarioCommit - Punto de entrada principal
# -*- coding: utf-8 -*-

import sys
from dotenv import load_dotenv

# Importar componentes necesarios del paquete
from sumario_commit import cli 
from sumario_commit import util_debug

def ejecutar_aplicacion():
    """Función principal que inicia la aplicación CLI."""
    util_debug.registrar_depuracion("Inicio de la aplicación SumarioCommit.")

    # Llama a la función principal de la interfaz CLI
    cli.iniciar_cli() # <--- Cambiado: Llamar a iniciar_cli()

    util_debug.registrar_depuracion("Fin de la aplicación.")


if __name__ == "__main__":
    # Cargar variables de entorno desde .env al inicio
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