from fastapi import FastAPI, Request, Header
from fastapi.responses import RedirectResponse, JSONResponse
from dotenv import load_dotenv
import os
import requests
import base64
import sys
import json

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from models.schemas import Song

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("SECRET_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
DEVICE_ID = os.getenv("DEVICE_ID")

app = FastAPI()

@app.get('/')
def main():
    url = "https://accounts.spotify.com/authorize?"
    url += "client_id=" + CLIENT_ID
    url += "&response_type=code"
    url += "&redirect_uri=" + REDIRECT_URI
    url += "&show_dialog=true"
    url += "&scope=user-modify-playback-state,user-read-private"

    return RedirectResponse(url)


@app.get('/access-token')
def access_token(code: str):


    client_credentials = f'{CLIENT_ID}:{CLIENT_SECRET}'
    client_credentials_b64 = base64.b64encode(client_credentials.encode())

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f'Basic {client_credentials_b64.decode()}'
    }

    body = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post("https://accounts.spotify.com/api/token", data=body, headers=headers)
    response_json = response.json()

    print(response_json)
    
    return response_json


@app.post('/search')
def search(query: str, access_token: str = Header()):

    headers = {
        "Authorization": f'Bearer {access_token}'
    }

    response = requests.get(f"https://api.spotify.com/v1/search?q={query}&type=track", headers=headers)
    response_json = response.json()

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
            imagen = song["album"]["images"][1]["url"]

            s = Song(id=id, artista=artista, titulo=titulo, imagen=imagen)
            song_list.append(s)

        return {"songs":song_list}

    else:
        return JSONResponse(status_code=response.status_code, content={"message": "Error al realizar la búsqueda. Inténtelo más tarde"})

def get_artists_song(artists):
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



@app.post('/add-song-to-queue')
def add_song_to_queue(song_id: str, access_token: str = Header()):

    headers = {
        "Authorization": f'Bearer {access_token}',
        "Content-Type": "application/json"
    }

    response = requests.post(f"https://api.spotify.com/v1/me/player/queue?uri={song_id}&device_id={DEVICE_ID}", headers=headers)

    print(response.json())

    if response.status_code == 204:
        return JSONResponse(status_code=204, content={"message": "Canción agregada a la cola"})

    elif response.status_code == 400:
        return JSONResponse(status_code=400, content={"message": "No se pudo añadir la canción a la cola. Id de canción no válido"})

    elif response.status_code == 403:
        return JSONResponse(status_code=403, content={"message": "No se pudo añadir la canción a la cola. No tienes permisos para agregar canciones"})

    elif response.status_code == 429:
        return JSONResponse(status_code=429, content={"message": "El sistema se encuentra saturado. Inténtelo más tarde"})




