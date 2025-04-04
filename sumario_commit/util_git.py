# -*- coding: utf-8 -*-
# Utilidades para interactuar con el repositorio Git

import subprocess
import os
from . import util_debug # Usar imports relativos

def es_repositorio_git(ruta_carpeta: str) -> bool:
    """Verifica si una ruta corresponde a un repositorio Git válido."""
    if not os.path.isdir(ruta_carpeta):
        return False
    comando = ["git", "-C", ruta_carpeta, "rev-parse", "--is-inside-work-tree"]
    util_debug.registrar_depuracion(f"Ejecutando: {' '.join(comando)}")
    try:
        # Usar startupinfo en Windows para evitar ventana de consola fantasma
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        resultado = subprocess.run(comando, capture_output=True, text=True, check=True, encoding='utf-8', startupinfo=startupinfo)
        es_repo = resultado.stdout.strip() == "true"
        util_debug.registrar_depuracion(f"Resultado es_repositorio_git: {es_repo}")
        return es_repo
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        util_debug.registrar_depuracion(f"Error al verificar si es repo Git: {e}")
        # No imprimir error aquí, la función que llama debe decidir
        return False
    except Exception as e: # Captura genérica por si acaso
        util_debug.registrar_depuracion(f"Excepción inesperada verificando repo: {e}")
        return False

def obtener_ultimo_commit_info(ruta_repo: str) -> tuple[str | None, str | None]:
    """Obtiene el hash COMPLETO y la fecha (YYYY-MM-DD) del último commit."""
    # No necesita verificar si es repo, se asume que quien llama lo hizo
    comando_hash = ["git", "-C", ruta_repo, "rev-parse", "HEAD"]
    # Obtener fecha del autor para consistencia
    comando_fecha = ["git", "-C", ruta_repo, "log", "-1", "--pretty=format:%ad", "--date=format:%Y-%m-%d"]

    try:
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        util_debug.registrar_depuracion(f"Ejecutando: {' '.join(comando_hash)}")
        hash_commit = subprocess.run(comando_hash, capture_output=True, text=True, check=True, encoding='utf-8', startupinfo=startupinfo).stdout.strip()

        util_debug.registrar_depuracion(f"Ejecutando: {' '.join(comando_fecha)}")
        fecha_commit = subprocess.run(comando_fecha, capture_output=True, text=True, check=True, encoding='utf-8', startupinfo=startupinfo).stdout.strip()

        util_debug.registrar_depuracion(f"Último commit: Hash={hash_commit}, Fecha={fecha_commit}")
        return hash_commit, fecha_commit
    except subprocess.CalledProcessError as e:
        print(f"Error al obtener información del último commit: {e.stderr or e}")
        util_debug.registrar_depuracion(f"Error en subprocess al obtener commit info: {e}")
        return None, None
    except FileNotFoundError:
         print("Error: Comando 'git' no encontrado. Asegúrate de que Git esté instalado y en el PATH.")
         util_debug.registrar_depuracion("Comando git no encontrado.")
         return None, None
    except Exception as e:
        util_debug.registrar_depuracion(f"Excepción inesperada obteniendo info commit: {e}")
        return None, None

# --- Nueva Función ---
def obtener_lista_commits(ruta_repo: str, limite: int = 30) -> list[dict] | None:
    """Obtiene una lista de los últimos N commits con hash, fecha y mensaje."""
    # Formato: hash_corto | hash_completo | fecha_autor (YYYY-MM-DD) | mensaje (asunto)
    formato = "%h|%H|%ad|%s"
    comando = [
        "git", "-C", ruta_repo, "log",
        f"--pretty=format:{formato}",
        "--date=format:%Y-%m-%d",
        f"--max-count={limite}"
    ]
    util_debug.registrar_depuracion(f"Ejecutando: {' '.join(comando)}")

    try:
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        resultado = subprocess.run(comando, capture_output=True, text=True, check=True, encoding='utf-8', startupinfo=startupinfo)
        lineas = resultado.stdout.strip().split('\n')

        commits = []
        for linea in lineas:
            if not linea: continue
            partes = linea.split('|', 3) # Divide máximo 3 veces por |
            if len(partes) == 4:
                commits.append({
                    'hash': partes[0],
                    'hash_completo': partes[1],
                    'fecha': partes[2],
                    'mensaje': partes[3]
                })
            else:
                util_debug.registrar_depuracion(f"Línea de log mal formada omitida: {linea}")


        util_debug.registrar_depuracion(f"Obtenidos {len(commits)} commits.")
        return commits

    except subprocess.CalledProcessError as e:
        print(f"Error al obtener la lista de commits: {e.stderr or e}")
        util_debug.registrar_depuracion(f"Error en subprocess al obtener log: {e}")
        return None
    except FileNotFoundError:
         print("Error: Comando 'git' no encontrado.")
         util_debug.registrar_depuracion("Comando git no encontrado al obtener log.")
         return None
    except Exception as e:
        util_debug.registrar_depuracion(f"Excepción inesperada obteniendo log: {e}")
        return None


# --- Función Renombrada/Adaptada ---
def generar_patch_commit(ruta_repo: str, hash_commit: str) -> str | None:
    """Genera el patch (diff) del commit especificado usando format-patch."""
    # No necesita verificar si es repo, se asume que quien llama lo hizo
    # -1 indica que queremos el patch relativo al commit anterior a hash_commit
    comando = ["git", "-C", ruta_repo, "format-patch", "-1", hash_commit, "--stdout"]
    util_debug.registrar_depuracion(f"Ejecutando: {' '.join(comando)}")
    try:
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        resultado = subprocess.run(comando, capture_output=True, text=True, check=True, encoding='utf-8', startupinfo=startupinfo)
        patch = resultado.stdout
        util_debug.registrar_depuracion("Patch generado exitosamente (primeros 100 chars):\n" + patch[:100])
        return patch
    except subprocess.CalledProcessError as e:
        # A menudo, el error es que no hay commit anterior (el primer commit)
        if "bad revision" in (e.stderr or ""):
             print(f"Advertencia: No se pudo generar patch para el commit {hash_commit[:7]}. ¿Es el primer commit del repositorio?")
             util_debug.registrar_depuracion(f"Error 'bad revision' generando patch para {hash_commit}. Probablemente primer commit.")
             # Podríamos intentar 'git show HASH' como alternativa para el primer commit
             return _generar_diff_show(ruta_repo, hash_commit) # Intentar con git show
        else:
            print(f"Error al generar el patch del commit {hash_commit[:7]}: {e.stderr or e}")
            util_debug.registrar_depuracion(f"Error en subprocess al generar patch: {e}")
        return None
    except FileNotFoundError:
         print("Error: Comando 'git' no encontrado.")
         util_debug.registrar_depuracion("Comando git no encontrado al generar patch.")
         return None
    except Exception as e:
        util_debug.registrar_depuracion(f"Excepción inesperada generando patch: {e}")
        return None

# --- Nueva Función Auxiliar para el primer commit ---
def _generar_diff_show(ruta_repo: str, hash_commit: str) -> str | None:
    """Intenta generar un diff usando 'git show' (útil para el primer commit)."""
    comando = ["git", "-C", ruta_repo, "show", hash_commit]
    util_debug.registrar_depuracion(f"Intentando generar diff con 'git show': {' '.join(comando)}")
    try:
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE

        resultado = subprocess.run(comando, capture_output=True, text=True, check=True, encoding='utf-8', startupinfo=startupinfo)
        diff_show = resultado.stdout
        # Añadir una cabecera similar a format-patch si es posible? Por ahora devolvemos directo.
        util_debug.registrar_depuracion("'git show' exitoso como alternativa a format-patch.")
        # El formato es diferente, pero Gemini podría manejarlo.
        return diff_show
    except Exception as e:
        print(f"Error también al intentar 'git show' para {hash_commit[:7]}: {e}")
        util_debug.registrar_depuracion(f"Fallo de 'git show' para {hash_commit}: {e}")
        return None

# --- Nueva función auxiliar para obtener hash corto ---
def obtener_hash_corto(ruta_repo: str, ref: str = "HEAD") -> str:
    """Obtiene el hash corto de una referencia (por defecto, HEAD)."""
    comando = ["git", "-C", ruta_repo, "rev-parse", "--short", ref]
    try:
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        resultado = subprocess.run(comando, capture_output=True, text=True, check=True, encoding='utf-8', startupinfo=startupinfo)
        return resultado.stdout.strip()
    except Exception:
        return "errorhash" # Retorna un placeholder si falla