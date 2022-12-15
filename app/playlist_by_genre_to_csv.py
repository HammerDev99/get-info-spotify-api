import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
from pathlib import PurePath

class playlist_by_genre_to_csv:

    client_id = ""
    client_secret = ""
    redirect_uri = ""
    sp = spotipy.Spotify()

    def get_keys(self):
        with open(PurePath("app/assets/keys.txt"), 'r', encoding='UTF-8', newline='\r\n') as f: # Se usa PurePath para manejar la ruta pura según sistema operativo
            secret_keys = f.readlines()
            self.client_id = secret_keys[0].strip()
            self.client_secret = secret_keys[1].strip()
            self.redirect_uri = secret_keys[2]

    def auth_without_user(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret))

    def auth_with_user(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.client_id, client_secret=self.client_secret, redirect_uri=self.redirect_uri, scope="playlist-read-collaborative"))

    def main(self):
        self.get_keys()
        self.auth_without_user()
        #self.auth_with_user()

        # playlists ids / solo se usa la primera
        ids=['37i9dQZEVXbOa2lmxNORXQ',
            '3lnMwmYF979bEedMa6WK38', 
            '6h6uzoRBXnkjeoEjwiX27R', 
            ]
        
        # Posible funcionalidad de obtener datos de varias listas validando los valores repetidos
        pl_id = 'spotify:playlist:'+ids[0] # Crea la direccion uri para acceder a la playlist
        df = self.get_spotify_data(pl_id) # dataframe que contiene datos de la playlist
        groupby_genre = df.groupby('artist_genres').groups # Diccionario que agrupa los indices del df por genero
        for genre, index in groupby_genre.items():
            newdf = df.loc[list(index)] # Crea subconjuntos del df agrupado por cada genero
            newdf.to_csv('output/{}.csv'.format(str(genre)),index=False) # Convierte el subconjunto en csv y renombra con genre

    def get_spotify_data(self, pl_id):
        # Crear lista con datos obtenidos
        ls = []
        # PENDIENTE de revisar la implementacion
        for track in self.sp.playlist_tracks(pl_id)["items"]:
            # Se obtienen los datos de la playlist
            artist_uri = track["track"]["artists"][0]["uri"]
            artist_info = self.sp.artist(artist_uri)
            artist_genres = artist_info["genres"]
            track_uri = track["track"]["uri"]
            track_name = track["track"]["name"]
            artist_name = track["track"]["artists"][0]["name"]
            # Se agregan en una lista
            data = str(artist_genres[0]), str(track_uri) ,str(track_name),str(artist_name)
            ls.append(data)
        df = pd.DataFrame(ls, columns=['artist_genres','track_uri','track_name','artist_name'])
        return(df)

if __name__ == '__main__':
    obj = playlist_by_genre_to_csv()
    obj.main()