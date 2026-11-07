
from pathlib import Path
from email.header import decode_header, make_header

from strands import tool
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Guardo las rutas de mis archivos
BASE_DIR = Path(__file__).resolve().parent
ARCHIVO_CREDENCIALES = BASE_DIR / "credentials.json"
ARCHIVO_TOKEN = BASE_DIR / "token_gmail.json"

PERMISOS = ["https://www.googleapis.com/auth/gmail.readonly"]


# Inicio sesión con mi cuenta de Gmail
def conectar_gmail():
    credenciales = None

    if ARCHIVO_TOKEN.exists():
        credenciales = Credentials.from_authorized_user_file(
            str(ARCHIVO_TOKEN), PERMISOS
        )

    if not credenciales or not credenciales.valid:
        if credenciales and credenciales.expired and credenciales.refresh_token:
            credenciales.refresh(Request())
        else:
            if not ARCHIVO_CREDENCIALES.exists():
                print("Zero IA: No encuentro credentials.json")
                print("Guarda ese archivo en:", BASE_DIR)
                return None

            flujo = InstalledAppFlow.from_client_secrets_file(
                str(ARCHIVO_CREDENCIALES), PERMISOS
            )

            credenciales = flujo.run_local_server(port=0)

        ARCHIVO_TOKEN.write_text(
            credenciales.to_json(),
            encoding="utf-8"
        )

    return build("gmail", "v1", credentials=credenciales)


# Dejo que Zero IA consulte mis últimos correos
@tool
def consultar_correos() -> str:
    """Consulta los últimos cinco correos de mi bandeja de Gmail."""

    gmail = conectar_gmail()

    if gmail is None:
        return "No he podido conectar con Gmail."

    respuesta = gmail.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=5
    ).execute()

    mensajes = respuesta.get("messages", [])

    if not mensajes:
        return "No tienes correos en la bandeja de entrada."

    resultado = []

    for mensaje in mensajes:
        correo = gmail.users().messages().get(
            userId="me",
            id=mensaje["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        datos = {}

        for cabecera in correo["payload"].get("headers", []):
            datos[cabecera["name"].lower()] = cabecera["value"]

        asunto = datos.get("subject", "Sin asunto")
        asunto = str(make_header(decode_header(asunto)))

        remitente = datos.get("from", "Desconocido")
        fecha = datos.get("date", "Sin fecha")

        resultado.append(
            f"De: {remitente}\n"
            f"Asunto: {asunto}\n"
            f"Fecha: {fecha}"
        )

    return "\n\n".join(resultado)


# Dejo que Zero IA compruebe mis mensajes sin leer
@tool
def correos_sin_leer() -> str:
    """Consulta cuántos correos tengo sin leer en Gmail."""

    gmail = conectar_gmail()

    if gmail is None:
        return "No he podido conectar con Gmail."

    respuesta = gmail.users().labels().get(
        userId="me",
        id="UNREAD"
    ).execute()

    cantidad = respuesta.get("messagesTotal", 0)

    return f"Tienes {cantidad} correos sin leer."


# Pruebo si mi correo funciona
if __name__ == "__main__":
    try:
        print(consultar_correos())
        print()
        print(correos_sin_leer())

    except Exception as error:
        print("Zero IA: Ha ocurrido un error:", error)
