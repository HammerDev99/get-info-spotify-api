# get-info-spotify-api

Consigna: Para este proyecto se requiere obtener el top de canciones de Colombia divididas por género (Cada genero tiene que ser un archivo csv). La extracción de los datos debe ser de la API de Spotify. Link API: https://developer.spotify.com/

---

## Conjunto de tecnologías utilizadas

En el desarrollo del reto 1, se encontró en documentación oficial de la API de Spotify, un apartado que relaciona dos librerías que permiten integrar el lenguaje de programación python. Estas [bibliotecas](https://developer.spotify.com/documentation/web-api/libraries/) son desarrolladas por miembros de la comunidad y no han sido revisadas por Spotify. Para el caso que nos ocupa se tiene disposición de las librerías [plamere/spotipy](https://spotipy.readthedocs.io/en/master/) y [tekore](https://pypi.org/project/tekore/) que una vez revisadas refiere más documentación la primera y por eso mismo se ha elegido como candidata para el presente desafío.

## Descripción, lecciones aprendidas y dificultades encontradas en el proceso

Revisada la documentación, foros y demás se encontró que la librería [Spotipy](https://github.com/plamere/spotipy) al ser instalada y realizado el proceso de configuración del [dashboard](https://developer.spotify.com/dashboard), debe de realizarse un proceso de autenticación que puede ser de dos formas (con autenticación de usuario y sin autenticación de usuario). Por lo anterior, se probaron ambos métodos de autenticación (`auth_with_user`, `auth_without_user`). Posteriormente, se procedió a identificar algunas listas de reproducción como fuentes de información que tienen como objeto recopilar la información requerida en la consigna, a saber: 

- [Top Colombia](https://open.spotify.com/playlist/37i9dQZEVXbOa2lmxNORXQ)
- [Top Colombia 2022](https://open.spotify.com/playlist/3lnMwmYF979bEedMa6WK38)
- [Colombia Top 100](https://open.spotify.com/playlist/6h6uzoRBXnkjeoEjwiX27R)

```python
# Proceso de autenticación
self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.client_id,
                                                                client_secret=self.client_secret))
```

Luego de confirmar que el proceso de captura de los datos son recibidos correctamente, se intentó identificar el género de cada canción como comúnmente se solicita, sin embargo, se evidenció una dificultad de interpretación del género musical ya que no es un proceso simple su identificación, dado que los músicos son muy creativos y no todas las canciones o artistas tienen un género definido y por parte de la API de spotify se puede obtener información relacionada con el `audio-features` como duración, tempo (BPM), clave, popularidad, felicidad, volumen, explicito, entre otros (para más detalles ingresa [aquí](https://developer.spotify.com/console/tracks/)). Por lo anterior, se obtuvo la referencia del género según el artista de la canción y para el caso de los resultados que tienen más de un género, se eligió el primero en la lista obtenida.

```python
def get_spotify_data(self, pl_id):
    ls = []
    for track in self.sp.playlist_tracks(pl_id)["items"]:
        track_uri = track["track"]["uri"]
        track_name = track["track"]["name"]
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = self.sp.artist(artist_uri)
        artist_name = track["track"]["artists"][0]["name"]
        artist_genres = artist_info["genres"]
        # Se obtienen los datos de la playlist y se agregan en una lista
        data = str(artist_genres[0]), str(track_uri) ,str(track_name),str(artist_name)
        ls.append(data)
    df = pd.DataFrame(ls, columns=['artist_genres','track_uri','track_name','artist_name'])
    return(df)
```

Por último se utilizó el método `pandas.DataFrame.groupby` para agrupar por genero el data frame que contiene toda la información obtenida de la API de Spotify.

```python
ids=['37i9dQZEVXbOa2lmxNORXQ']
pl_id = 'spotify:playlist:'+ids[0] # Crea la direccion uri para acceder a la playlist
df = self.get_spotify_data(pl_id) # Genera un df que contiene datos de la playlist
groupby_genre = df.groupby('artist_genres').groups # Diccionario que agrupa los indices del df por genero
for genre, index in groupby_genre.items():
    newdf = df.loc[list(index)] # Crea subconjuntos del df agrupado por cada genero
    newdf.to_csv('output/{}.csv'.format(str(genre)),index=False)
```

## Documentación adicional

Puede acceder al script y los resultados del reto 1 en el siguiente link: [script](tracks_by_genre_to_csv.py), [outputs](output/)

Referencias:

- [Extracting Song Data From the Spotify API Using Python](https://towardsdatascience.com/extracting-song-data-from-the-spotify-api-using-python-b1e79388d50)
- [Music Genre Finder: Check genres of any Song or Artist](https://www.chosic.com/music-genre-finder/)

---

## Construir y Ejecutar

1. Crear el ambiente virtual

```Bash
python3 -m venv venv
```

2. Activando el ambiente virtual

```Bash
source venv/bin/activate
```

3. Instalar los módulos necesarios

```Bash
python3 -m install ./requirements.txt
```

4. Ejecutar la aplicación

```Bash
python ./app/playlist_by_genre_to_csv.py
```
