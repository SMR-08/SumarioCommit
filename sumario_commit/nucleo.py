
# -*- coding: utf-8 -*-
# Lógica principal y orquestación de SumarioCommit

import os
from . import util_config, util_git, util_ia, constantes, util_debug 

def ejecutar_resumen_para_commit(ruta_repo: str, hash_commit: str, fecha_commit: str) -> bool:
    """
    Genera, muestra y guarda el resumen para un HASH de commit específico.

    Args:
        ruta_repo: Ruta al repositorio Git.
        hash_commit: Hash completo del commit a procesar.
        fecha_commit: Fecha del commit (YYYY-MM-DD) para nombrar el archivo.

    Returns:
        True si el resumen se generó y guardó (o se mostró) correctamente, False en caso contrario.
    """
    util_debug.registrar_depuracion(f"Ejecutando resumen para commit: {hash_commit} ({fecha_commit}) en {ruta_repo}")

    patch = util_git.generar_patch_commit(ruta_repo, hash_commit) # Usa la función renombrada/adaptada
    if not patch:
        print("Error: No se pudo generar el patch del commit.")
        util_debug.registrar_depuracion(f"Fallo al generar patch para {hash_commit}")
        return False

    # Verificar si la IA está lista (por si falló al inicio o se necesita reconfigurar)
    if util_ia.modelo_ia is None:
         if not util_ia.configurar_ia():
              print("Error: Fallo al configurar la IA. No se puede generar el resumen.")
              util_debug.registrar_depuracion("Fallo configuración IA antes de generar resumen.")
              return False

    print("Generando resumen con IA... (puede tardar unos segundos)")
    resumen_ia = util_ia.generar_resumen_con_ia(patch)

    if resumen_ia:
        print("\n--- Resumen Generado ---")
        print(resumen_ia)
        print("------------------------\n")
        guardar_resumen(fecha_commit, resumen_ia, ruta_repo) # Usa la fecha proporcionada
        return True
    else:
        print("Error: No se pudo generar el resumen usando la IA.")
        util_debug.registrar_depuracion(f"Fallo al obtener resumen de IA para {hash_commit}")
        return False

def generar_resumen_ultimo_commit(ruta_repo: str):
    """Obtiene el último commit y llama a la función de generación de resumen."""
    util_debug.registrar_depuracion("Iniciando flujo para obtener y resumir último commit.")

    hash_commit, fecha_commit = util_git.obtener_ultimo_commit_info(ruta_repo)
    if not hash_commit or not fecha_commit:
        print("Error: No se pudo obtener la información del último commit.")
        util_debug.registrar_depuracion("Fallo al obtener info del último commit.")
        return

    util_debug.registrar_depuracion(f"Último commit encontrado: {hash_commit} ({fecha_commit})")
    # Llama a la función genérica con los datos del último commit
    ejecutar_resumen_para_commit(ruta_repo, hash_commit, fecha_commit)

def cargar_configuracion_inicial() -> dict | None:
    """Carga la configuración y verifica la API key al inicio."""
    util_debug.registrar_depuracion("Iniciando carga de configuración inicial.")
    config = util_config.cargar_configuracion()
    # Intenta configurar la IA para verificar la API key temprano
    if not util_ia.configurar_ia():
        # Ya se imprime advertencia dentro de configurar_ia si falla
        util_debug.registrar_depuracion("Configuración inicial de IA fallida o API Key ausente.")
        # No es fatal, la app puede continuar para otras opciones
    return config

def guardar_resumen(fecha_commit: str, contenido_resumen: str, ruta_base_repo: str) -> bool:
    """Guarda el resumen generado en un archivo."""
    nombre_archivo = f"{constantes.PREFIJO_ARCHIVO_RESUMEN}{fecha_commit}_{util_git.obtener_hash_corto(ruta_base_repo, 'HEAD')}.{constantes.EXTENSION_ARCHIVO_RESUMEN}" # Añadir hash corto para diferenciar commits del mismo día

    # Guardar en una subcarpeta 'resumenes_generados' dentro del directorio de la app
    directorio_base_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_carpeta_resumenes = os.path.join(directorio_base_app, "resumenes_generados")
    ruta_completa_archivo = os.path.join(ruta_carpeta_resumenes, nombre_archivo)

    util_debug.registrar_depuracion(f"Intentando guardar resumen en: {ruta_completa_archivo}")

    try:
        # Crear la carpeta si no existe
        os.makedirs(ruta_carpeta_resumenes, exist_ok=True)

        # Escribir el contenido en el archivo
        encabezado = f"# Resumen del Commit ({fecha_commit} - {util_git.obtener_hash_corto(ruta_base_repo, 'HEAD')})\n\n" # Encabezado más informativo
        with open(ruta_completa_archivo, 'w', encoding=constantes.CODIFICACION_ARCHIVOS) as f:
            f.write(encabezado)
            f.write(contenido_resumen)

        print(f"Resumen guardado exitosamente en: {ruta_completa_archivo}")
        util_debug.registrar_depuracion("Archivo de resumen guardado.")
        return True
    except OSError as e:
        print(f"Error al crear el directorio o archivo de resumen: {e}")
        util_debug.registrar_depuracion(f"Error de OS al guardar resumen: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado al guardar el resumen: {e}")
        util_debug.registrar_depuracion(f"Excepción inesperada al guardar resumen: {e}")
        return False
    
def seleccionar_ruta_repositorio(config_actual: dict, pedir_si_no_existe=False) -> str | None:
    """
    Obtiene una ruta de repositorio válida, ya sea la guardada o pidiéndola al usuario.

    Args:
        config_actual: El diccionario de configuración actual.
        pedir_si_no_existe: Si es True, siempre pedirá la ruta si no hay una válida guardada.
                            Si es False, solo devuelve la guardada si es válida, si no, None.

    Returns:
        La ruta del repositorio válida o None si no se pudo obtener.
    """
    ruta_guardada = config_actual.get(constantes.CLAVE_ULTIMA_RUTA)
    util_debug.registrar_depuracion(f"Ruta guardada en config: {ruta_guardada}")

    if ruta_guardada and os.path.isdir(ruta_guardada) and util_git.es_repositorio_git(ruta_guardada):
        util_debug.registrar_depuracion(f"Usando ruta guardada válida: {ruta_guardada}")
        return ruta_guardada
    elif not pedir_si_no_existe:
        # Si no se debe pedir y la guardada no es válida, devuelve None
        util_debug.registrar_depuracion("Ruta guardada no válida y no se pide nueva.")
        return None
    else:
        # La ruta guardada no es válida o no existe, y se debe pedir una nueva
        if ruta_guardada:
            print(f"La ruta guardada ('{ruta_guardada}') ya no es válida o no es un repo Git.")
        else:
            print("No hay una ruta de repositorio configurada.")

        print("\nIntroduce la ruta completa a tu repositorio Git local:")
        while True:
            try:
                ruta_introducida = input("> ").strip()
                if not ruta_introducida: # Permitir cancelar si no escribe nada? Por ahora no.
                    continue
                util_debug.registrar_depuracion(f"Usuario introdujo ruta: {ruta_introducida}")

                if os.path.isdir(ruta_introducida):
                    if util_git.es_repositorio_git(ruta_introducida):
                        # Guardar la nueva ruta válida
                        config_actual[constantes.CLAVE_ULTIMA_RUTA] = ruta_introducida
                        util_config.guardar_configuracion(config_actual)
                        util_debug.registrar_depuracion(f"Nueva ruta válida seleccionada y guardada: {ruta_introducida}")
                        return ruta_introducida
                    else:
                        print("   Error: La ruta es un directorio, pero no parece ser un repositorio Git.")
                        util_debug.registrar_depuracion(f"Ruta introducida no es repo Git: {ruta_introducida}")
                else:
                    print("   Error: La ruta introducida no es un directorio válido.")
                    util_debug.registrar_depuracion(f"Ruta introducida no es directorio: {ruta_introducida}")
                print("   Inténtalo de nuevo o presiona Ctrl+C para cancelar.")

            except KeyboardInterrupt:
                print("\nOperación cancelada por el usuario.")
                return None # Indicar que no se seleccionó ruta

# Se podría añadir aquí lógica para interfaz gráfica si se usa interfaz.py