
import os
from pathlib import Path
from dotenv import load_dotenv
from strands import Agent
from strands.models.gemini import GeminiModel
from strands.types.exceptions import ModelThrottledException

from calendario import (
    crear_calendario,
    ver_calendario,
    obtener_fecha_actual,
    guardar_cita,
    eliminar_cita
)

from tiempo import consultar_tiempo
from correo import consultar_correos, correos_sin_leer


# Cargo las variables de mi archivo .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Obtengo mi clave API de Gemini
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("Zero IA: No encuentro mi clave API de Gemini.")
    exit()


# Configuro el modelo que voy a utilizar
model = GeminiModel(
    client_args={"api_key": api_key},
    model_id="gemini-2.5-flash"
)


# Cargo las instrucciones de mi asistente
try:
    with open(BASE_DIR / "system_prompt.txt", "r", encoding="utf-8") as archivo:
        instructions = archivo.read()

except FileNotFoundError:
    print("Zero IA: No encuentro el archivo system_prompt.txt.")
    exit()


# Preparo mi calendario local
crear_calendario()


# Creo mi asistente con acceso al calendario, tiempo y correo
agente = Agent(
    model=model,
    system_prompt=instructions,
    tools=[
        ver_calendario,
        obtener_fecha_actual,
        guardar_cita,
        eliminar_cita,
        consultar_tiempo,
        consultar_correos,
        correos_sin_leer
    ],
    callback_handler=None
)


# Inicio mi asistente
print("\n===================================")
print("       ZERO IA - ASISTENTE")
print("===================================")
print("Zero IA está lista. Escribe 'salir' para terminar.\n")


# Inicio la conversación con Zero IA
while True:

    pregunta = input("Usuario: ").strip()

    # Compruebo si quiero cerrar el programa
    if pregunta.lower() == "salir":
        print("Zero IA: ¡Hasta luego! Que tengas un gran día.")
        break

    # Evito enviar mensajes vacíos
    if not pregunta:
        continue

    try:
        # Envío mi pregunta al asistente
        print("\nZero IA está pensando...\n")

        respuesta = agente(pregunta)

        # Muestro la respuesta
        print(f"Zero IA: {respuesta}\n")

    except ModelThrottledException as error:
        print("Zero IA: He alcanzado temporalmente un límite de uso.")
        print("Detalles:", error)

    except Exception as error:
        print(f"Zero IA: Ha ocurrido un error: {error}")