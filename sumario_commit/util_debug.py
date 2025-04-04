# -*- coding: utf-8 -*-
# Utilidades para el registro de depuración (modo debug)

import os
from sumario_commit import constantes

# Variable global para controlar el estado del modo debug
MODO_DEBUG_ACTIVO = False

def configurar_depuracion():
    """Lee la variable de entorno para activar/desactivar el modo debug."""
    global MODO_DEBUG_ACTIVO
    valor_debug = os.getenv(constantes.VAR_ENTORNO_DEBUG, "0")
    MODO_DEBUG_ACTIVO = (valor_debug == "1")
    if MODO_DEBUG_ACTIVO:
        print("[DEBUG] Modo de depuración ACTIVADO.")

def registrar_depuracion(mensaje: str):
    """Imprime un mensaje solo si el modo debug está activo."""
    if MODO_DEBUG_ACTIVO:
        print(f"[DEBUG] {mensaje}")