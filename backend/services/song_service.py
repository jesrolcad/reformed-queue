"""
    Módulo que permite buscar canciones en Spotify y añadirlas a la cola
    del dispositivo configurado.
"""

import requests
from fastapi.responses import JSONResponse
import os
from models.schemas import Song

#Variables de entorno
DEVICE_ID = os.getenv('DEVICE_ID')

def search_song(query: str, access_token: str):
    """
        Función que permite buscar canciones en Spotify.
        Parámetros de entrada:
            - query (str): Término de búsqueda
            - access_token (str): Token de acceso a la API de Spotify
    """

    headers = {
        "Authorization": f'Bearer {access_token}'
    }

    response = requests.get(f"https://api.spotify.com/v1/search?q={query}&type=track", headers=headers)
    response_json = response.json()
    print(response_json)

    if response.status_code == 200:

        songs = response_json["tracks"]["items"]
        song_list = []

        for song in songs:
            id = ''
            titulo = ''
            imagen = ''
            artists = song["artists"]
            artista = get_artists_song(artists)
            id = song["uri"]
            titulo = song["name"]
            imagen = song["album"]["images"][2]["url"]

            s = Song(id=id, artista=artista, titulo=titulo, imagen=imagen)
            song_list.append(s)

        return {"songs":song_list}

    elif response.status_code == 400:
        return JSONResponse(status_code=400, content={"message": "Inserte un término de búsqueda"})

    elif response.status_code == 401:
        return JSONResponse(status_code=401, content={"message": "Token de acceso no válido o expirado. Vuelve a iniciar sesión"})

    elif response.status_code == 403:
        return JSONResponse(status_code=403, content={"message": "No tienes permisos para buscar canciones"})
        
    elif response.status_code == 429:
        return JSONResponse(status_code=429, content={"message": "El sistema se encuentra saturado. Inténtelo más tarde"})


def get_artists_song(artists: list)->str:
    """
        Función que calcula los artistas que participan en una canción.

        Parámetros de entrada:
            - artists (list): Lista de artistas que participan en la canción

        Devuelve:
            - artistas de la canción en una variable de tipo str
    """
    artista = ''
    if len(artists) > 1:
        for i in range(0, len(artists)):
            if i != len(artists) - 1:
                artista += artists[i]["name"] + ", "
            else:
                artista += artists[i]["name"]
    else:
        artista = artists[0]["name"]

    return artista


def add_song_to_queue(song_id: str, access_token: str):
    """
        Función que permite añadir una canción a la cola del dispositivo.
        Parámetros de entrada:
            - song_id (str): Identificador de la canción que se quiere añadir a la cola
            - access_token (str): Token de acceso a la API de Spotify
    """

    headers = {
        "Authorization": f'Bearer {access_token}',
        "Content-Type": "application/json"
    }

    response = requests.post(f"https://api.spotify.com/v1/me/player/queue?uri={song_id}&device_id={DEVICE_ID}", headers=headers)

    if response.status_code == 204:
        return {"message": "Canción agregada a la cola"}

    elif response.status_code == 400:
        return JSONResponse(status_code=400, content={"message": "No se pudo añadir la canción a la cola. Id de canción no válido"})

    elif response.status_code == 404:
        return JSONResponse(status_code=404, content={"message": "No se pudo añadir la canción a la cola. Dispositivo no válido o inactivo"})

    elif response.status_code == 403:
        return JSONResponse(status_code=403, content={"message": "No se pudo añadir la canción a la cola. No tienes permisos para agregar canciones"})

    elif response.status_code == 429:
        return JSONResponse(status_code=429, content={"message": "El sistema se encuentra saturado. Inténtelo más tarde"})