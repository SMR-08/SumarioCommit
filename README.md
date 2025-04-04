# SumarioCommit: Resúmenes de tu Día con IA desde Git

**SumarioCommit** es una herramienta de línea de comandos (CLI) creada para simplificar tus resumenes de trabajo diario en la empresa de las practicas. Funciona de la siguiente manera:

1.  Analiza los cambios (`diff`) del último commit (o uno específico que elijas) de tu repositorio Git local.
2.  Envía esos cambios a la IA de Google Gemini (modelo Flash por defecto).
3.  La IA extrae las **tareas realizadas** y los **aprendizajes clave** basándose *únicamente* en el código modificado y los mensajes de commit.
4.  Presenta este resumen en tu terminal y lo guarda automáticamente en un archivo Markdown (`.md`) fechado en la carpeta `resumenes_generados/` para tu registro.

El objetivo es que, al final del día, con solo hacer tu commit habitual, puedas ejecutar esta herramienta y obtener un resumen útil de lo que hiciste y aprendiste.

## Características

*   **Interfaz CLI sencilla:** Menú interactivo en la consola para todas las acciones.
*   **Resumen automático:** Genera resúmenes para el último commit o uno específico seleccionado de una lista.
*   **Análisis IA:** Utiliza Google Gemini para interpretar los cambios del código.
*   **Resultados claros:** Separa "Tareas Realizadas" y "Aprendizajes". Incluye resúmenes generales breves.
*   **Guardado persistente:** Almacena los resúmenes en archivos `.md` con fecha y hash.
*   **Configuración simple:** Solo necesitas tu API Key de Gemini y la ruta a tu repo. Recuerda la última ruta usada.
*   **Utilidades:** Permite ver la configuración, listar y consultar resúmenes anteriores.
*   **Modo Debug:** Opción para ver el funcionamiento interno si necesitas solucionar problemas.

## Requisitos Previos (Lo que necesitas tener)

1.  **Python:** Versión 3.8 o superior instalada. Puedes verificar ejecutando `python --version` en tu terminal. Si no lo tienes, descárgalo desde [python.org](https://www.python.org/).
2.  **Git:** La herramienta interactúa directamente con Git. Asegúrate de que esté instalado y funcione en tu terminal (prueba con `git --version`). Descárgalo desde [git-scm.com](https://git-scm.com/) si es necesario.
3.  **API Key de Google Gemini:** Necesitas una clave API para usar el modelo de IA. Puedes obtener una (generalmente con un nivel gratuito generoso) desde [Google AI Studio](https://aistudio.google.com/). Guárdala, la necesitarás en un momento.

## Puesta en Marcha (Cómo hacerlo funcionar)

Sigue estos pasos exactamente:

1.  **Obtén el Código:**
    *   Descarga todos los archivos de este proyecto y colócalos juntos en una carpeta en tu ordenador. Llamaremos a esta carpeta la "carpeta raíz" del proyecto (puedes llamarla `SumarioCommit` o como prefieras).

2.  **Instala las Dependencias:**
    *   Abre tu **terminal** o símbolo del sistema (como `cmd`, `PowerShell`, `bash`, etc.).
    *   **Navega** usando el comando `cd` hasta la carpeta raíz donde descargaste los archivos. Por ejemplo: `cd ruta/carpeta/SumarioCommit`.
    *   Ejecuta el siguiente comando para instalar las librerías que necesita el programa:
        ```bash
        pip install -r requirements.txt
        ```
        *Nota: Si tienes varias versiones de Python, podrías necesitar usar `pip3` en lugar de `pip`.*

3.  **Crea el Archivo de Configuración Esencial (`.env`):**
    *   Dentro de la **carpeta raíz** del proyecto (la misma donde ejecutaste `pip install`), crea un **nuevo archivo de texto** llamado exactamente:
        ```
        .env
        ```
        *(Puede no ser visible en algunos sistemas, habilita `ver archivos ocultos`)*.
    *   Abre este archivo `.env` con un editor de texto simple o IDE (como Notepad++, VS Code, Sublime Text, Nano, etc.).
    *   Pega la siguiente línea dentro del archivo, **reemplazando `"TU_API_KEY_AQUI"` con la clave API real que obtuviste de Google AI Studio**:
        ```dotenv
        GOOGLE_API_KEY="TU_API_KEY_AQUI"
        ```
    *   **(Opcional) Para Depuración:** Si quieres activar los mensajes de DEBUG para ver qué hace el programa por dentro (útil si algo falla), añade esta segunda línea al archivo `.env`:
        ```dotenv
        SUMARIOCOMMIT_DEBUG="1"
        ```
        *Si no la añades o pones `"0"`, los mensajes de DEBUG estarán desactivados.*
    *   **Guarda** el archivo `.env`. **¡Este archivo es crucial y contiene tu clave API!.** (El archivo `.gitignore` incluido en el proyecto está configurado para evitar que subas `.env` accidentalmente si usas Git para gestionar este propio proyecto, de nada).

## Ejecución

1.  Asegúrate de estar en tu **terminal**, dentro de la **carpeta raíz** del proyecto.
2.  Ejecuta el programa con el comando:
    ```bash
    python main.py
    ```
3.  ¡Listo! Verás el menú principal en la consola.
    *   **La primera vez que lo ejecutes**, como no sabe dónde está tu proyecto, deberás usar la opción **`3. Cambiar/Establecer Repositorio Git`**. Introduce la ruta completa a la carpeta de tu repositorio Git local (el proyecto del que quieres hacer resúmenes).
    *   Una vez configurado el repositorio, puedes usar la opción **`1`** para el último commit o la **`2`** para elegir uno específico.
    *   Navega por el resto de opciones usando los números indicados.
    *   Selecciona **`0`** para salir de la aplicación.

## Opciones del Menú (Resumen Rápido)

*   `1`: Resumen del último commit.
*   `2`: Elige un commit de una lista para resumir.
*   `3`: Indica o cambia la ruta a tu proyecto Git.
*   `4`: Muestra la ruta actual y si el debug está activo.
*   `5`: Lista los archivos `.md` de resúmenes ya guardados.
*   `6`: Muestra el contenido de un resumen guardado que elijas.
*   `7`: Ayuda básica sobre las opciones.
*   `0`: Salir.

## Modo Debug (Si algo va mal)

Si activaste `SUMARIOCOMMIT_DEBUG="1"` en tu archivo `.env`, verás mensajes adicionales en la consola que empiezan con `[DEBUG]`. Estos te darán pistas sobre qué comandos se ejecutan o dónde puede estar fallando algo.

## Licencia

(En proceso...)
