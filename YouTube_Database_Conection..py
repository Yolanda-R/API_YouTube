import mysql.connector
import requests # hacer la lista y validar que corresponden los valores
from datetime import datetime #convertir la cadena de fecha y hora en un formato 

# Cambia estos valores con tus propias credenciales de MySQL
host = "localhost"
user = "testing"
password = "****"
database = "youtube_videos"

# Tu clave de API de YouTube
api_key = "*******"

# URL de la API de búsqueda de YouTube
url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q=testing&maxResults=100&key={api_key}"

# Realizar la solicitud a la API
response = requests.get(url)
data = response.json()

# Crear una lista para almacenar los resultados
resultados = []

# Iterar a través de los elementos de la respuesta y agregarlos a la lista
for item in data.get('items', []):
    video = {
        'video_id': item['id']['videoId'],
        'titulo': item['snippet']['title'],
        'descripcion': item['snippet']['description'],
        'autor_channel': item['snippet']['channelTitle'],
        'fecha_publicacion': item['snippet']['publishedAt']
    }
    resultados.append(video)

# Crear la conexión a MySQL
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

# Crear un cursor
cursor = connection.cursor()



# Iterar a través de la lista de resultados y realizar la inserción en la tabla
for video in resultados:
    fecha_publicacion_str = video['fecha_publicacion']
    fecha_publicacion_dt = datetime.strptime(fecha_publicacion_str, "%Y-%m-%dT%H:%M:%SZ")

    query = "INSERT INTO videotest (video_id, titulo, descripcion, autor_channel, fecha_publicacion) VALUES (%s, %s, %s, %s, %s)"
    values = (video['video_id'], video['titulo'], video['descripcion'], video['autor_channel'], fecha_publicacion_dt)
    cursor.execute(query, values)
    connection.commit()


cursor.close()
connection.close()



