
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from strands import tool

# Defino la ruta donde voy a guardar mi calendario
BASE_DIR = Path(__file__).resolve().parent
RUTA_BD = BASE_DIR / "calendario.db"


# Creo la base de datos de mi calendario
def crear_calendario():
    with sqlite3.connect(RUTA_BD) as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                descripcion TEXT,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL
            )
        """)

    print("Zero IA: Calendario preparado.")


# Añado un evento a mi calendario
def agregar_evento(titulo, fecha, hora, descripcion=""):
    with sqlite3.connect(RUTA_BD) as conexion:
        conexion.execute("""
            INSERT INTO eventos (titulo, descripcion, fecha, hora)
            VALUES (?, ?, ?, ?)
        """, (titulo, descripcion, fecha, hora))

    return f"Evento '{titulo}' guardado para el {fecha} a las {hora}."


# Consulto los eventos que tengo guardados
def consultar_eventos():
    with sqlite3.connect(RUTA_BD) as conexion:
        eventos = conexion.execute("""
            SELECT id, titulo, fecha, hora, descripcion
            FROM eventos
            ORDER BY fecha, hora
        """).fetchall()

    return eventos


# Dejo que Zero IA consulte mis eventos
@tool
def ver_calendario() -> str:
    """Consulta los eventos guardados en el calendario."""

    eventos = consultar_eventos()

    if not eventos:
        return "No hay eventos guardados."

    resultado = ""

    for id_evento, titulo, fecha, hora, descripcion in eventos:
        resultado += f"{id_evento}. {titulo} - {fecha} a las {hora}"

        if descripcion:
            resultado += f" ({descripcion})"

        resultado += "\n"

    return resultado


# Le doy a Zero IA la fecha actual
@tool
def obtener_fecha_actual() -> str:
    """Consulta la fecha y hora actuales del ordenador."""

    ahora = datetime.now().astimezone()
    manana = ahora + timedelta(days=1)

    return (
        f"Hoy es {ahora.strftime('%Y-%m-%d')} "
        f"y son las {ahora.strftime('%H:%M')}. "
        f"Mañana es {manana.strftime('%Y-%m-%d')}."
    )


# Dejo que Zero IA guarde citas
@tool
def guardar_cita(
    titulo: str,
    fecha: str,
    hora: str,
    descripcion: str = ""
) -> str:
    """Guarda una cita usando fecha AAAA-MM-DD y hora HH:MM."""

    try:
        datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
    except ValueError:
        return "La fecha o la hora no son válidas."

    return agregar_evento(titulo, fecha, hora, descripcion)


# Dejo que Zero IA elimine eventos de mi calendario
@tool
def eliminar_cita(id_evento: int) -> str:
    """Elimina un evento del calendario utilizando su ID."""

    with sqlite3.connect(RUTA_BD) as conexion:
        evento = conexion.execute(
            "SELECT titulo FROM eventos WHERE id = ?",
            (id_evento,)
        ).fetchone()

        if not evento:
            return "No he encontrado ningún evento con ese ID."

        conexion.execute(
            "DELETE FROM eventos WHERE id = ?",
            (id_evento,)
        )

    return f"He eliminado el evento '{evento[0]}'."


# Pruebo mi calendario
if __name__ == "__main__":
    crear_calendario()

    for evento in consultar_eventos():
        print(evento)
