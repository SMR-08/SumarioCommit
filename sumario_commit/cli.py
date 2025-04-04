# -*- coding: utf-8 -*-
# Interfaz de Línea de Comandos (CLI) para SumarioCommit

import os
import sys
import subprocess
from . import nucleo, util_config, util_git, util_debug, constantes,util_ia

def _limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    # Para Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Para macOS y Linux
    else:
        _ = os.system('clear')

def _pausar_pantalla():
    """Pausa la ejecución hasta que el usuario presione Enter."""
    input("\nPresiona Enter para continuar...")

def _mostrar_menu(config: dict):
    """Muestra el menú principal de opciones."""
    _limpiar_pantalla()
    print("-------------------------------------")
    print("        SumarioCommit CLI")
    print("-------------------------------------")
    ruta_actual = config.get(constantes.CLAVE_ULTIMA_RUTA)
    if not ruta_actual or not os.path.exists(ruta_actual):
        ruta_display = "Ninguno seleccionado"
    else:
        ruta_display = ruta_actual
    print(f"Repositorio Actual: {ruta_display}")
    print("-------------------------------------")
    print("\nSelecciona una opción:\n")
    print(" 1. Generar Resumen (Último Commit)")
    print(" 2. Generar Resumen (Commit Específico)")
    print(" 3. Cambiar/Establecer Repositorio Git")
    print(" 4. Ver Configuración Actual")
    print(" 5. Listar Resúmenes Guardados")
    print(" 6. Ver un Resumen Guardado")
    print(" 7. Ayuda")
    print(" 0. Salir")
    print("-" * 37) # Separador visual

def _manejar_opcion_1_ultimo_commit(config: dict):
    """Maneja la opción de generar resumen para el último commit."""
    print("\n--- Generar Resumen (Último Commit) ---")
    ruta_repo = config.get(constantes.CLAVE_ULTIMA_RUTA)
    if not ruta_repo or not util_git.es_repositorio_git(ruta_repo):
        print("Error: No hay un repositorio Git válido configurado.")
        print("Por favor, usa la opción 3 para establecer uno.")
        return

    # Llama a la función refactorizada en nucleo
    nucleo.generar_resumen_ultimo_commit(ruta_repo)

def _manejar_opcion_2_commit_especifico(config: dict):
    """Maneja la opción de generar resumen para un commit específico."""
    print("\n--- Generar Resumen (Commit Específico) ---")
    ruta_repo = config.get(constantes.CLAVE_ULTIMA_RUTA)

    if not ruta_repo or not util_git.es_repositorio_git(ruta_repo):
        print("\nError: No hay un repositorio Git válido configurado.")
        print("Por favor, usa la opción 3 para establecer uno.")
        return

    util_debug.registrar_depuracion(f"Buscando commits en: {ruta_repo}")
    commits = util_git.obtener_lista_commits(ruta_repo, limite=30)

    if not commits:
        print(f"\nNo se encontraron commits en el repositorio '{ruta_repo}' o hubo un error.")
        return

    while True:
        _limpiar_pantalla()
        print("-------------------------------------")
        print("   Selecciona un Commit para Resumir")
        print("-------------------------------------")
        print(f"Repositorio: {ruta_repo}")
        print("-------------------------------------")

        for i, commit in enumerate(commits):
            # Formato: Mensaje (primera línea), Fecha, Hash corto
            print(f" {i+1:>2}. {commit['mensaje'][:70]} ({commit['fecha']}) [{commit['hash']}]") # Limita el mensaje a 70 caracteres

        print("-" * 37)
        print("  0. Volver al Menú Principal")
        print("-" * 37)

        try:
            eleccion = input("Tu elección: ").strip()
            if not eleccion: continue # Si no escribe nada, vuelve a mostrar
            indice = int(eleccion)

            if indice == 0:
                util_debug.registrar_depuracion("Usuario seleccionó volver al menú principal.")
                break # Sale del bucle de selección de commit

            if 1 <= indice <= len(commits):
                commit_seleccionado = commits[indice - 1]
                hash_commit = commit_seleccionado['hash_completo'] # Usar hash completo para git format-patch
                fecha_commit = commit_seleccionado['fecha']
                util_debug.registrar_depuracion(f"Usuario seleccionó commit: {hash_commit} ({fecha_commit})")

                print(f"\nGenerando resumen para el commit: {commit_seleccionado['mensaje'][:50]}...")
                # Llama a la función refactorizada en nucleo
                nucleo.ejecutar_resumen_para_commit(ruta_repo, hash_commit, fecha_commit)
                _pausar_pantalla() # Pausa después de generar/mostrar el resumen
                # Podríamos preguntar si quiere seleccionar otro o volver directamente
                break # Vuelve al menú principal después de una selección

            else:
                print("\nOpción inválida. Introduce un número de la lista.")
                _pausar_pantalla()

        except ValueError:
            print("\nEntrada inválida. Introduce un número.")
            _pausar_pantalla()
        except KeyboardInterrupt:
             print("\nOperación cancelada por el usuario.")
             break # Salir del bucle interno


def _manejar_opcion_3_cambiar_repo(config: dict):
    """Maneja la opción de cambiar el repositorio."""
    print("\n--- Cambiar/Establecer Repositorio Git ---")
    # La función seleccionar_ruta_repositorio ya hace todo (pide, valida, guarda)
    nueva_ruta = nucleo.seleccionar_ruta_repositorio(config, pedir_si_no_existe=True)
    if nueva_ruta:
        print(f"\nRepositorio establecido en: {nueva_ruta}")
    else:
        # El mensaje de error ya se muestra dentro de seleccionar_ruta_repositorio
        print("\nNo se pudo establecer un nuevo repositorio.")


def _manejar_opcion_4_ver_config(config: dict):
    """Muestra la configuración actual."""
    print("\n--- Configuración Actual ---")
    ruta_actual = config.get(constantes.CLAVE_ULTIMA_RUTA, "Ninguno")
    debug_activo = os.getenv(constantes.VAR_ENTORNO_DEBUG, "0") == "1"
    directorio_base_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_resumenes = os.path.join(directorio_base_app, "resumenes_generados")

    print(f"Ruta del Repositorio: {ruta_actual}")
    print(f"Modo Debug Activo: {'Sí' if debug_activo else 'No'}")
    print(f"Carpeta de Resúmenes: {ruta_resumenes}")

def _manejar_opcion_5_listar_resumenes():
    """Lista los archivos de resumen guardados."""
    print("\n--- Resúmenes Guardados ---")
    directorio_base_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_carpeta_resumenes = os.path.join(directorio_base_app, "resumenes_generados")
    util_debug.registrar_depuracion(f"Buscando resúmenes en: {ruta_carpeta_resumenes}")

    if not os.path.isdir(ruta_carpeta_resumenes):
        print("La carpeta de resúmenes 'resumenes_generados' no existe aún.")
        return

    archivos_resumen = []
    try:
        for nombre_archivo in os.listdir(ruta_carpeta_resumenes):
            if nombre_archivo.startswith(constantes.PREFIJO_ARCHIVO_RESUMEN) and \
               nombre_archivo.endswith(constantes.EXTENSION_ARCHIVO_RESUMEN):
                archivos_resumen.append(nombre_archivo)
    except OSError as e:
        print(f"Error al leer la carpeta de resúmenes: {e}")
        util_debug.registrar_depuracion(f"Error OSError al listar resúmenes: {e}")
        return

    if not archivos_resumen:
        print("No se encontraron resúmenes guardados.")
    else:
        print("Archivos encontrados:")
        # Ordenar por nombre (fecha)
        archivos_resumen.sort(reverse=True)
        for nombre in archivos_resumen:
            print(f"- {nombre}")

def _manejar_opcion_6_ver_resumen():
    """Muestra el contenido de un archivo de resumen específico."""
    print("\n--- Ver un Resumen Guardado ---")
    directorio_base_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_carpeta_resumenes = os.path.join(directorio_base_app, "resumenes_generados")

    if not os.path.isdir(ruta_carpeta_resumenes):
        print("La carpeta de resúmenes 'resumenes_generados' no existe aún.")
        return

    archivos_resumen = []
    try:
        for nombre_archivo in os.listdir(ruta_carpeta_resumenes):
             if nombre_archivo.startswith(constantes.PREFIJO_ARCHIVO_RESUMEN) and \
                nombre_archivo.endswith(constantes.EXTENSION_ARCHIVO_RESUMEN):
                 archivos_resumen.append(nombre_archivo)
    except OSError as e:
        print(f"Error al leer la carpeta de resúmenes: {e}")
        return

    if not archivos_resumen:
        print("No se encontraron resúmenes guardados para mostrar.")
        return

    archivos_resumen.sort(reverse=True) # Ordenar para mostrar los más recientes primero

    print("Resúmenes disponibles:")
    for i, nombre in enumerate(archivos_resumen):
        print(f" {i+1:>2}. {nombre}")
    print("-" * 37)
    print("  0. Volver al Menú Principal")
    print("-" * 37)

    while True:
        try:
            eleccion_str = input("Elige el número del resumen a ver (0 para volver): ").strip()
            if not eleccion_str: continue
            eleccion_num = int(eleccion_str)

            if eleccion_num == 0:
                break
            if 1 <= eleccion_num <= len(archivos_resumen):
                archivo_seleccionado = archivos_resumen[eleccion_num - 1]
                ruta_completa = os.path.join(ruta_carpeta_resumenes, archivo_seleccionado)
                util_debug.registrar_depuracion(f"Mostrando archivo: {ruta_completa}")
                _limpiar_pantalla()
                print(f"--- Mostrando: {archivo_seleccionado} ---")
                try:
                    with open(ruta_completa, 'r', encoding=constantes.CODIFICACION_ARCHIVOS) as f:
                        print(f.read())
                    print("-" * (len(archivo_seleccionado) + 16)) # Separador final
                    break # Salir después de mostrar
                except Exception as e:
                    print(f"\nError al leer el archivo '{archivo_seleccionado}': {e}")
                    util_debug.registrar_depuracion(f"Error leyendo archivo resumen {archivo_seleccionado}: {e}")
                    # Permite intentar de nuevo
            else:
                print("Número fuera de rango.")

        except ValueError:
            print("Entrada inválida. Introduce un número.")
        except KeyboardInterrupt:
            print("\nOperación cancelada.")
            break


def _manejar_opcion_7_ayuda():
    """Muestra un texto de ayuda."""
    print("\n--- Ayuda de SumarioCommit ---")
    print("Esta aplicación genera resúmenes de trabajo basados en commits de Git.")
    print("\nOpciones del menú:")
    print(" 1. Generar Resumen (Último Commit): Analiza el commit más reciente del repositorio configurado.")
    print(" 2. Generar Resumen (Commit Específico): Lista los últimos commits y permite elegir uno para analizar.")
    print(" 3. Cambiar/Establecer Repositorio Git: Permite seleccionar la carpeta raíz de tu proyecto Git.")
    print(" 4. Ver Configuración Actual: Muestra la ruta del repositorio en uso y otros detalles.")
    print(" 5. Listar Resúmenes Guardados: Muestra los nombres de los archivos de resumen generados previamente.")
    print(" 6. Ver un Resumen Guardado: Permite elegir un resumen de la lista y ver su contenido.")
    print(" 7. Ayuda: Muestra esta pantalla de ayuda.")
    print(" 0. Salir: Cierra la aplicación.")
    print("\nNota: Necesitas tener Git instalado y una API Key de Gemini configurada en el archivo .env.")


# --- Bucle Principal de la CLI ---

def iniciar_cli():
    """Inicia el bucle principal de la interfaz de línea de comandos."""
    config = nucleo.cargar_configuracion_inicial()
    if not config:
        print("Error crítico al cargar la configuración inicial. Saliendo.")
        sys.exit(1)

    # Verifica si la IA está configurada al inicio (ya se hace en cargar_configuracion_inicial)
    if not util_config.obtener_api_key() or util_ia.modelo_ia is None:
         print("\nAdvertencia: La API Key de Gemini no está configurada o no es válida.")
         print("Algunas funciones (generar resumen) no funcionarán.")
         print("Asegúrate de tener la variable GOOGLE_API_KEY en tu archivo .env")
         _pausar_pantalla() # Pausa para que el usuario vea el mensaje

    while True:
        _mostrar_menu(config)
        opcion = input("Tu elección: ").strip()

        try:
            if opcion == '1':
                _manejar_opcion_1_ultimo_commit(config)
                _pausar_pantalla()
            elif opcion == '2':
                # La pausa ya está dentro de esta función si se genera resumen
                _manejar_opcion_2_commit_especifico(config)
                # No pausar aquí, la pausa está dentro o el usuario vuelve directamente
            elif opcion == '3':
                _manejar_opcion_3_cambiar_repo(config)
                _pausar_pantalla()
            elif opcion == '4':
                _manejar_opcion_4_ver_config(config)
                _pausar_pantalla()
            elif opcion == '5':
                _manejar_opcion_5_listar_resumenes()
                _pausar_pantalla()
            elif opcion == '6':
                # La pausa ya está controlada dentro de la función
                 _manejar_opcion_6_ver_resumen()
                 _pausar_pantalla() # Pausar al volver al menú
            elif opcion == '7':
                _manejar_opcion_7_ayuda()
                _pausar_pantalla()
            elif opcion == '0':
                util_debug.registrar_depuracion("Usuario seleccionó salir.")
                print("\n¡Hasta luego!")
                break # Sale del bucle while
            else:
                print("\nOpción no válida. Inténtalo de nuevo.")
                _pausar_pantalla()

        except KeyboardInterrupt:
             print("\n\nOperación interrumpida por el usuario. Saliendo.")
             break # Salir del bucle principal
        except Exception as e:
            print(f"\nError inesperado en el menú principal: {e}")
            util_debug.registrar_depuracion(f"Excepción no controlada en el bucle CLI: {e}")
            _pausar_pantalla()