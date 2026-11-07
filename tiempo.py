
import requests
from datetime import date, timedelta
from strands import tool


# Busco las coordenadas de una ciudad
def buscar_ciudad(ciudad):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    respuesta = requests.get(
        url,
        params={
            "name": ciudad,
            "count": 1,
            "language": "es"
        },
        timeout=10
    )
    respuesta.raise_for_status()

    lugares = respuesta.json().get("results", [])

    if not lugares:
        return None

    return lugares[0]


# Consulto el tiempo de una ciudad
@tool
def consultar_tiempo(ciudad: str, dia: str = "hoy") -> str:
    """Consulta el tiempo de hoy o mañana en una ciudad."""

    try:
        lugar = buscar_ciudad(ciudad)

        if not lugar:
            return f"No he encontrado la ciudad {ciudad}."

        # Obtengo las coordenadas de la ciudad
        latitud = lugar["latitude"]
        longitud = lugar["longitude"]

        # Consulto la previsión meteorológica
        url = "https://api.open-meteo.com/v1/forecast"

        respuesta = requests.get(
            url,
            params={
                "latitude": latitud,
                "longitude": longitud,
                "daily": [
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_probability_max",
                    "weather_code"
                ],
                "timezone": "auto",
                "forecast_days": 2
            },
            timeout=10
        )
        respuesta.raise_for_status()

        datos = respuesta.json()["daily"]

        # Selecciono el día que quiero consultar
        if dia.lower() in ["mañana", "manana", "tomorrow"]:
            posicion = 1
        elif dia.lower() in ["hoy", "today"]:
            posicion = 0
        else:
            return "Solo puedo consultar el tiempo de hoy o mañana."

        fecha = datos["time"][posicion]
        maxima = datos["temperature_2m_max"][posicion]
        minima = datos["temperature_2m_min"][posicion]
        lluvia = datos["precipitation_probability_max"][posicion]
        codigo = datos["weather_code"][posicion]

        # Interpreto el estado del cielo
        if codigo == 0:
            estado = "Despejado"
        elif codigo in [1, 2, 3]:
            estado = "Algo nuboso o nublado"
        elif codigo in [45, 48]:
            estado = "Niebla"
        elif codigo in [51, 53, 55, 56, 57]:
            estado = "Llovizna"
        elif codigo in [61, 63, 65, 66, 67, 80, 81, 82]:
            estado = "Lluvia"
        elif codigo in [71, 73, 75, 77, 85, 86]:
            estado = "Nieve"
        elif codigo in [95, 96, 99]:
            estado = "Tormenta"
        else:
            estado = "Condiciones variables"

        return (
            f"Tiempo en {lugar['name']}, "
            f"{lugar.get('country', '')} para {fecha}:\n"
            f"Estado: {estado}\n"
            f"Temperatura máxima: {maxima} °C\n"
            f"Temperatura mínima: {minima} °C\n"
            f"Probabilidad máxima de precipitación: {lluvia}%"
        )

    except requests.RequestException:
        return "No he podido consultar el tiempo. Comprueba tu conexión."

    except (KeyError, IndexError, ValueError):
        return "He tenido un problema al interpretar los datos del tiempo."


# Pruebo mi consulta meteorológica
if __name__ == "__main__":
    print(consultar_tiempo("Madrid", "hoy"))
