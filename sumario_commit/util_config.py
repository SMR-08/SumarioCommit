# -*- coding: utf-8 -*-
# Utilidades para la gestión de la configuración

import json
import os
from sumario_commit import constantes
from sumario_commit import util_debug

def obtener_ruta_config() -> str:
    """Devuelve la ruta completa al archivo de configuración."""
    # Se asume que config.json está al mismo nivel que main.py
    directorio_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(directorio_base, constantes.NOMBRE_ARCHIVO_CONFIG)

def cargar_configuracion() -> dict:
    """Carga la configuración desde el archivo JSON."""
    ruta_archivo = obtener_ruta_config()
    util_debug.registrar_depuracion(f"Intentando cargar configuración desde: {ruta_archivo}")
    config = {constantes.CLAVE_ULTIMA_RUTA: None} # Valores por defecto

    if os.path.exists(ruta_archivo):
        try:
            with open(ruta_archivo, 'r', encoding=constantes.CODIFICACION_ARCHIVOS) as f:
                config_cargada = json.load(f)
                # Asegura que las claves esperadas existan
                config.update(config_cargada)
                util_debug.registrar_depuracion("Configuración cargada exitosamente.")
        except json.JSONDecodeError:
            print(f"Advertencia: Archivo de configuración '{ruta_archivo}' corrupto. Se usarán valores por defecto.")
            util_debug.registrar_depuracion("Error al decodificar JSON de configuración.")
        except Exception as e:
            print(f"Error inesperado al leer configuración: {e}")
            util_debug.registrar_depuracion(f"Excepción al leer config: {e}")
    else:
        util_debug.registrar_depuracion("Archivo de configuración no encontrado. Creando con valores por defecto.")
        guardar_configuracion(config) # Crea el archivo si no existe

    return config

def guardar_configuracion(config: dict):
    """Guarda la configuración en el archivo JSON."""
    ruta_archivo = obtener_ruta_config()
    util_debug.registrar_depuracion(f"Guardando configuración en: {ruta_archivo}")
    try:
        with open(ruta_archivo, 'w', encoding=constantes.CODIFICACION_ARCHIVOS) as f:
            json.dump(config, f, indent=4)
        util_debug.registrar_depuracion("Configuración guardada exitosamente.")
    except Exception as e:
        print(f"Error al guardar la configuración: {e}")
        util_debug.registrar_depuracion(f"Excepción al guardar config: {e}")

def obtener_api_key() -> str | None:
    """Obtiene la API Key de Google desde las variables de entorno."""
    api_key = os.getenv(constantes.VAR_ENTORNO_API_KEY)
    if not api_key:
        util_debug.registrar_depuracion("API Key no encontrada en variables de entorno.")
        print(f"Error: La variable de entorno '{constantes.VAR_ENTORNO_API_KEY}' no está configurada.")
        print("Asegúrate de tener un archivo .env con la clave o de haberla exportado.")
    else:
        util_debug.registrar_depuracion("API Key encontrada en variables de entorno.")
    return api_key