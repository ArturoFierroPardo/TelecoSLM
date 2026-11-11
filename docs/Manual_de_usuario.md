[English](USER_MANUAL.md) · **Español**

# Teleco SLM — Manual de Usuario

**Versión 1.0.0 · Junio 2026**

Inferencia LLM local para ingeniería de telecomunicaciones. Ejecuta Qwen 3 1.7B Fine-tuned con llama.cpp en CPU, completamente offline.

Arturo Fierro Pardo — Universidad CEU San Pablo

---

## Índice

1. [Introducción](#1-introducción)
2. [Requisitos del sistema](#2-requisitos-del-sistema)
3. [Instalación](#3-instalación)
4. [Primer inicio y configuración](#4-primer-inicio-y-configuración)
5. [Uso de la aplicación](#5-uso-de-la-aplicación)
6. [Ajustes](#6-ajustes)
7. [Métricas de inferencia](#7-métricas-de-inferencia)
8. [Gestión de datos](#8-gestión-de-datos)
9. [Solución de problemas](#9-solución-de-problemas)
10. [Información técnica](#10-información-técnica)

---

## 1. Introducción

Teleco SLM es una aplicación de inteligencia artificial generativa diseñada para estudiantes y profesionales de ingeniería de telecomunicaciones. La aplicación permite realizar consultas sobre contenidos específicos del dominio de telecomunicaciones y obtener respuestas generadas por un modelo de lenguaje especializado, ejecutado de forma completamente local en el dispositivo del usuario.

El modelo integrado es **Qwen 3 1.7B Fine-tuned**, un Modelo de Lenguaje Pequeño (Mini-SLM) ajustado mediante LoRA sobre un corpus de 24.680 pares pregunta-respuesta extraídos del plan de estudios de Ingeniería de Telecomunicaciones de la Universidad CEU San Pablo. El modelo se distribuye en formato GGUF (cuantización Q4_K_M, ~1,1 GB) y se ejecuta mediante llama.cpp, lo que permite inferencia eficiente en CPU sin necesidad de GPU dedicada ni conexión a internet.

La aplicación está disponible para Android y Windows, con arquitecturas de inferencia adaptadas a cada plataforma.

**Características principales**

- Inferencia 100% offline: los datos nunca salen del dispositivo.
- Modelo especializado en telecomunicaciones con soporte de fórmulas matemáticas.
- Renderizado de expresiones LaTeX en las respuestas.
- Historial de conversaciones almacenado localmente (SQLite).
- Panel de métricas de rendimiento (tokens/s, latencia, memoria).
- Descarga directa del modelo desde Hugging Face o carga de archivo local.
- Soporte de conexión a servidor remoto `llama-server` en red local.

---

## 2. Requisitos del sistema

### 2.1 Android

| Componente | Requisito |
|------------|-----------|
| Sistema operativo | Android 8.0 (API 26) o superior |
| Arquitectura | ARM64 (aarch64) |
| RAM mínima | 4 GB (recomendado 6 GB o más) |
| Almacenamiento | ~1,5 GB libres (modelo + aplicación) |
| GPU | No requerida (inferencia en CPU con NEON) |
| Conexión a internet | Solo para la descarga inicial del modelo |

### 2.2 Windows

| Componente | Requisito |
|------------|-----------|
| Sistema operativo | Windows 10/11 (64 bits) |
| RAM mínima | 4 GB (recomendado 8 GB) |
| Almacenamiento | ~1,5 GB libres (modelo + aplicación) |
| Dependencia | `llama-server.exe`, incluido en la instalación |
| Conexión a internet | Solo para la descarga inicial del modelo |

---

## 3. Instalación

### 3.1 Android

La aplicación se distribuye como archivo APK. Para instalarla:

1. Descargar el archivo `TelecoSLM.apk` en el dispositivo Android.
2. Acceder a la carpeta de descargas con un gestor de archivos.
3. Pulsar sobre el archivo APK. Si es la primera vez, el sistema solicitará habilitar la instalación desde orígenes desconocidos en **Ajustes > Seguridad**.
4. Confirmar la instalación y esperar a que finalice.
5. Abrir la aplicación desde el cajón de aplicaciones.

La aplicación se encuentra también en Google Play Store.

### 3.2 Windows

En Windows, la aplicación se distribuye como carpeta portable o instalador:

1. Descargar la carpeta de distribución de TelecoSLM para Windows.
2. Extraer el contenido en `C:\Program Files\TelecoSLM\` o la ubicación deseada.
3. Ejecutar `TelecoSLM.exe` para iniciar la aplicación.
4. El servidor de inferencia `llama-server.exe` se iniciará automáticamente en segundo plano al cargar el modelo.

---

## 4. Primer inicio y configuración

Al abrir la aplicación por primera vez, es necesario disponer del modelo de lenguaje para poder realizar inferencias. La pantalla de **Ajustes** permite configurar la fuente del modelo.

### 4.1 Descarga del modelo

La sección **Modelo Local** de los ajustes muestra la información del modelo preconfigurado: Qwen 3 1.7B Fine-tuned en formato Q4_K_M (~1,1 GB). Existen dos opciones para obtener el modelo:

- **Descargar modelo** — descarga automática del archivo GGUF desde el repositorio de Hugging Face. Requiere conexión a internet. El progreso se muestra en pantalla.
- **Seleccionar archivo GGUF** — permite cargar un archivo GGUF que ya se encuentre almacenado en el dispositivo. Útil si el modelo fue descargado previamente o se transfirió mediante cable USB.

![Pantalla de Ajustes — Modelo Local y Servidor Remoto](manual/manual-01-settings-model.png)

*Figura 1. Pantalla de Ajustes — Modelo Local y Servidor Remoto.*

Una vez descargado o seleccionado el modelo, la ruta del archivo aparecerá en el campo correspondiente y el indicador **Modelo activo** (punto verde) se mostrará en la cabecera de la aplicación, confirmando que el modelo está cargado y listo para su uso.

### 4.2 Servidor remoto

Alternativamente, la aplicación puede conectarse a un servidor `llama-server` que se ejecute en otro equipo de la red local. Para ello, se debe introducir la dirección IP y el puerto del servidor (por ejemplo, `192.168.1.100:8089`) en la sección **Servidor Remoto** y pulsar **Conectar**.

> **Nota:** El modo remoto es útil para equipos Android de gama baja: el modelo se ejecuta en un PC más potente y el dispositivo móvil actúa como interfaz.

---

## 5. Uso de la aplicación

### 5.1 Pantalla principal

La pantalla principal muestra el nombre de la aplicación, el estado del modelo y el acceso a las funciones principales:

- **Indicador de estado** — el badge verde «Modelo activo» confirma que el modelo está cargado. Si el modelo no se ha descargado aún, este indicador aparecerá en rojo con el mensaje «Modelo inactivo».
- **Nuevo Chat** — tarjeta principal para iniciar una nueva conversación.
- **Chats Recientes** — listado de conversaciones anteriores con su primera pregunta como título. Un contador indica el número total. Cada entrada tiene un botón (×) para eliminar la conversación individualmente.
- **Icono de ajustes** (esquina superior derecha) — accede a la pantalla de configuración.

![Pantalla principal de Teleco SLM](manual/manual-02-home.png)

*Figura 2. Pantalla principal de Teleco SLM.*

### 5.2 Conversaciones

Al pulsar **Nuevo Chat** o seleccionar una conversación existente, se abre la pantalla de chat. El funcionamiento es similar a otras aplicaciones de mensajería:

- Escribir la pregunta en el campo de texto inferior y pulsar el botón de envío (flecha azul).
- La respuesta se genera de forma progresiva (token a token) en tiempo real.
- Los mensajes del usuario aparecen a la derecha (burbuja azul con icono de persona) y las respuestas del modelo a la izquierda (burbuja oscura con icono del modelo).
- Cada conversación se guarda automáticamente en la base de datos local (SQLite) y es accesible desde la sección **Chats Recientes** de la pantalla principal.

En la parte inferior de la pantalla de chat se muestra un aviso legal recordando que las respuestas pueden contener errores y no sustituyen la consulta de fuentes académicas oficiales.

### 5.3 Renderizado LaTeX

Teleco SLM soporta la renderización de expresiones matemáticas en formato LaTeX directamente dentro de las respuestas. El modelo ha sido entrenado para generar fórmulas usando delimitadores estándar: `\(...\)` para expresiones en línea y `\[...\]` para expresiones en bloque. Las fórmulas se renderizan automáticamente sin que el usuario tenga que realizar ninguna acción adicional.

![Pantalla de chat con respuesta generada incluyendo fórmula LaTeX](manual/manual-03-chat-latex.png)

*Figura 3. Pantalla de chat con respuesta generada incluyendo fórmula LaTeX.*

---

## 6. Ajustes

La pantalla de Ajustes se organiza en las siguientes secciones:

**Modelo Local** — Muestra la información del modelo configurado (nombre, formato de cuantización, tamaño aproximado y modo de ejecución). Desde aquí se puede descargar el modelo desde Hugging Face o seleccionar un archivo GGUF almacenado localmente.

**Servidor Remoto** — Permite conectar la aplicación a una instancia de `llama-server` que se ejecute en la red local. Se introduce la dirección IP y el puerto y se pulsa **Conectar**.

**Rendimiento** — Acceso al panel de Métricas de Inferencia, que se detalla en la sección 7.

**Datos** — El botón **Borrar todo el historial** elimina todas las conversaciones almacenadas en la base de datos local. Esta acción es irreversible.

**Acerca de** — Muestra la versión de la aplicación, una breve descripción y las tecnologías utilizadas: llama.cpp, SQLite y modo Offline.

![Ajustes — Rendimiento, Datos y Acerca de](manual/manual-04-settings-data.png)

*Figura 4. Ajustes — Rendimiento, Datos y Acerca de.*

---

## 7. Métricas de inferencia

El panel de Métricas de Inferencia permite monitorizar el rendimiento del modelo en cada petición realizada. Se accede desde **Ajustes > Rendimiento > Métricas de Inferencia**.

Para cada consulta se registran las siguientes métricas:

| Métrica | Descripción |
|---------|-------------|
| Tokens generados | Número total de tokens producidos en la respuesta. |
| Tiempo al primer token | Latencia (en milisegundos) desde el envío de la petición hasta la generación del primer token. |
| Tiempo total | Duración total de la generación de la respuesta (en segundos). |
| Velocidad | Tasa de generación medida en tokens por segundo (tok/s). |
| Memoria (RSS) | Porcentaje de memoria RAM física utilizada por el proceso de inferencia. |

![Panel de Métricas de Inferencia con datos de una consulta](manual/manual-05-metrics.png)

*Figura 5. Panel de Métricas de Inferencia con datos de una consulta.*

Cada entrada del historial de métricas incluye la hora de la petición, la fuente (`llama-server` local o remoto) y el texto de la consulta realizada. Esta información es útil para diagnosticar problemas de rendimiento o comparar la velocidad de inferencia en distintos dispositivos.

---

## 8. Gestión de datos

Toda la información generada por la aplicación se almacena exclusivamente en el dispositivo del usuario. Teleco SLM no envía datos a servidores externos en ningún momento. Los datos gestionados son:

- **Conversaciones** — almacenadas en una base de datos SQLite local. Cada conversación incluye los mensajes del usuario y las respuestas del modelo con marcas de tiempo.
- **Preferencias** — configuración de la aplicación (ruta del modelo, dirección del servidor remoto) almacenada mediante SharedPreferences.
- **Modelo** — el archivo GGUF del modelo se almacena en el directorio de la aplicación.

### Eliminar conversaciones

Se pueden eliminar conversaciones individuales desde la pantalla principal pulsando el botón (×) junto a cada chat, o eliminar todo el historial desde **Ajustes > Datos > Borrar todo el historial**.

> **Advertencia:** La eliminación del historial es irreversible. No es posible recuperar conversaciones borradas.

---

## 9. Solución de problemas

**El indicador «Modelo activo» no aparece**
El modelo no se ha descargado o la ruta del archivo es incorrecta. Acceder a Ajustes y verificar que la ruta del archivo GGUF es válida. Si es necesario, pulsar «Seleccionar archivo .gguf» para reconfigurar la ruta.

**La descarga del modelo se interrumpe**
Comprobar la conexión a internet y el espacio disponible en el dispositivo (~1,1 GB). Reiniciar la descarga desde **Ajustes > Descargar modelo**.

**Las respuestas son muy lentas**
La velocidad de inferencia depende del hardware del dispositivo. En dispositivos Android de gama baja, considerar utilizar el modo Servidor Remoto ejecutando `llama-server` en un PC con más recursos. Velocidades típicas: 8-15 tok/s en dispositivos móviles modernos, 15-30 tok/s en PCs de gama media.

**La aplicación se cierra inesperadamente**
Puede deberse a falta de memoria RAM. Cerrar otras aplicaciones en segundo plano y reiniciar Teleco SLM. El modelo requiere aproximadamente 1,5 GB de RAM libre.

**Las fórmulas LaTeX no se renderizan correctamente**
Verificar que la respuesta contiene los delimitadores correctos. En algunos casos, el modelo puede generar formato incorrecto. Reformular la pregunta solicitando explícitamente la fórmula.

**No se puede conectar al servidor remoto**
Verificar que ambos dispositivos están en la misma red local, que la dirección IP y el puerto son correctos, y que `llama-server` está en ejecución en el equipo destino.

---

## 10. Información técnica

| Componente | Detalle |
|------------|---------|
| Framework | Flutter (Android + Windows) |
| Motor de inferencia | llama.cpp (ARM64 NEON en Android, HTTP en Windows) |
| Modelo | Qwen 3 1.7B Fine-tuned (LoRA) |
| Formato del modelo | GGUF — Q4_K_M (~1,1 GB) |
| Contexto máximo | 2.048 tokens |
| Base de datos | SQLite (almacenamiento local de conversaciones) |
| Configuración | SharedPreferences |
| Gestión de estado | Provider (Flutter) |
| Renderizado matemático | gpt_markdown (delimitadores LaTeX) |
| Filtrado thinking-mode | Máquina de estados con auto-retry `/no_think` |
| GPU (Android) | Deshabilitada (`gpu_layers = 0`, compatibilidad Adreno 612) |
| Versión | 1.0.0 |

---

*Teleco SLM v1.0.0 — Arturo Fierro Pardo · Universidad CEU San Pablo — Junio 2026*
