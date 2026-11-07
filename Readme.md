# Zero IA
Zero IA es mi asistente personal hecho en Python. Lo he creado para poder hablar con una inteligencia artificial desde la terminal y tener en un mismo sitio mi calendario, el tiempo y mi correo de Gmail.

Qué puede hacer
- Conversar conmigo: utilizo Gemini a través de Strands Agents.
- Gestionar mi calendario: guardo, consulto y elimino citas en una base de datos SQLite local.
- Consultar el tiempo: puedo preguntar por la previsión de hoy o mañana en una ciudad gracias a Open-Meteo.
- Consultar Gmail: puedo ver el remitente, el asunto y la fecha de los últimos cinco correos, y saber cuántos mensajes tengo sin leer. El acceso a Gmail es de solo lectura.
- Responder en español o inglés: personalizo su comportamiento en system_prompt.txt.
  
# Archivos de mi proyecto
Zero IA 
  -  main.py
  -  calendario.py
  - tiempo.py
  - correo.py
  - system_prompt.txt
  - requirements.txt
  - .env
  - credentials.json
  - calendario.db
  - token_gmail.json

1. agente.py: inicio Zero IA y conecto las herramientas al agente.
2. calendario.py: gestiono mis citas con SQLite.
3. tiempo.py: consulto las previsiones meteorológicas.
4. correo.py: me conecto a Gmail y consulto información de mis mensajes.
5. system_prompt.txt: guardo las instrucciones de mi asistente.
6. requirements.txt: anoto las librerías que necesita mi proyecto.
7. .env: guardo mi clave API de Gemini.
8. credentials.json: guardo la configuración OAuth que descargo de Google Cloud.
9. calendario.db: almaceno mis citas; se crea al preparar el calendario.
10. token_gmail.json: guardo mi autorización de Gmail después del primer inicio de sesión.

# Cómo lo preparo
Primero necesito tener Python instalado. Desde la carpeta del proyecto instalo las dependencias:
python -m pip install -r requirements.txt

Después creo un archivo .env con mi clave de Gemini:
GEMINI_API_KEY=mi_clave_api

Para usar Gmail, activo la API de Gmail en Google Cloud, configuro OAuth para una aplicación de escritorio y guardo el archivo descargado como credentials.json en la carpeta del proyecto. En la primera conexión autorizo el acceso desde el navegador.

# Cómo lo ejecuto
Inicio mi asistente con:
python main.py
Puedo escribir preguntas como estas:
- «Zero, ¿qué citas tengo guardadas?»
- «Zero, recuérdame una reunión mañana a las 17:00».
- «Zero, ¿qué tiempo hará mañana en Madrid?»
- «Zero, ¿cuántos correos tengo sin leer?»
- «Zero, dime los últimos cinco correos».
Para terminar escribo salir.

# Privacidad y límites
Mi calendario se guarda de forma local en SQLite. No subo .env, credentials.json ni token_gmail.json a repositorios públicos. Cuando consulto Gmail a través del agente, los datos recuperados pueden enviarse a Gemini para generar una respuesta.

Por ahora, mi integración de Gmail solo consulta metadatos de los mensajes: no lee el cuerpo completo, no envía correos y no los borra. La herramienta meteorológica consulta hoy y mañana; no es un sistema de alertas automáticas.

# Próximas mejoras
Quiero seguir mejorando Zero IA para que pueda ayudarme con más tareas y resulte cada vez más cómoda de utilizar.
